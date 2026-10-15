# Area 8 v082 → Foundry VTT core pilot: LOAD FAILURE / SAFE STOP — 2026-10-15

## Authority
DM authorized concrete Area8 approved visual integration; strict no fabricated visible meshes and source fidelity. Original DM artistically accepted `G:\My Drive\D&D\Foundry Bridge\assets\Area8_Rebuild_v082_SicklySewerFinal.blend` (do not alter). DM approved hero screenshot https://drive.google.com/file/d/1OBJJchJMTV4BtGjtc1SWeI6uH4IRUbFA/view .

## Actions verified
- Connected Blender initially loaded Area9 v069 saved clean/dirty false; opened original Area8 v082 read-only and found 519 scene objects, 183 rendered mesh objects, 11 unique mesh datablocks and ~21,342,343 nominal repeated visible vertices. Area8 source still dirty=false.
- Exported ONLY five approved existing genuine asset-derived meshes without modifying mesh datablocks: `POOL_SEWAGE_SURFACE_v001`, `AREA8_PLANAR_TENTACLE_APPROVED_DECOR`, `SEWER_DISCHARGE_01`, `SEWER_DISCHARGE_02`, `POOL_SHALLOW_SHELF_00` to `G:\My Drive\D&D\Foundry Bridge\assets\Area8_v082_Foundry_CorePilot.glb`, **177,719,956 bytes**; Blender glTF exporter warned multiple shader image nodes -> sampler choice may differ; PBR QA UNVERIFIED.
- Evaluated Blender world AABB of five meshes: min (-7.711,-7.700,-1.087) meters, max (7.702,7.710,4.275) meters; size 15.413×15.411×5.362 meters.
- Staged byte-count-matching model to `C:\Users\denze\AppData\Local\FoundryVTT\Data\assets\acq-inc\Area8_v082_Foundry_CorePilot.glb` without overwrite; Foundry-relative `assets/acq-inc/Area8_v082_Foundry_CorePilot.glb`. Local copy only; Drive cloud not independently verified.
- Actual installed Acq bridge module v0.2.8 source read via Windows dev agent GitHub result `automation/results/bridge-js-read-area8-pilot-20261015.json`, hash c6f0a4e21beae724abe8a751033df201001276874d097c056d02b17267352008. `inspect3dScene` DOES compute `runtime_bounds` from runtime Tile Three.js `_worldBoundingBox`; previous general claim 'no measured bounds' must be corrected to 'partial AABB support exists, no full world matrix/OBB'. Internal `asset_upload` and tile_set_model3d operations exist but are not exposed among seven Acq_3D_Map tools.
- Foundry world `acquisitions-incorporated`, default active scene `NUEDEFAULTSCENE0`, native 3840×1920 pixels grid 100px=1, five lights, one ordinary branded background Tile. Revision before pilot `d93c7518ac199375b7705715c1faf124b5cd35136ba8e8707ddc326ac15546ad`.
- Custom MCP `apply_semantic_objects` dry_run PASS, then actual Tile CREATE PASS, id **`qeO84LaE0Q06mZgg`**, semantic_id **`area8:v082:core-pilot`**, build `area8-v082-core-pilot`, x1414 y454 width1012 height1012 elevation0 rotation0, flags model3d path above, autoCenter false, autoGround false; after revision `0e8194eac71dfe0672b0e3ab5722bec22df268dac1de3fea06d68abc6eba2704`.

## Failure and STOP
Immediately after Tile creation, custom MCP `inspect_3d_scene` and `capture_3d_view` both errored; independent hosted Foundry MCP `scene_get` timed out; custom manifest and asset search also errored. May be client/render/memory load from 177MB multi-million polygon GLB, but CAUSE **UNVERIFIED**. One rollback request to `apply_semantic_objects({objects:[{document:'Tile',semantic_id:'area8:v082:core-pilot',delete:true}]})` also failed. **ROLLBACK NOT CONFIRMED**. STOP without retries or further changes. Live Foundry process state UNKNOWN; don't claim the Tile removed. Original .blend and GLB export preserved.

## Next safe recovery
1. Have DM verify Foundry GM client responsive; if frozen, restart **once** with 3D Canvas not activated if needed (do not delete scene or source assets); use Foundry core interface or public MCP to delete ONLY Tile id `qeO84LaE0Q06mZgg` after core UI available, or targeted semantic_id deletion if custom bridge recovers; confirm readback. No broad scene resets.
2. Add strict 3D model resource/triangle/texture/file size preflight and calibrated small multi-stage pilot; 177MB is not viable to assume safe. Prove tiny GLB path with actual capture then expand with measured perf budget. Check material sampler warning.
3. Separate visual core at lower evaluated triangle count using controlled independent source-derived decimation with UV/textures/regression (asset-only rule) and no unauthorized geometric fillers. Preserve original 177MB GLB, version new candidate; avoid blindly rerunning heavy load.
4. Genuine full room still NOT in Foundry, image/collision/fog/lighting QA NOT PASS; user pilot goal partially complete only.

State terms: DM visually ACCEPTED Blender v082; GLB core EXPORTED and STAGED locally; Foundry Tile CREATED; 3D scene runtime FAILED/UNKNOWN; Foundry pilot NOT ACCEPTED and unsafe until recovered.
