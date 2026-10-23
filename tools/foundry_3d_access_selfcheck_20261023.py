#!/usr/bin/env python3
"""Read-only inventory of the installed Foundry / 3D Canvas / Acq MCP access boundary.

No browser commands, UI actions, command queuing, file writes, process changes,
scene changes, module changes, secrets, or remote traffic. HTTP probes only
127.0.0.1 /health, Foundry root and MCP tools/list.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request


def _request_json(url: str, payload: dict | None = None, timeout: float = 3):
    headers = {"Accept": "application/json, text/event-stream"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        url, data=None if payload is None else json.dumps(payload).encode("utf-8"),
        method="GET" if payload is None else "POST", headers=headers
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read(180000).decode("utf-8", "replace")
            return {"http": response.status, "data": json.loads(data) if data.lstrip().startswith("{") else None}
    except urllib.error.HTTPError as exc:
        return {"http": exc.code, "error": "HTTP error"}
    except Exception as exc:
        return {"error": type(exc).__name__ + ": " + str(exc)[:120]}


def _get_root_http(url: str):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return {"http": response.status}
    except Exception as exc:
        return {"error": type(exc).__name__}


def _age_file(path: Path) -> dict:
    if not path.is_file():
        return {"present": False}
    age = max(0, dt.datetime.now(dt.timezone.utc).timestamp() - path.stat().st_mtime)
    answer = {"present": True, "age_seconds": round(age, 1)}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        answer.update({k: data.get(k) for k in ("scene_id", "scene_name", "revision", "reason") if k in data})
    except (OSError, ValueError):
        answer["metadata_error"] = True
    return answer


def collect_access_audit(chatgpt_visible_tools: list[str] | None = None):
    local = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\denze\AppData\Local"))
    modules = local / "FoundryVTT" / "Data" / "modules"
    firstparty = modules / "acq-foundry-bridge" / "scripts" / "acq-foundry-bridge.js"
    agent = Path(os.environ.get("USERPROFILE", r"C:\Users\denze")) / "Downloads" / "Acq_Foundry_3D_MCP" / "agent" / "mcp_server.py"
    transport = Path(os.environ.get("ACQ_BRIDGE_TRANSPORT", r"G:\My Drive\D&D\Foundry Bridge"))
    module_ids = ("levels-3d-preview", "canvas3dcompendium",
                  "canvas3d-premium", "canvas3dtokencompendium",
                  "acq-foundry-bridge")
    versions = {}
    for name in module_ids:
        manifest = modules / name / "module.json"
        if manifest.is_file():
            try:
                j = json.loads(manifest.read_text(encoding="utf-8"))
                versions[name] = j.get("version")
            except (OSError, ValueError):
                versions[name] = "metadata_error"
        else:
            versions[name] = None
    bridge_ops = []
    js_hash = None
    if firstparty.is_file():
        contents = firstparty.read_text(encoding="utf-8", errors="replace")
        bridge_ops = sorted(set(re.findall(r"""if\s*\(type\s*===\s*['"]([^'"]+)""", contents)))
        js_hash = hashlib.sha256(firstparty.read_bytes()).hexdigest()
    mcp_tools = _request_json("http://127.0.0.1:18748/mcp", {
        "jsonrpc": "2.0", "id": 71, "method": "tools/list", "params": {}
    }, timeout=6)
    advertised = sorted(t["name"] for t in (
        ((mcp_tools.get("data") or {}).get("result") or {}).get("tools") or []
    ))
    visible = sorted(chatgpt_visible_tools or [])
    bridge_health = _request_json("http://127.0.0.1:18747/health")
    tunnel_health = _request_json("http://127.0.0.1:8083/health")
    status = (bridge_health.get("data") or {}).get("status", {})
    tun = tunnel_health.get("data") or {}
    out = {
        "audit_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "policy": "read_only_no_browser_commands",
        "versions": versions,
        "http": {"foundry": _get_root_http("http://127.0.0.1:30000/"),
                 "bridge_agent": bridge_health.get("http"),
                 "mcp_server": mcp_tools.get("http"),
                 "tunnel": tunnel_health.get("http")},
        "agent_command_queue": {
            "queued_count": len(status.get("queued") or []),
            "rpc_queued_count": len(status.get("rpc_queued") or []),
            "inflight_count": len(status.get("inflight") or []),
            "latest_scene": status.get("latest_scene"),
        },
        "tunnel_ready": bool(tun.get("live") and tun.get("ready")),
        "browser_poll_telemetry": status.get("browser_poll", "UNAVAILABLE_IN_RUNNING_AGENT"),
        "browser_result_telemetry": status.get("browser_result", "UNAVAILABLE_IN_RUNNING_AGENT"),
        "last_browser_scene_snapshot": _age_file(transport / "state" / "current_scene.json"),
        "firstparty_bridge_js_sha256": js_hash,
        "mcp_server_script_present": agent.is_file(),
        "native_bridge_op_count": len(bridge_ops),
        "native_bridge_operations": bridge_ops,
        "running_mcp_tool_count": len(advertised),
        "running_mcp_tools": advertised,
        "chatgpt_tool_count_snapshot": len(visible) if chatgpt_visible_tools is not None else None,
        "chatgpt_tools_missing_from_running_mcp": sorted(set(advertised)-set(visible))
            if chatgpt_visible_tools is not None else None,
        "chatgpt_tools_not_advertised_by_running_mcp": sorted(set(visible)-set(advertised))
            if chatgpt_visible_tools is not None else None,
        "notes": [
            "A browser scene snapshot is event-driven, not a heartbeat: age does not prove GM polling is alive.",
            "An HTTP 200 for /mcp does not prove a Foundry browser command can complete.",
            "Native 3D Canvas code availability does not imply the function is exposed by a typed MCP tool.",
            "A tool may be advertised by the running MCP server but not yet surfaced in ChatGPT.",
        ],
    }
    return out


if __name__ == "__main__":
    print(json.dumps(collect_access_audit(), indent=2))
