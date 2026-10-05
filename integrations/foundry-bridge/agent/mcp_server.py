#!/usr/bin/env python3
"""
Acq 3D MCP

Narrow project-specific MCP surface for Foundry VTT + 3D Canvas.
Generic Foundry/D&D5e automation remains delegated to Foundry MCP.

Transport:
  ChatGPT -> Secure MCP Tunnel -> this server -> Acq Bridge Agent -> Foundry module
"""

from __future__ import annotations

import json
import os
import uuid
from typing import Any
from urllib import error, request

from mcp.server import MCPServer

AGENT_URL = os.environ.get("ACQ_BRIDGE_AGENT_URL", "http://127.0.0.1:18747").rstrip("/")
HOST = os.environ.get("ACQ_3D_MCP_HOST", "127.0.0.1")
PORT = int(os.environ.get("ACQ_3D_MCP_PORT", "18748"))

mcp = MCPServer("Acq 3D MCP")


def _rpc(
    operations: list[dict[str, Any]],
    *,
    scene_id: str | None = None,
    expected_revision: str | None = None,
    dry_run: bool = False,
    timeout_seconds: float = 45.0,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "protocol_version": 1,
        "command_id": f"mcp-{uuid.uuid4()}",
        "operations": operations,
        "dry_run": dry_run,
        "_timeout_seconds": timeout_seconds,
    }
    if scene_id:
        payload["scene_id"] = scene_id
    if expected_revision:
        payload["expected_revision"] = expected_revision

    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{AGENT_URL}/rpc",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds + 5.0) as response:
            result = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw)
        except json.JSONDecodeError:
            detail = {"error": raw or str(exc)}
        raise RuntimeError(detail.get("error") or f"Bridge RPC failed with HTTP {exc.code}") from exc
    except error.URLError as exc:
        raise RuntimeError(
            f"Cannot reach Acq Bridge Agent at {AGENT_URL}. "
            "Start the local bridge agent and keep the Foundry GM world open."
        ) from exc

    if not result.get("ok"):
        raise RuntimeError(result.get("error") or "Foundry command failed")
    return result


def _operation(result: dict[str, Any], index: int = 0) -> dict[str, Any]:
    operations = result.get("operations") or []
    if index >= len(operations):
        return {"ok": False, "error": "Bridge returned no operation result", "bridge": result}
    out = dict(operations[index])
    out["scene_id"] = result.get("scene_id")
    out["before_revision"] = result.get("before_revision")
    out["after_revision"] = result.get("after_revision")
    return out


@mcp.tool()
def inspect_3d_scene(scene_id: str | None = None) -> dict[str, Any]:
    """Inspect active 3D Canvas state, camera, environment, semantic 3D tiles, lights and regions."""
    return _operation(_rpc([{"op": "inspect_3d_scene"}], scene_id=scene_id))


@mcp.tool()
def search_3d_assets(
    query: str,
    limit: int = 50,
    roots: list[str] | None = None,
    max_depth: int = 5,
    scene_id: str | None = None,
) -> dict[str, Any]:
    """Search installed 3D Canvas/module asset paths without copying third-party asset binaries."""
    op: dict[str, Any] = {
        "op": "search_3d_assets",
        "query": query,
        "limit": limit,
        "max_depth": max_depth,
    }
    if roots:
        op["roots"] = roots
    return _operation(_rpc([op], scene_id=scene_id, timeout_seconds=90.0))


@mcp.tool()
def set_3d_camera(
    position: dict[str, float] | None = None,
    target: dict[str, float] | None = None,
    save_as_initial: bool = False,
    scene_id: str | None = None,
    expected_revision: str | None = None,
) -> dict[str, Any]:
    """Move the GM 3D camera. By default this is ephemeral; save_as_initial persists the view on the Scene."""
    if position is None and target is None:
        raise ValueError("Provide position and/or target.")
    return _operation(
        _rpc(
            [{
                "op": "set_3d_camera",
                "position": position,
                "target": target,
                "save_as_initial": save_as_initial,
            }],
            scene_id=scene_id,
            expected_revision=expected_revision,
        )
    )


@mcp.tool()
def reload_3d_scene(
    scene_id: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Safely reload the active 3D Canvas runtime for the current Scene without changing canonical Scene data."""
    return _operation(
        _rpc(
            [{"op": "reload_3d_scene"}],
            scene_id=scene_id,
            dry_run=dry_run,
            timeout_seconds=30.0,
        )
    )


@mcp.tool()
def capture_3d_view(
    position: dict[str, float] | None = None,
    target: dict[str, float] | None = None,
    width: int | None = None,
    height: int | None = None,
    format: str = "webp",
    quality: float = 0.85,
    restore_camera: bool = True,
    scene_id: str | None = None,
) -> dict[str, Any]:
    """Capture the actual 3D Canvas Three.js renderer, optionally from a temporary camera position."""
    return _operation(
        _rpc(
            [{
                "op": "capture_3d_view",
                "position": position,
                "target": target,
                "width": width,
                "height": height,
                "format": format,
                "quality": quality,
                "restore_camera": restore_camera,
            }],
            scene_id=scene_id,
            timeout_seconds=60.0,
        )
    )


@mcp.tool()
def set_3d_environment(
    values: dict[str, Any],
    scene_id: str | None = None,
    expected_revision: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Update allow-listed 3D Canvas Scene environment settings with optional revision checking."""
    return _operation(
        _rpc(
            [{"op": "set_3d_environment", "values": values}],
            scene_id=scene_id,
            expected_revision=expected_revision,
            dry_run=dry_run,
        )
    )


@mcp.tool()
def apply_semantic_objects(
    objects: list[dict[str, Any]],
    build_id: str | None = None,
    scene_id: str | None = None,
    expected_revision: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Idempotently create/update allow-listed Scene documents by stable flags.acq.semantic_id."""
    if not objects:
        raise ValueError("objects must not be empty")
    return _operation(
        _rpc(
            [{
                "op": "apply_semantic_objects",
                "objects": objects,
                "build_id": build_id,
            }],
            scene_id=scene_id,
            expected_revision=expected_revision,
            dry_run=dry_run,
            timeout_seconds=90.0,
        )
    )



@mcp.tool()
def delete_semantic_objects(
    semantic_ids: list[str],
    scene_id: str | None = None,
    expected_revision: str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Delete Scene documents previously created by this MCP using stable flags.acq.semantic_id."""
    if not semantic_ids:
        raise ValueError("semantic_ids must not be empty")
    return _operation(
        _rpc(
            [{"op": "delete_semantic_objects", "semantic_ids": semantic_ids}],
            scene_id=scene_id,
            expected_revision=expected_revision,
            dry_run=dry_run,
            timeout_seconds=90.0,
        )
    )


@mcp.tool()
def validate_scene_manifest(
    expected_manifest: dict[str, Any],
    scene_id: str | None = None,
) -> dict[str, Any]:
    """Validate semantic IDs and document counts against the live Scene without modifying it."""
    return _operation(
        _rpc(
            [{"op": "validate_scene_manifest", "expected_manifest": expected_manifest}],
            scene_id=scene_id,
        )
    )


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        stateless_http=True,
        json_response=True,
    )
