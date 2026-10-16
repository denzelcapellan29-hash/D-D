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
## 2026-10-16 incremental bridge audit
- Read-only runtime reconfirmed: Foundry 14.368, scene NUEDEFAULTSCENE0 empty, 3D Canvas active, accepted Blender Area8 v082 saved clean; no scene write.
- The staged bridge diagnostics include additional 3D Tile flags (dynamesh, autoCenter, autoGround, depth, tilt, offsets); exact v9.0.35 names still need installed-source corroboration.
- A staged-only code change explicitly marks mesh evidence as NOT proof of requested GLB loading, avoiding false positives from fallback meshes. Verified GitHub commit e2369a61e6d216b013b6cc47f031ab164df1101c and syntax parse. No deployment.
- Independent world-space geometry bounds remain pending. Attempted broad edit did not land; GitHub readback confirmed absence.
- Next gate is authorized, read-only installed tile3d.js inspection and a rollback-capable local bridge deployment path. Do not mutate approved Blender Area8 v082 or frozen Area9.

## 2026-10-16 live control Tile create anomaly
- Read-only baseline: Foundry scene NUEDEFAULTSCENE0, 3D Canvas active, zero semantic 3D Tiles, revision d93c7518ac199375b7705715c1faf124b5cd35136ba8e8707ddc326ac15546ad. Foundry public scene_get reports one Tile total; these counts have different scopes. Approved Blender Area8 v082 clean.
- Built-in canvas3dcompendium Medieval Dungeon Wall_Modular.glb diagnostic fixture passed revision-guarded apply_semantic_objects dry run.
- A subsequent apply_semantic_objects request with dry_run:false returned ok:true and created Tile with id:null, but identical before/after revision. This is NOT proof of a Tile creation and must be treated as a no-op/bridge anomaly.
- First post-operation inspect_3d_scene errored; one recovery inspection PASS confirmed 0 semantic 3D Tiles and unchanged baseline revision. No renderer QA or GLB load success is claimed. No further scene edits pursued.
- First-party staged bridge code now explicitly throws if createEmbeddedDocuments returns no ID; GitHub commit 8d469ea93b51d91f76b3de1ec76c185592597b54, JS syntax PASS. This is NOT deployed and does not by itself explain no-op response from currently running bridge.
- Next: investigate actual bridge response correlation, dry_run forwarding and create path against installed runtime; only repeat test once a returned non-null document ID, post-create manifest and revision guard are enforced.
