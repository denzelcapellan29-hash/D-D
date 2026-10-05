#!/usr/bin/env python3
"""
Acq Foundry Bridge Agent v0.1

Standard-library-only loopback HTTP service that bridges:
  Foundry module <-> local synced transport folder

Intended transport root:
  local Google Drive for Desktop mirror of D&D / Foundry Bridge
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import shutil
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PROTOCOL_VERSION = 1
DEFAULT_PORT = 18747
MAX_BODY = 128 * 1024 * 1024
LOCAL_ORIGIN_RE = re.compile(r"^https?://(?:localhost|127\.0\.0\.1)(?::\d+)?$", re.I)


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=False), encoding="utf-8")
    os.replace(tmp, path)


class BridgeStore:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.commands = self.root / "commands"
        self.processed = self.commands / "processed"
        self.results = self.root / "results"
        self.state = self.root / "state"
        self.backups = self.root / "backups"
        self.incoming = self.root / "assets" / "incoming"
        self.lock = threading.RLock()
        self.inflight: dict[str, Path | None] = {}
        self.transient_queue: list[dict] = []
        self.transient_waiters: dict[str, threading.Event] = {}
        self.transient_results: dict[str, dict] = {}

        for p in [self.commands, self.processed, self.results, self.state, self.backups, self.incoming]:
            p.mkdir(parents=True, exist_ok=True)

        atomic_json(self.state / "agent_status.json", {
            "protocol_version": PROTOCOL_VERSION,
            "agent": "Acq Foundry Bridge Agent",
            "status": "starting",
            "started_at": utcnow(),
            "transport_root": str(self.root)
        })

    def write_state(self, payload: dict) -> None:
        with self.lock:
            atomic_json(self.state / "current_scene.json", payload)
            atomic_json(self.state / "agent_status.json", {
                "protocol_version": PROTOCOL_VERSION,
                "agent": "Acq Foundry Bridge Agent",
                "status": "connected",
                "updated_at": utcnow(),
                "scene_id": payload.get("scene_id"),
                "scene_name": payload.get("scene_name"),
                "revision": payload.get("revision"),
                "transport_root": str(self.root)
            })

    def current_state(self) -> dict | None:
        path = self.state / "current_scene.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def _candidate_commands(self):
        return sorted(
            [p for p in self.commands.glob("*.json") if p.name not in {".DS_Store"}],
            key=lambda p: (p.stat().st_mtime, p.name)
        )

    def _expand_assets(self, command: dict) -> dict:
        cmd = json.loads(json.dumps(command))
        for op in cmd.get("operations", []):
            if op.get("op") != "asset_upload" or not op.get("asset_file"):
                continue
            rel = Path(str(op["asset_file"]))
            if rel.is_absolute() or ".." in rel.parts:
                raise ValueError("asset_file must be a safe path relative to assets/incoming")
            path = (self.incoming / rel).resolve()
            if self.incoming not in path.parents and path != self.incoming:
                raise ValueError("asset_file escaped incoming assets directory")
            if not path.exists():
                raise FileNotFoundError(f"Incoming asset does not exist: {rel}")
            op["filename"] = op.get("filename") or path.name
            op["mime_type"] = op.get("mime_type") or mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            op["file_b64"] = base64.b64encode(path.read_bytes()).decode("ascii")
        return cmd

    def enqueue_rpc(self, command: dict, timeout: float = 30.0) -> dict:
        command = json.loads(json.dumps(command))
        command_id = str(command.get("command_id") or f"rpc-{time.time_ns()}")
        command["command_id"] = command_id
        command.setdefault("protocol_version", PROTOCOL_VERSION)

        waiter = threading.Event()
        with self.lock:
            if command_id in self.transient_waiters or command_id in self.inflight:
                raise ValueError(f"Duplicate command_id: {command_id}")
            self.transient_waiters[command_id] = waiter
            self.transient_queue.append(command)

        if not waiter.wait(timeout):
            with self.lock:
                self.transient_waiters.pop(command_id, None)
                self.transient_results.pop(command_id, None)
                self.transient_queue = [
                    cmd for cmd in self.transient_queue
                    if str(cmd.get("command_id")) != command_id
                ]
                self.inflight.pop(command_id, None)
            raise TimeoutError(f"Timed out waiting for Foundry command {command_id}")

        with self.lock:
            result = self.transient_results.pop(command_id, None)
            self.transient_waiters.pop(command_id, None)
        if result is None:
            raise RuntimeError(f"Foundry command {command_id} completed without a result")
        return result

    def _claim_transient(self, world_id: str | None, scene_id: str | None) -> dict | None:
        for index, raw in enumerate(self.transient_queue):
            if raw.get("world_id") and world_id and raw["world_id"] != world_id:
                continue
            if raw.get("scene_id") and scene_id and raw["scene_id"] != scene_id:
                continue
            command = self.transient_queue.pop(index)
            command_id = str(command["command_id"])
            state = self.current_state()
            if state:
                atomic_json(self.backups / f"{command_id}__before.json", state)
            self.inflight[command_id] = None
            return command
        return None

    def claim_next(self, world_id: str | None, scene_id: str | None) -> dict | None:
        with self.lock:
            transient = self._claim_transient(world_id, scene_id)
            if transient is not None:
                return transient

            for path in self._candidate_commands():
                raw = json.loads(path.read_text(encoding="utf-8"))
                command_id = raw.get("command_id") or path.stem
                raw["command_id"] = command_id
                raw.setdefault("protocol_version", PROTOCOL_VERSION)

                if command_id in self.inflight:
                    continue
                if raw.get("world_id") and world_id and raw["world_id"] != world_id:
                    continue
                if raw.get("scene_id") and scene_id and raw["scene_id"] != scene_id:
                    continue

                state = self.current_state()
                if state:
                    atomic_json(self.backups / f"{command_id}__before.json", state)

                expanded = self._expand_assets(raw)
                self.inflight[command_id] = path
                return expanded
        return None

    def write_result(self, result: dict) -> None:
        command_id = str(result.get("command_id") or "unknown")
        with self.lock:
            atomic_json(self.results / f"{command_id}_result.json", result)
            src = self.inflight.pop(command_id, None)
            waiter = self.transient_waiters.get(command_id)
            if waiter is not None:
                self.transient_results[command_id] = result
                waiter.set()
            if src and src.exists():
                dst = self.processed / src.name
                if dst.exists():
                    dst = self.processed / f"{src.stem}_{int(time.time())}{src.suffix}"
                shutil.move(str(src), str(dst))

    def queue_status(self) -> dict:
        with self.lock:
            return {
                "queued": [p.name for p in self._candidate_commands()],
                "rpc_queued": [str(cmd.get("command_id")) for cmd in self.transient_queue],
                "inflight": list(self.inflight),
                "latest_scene": (self.current_state() or {}).get("scene_name")
            }


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "AcqFoundryBridge/0.1"

    @property
    def store(self) -> BridgeStore:
        return self.server.store

    def log_message(self, fmt, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {fmt % args}\n")

    def _origin_allowed(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True
        return bool(LOCAL_ORIGIN_RE.match(origin))

    def _cors(self):
        origin = self.headers.get("Origin")
        if origin and LOCAL_ORIGIN_RE.match(origin):
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def _json(self, status: int, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _empty(self, status: int):
        self.send_response(status)
        self._cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _read_json(self):
        n = int(self.headers.get("Content-Length", "0") or "0")
        if n > MAX_BODY:
            raise ValueError("Request body too large")
        data = self.rfile.read(n)
        return json.loads(data.decode("utf-8")) if data else {}

    def do_OPTIONS(self):
        if not self._origin_allowed():
            return self._empty(403)
        self._empty(204)

    def do_GET(self):
        if not self._origin_allowed():
            return self._json(403, {"ok": False, "error": "Origin not allowed"})
        parsed = urlparse(self.path)

        if parsed.path == "/health":
            return self._json(200, {
                "ok": True,
                "protocol_version": PROTOCOL_VERSION,
                "status": self.store.queue_status()
            })

        if parsed.path == "/bridge/next":
            qs = parse_qs(parsed.query)
            world_id = (qs.get("world_id") or [None])[0]
            scene_id = (qs.get("scene_id") or [None])[0]
            try:
                command = self.store.claim_next(world_id, scene_id)
            except Exception as exc:
                return self._json(500, {"ok": False, "error": str(exc)})
            if command is None:
                return self._empty(204)
            return self._json(200, command)

        return self._json(404, {"ok": False, "error": "Not found"})

    def do_POST(self):
        if not self._origin_allowed():
            return self._json(403, {"ok": False, "error": "Origin not allowed"})
        parsed = urlparse(self.path)
        try:
            payload = self._read_json()
        except Exception as exc:
            return self._json(400, {"ok": False, "error": f"Invalid JSON: {exc}"})

        if parsed.path == "/rpc":
            try:
                timeout = float(payload.pop("_timeout_seconds", 30.0))
                timeout = max(1.0, min(timeout, 120.0))
                result = self.store.enqueue_rpc(payload, timeout=timeout)
                return self._json(200 if result.get("ok") else 409, result)
            except TimeoutError as exc:
                return self._json(504, {"ok": False, "error": str(exc)})
            except Exception as exc:
                return self._json(500, {"ok": False, "error": str(exc)})

        if parsed.path == "/bridge/state":
            try:
                self.store.write_state(payload)
                return self._json(200, {"ok": True})
            except Exception as exc:
                return self._json(500, {"ok": False, "error": str(exc)})

        if parsed.path == "/bridge/result":
            try:
                self.store.write_result(payload)
                return self._json(200, {"ok": True})
            except Exception as exc:
                return self._json(500, {"ok": False, "error": str(exc)})

        return self._json(404, {"ok": False, "error": "Not found"})


def serve(transport: Path, host: str, port: int):
    store = BridgeStore(transport)
    server = ThreadingHTTPServer((host, port), BridgeHandler)
    server.store = store

    atomic_json(store.state / "agent_status.json", {
        "protocol_version": PROTOCOL_VERSION,
        "agent": "Acq Foundry Bridge Agent",
        "status": "listening",
        "started_at": utcnow(),
        "listen": f"http://{host}:{port}",
        "transport_root": str(store.root)
    })

    print("Acq Foundry Bridge Agent v0.1")
    print(f"  listening: http://{host}:{port}")
    print(f"  transport: {store.root}")
    print("  Press Ctrl+C to stop.")
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        print("\nStopping bridge.")
    finally:
        server.server_close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transport", required=True, type=Path,
                    help="Local synced D&D/Foundry Bridge directory.")
    ap.add_argument("--host", default="127.0.0.1",
                    help="Bind address. Keep 127.0.0.1 unless you understand the security impact.")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = ap.parse_args()

    if args.host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("v0.1 intentionally refuses non-loopback bind addresses.")
    serve(args.transport, args.host, args.port)


if __name__ == "__main__":
    main()
