# Episode 2 High Road — Godot v044 Artistic Review Candidate (2026-10-20)

Status: **SAVED / RUNTIME-QA-REVIEWABLE / NOT DM ACCEPTED / NOT RELEASE READY**.

## Active source and rollback
- Godot current review scene: `res://poc/high_road_blendedfar_v044.tscn`.
- Runtime script: `res://poc/combat_staging_v044_blendedfar.gd`.
- Rollback scenes: v029 baseline, v038 vegetation pass, v040 HDRI first balanced pass, v043 cleaned sedge LOD.
- Blender source unchanged live saved and clean: `G:\My Drive\D&D\Foundry Bridge\assets\Episode2_HighRoad_WetBank_IsolatedQA_v010.blend`.
- Source-derived Blender shoreline experimental checkpoint: `Episode2_HighRoad_ShorelineSourceDerivative_v020.blend`. Keep as experimental; do not promote source-geometry edit policy globally.

## Verified actual Google Drive review
[QA folder](https://drive.google.com/drive/folders/1chdM3abqU2C5FjBzc36Tq3GdB-xXx9SB) — independently listed and files verified:
- [Default first-person player-eye](https://drive.google.com/file/d/1VTSZ0uvMFSD8z16CAOVu9Y1nxS1TSuL8/view)
- [Monk movement from (-1.8, ~1,5) to (-1,0.901,2.1)](https://drive.google.com/file/d/1_SUjQdXl8gLtWmem7IAk9z_2M98aD38U/view)
- [Side off-axis QA](https://drive.google.com/file/d/1iTuHlEz6DaFbfvDMfCrXXXxZNrAwfS-z/view)
- [Elevated structural QA](https://drive.google.com/file/d/1xslcKYGwI8SJ27fEaOpQ5rp2MTMZuqSJ/view)
- [Wagon rear and water](https://drive.google.com/file/d/1VNQjqjOF72_x0jrw6Ud1yerHDcu6EKo1/view)
- [Left bank](https://drive.google.com/file/d/1Yp6xrIjgCk46B69bdOcLa44YfVDYvGs8/view)
- Prior comparison `qa_subtlecloud_v029.png` also in folder.

## Iterations and QA evidence
1. v031–v033: library Meshy willow skyline and midground vegetation; rotating 32m terrain tiles introduced an extra visible road, rejected; untextured distant bank looked flat, rejected.
2. v034: custom procedural cloud shader caused chunked/angular clouds, rejected.
3. v035–v037: approved source-bank PBR material and sky hemisphere corrected; tested high/far camera: a hard diagonal near/far material seam persisted.
4. v038: 36 source-library midground dead-willow instances, plus 22 approved Meshy sedge instances in v041. Scenic/non-GM free camera hides placeholder actor capsules; GM overlay can show them. No new visible procedural art geometry.
5. v039: Poly Haven `overcast_soil_puresky_2k.hdr` CC0 panoramic sky (source https://polyhaven.com/a/overcast_soil_puresky; direct https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/overcast_soil_puresky_2k.hdr; SHA256 `5414e1ac0c35e451d28595b2a2cba05e2ca301fdeb755b0a469408443093dafc`). No Meshy credits.
6. v040: corrected sky background exposure / ambient lighting; natural textured overcast cloud cover, markedly improved from blank gray void.
7. v042: sedge LOD downsampled 65,006 to ~15,931 faces but erroneously exported an imported fixture Cube and rendered white boxes; REJECTED. v043 re-exported only approved sedge Mesh_0 at 15,925 faces, confirmed clean.
8. v044: custom Godot spatial PBR-like shader **only** on genuine imported far-field terrain tile instances, blending already-approved source terrain and bank albedo textures by world distance with irregularity. Actual elevated and side screenshots show diagonal material edge markedly reduced. No new visible mesh geometry.

## Runtime numbers and acceptance
- Godot 4.7.2 scene checks: 0 runtime errors; deep res://poc scene validation 0 errors and warnings.
- 133 FPS in sampled v044 view; ~9.34 million primitives and 85 draw calls (hardware/session-specific; do not infer other-device FPS).
- Monk scripted movement to `Vector3(-1,0.90099335,2.1)` rendered against real terrain; no black captures.
- Scene provides **artistic review**, not confirmed open-world traversal. Beyond central terrain, far-field GLB instances have **no verified collision**, free-camera and hero art passes are not proof of edge navigation.
- Remaining defects and decisions: some oblique reflective waterline and willow root/bank interfaces, vegetation repetition, character-avatar replacement for current GM diagnostic tokens, player camera collision/visibility, far-field collision and gameplay traversal, performance and artifact checks on target hardware.

## Next
Await DM aesthetic review of linked runtime captures; keep v044 checkpoint. After comments, revise scene via numbered backups and run fixed-angle player-eye + side/rear/elevated QA. Do not claim DM approval until explicit.