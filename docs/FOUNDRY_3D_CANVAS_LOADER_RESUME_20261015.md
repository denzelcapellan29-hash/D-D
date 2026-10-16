# Foundry 3D Canvas loader investigation — 2026-10-15

## Verified this session
- Blender live: accepted Area8 v082 saved clean; no edits.
- Foundry V14.368 and dnd5e 6.0.5, scene NUEDEFAULTSCENE0 active.
- Custom bridge: initial inspect error, then inspect PASS, capture PASS, asset search PASS; current Tile count 0; five lights.
- Empty manifest PASS with before/after revision d93c7518ac199375b7705715c1faf124b5cd35136ba8e8707ddc326ac15546ad unchanged.
- Two built-in Wall_Modular.glb choices were found in canvas3dcompendium as learning-only test fixtures.
- No scene writes or GLB imports in this pass.

## Creator-backed Tile rules
TheRipper93 source https://wiki.theripper93.com/levels-3d-preview/info/entities/tiles: GLB assigned via Tile 3D Model path; Dynamic Mesh must be None (use 3d model) or model path ignored; width, height, depth and Auto Ground / Auto Center are separate transform controls; Tiles can govern collision/sight. Tile doc bounds alone do not establish descendant GLB geometry.

## Static bridge source audit
Retrieved GitHub tools/foundry3d/acq-foundry-bridge-v029-mesh-diagnostics.js and syntax parsed successfully using JS Function constructor. Patch is STAGED NOT DEPLOYED. Its acqReadOnlyMeshEvidence enumerates direct Object3D fields on tileEntity and traverses descendants; the installed runtime loaded-model root is not verified. Runtime _worldBoundingBox is still reported without independently evaluated model Box3, and relevant3dFlags omits the Dynamic Mesh/Auto Center/Auto Ground properties. A nonzero mesh_count can include a fallback mesh. Therefore syntax PASS does not equal renderer diagnostics PASS.

## Next controlled gates
1. Read installed loader Tile3D source via authorized source-reading route; identify actual root and model-load state/error, exact module flag keys and version.
2. Extend first-party read-only diagnostics to expose dynamesh/model URL/resolved HTTP status, Three.js model root, descendant mesh geometry, computed world Box3/matrix and typed load errors.
3. Test code against fixtures; backup installed bridge and deploy only with rollback capability, never during play.
4. Disposable scene A/B using built-in wall as learning-only known-good control; then genuine Area8 optimized wall; validate image, scale and restore scene by ID/revision.
5. Build complete Area8 runtime scene only after actual mesh rendering and transform QA PASS.

## Unknowns
Dynamic Mesh setting, asset-path fetch, GLB loader errors, 3D Canvas initialisation, 0.1 apparent bound factor, ground/center transformations, and camera occlusion remain hypotheses. Draco and PBR alone did not resolve prior tests. Area8 accepted Blender v082 and Area9 frozen work remain protected.