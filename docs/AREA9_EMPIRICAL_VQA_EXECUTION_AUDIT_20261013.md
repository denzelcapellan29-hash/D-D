# Area 9 empirical VQA execution audit — 2026-10-13

## Scope and evidence
Audited **installed AI 3D Asset Workflow v2.7.5** and binding `EMPIRICAL_VQA_PROTOCOL_V2.md`, `EMPIRICAL_SCENE_OPTIMIZATION_V170.md`, `SCENE_QA_CHECKLIST.md`, and `PROTOTYPE_FIRST_AND_GPT_REFERENCE_V275.md` against documented Area9 v024–v030 experimental work. Live Blender read-only health check returned **Session terminated**; no Blender writes were attempted. Latest previously verified saved clean scene is v029, with v030 saved but measured worse and v031 state unknown.

## Already written into the current skill
- G3-F/G3-W/G3-R physical connector tests and 2x2 4-floor/2-wall/2-roof gate before full replication.
- Separate player entrance, fixed-calibrated structural/isometric, and seam detail views. Record exact camera matrices, units, render config and geometry provenance.
- Four explicit empirical VQA categories: **Grid-Relative Matrix Shifts (X,Y,Z Translation)**; **Volume & Bounding Box Scaling**; **Z-Depth & Layering Corrections**; **Luminance & Color Balance (RGB Mapping)**.
- Plus hard **Physical Connectivity & Collision** and **Official Layout & Playability** gates, and independent structural and artistic loops.
- Source/reference PNG, entrance color, fixed isometric color, calibrated grid overlay (image-space, not procedural mesh), raw 32bit Z-depth EXR, normalized depth diagnostic where useful, transforms.json, qa_manifest.json, visual_delta_report.md, numeric tolerances and uncertainty/evidence tiers.
- Actual image integrity checks, matched camera/color/render conditions per regression, no bounding-box contact interpreted as actual joint, and explicit PASS/FAIL/UNVERIFIED.
- Saved != QA PASS != explicit DM accepted. Freeze a reproducible best verified checkpoint; stop after broken Blender connection/corruption.

## Actual Area 9 usage and gaps
Observed in recorded Area9 trials: real structural/player PNG renders for v024–v029; saved numbered checkpoints; some real `matrix_world` raycast sample geometry and measured roof-wall deltas; successful detection that 7cm Z change improved 1/12 -> 4/12 samples within 5cm and 10-degree pitch regressed 4/12 -> 1/12; stopping on failed v031 call. This is **partial manual VQA**, not complete protocol.

**Not demonstrated or absent** in Area9 checkpoint records:
1. Locked camera matrices and a common repeatable before/after viewpoint across all trials (camera was changed while evaluating).
2. Proper QA evidence bundle with raw EXR Z-depth, calibrated image-grid overlay, transforms.json, qa_manifest.json and structured delta report.
3. Measured area-density/contact normals, manifold and watertight support assessment along full interfaces. Sparse hit/height pairs do not prove supported contact.
4. Walkable floor **coverage**, navigability, source-layout path graph and wall↔floor / roof↔roof verification on the full 2×2.
5. Matched-color-space quantitative luminance/texture/repetition comparison and consistent material/lighting controls.
6. A fixture-test proven executable numerical validation pipeline. Docs prescribe but do not establish code exists.
7. Signed-off image QA from isolated entrance, isometric and each mandatory connector closeup for the same exact clean saved scene. Some renders accidentally included unrelated comparison source meshes.

**Important historical contradiction:** `SCENE_QA_CHECKLIST.md` v1.3.5 says "no mesh editing" and "linked/instanced assets only." This conflicts with higher-precedence installed v2.7.5 / `BLENDER_DERIVATIVE_FABRICATION_V263.md`, which permit **independent versioned Meshy-derived connector sculpt and topology work** while keeping original GLBs immutable. Mark legacy checklist historical or update it only via a verified release.

## Recommended enforcement plan (not claimed implemented)
A. A small external `prototype_vqa_validate.py` script + JSON schema to read the active saved checkpoint and produce scene/camera/source manifest, 2×2 occupancy and connector sampling with normalized world-space points/normals, tolerances and coverage fractions. Source-only data; no created visible geometry.
B. Render-check harness confirms each expected camera/render is fresh, matches active .blend hash/config and has nonblack valid pixels, with optional 32-bit raw depth pass and separate calibrated image-space grid. Do not claim missing outputs exist.
C. Gate executor blocks advancing G4 unless G3 floor/wall/roof/roof-roof and artistically installed-face checks all PASS. Print explicit UNVERIFIED for unimplemented checks.
D. Build a known-fail v028/v029 fixture regression: validator MUST refuse them; use 1/12 and 4/12 partial-contact findings as checks against false positives.
E. Benchmark only after Blender connection restored and prior v031 state read-only verified; then enforce one variable, matched camera and source provenance.

## Current status
**Audit only.** No plugin change, no Blender modification, no paid Meshy. Last verified v029; v030 rejected, v031 unknown after internal failure. Need operator/tool recovery before code fixture testing. Area8 DM visually accepted v082 preserved. Never represent protocol prose as executable QA capability.
