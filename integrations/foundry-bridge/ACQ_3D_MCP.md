# Acq 3D MCP — narrow control-plane design

Status: draft selected architecture, 2026-10-05

## Purpose

The hosted Foundry MCP is now proven live and owns generic Foundry/D&D5e automation. This private MCP exists only for the capabilities the hosted toolset does not expose adequately for the campaign's 3D authoring loop.

The governing rule is **do not rebuild Foundry**.

## What the existing Acq bridge already gives us

The current module already has the core write primitives needed for 3D authoring:

- revision-hashed full Scene snapshots;
- allow-listed Scene updates;
- create/update/delete for embedded Tiles, AmbientLights, Walls, Regions, Notes, Tokens and related documents;
- allow-listed 3D Canvas Scene environment flags;
- direct 3D Tile model assignment through `flags.levels-3d-preview.model3d`;
- asset upload through Foundry FilePicker;
- GM-only operation;
- no eval / arbitrary JavaScript / shell;
- pre-command state backup in the existing local agent.

Therefore the new MCP must mostly be an **adapter over proven primitives**, not a new scene engine.

## 3D Canvas runtime facts verified upstream

3D Canvas exposes its live runtime at `game.Levels3DPreview`.

Relevant stable-enough runtime members used by 3D Canvas itself include:

- `game.Levels3DPreview.scene` — Three.js scene;
- `game.Levels3DPreview.renderer` — Three.js renderer;
- `game.Levels3DPreview.camera.position`;
- `game.Levels3DPreview.controls.target`;
- `game.Levels3DPreview.controls.update()`.

3D Canvas itself persists/captures initial camera state as:

- `flags.levels-3d-preview.initialPosition.position`;
- `flags.levels-3d-preview.initialPosition.target`;
- `flags.levels-3d-preview.initialPosition.firstPersonMode`.

3D Tiles are ordinary Foundry Tile documents with `flags.levels-3d-preview.*`. Verified useful flags include:

- `model3d`;
- `material`;
- `color`;
- `scale`;
- `collision`;
- `sight`;
- `cameraCollision`;
- `doorType`;
- `doorState`;
- `doorStyle`.

The existing bridge already supports arbitrary allow-listed embedded Tile create/update, so we do not need a second placement engine.

## Missing capabilities to add

Only four genuinely missing capabilities are required before the vertical slice can be rebuilt through ChatGPT:

1. **True 3D runtime inspection**
   - report whether 3D Canvas is active;
   - report camera/target;
   - surface relevant 3D Tile flags and environment flags.

2. **True 3D camera control**
   - set `camera.position`;
   - set `controls.target`;
   - call controls update;
   - optionally persist as initial scene camera only on explicit request.

3. **True 3D capture**
   - render/capture from `game.Levels3DPreview.renderer`, not `canvas.app.view`;
   - allow canonical camera stations;
   - return WebP/PNG payload plus camera metadata.

4. **Asset discovery**
   - search installed, licensed 3D asset/module paths and return references;
   - never copy third-party asset binaries into GitHub;
   - catalog semantic roles to existing Foundry paths.

Everything else should use hosted Foundry MCP or the bridge's current declarative primitives.

## Safety and transaction model

Meaningful scene writes follow:

```
inspect
  -> snapshot/clone
  -> expected_revision check
  -> idempotent semantic apply
  -> structural readback
  -> 3D camera capture
  -> accept or restore
```

Every generated placeable should carry project flags:

- `flags.acq.semantic_id`
- `flags.acq.build_id`
- `flags.acq.provenance`
- `flags.acq.classification`

No tool may expose arbitrary JS, shell, database access or generic macro execution.

## Transport

The preferred final route is:

```
ChatGPT
  -> OpenAI Secure MCP Tunnel
  -> local Acq 3D MCP
  -> loopback Acq bridge agent
  -> Acq Foundry Bridge module
  -> Foundry + 3D Canvas
```

The Secure MCP Tunnel is appropriate because the MCP server remains private and the tunnel client makes an outbound connection; Foundry does not need a public listener.

Google Drive remains artifact/private-source/release storage and emergency fallback transport, not the normal interactive command bus.

## Implementation order

1. Add 3D runtime inspect/camera/capture operations to the existing Foundry module.
2. Add local loopback RPC endpoints in the agent so MCP calls do not need Drive files.
3. Wrap those endpoints in the small MCP tool surface defined in `MCP_TOOL_SURFACE.json`.
4. Validate locally with MCP Inspector.
5. Connect through Secure MCP Tunnel.
6. Run read-only inspection/capture tests.
7. Run one disposable Tile create/update/delete transaction.
8. Only then begin the Episode 1 asset-first vertical-slice rebuild.
