#!/usr/bin/env python3
"""Guarded FIRST-PARTY Bridge agent telemetry upgrade; never touch third-party modules.

Dry-run by default. Opt-in apply explicitly requires --allow-deploy.
Source bytes are supplied offline as a local candidate file; both source and
installed SHA256 pins are immutable. Rollback is attempted once on failed restart.
No Foundry Scene, world setting, vendor file, or MCP server is modified.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time
import urllib.request

EXPECTED_OLD = "b1a023d388f4be1b28dc2636f95c05390f563bce18d1f52b2b5648ae7704ce09"
EXPECTED_NEW = "93edf24c0bcc60f3a3a63fe611b83303fec024fff4f5289194203b23184f49d2"
SCENE_ID = "NUEDEFAULTSCENE0"
SCENE_SHA = "e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def health(timeout=2.0):
    with urllib.request.urlopen("http://127.0.0.1:18747/health", timeout=timeout) as r:
        if r.status != 200:
            raise RuntimeError("Bridge health HTTP != 200")
        return json.loads(r.read())


def processes_and_listener():
    ps = r'''$p=@(Get-CimInstance Win32_Process | Where-Object {
 $_.Name -in @("python.exe","pythonw.exe") -and $_.CommandLine -match "acq_bridge_agent[.]py"
} | ForEach-Object { [pscustomobject]@{pid=[int]$_.ProcessId;parent=[int]$_.ParentProcessId;cmd=[string]$_.CommandLine} })
$l=@(Get-NetTCPConnection -LocalPort 18747 -State Listen -ErrorAction SilentlyContinue |
 ForEach-Object { [int]$_.OwningProcess })
[pscustomobject]@{processes=$p;listeners=$l} | ConvertTo-Json -Depth 5 -Compress'''
    r = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps],
        text=True, capture_output=True, timeout=12, check=True,
    )
    j = json.loads(r.stdout)
    return j.get("processes") or [], j.get("listeners") or []


def cli_details(process: dict):
    argv = [x.strip('"') for x in shlex.split(process["cmd"], posix=False)]
    if len(argv) < 4 or not argv[1].lower().endswith("acq_bridge_agent.py"):
        raise RuntimeError("Unrecognized running Bridge command")
    if "--transport" not in argv:
        raise RuntimeError("Bridge lacks explicit transport path")
    idx = argv.index("--transport")
    if idx + 1 >= len(argv):
        raise RuntimeError("No transport path")
    transport = Path(argv[idx + 1])
    if not transport.is_dir():
        raise RuntimeError("Transport root unavailable")
    for forbidden in ("--host", "--port"):
        if forbidden in argv:
            raise RuntimeError("Non-default port/host args require separate source audit")
    return transport


def preflight(candidate: bytes, target: Path, backup_root: Path):
    if target.name != "acq_bridge_agent.py" or target.parent.name != "agent":
        raise ValueError("Non-allowlisted first-party destination")
    installed = target.read_bytes()
    if sha(installed) != EXPECTED_OLD:
        raise RuntimeError("STOP: installed agent SHA does not match expected pre-upgrade pin")
    if sha(candidate) != EXPECTED_NEW:
        raise RuntimeError("STOP: candidate agent SHA not approved pin")
    import ast
    ast.parse(candidate.decode("utf-8"))
    h = health()
    queue = h["status"]
    if any(queue.get(k) for k in ("queued", "rpc_queued", "inflight")):
        raise RuntimeError("STOP: Bridge commands in-flight or queued")
    ps, listeners = processes_and_listener()
    if len(set(listeners)) != 1:
        raise RuntimeError(f"STOP: expected one Bridge listener, found {listeners}")
    worker_pid = int(listeners[0])
    workers = [p for p in ps if int(p["pid"]) == worker_pid]
    if len(workers) != 1:
        raise RuntimeError("STOP: Bridge listener does not belong to the expected agent worker")
    if len(ps) > 2:
        raise RuntimeError("STOP: unexpected multiple Bridge processes")
    transport = cli_details(workers[0])
    if target.resolve() != Path.home().joinpath(
        "Downloads", "Acq_Foundry_3D_MCP", "agent", "acq_bridge_agent.py"
    ).resolve():
        raise RuntimeError("STOP: destination is not the pinned installed first-party agent")
    if not backup_root.is_dir():
        raise RuntimeError("STOP: existing backup root missing")
    state_path = transport / "state" / "current_scene.json"
    state = json.loads(state_path.read_text(encoding="utf8"))
    if state.get("scene_id") != SCENE_ID or state.get("revision") != SCENE_SHA:
        raise RuntimeError("STOP: source Scene state differs from pinned accepted checksum")
    return {
        "ok": True, "mode": "dry_run", "old_sha": sha(installed),
        "candidate_sha": sha(candidate), "worker_pid": worker_pid,
        "parent_pid": workers[0].get("parent"), "transport": str(transport),
        "before_scene_revision": state["revision"], "running_agent_healthy": True,
        "queued": 0, "inflight": 0,
    }


def stop_specific_worker(pid: int):
    current, listeners = processes_and_listener()
    if set(listeners) != {pid} or not any(int(p["pid"]) == pid for p in current):
        raise RuntimeError("Refusing stop: listener identity changed since preflight")
    subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
         f"Stop-Process -Id {pid} -ErrorAction Stop"],
        capture_output=True, text=True, timeout=8, check=True,
    )
    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline:
        _, listeners = processes_and_listener()
        if not listeners:
            return
        time.sleep(0.25)
    raise RuntimeError("Bridge port 18747 did not close after bounded stop")


def spawn_agent(target: Path, transport: str, log_root: Path, label: str):
    exe = Path.home() / "AppData" / "Local" / "Python" / "pythoncore-3.14-64" / "python.exe"
    if not exe.is_file():
        raise RuntimeError("Pinned Python interpreter not installed")
    out = (log_root / f"{label}.out.log").open("ab")
    err = (log_root / f"{label}.err.log").open("ab")
    flags = (getattr(subprocess, "DETACHED_PROCESS", 0) |
             getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))
    try:
        proc = subprocess.Popen(
            [str(exe), "-u", str(target), "--transport", transport],
            cwd=str(target.parent), stdin=subprocess.DEVNULL,
            stdout=out, stderr=err, close_fds=True, creationflags=flags,
        )
    finally:
        out.close()
        err.close()
    return proc


def await_health(marker: bool, timeout: float = 7):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            status = health(0.7).get("status") or {}
            if ("browser_poll" in status) == marker:
                return status
        except Exception:
            pass
        time.sleep(0.3)
    raise RuntimeError("Bridge did not answer expected health schema after bounded startup")


def upgrade(candidate: bytes, target: Path, backup_root: Path, *, apply: bool,
            allow_deploy: bool):
    info = preflight(candidate, target, backup_root)
    if not apply:
        return info
    if not allow_deploy:
        raise PermissionError("Explicit --allow-deploy required")
    backup_id = "bridge-agent-heartbeat-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    checkpoint = backup_root / backup_id
    checkpoint.mkdir(mode=0o700, parents=False, exist_ok=False)
    original = target.read_bytes()
    (checkpoint / "acq_bridge_agent.py.preupgrade").write_bytes(original)
    (checkpoint / "manifest.json").write_text(
        json.dumps({k: info[k] for k in ("old_sha", "candidate_sha", "before_scene_revision")}, indent=2),
        encoding="utf8",
    )
    # Do not touch the production file unless the immutable backup was verified.
    if sha((checkpoint / "acq_bridge_agent.py.preupgrade").read_bytes()) != EXPECTED_OLD:
        raise RuntimeError("STOP: backup verify failed")
    halted = False
    started_pid = None
    try:
        stop_specific_worker(info["worker_pid"])
        halted = True
        tmp = target.with_suffix(".heartbeat-stage.tmp")
        try:
            tmp.write_bytes(candidate)
            if sha(tmp.read_bytes()) != EXPECTED_NEW:
                raise RuntimeError("Candidate stage verification failed")
            os.replace(tmp, target)
        finally:
            tmp.unlink(missing_ok=True)
        proc = spawn_agent(target, info["transport"], checkpoint, "new-v04-bridge-agent")
        started_pid = proc.pid
        state = await_health(marker=True)
        if sha(target.read_bytes()) != EXPECTED_NEW:
            raise RuntimeError("Unexpected on-disk agent checksum after deployment")
        scene = json.loads((Path(info["transport"]) / "state" / "current_scene.json").read_text(encoding="utf8"))
        if scene.get("revision") != SCENE_SHA:
            raise RuntimeError("Accepted source Scene revision changed during agent restart")
        return {
            "ok": True, "status": "INSTALLED_HEALTH_VERIFIED",
            "backup_id": backup_id, "new_pid": started_pid,
            "new_sha": sha(target.read_bytes()),
            "recent_gm_poll": bool(state.get("browser_poll", {}).get("recent_within_10s")),
            "poll_count": state.get("browser_poll", {}).get("total_polls"),
            "source_scene_unchanged": True,
            "note": "HTTP health is verified. GM command reliability requires separate repeated read-only QA.",
        }
    except Exception as failure:
        if not halted:
            raise
        errors = []
        # One verified rollback; do not retry endlessly.
        try:
            active, listeners = processes_and_listener()
            if len(listeners) == 1:
                owner = int(listeners[0])
                if started_pid and owner == started_pid:
                    stop_specific_worker(owner)
                else:
                    errors.append("Unexpected Bridge listener owner during rollback; left untouched")
            if errors:
                raise RuntimeError("; ".join(errors))
            temp = target.with_suffix(".rollback-stage.tmp")
            try:
                temp.write_bytes(original)
                if sha(temp.read_bytes()) != EXPECTED_OLD:
                    raise RuntimeError("Backup rollback hash mismatch")
                os.replace(temp, target)
            finally:
                temp.unlink(missing_ok=True)
            restore = spawn_agent(target, info["transport"], checkpoint, "rolled-back-old-agent")
            await_health(marker=False)
            raise RuntimeError(
                "Upgrade FAILED; old agent restored and health verified, "
                f"restore PID {restore.pid}; original error: {failure}"
            )
        except Exception as rollback_error:
            raise RuntimeError(
                f"STOP: initial upgrade error: {failure}; rollback state: {rollback_error}; "
                f"checkpoint: {checkpoint}"
            ) from rollback_error


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--candidate", required=True, type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--allow-deploy", action="store_true")
    args = ap.parse_args()
    target = Path.home() / "Downloads" / "Acq_Foundry_3D_MCP" / "agent" / "acq_bridge_agent.py"
    backup_root = Path.home() / "Acq3DDeployAgent" / "backups"
    print(json.dumps(upgrade(args.candidate.read_bytes(), target, backup_root,
                             apply=args.apply, allow_deploy=args.allow_deploy), indent=2))


if __name__ == "__main__":
    main()
