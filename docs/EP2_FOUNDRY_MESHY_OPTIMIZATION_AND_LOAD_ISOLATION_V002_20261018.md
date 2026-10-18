# Episode 2 Foundry-first: mandatory Meshy GLB optimization and loading isolation v002
Date 2026-10-18. **Optimization artifacts and one-live-tile isolation VERIFIED; 3D Canvas loader recovery NOT yet verified.**

## Why this happened / corrected skill
DM correctly flagged existing installed AI 3D Asset Workflow `references/FOUNDRY_AREA8_SCENE_BUILD_V2717.md` and `references/FOUNDRY_TILE_PRODUCTION_V2716.md`: Area8's Foundry pipeline always used **separate genuine Meshy-derived reduced-face, 1K texture, origin-zero GLBs** and never directly staged the massive cinematic original models. Earlier Episode2 Test placed unoptimized road GLB 229,048 faces each and 25%-face wetbanks roughly 501,930 faces each, all with 2K PBR images; this skipped the already binding staged-asset optimization gate. Do not repeat. A 3D runtime loading spinner does NOT prove that mesh size is sole cause; must test smallest reliable fixture and browser runtime logs.

## Current protected state
- Original accepted Area8 Scene `NUEDEFAULTSCENE0` inactive/unchanged, DM accepted Blender v082 never edited.
- Live `Test` Scene `CcBZsHkVPHpGtcZp`; four QA-disposable Foundry Tiles with protected semantic IDs remain.
- Previous isolation: two heavy wetbank Tiles `wetbank:00/01` hidden and model3d cleared/collision disabled. DM provided screenshot *after F5* still showing 3D Canvas spinner about 50%, so **wetbank removal ALONE DID NOT FIX**.
- Previously saved independent Blender `Episode2_HighRoad_WetBank_IsolatedQA_v010.blend` remains **CLEAN**, verified original road 229,048 polys/129,195 vertices and original bank 2,007,720 polys/1,070,691 vertices, original 2048² packed JPEG images untouched.

## Two proper source-derived Foundry LODs CREATED AND VERIFIED
All output separate new filenames, source meshes unchanged. Blender copied Object+Mesh+Material+three JPEG Image objects, independently resized copies to 1024×1024, decimated ONLY disposable copy, exported 1 mesh, material and 3 internally embedded PBR JPEGs using standard GLB exporter, cleaned temporary objects and copies. No arbitrary procedural visible mesh. No new Meshy generation/credits.

| Purpose | Foundry staged path under `assets/acq-inc/` | Actual triangles | GLB bytes | SHA-256 |
|---|---|---:|---:|---|
| Road pilot source `HighRoad_SourceTile_00`, 12% Decimate | `Episode2_Road_Meshy71_LOD12_1K_OriginZero_v002.glb` | **27,484** | **1,277,068** | `f6d17bf44f1c43d280406b17db6662fb8309e4b3ab1ee52daa6c7e96be97ac12` |
| Peat bank source `Mesh_0.003`, 3% Decimate | `Episode2_WetBank_Meshy71_LOD03_1K_OriginZero_v002.glb` | **60,231** | **2,412,052** | `c71a6aada5d7913669be2afd2f62931a43cd24ebc8a5fcdc0c230755e3d52c3e` |

Both GLB version 2 proper, exact bytes match declared lengths, 1 mesh, 3 embedded JPEGs, **no required glTF extensions**, and independent original meshes retained. Visually inspected in actual Foundry renderer? **NOT YET**. Aggressive decimation might distort foliage/silhouette; do not DM accept until renderer closeups and image comparison.

## Current controlled active Scene QA test (one low-cost model)
After user screenshot confirmed persistent loading with two original road Tiles:
- Read-only current prior Test revision `dcfb1494a99fecf065a67ebb76313550379426a82eb23bdb493495e0d64b4ced`.
- Dry-run + guarded LIVE `apply_semantic_objects` updated **only** road semantic `ep2:builder-test:road:00` ID `diINlKkXs291o24i` model path to new optimized `Episode2_Road_Meshy71_LOD12_1K_OriginZero_v002.glb`, kept visible/collision.
- road `...:road:01` ID `Bn5B6rAMORIZVibG` set hidden true/model3d empty/collision false temporarily.
- Both bank Tiles remain hidden and model3d empty.
- New verified LIVE Test revision `53c81d4ece63a354c7611b5cd3c4b36d9b9fed6b5119c1205a73db61d3a219e2`. Foundry scene_get readback `Tiles:4 (1 visible)`, exact manifest PASS with all four semantic IDs and no unexpected objects.
- `inspect_3d_scene` intermittently throws MCP RuntimeException while 3D Canvas is hung; no valid runtime model bounds or screenshot obtained. NO RENDER/PERFORMANCE PASS.
- **NEXT:** DM presses F5 and tries 3D on active Test with **only ONE optimized 27.5K triangle / 1.28MB road Tile**. If it loads, renderer/screenshot and core path calibration plus one optimized 60K bank. If still hangs: remove final QA road model flag too in a reversible guarded change, run **empty Test**. If empty still hangs, investigate native 3D Canvas v9.0.35 client loading/WebGL errors, scene flags, and possible module conflicts instead of blaming Meshy. Do not modify Area8.

## Mandatory pre-import performance gate for future skills
1. Every Foundry-eligible Meshy asset **MUST** have an independently saved, versioned, source-derived performance-specific GLB and isolated renderer QA **before any Tile placement**, with measured GLB source hash, target triangles, 1K texture copies and source immutability. Defaults from Area8 are empirical baseline (not unconditional global max): repeated modular structural model target approx 20–40K triangles; hero props may be larger by measured ROI; wet foliage maybe 30–60K for first pass; scene total performance measured on GPU and real FPS. Keep model silhouettes and PBR fidelity; more decimation if needed, report art degradation.
2. Optimize once per unique asset, duplicate linked Foundry asset paths rather than regenerate Meshy/GLB each instance; prevent 2K/4K textures and 500K triangles per repeated Tile.
3. Quarantine/preflight invalid single GLBs in disposable scene, initial **one model → two adjacent models → road/bank prototype**, with F5 renderer confirmation each step and no untouched live campaign scene edits.
4. Capture actual client GPU/renderer status and image, with load-time threshold; a successful Foundry Tile database manifest is NOT proof model loads. If scene fails empty, stop asset work and repair native module/client.
5. Store versioned Foundry-specific GLB hash/path in shared semantic registry so Blender remains isolated asset workshop and Foundry remains sole assembly.

## Documentation and follow-up
This note supersedes previous High Road asset performance assumptions but does not supersede historical source/policy. Tool safety checks remain binding. No new Meshy credits; last observed 679. User visual test outstanding for optimized single-road configuration.
