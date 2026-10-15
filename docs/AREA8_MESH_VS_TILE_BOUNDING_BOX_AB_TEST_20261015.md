# Area 8 loaded mesh A/B diagnostic — 2026-10-15

Read-only renderer capture of existing geometry-only Draco Tile `Z2v1DQS8WOnBGgLS`, semantic `area8:v082:geometry-loader-test`, in scene `NUEDEFAULTSCENE0`. Camera position (1.60,0.25,0.85), target (1.4,0.013,0.7), temporary capture with camera restore, 1920x992 WebP. Capture PASS, runtime `ready=true`, scene revision unchanged `c5e76310ecbf2919f7fdd90d5d206bf70781e15ef52677b7d01c2cb402f6e9c7`. Actual screenshot inspected: default red/orange Foundry Virtual Tabletop graphic fills image, no identifiable gray wall geometry. This is a **visual FAIL/UNVERIFIED MODEL LOADING**, not proof of mesh absence (occlusion/scale/loading may apply).

Installed bridge source review confirms `inspect3dScene` reads `l3d.tiles[tile.id]._worldBoundingBox` but **does not inspect loaded mesh descendants, GLB parser results or model-material state**. Consequently `_worldBoundingBox` numerics resembling Tile width/depth/height cannot prove actual GLB loaded. Exact 10:1 relation to source Blender geometry is not yet a calibrated unit rule.

Attempted safe A/B (remove pilot Tile then identical camera capture) BLOCKED: read-only `validate_scene_manifest` errored; one subsequent read-only `inspect_3d_scene` also errored. **Did not execute Tile deletion or new scene writes**; pilot Tile may still exist. Do not claim A/B complete. Next attempt only after MCP reliably returns scene revision; then targeted delete with expected revision and after-capture, verified inventory. Do not experiment with another import while this one is unresolved.

Approved Blender Area8 v082 clean and untouched. Knowledge base and skill requirement: actual model loader/node state is separate from Tile document AABB or _worldBoundingBox.
