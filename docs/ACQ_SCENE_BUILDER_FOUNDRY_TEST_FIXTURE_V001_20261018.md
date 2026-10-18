# Acquisitions Scene Builder — real Foundry Test fixture v0.1 (2026-10-18)

**Status: LIVE FOUNDRY DOCUMENT PLACEMENT PASS; 3D RENDER / COLLISION / ART QA UNVERIFIED.** DM created separate Foundry Scene named `Test`; this pass did not create the scene or alter Area 8.

## Actual runtime / scene safety
- Read-only world v14.368, D&D 5e v6.0.5. Scene list returned **two scenes**: protected inactive Area 8 / original `NUEDEFAULTSCENE0`, and active distinct **`Test`** Scene `CcBZsHkVPHpGtcZp`.
- `Test` originally had **0 tiles**, 4000×3000 scene pixels, grid **100px = 5ft**.
- Acq 3D Bridge `inspect_3d_scene` established revision `a59fd2ad1f9a5692d480e5373517d821c59f32087def5e2cda5f63b1e85e1808`, Levels 3D installed. First read showed 3D not active; later reads showed `levels3d_active: true`.
- Original Area 8 `NUEDEFAULTSCENE0` independently still has 162 Tiles, 36 walls, 13 regions, 6 lights and two QA tokens. **No Area 8 scene edit**.
- No reversible scene snapshot tool exposed; therefore restricted live operations to explicitly tagged `qa-disposable` fixtures in DM-created empty Test and guarded by `expected_revision` on every write. No delete or modification of released documents. No Scene activation needed.

## Genuine approved asset staging (one source + one isolated derivative)
- The existing real Meshy 7.1 source road GLB was copied unchanged into Foundry Data `assets/acq-inc/Episode2_Road_Meshy71_Source_v001.glb`, 14,338,700 bytes, SHA-256 `f7670525391672f92c216fb3d9998c613ac7f33167324ab13b71954ddb847bf4`; original `Episode2_HighRoad_RoadTile_Meshy7_1_01a1481a.glb` preserved at Drive-backed local G: path. Meshy road original task `01a1481a-5c7d-7003-8869-7264a2181d59`.
- Existing Meshy 7.1 original peat-bank GLB task `01a14d76-d7a2-75ec-a29e-8cbc38e1ed50` downloaded **without new credits** as `G:\\My Drive\\D&D\\Foundry Bridge\\assets\\Episode2_WetBank_Meshy71_Source_01a14d76.glb`, 67,739,684 bytes, source preserved.
- Clean saved Blender `Episode2_HighRoad_WetBank_IsolatedQA_v010.blend` remained unchanged: source `Mesh_0.003` had 1,070,691 vertices, 2,007,720 polygons and three packed 2048 textures, 1 UV; Blender source remains unmodified. Independent temporary copy exported GLB via normal `bpy.ops.export_scene.gltf(use_selection=True,use_active_scene=True,export_format=GLB,export_apply=True)` with decimation ratio 0.25. Exporter's post-export cleanup code threw ReferenceError after removing the disposable object, but follow-up **read-only verification** confirmed no temp objects, original mesh still 2,007,720 polys, .blend saved clean, output valid GLB header 2, length 25,417,136 bytes, **exactly 1 node/mesh/material, 3 embedded textures** and SHA-256 `65df429ac3f861a03875aaa72e8cc11ecbc549c36d3632b3d4dd8b05df0c2f04`. Staged at Foundry `assets/acq-inc/Episode2_WetBank_Meshy71_LOD25_Test_v001.glb`. **LOD is test derivative; visual quality UNVERIFIED, not DM approved**.
- Source peat-bank top-side sampling suggests the road-facing high lip is toward **negative local X**. Conventions X/Y in Blender vs X/Z horizontal in 3D Canvas require live QA.

## Four real Tile documents (ALL persisted, independent manifest PASS)
First two road Tiles were created independently with dry run, revision-checked real apply, inspector readback and exact manifest. Then two bank Tiles were applied with one guarded batch after dry run. Foundry 2D texture uses conventional `modules/levels-3d-preview/assets/blank.webp` and 3D flags `flags.levels-3d-preview.model3d`, autoGround/autoCenter/stretch, cameraCollision and collision; NO procedural meshes or third-party substitutes.

| Semantic ID (QA-only) | Foundry Tile ID | Tile x,y | Footprint px | depth px | Staged GLB |
|---|---|---|---|---|---|
| `ep2:builder-test:road:00` | `diINlKkXs291o24i` | 1950,1450 | 100×100 | 16 | `Episode2_Road_Meshy71_Source_v001.glb` |
| `ep2:builder-test:road:01` | `Bn5B6rAMORIZVibG` | 1950,1550 | 100×100 | 16 | same source |
| `ep2:builder-test:wetbank:00` | `A9CuRt5pDUpE0GVp` | 2075,1450 | 150×100 | 68 | `Episode2_WetBank_Meshy71_LOD25_Test_v001.glb` |
| `ep2:builder-test:wetbank:01` | `v20MwV3NuWfb7rYO` | 2075,1550 | 150×100 | 68 | same derivative |

All four classified `qa-disposable`, build_id `ep2-builder-r1-smoke-v001`, stable semantic IDs and provenance text. Final Foundry revision `981ede50ab4eb2003207703e15aad76cf05deecee75f56fc2f305a51d8697c79`. `validate_scene_manifest` PASS with exact 4 IDs and count `Tile=4`, no missing, unexpected or mismatched objects. `inspect_3d_scene` confirmed exact correct staged `model3d` paths. Original Area8 scene remains unchanged.

## Not yet validated / stop conditions
- 3D Canvas became ACTIVE per bridge inspector, but both `capture_3d_view` attempts (one targeted temporary perspective, one default) failed with MCP transport `INVALID_ARGUMENT / Error executing tool capture_3d_view`. This is **not a rendered screenshot**, nor evidence the GLBs loaded successfully.
- Per-Tile `runtime_bounds` remain null in `inspect_3d_scene`, so **model loader status, root orientation, contact alignment, actual rendered texture and collision are UNVERIFIED**. Never claim G3 pass, art pass, collision pass or playable map based solely on Tile document creation or bounding boxes.
- A separate **ephemeral** `set_3d_camera` was blocked by OpenAI safety; no retry or bypass. Manual direct look in active Test or a future fixed safe capture route is needed for real visuals.
- Foundry Tile pixel dimensions are provisional based on 100px = 5ft grid and measured source shape, not calibrated from the actual model world transforms. Bank upper lip vs road floor elevation may be too high despite visually intended adjacent x, and y-axis/top-left semantics remain to be calibrated. Do not propagate to full Episode 2 before one two-tile QA.
- No new Meshy generation/credits spent during this test, last balance observed **679**, and no DM approval or Foundry gameplay release.

## Next strictly reversible test
1. With `Test` open in 3D Canvas, inspect whether there are actually **two roads and two peat banks**, their scale, orientation and separation. A user-provided screenshot is acceptable interim visual evidence if `capture_3d_view` remains broken; do not call it verified renderer evidence absent an actual image.
2. Read current Test revision and 3D active state; if visible, adjust only tagged QA Tile flags/x/y/width/height/elevation with one normal revision-checked apply after dry run and manifest readback; verify road-bank physical contact with visual closeup. Fix camera capture tool separately with explicit tests, not by changing released scene.
3. Validate two-road seam, two-bank seam and road-to-bank true contact, walkable surface and first-person navigation; then prefab/stamp logic, visual palette inside Foundry and G3 gameplay. No dual full-scene Blender composition.
4. Keep DM accepted Area8 v082 immutable, prior Episode2 .blend numbered checkpoints, source Meshy GLBs and GitHub single semantic authority. This is a **Test scene fixture**, not a player map or artistic approval.
