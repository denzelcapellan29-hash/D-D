# Acq Foundry Bridge + Acq 3D MCP

Project-specific control plane for Foundry VTT v14 + 3D Canvas.

Generic Foundry/D&D5e automation is delegated to the hosted Foundry MCP. This bridge exists only for specialized 3D Canvas authoring and visual QA.

## Architecture

```
ChatGPT
  |\
  | \ hosted Foundry MCP -> generic actors/items/journals/scenes/tokens/combat/compendiums
  |
  +-> OpenAI Secure MCP Tunnel
        -> Acq 3D MCP (127.0.0.1:18748)
        -> Acq Bridge Agent RPC (127.0.0.1:18747)
        -> Acq Foundry Bridge module
        -> Foundry + 3D Canvas
```

Google Drive remains available for private sources, releases, captures, backups and emergency command transport. It is no longer the preferred interactive command bus.

## Security model

- Both local services bind to loopback only.
- The Foundry module executes commands only for an active GM client.
- Meaningful Scene writes can require an `expected_revision`.
- No arbitrary JavaScript eval, shell execution or direct Foundry database writes.
- Script macros remain disabled in the generic Foundry API Bridge.
- Third-party 3D assets are referenced by installed Foundry paths; they are not copied into GitHub.

## Current specialized operations

- `inspect_3d_scene`
- `search_3d_assets`
- `set_3d_camera`
- `capture_3d_view`
- `set_3d_environment`
- `apply_semantic_objects`
- `validate_scene_manifest`
- existing declarative embedded-document CRUD / model assignment / asset upload

See `PROTOCOL.json`, `MCP_TOOL_SURFACE.json` and `ACQ_3D_MCP.md`.

## Direct RPC

The local agent exposes `POST /rpc` for synchronous MCP calls. The request is queued in memory, the Foundry module claims it through its existing polling loop, and the agent returns the result to the MCP caller. This bypasses Google Drive command files while preserving the existing revision checks and module allow-list.

The original Drive command transport remains operational as a fallback.

## MCP server

The narrow Streamable HTTP MCP server lives at:

`agent/mcp_server.py`

Default endpoint:

`http://127.0.0.1:18748/mcp`

It targets MCP Python SDK v2 and uses stateless JSON responses. For private ChatGPT access, connect it through OpenAI Secure MCP Tunnel rather than exposing port 18748 publicly.

## Windows install / launch

`install_windows.ps1` copies the Foundry module and generates a launcher that:

1. creates a local Python virtual environment if needed;
2. installs `requirements-mcp.txt`;
3. starts the loopback bridge agent;
4. starts the Acq 3D MCP server.

The user still must perform the unavoidable Foundry restart/module-enable step and create/authorize the OpenAI tunnel.

## Development QA

`.github/workflows/foundry-bridge-smoke.yml` checks:

- protocol JSON;
- Python syntax;
- JavaScript syntax;
- MCP SDK installation;
- MCP server import.

Before production scene writes, the remaining runtime gate is:

1. install the updated module;
2. start the local stack;
3. connect Secure MCP Tunnel;
4. verify read-only 3D inspection and capture;
5. perform one disposable semantic Tile create/update/delete transaction;
6. only then begin the Episode 1 vertical-slice rebuild.
