# 3D Canvas creator documentation gap analysis — 2026-10-15

Status: documentation-backed research (TheRipper93 wiki), no Foundry scene edits and no custom MCP runtime pass. Supersedes early speculative assumptions where indicated. Source links below are public creator documentation; verify the installed v9.0.35 behavior independently.

## Sources
- https://wiki.theripper93.com/levels-3d-preview
- https://wiki.theripper93.com/levels-3d-preview/info/entities/tiles
- https://wiki.theripper93.com/levels-3d-preview/info/entities/lights
- https://wiki.theripper93.com/levels-3d-preview/info/entities/walls
- https://wiki.theripper93.com/levels-3d-preview/info/fow
- https://wiki.theripper93.com/levels-3d-preview/info/shaders
- https://wiki.theripper93.com/levels-3d-preview/info/entities/templates
- https://wiki.theripper93.com/levels-3d-preview/canvas3dcompendium
- https://wiki.theripper93.com/levels

## Platform architecture
3D Canvas uses GLB/GLTF (recommended; FBX being phased out). 3D Tiles are the core spatial unit for floors, walls, roofs, ceilings, decorations and sight/movement-blocking architecture. Ordinary 2D Foundry Walls render in 3D but creator recommends Tiles for 3D architecture. The public hosted Foundry MCP has 121 RPG/document tools, with scene read, activate, door-state but **no general 3D Tile create/update/delete or lights/camera/material/renderer ops** in its advertised surface. The seven custom Acq_3D_Map tools cover inspect, assets search, camera set, camera capture, environment set, semantic object application and manifest validation; yet actual tunnel disconnected so these remain unverified end-to-end.

## Important 3D Tile fields and engine behavior
- 3D model path URL; source-authoritative Meshy GLB with original geometry immutable. 3D model may be recentered or autogrounded; Auto Ground documented enabled by default. Calibrate disabled vs enabled with origin/bounds readback; Depth distinct from width/height; tilt X/Y.
- 3D Tile has Block Movement, Block Sight, Camera Collider, is Door, Door State. Non-occluding decorative tiles should have sight blocking disabled for performance.
- Creator documents case-sensitive GLTF/GLB object custom properties `collision` integer 0/1, `sight` integer 0/1, `isDoor` int 0/1/2, `doorId` unique string, `ds` int 0/1/2, `doorStyle` int 0/1, `doorAnimateAngle` integer degrees. Preserve original Meshy vertices but include node custom properties in exported copy, then validate loaded Three.js door/collision behavior.
- Material options tint, texture/repeat, roughness, reflectivity (metalness), opacity, shading, sides, optional per-object shaders. Do not equate Blender and Foundry color hex; fixed-light capture and PBR comparison essential.
- Tile Repeat and merge improve duplicate instance efficiency, but merge can replace tiles; automatic merge documentation explicitly requires backup and skips doors. Our semantic identifiers/rollback must be reconciled with merge.
- Multi-level visibility requires level configuration, Mirror Levels Tile Visibility; verify 3D behavior with actual player token.

## Camera and rendering
3D Canvas camera has free rotate/pan/zoom, first person, reset initial, focus selected token, Game Camera and top-down mode. Seven custom tools provide position/target and actual canvas capture, **no advertised calibration of FOV, aspect, near/far, up vector, scene-to-Three coordinate conversion or renderer statistics**. Need explicit camera-state readback and 4 anchored QA cameras (player, overhead, section, joint closeup), restore previous state, actual PNG/webp capture inspection.

## Lighting
Ordinary lights supported but 3D lighting shadows/occlusion generally do not operate unless special shadow casting/blocking is enabled. Creator warns no more than 2-3 shadow casting/blocking lights per scene due severe performance/crash risk; shader compilation can freeze when lights added. Support only Pulse, Chroma and Flickering Light animations. Need per-light budget, ambient/sky baseline, emission PBR inspection and GPU performance measurements.

## Vision and secret protection
3D fog defaults OFF; Token Vision and Fog Exploration defaults ON, Use 3D Geometry for sight calculations defaults OFF. Full 3D mode requires geometry sight and fog both enabled, is expensive. Fog exploration is 2D (multilevel vertical reveal risk), creator supports fog boxes using rectangular measured templates as a partial workaround. GM capture NEVER substitutes player visibility QA. Note enabling 3D geometry sight calculations disables vision in 2D mode (creator's caveat).

## API/integration and newer platform changes
Mapmaking Pack has Environment Panel, Asset Browser, Material Browser, Dungeons & Interiors, Cutscene Panel and 3000+ 3D tiles/1000+ materials, but source assets from libraries are not automatically approved for our visual scenes. API exposes `game.canvas3D.CONFIG.UI.TokenBrowser...`, while older local custom module uses `game.Levels3DPreview`. Installed version must inspect which APIs are aliases/current; do not assume legacy private API stable.
Levels creator says V14 core Foundry Scene Levels now supersedes the original Levels module, which is being retired, with non-1:1 migration. This is a high-priority compatibility gate in Foundry 14.368 with 3D Canvas 9.0.35.

## MCP extension backlog ranked
P0: custom tunnel/control-plane recover; read-only actual installed module versions/runtime objects; source-safe scene snapshot/restore with revision checks; live 3D model world transforms incl evaluated bounds and auto center/ground status; camera readback/projection; true screenshot + pixel QA.
P1: explicit GLB upload/import and Tile model refs with provenance; per-mesh collision/sight/door tagging report; light & PBR environment parameter query; token movement/vision blocked test; GPU/render timings.
P2: multi-level visibility, camera presets, cutscenes, shader/particle controls with allowlist and source semantics.
No bulk scene construction until isolated source-derived GLB fixture passes real Foundry player/GM render, scale, movement, sight, camera, recoverability and performance QA.

## Runtime status
Foundry public MCP connected `acquisitions-incorporated`, 1 default scene. Custom MCP remote tool call returned tunnel-client has not been seen for 300 seconds. Therefore NONE of the above 3D renderer features have yet been validated in the current live Foundry scene. Area9 frozen. No maps created or modified by this research.
