# Foundry 3D Canvas tested construction route — 2026-10-16

Installed plugin **ai-3d-asset-workflow v2.7.16** is now the canonical detailed technical recipe, reference `skills/meshy-asset-pipeline/references/FOUNDRY_TILE_PRODUCTION_V2716.md`. This note records independently observed state and the outstanding release gates.

## Verified
- 3D Canvas real `Tile` creation using `Acq_3D_Map.apply_semantic_objects`, `document:'Tile'`, conventional `texture.src:'modules/levels-3d-preview/assets/blank.webp'`, plus `flags.levels-3d-preview.model3d` pointing to a GLB. Earlier attempts with wrong `texture.src` returned `id:null` and no revision change; never rely on operation.ok alone. Tile u5mvll6cXb5XKBD0 created and manifest validated, scene revision changed.
- Original approved Area8 v082 `.blend` remains clean and immutable. One-wall source-only export MUST set BOTH Blender glTF `use_selection=True` and `use_active_scene=True`; omitting active scene unexpectedly exported 97 nodes from unrelated scene. One genuine 75%-face-decimated + 1K-texture wall derivative is 1,457,188 bytes, verified SHA256 d5390081c01a99d9e439ef90d556656dd1f0b69ed843a6342887067229ab6b9c in Foundry assets/acq-inc.
- Runtime Tile dimension calibration: x900,y650,width188,height26,depth78,elevation0 produces world x center0.900, z center0.650, width0.188, horizontal other-axis0.026, vertical y0.078. Elevation100 produced y10 and was wrong; floor corrected to elevation0.
- Installed Kenney Medieval floor.glb only 16,812 bytes, 10 triangles; Medieval Wall_Modular 28,432 bytes and 1,672 triangles. Used as controls ONLY, not approved Area8 final art. Genuine Area8 original wall GLB 13.11 MB/144,990 triangles; 75%-face derivative 9.82 MB/36,246 triangles; 1K texture derivative 1.46 MB.
- A 1920x992 actual 3D Canvas renderer screenshot showed the gray library floor model. Subsequent read-only inspection identified 8 test Tiles (floor grid, optimized wall, two tentative wall-ring modules), not a completed Area8.

## Tabletop and scene strategy
DM reports newly created Scenes show a plain white background instead of the branded red tabletop. This is a useful alternative: create a disposable dedicated Area8 Scene with cloned/verifiable geometry, then validate camera and backdrop. This has NOT yet been executed in current seven-function Acq_3D_Map interface (scene_create not exposed). An attempted revision-guarded update of `flags.levels-3d-preview.renderTable:false` on default Scene failed; no change recorded. Do not claim table has been disabled.

## Next gates
1. Expose a reversible, revision-safe scene creation path via first-party bridge or verified Foundry API, snapshot current scene, create dedicated test Scene instead of editing default branded backdrop.
2. Confirm full four-piece floor is visible and truly joins, no red table. Validate actual loaded geometry rather than only Tile runtime AABB and GLB path.
3. Port source-approved Area8 floor/wall/roof/pool/pipe/tentacle assets as optimized derivative GLBs, fixed camera visual and collision QA, eventually gameplay ready.

Source precedence: `docs/DOCUMENTATION_AUTHORITY.md`, DM approved Area8 v082, skill v2.7.16. DM acceptance is NOT implied by a screenshot or persisted Tile.
