# Area 9 v034 — Connector-protected Decimate modifier fixture (2026-10-13)

## Actual live checkpoint and action
From clean v033, saved new `G:\My Drive\D&D\Foundry Bridge\assets\Area9_Prototype2x2_v034_ConnectorProtectedLODTrial.blend`, verified clean. Source Meshy GLBs unchanged; separate v033 derivative mesh datablocks with unapplied Decimate modifier remain. This is an executable modifier behavior test on the small 2x2, not a certified connection.

## Protection mask test
World-local candidate joint band: abs(X)<0.70m, 1.65<Y<2.35m; wall Z>2.10m; roof Z<2.55m. Vertex group `JOINT_BEARING_PROTECT` assigned weight 1 to selected raw vertices: wall 59,240; roof 178,252. At 50% COLLAPSE, `vertex_group_factor=0.0`, non-inverted gave evaluated region 29,207 wall vertices and 89,447 roof vertices, hence **NOT PROTECTED**. Changed to `vertex_group_factor=100.0`, `invert_vertex_group=True`: evaluated region wall 59,243, roof 178,255 (minor edge count variation due region bbox), source region approximately retained. This experimentally establishes region population preservation for this scene / Blender 5.2.2. It does **not** guarantee exact source vertex identity/positions, perimeter normal integrity, contact area or UV fidelity. Evaluated wall polygons 591,707, roof 509,822 vs v033 unprotected 591,707 and 509,823.

## Joint and visual QA
Same 15-point ray diagnostic: 12 paired intersections, 8 within 5cm; measured z gaps `[1.703, 0.006, -0.014, 0.006, -0.036, 0.014, 0.167, 0.033, 0.023, 0.112, 0.043, 0.128]` m. **G3 roof bearing FAIL**, not certified. Actual rendered `G:\My Drive\D&D\Foundry Bridge\captures\Area9_v034_ProtectedLOD_Player.png` copied byte-verified from actual Blender render and visually inspected, still obviously disconnected along irregular roof/wall tops; repeated wall and roof profiles. Drive cloud sync not independently confirmed. No full fixed-camera image set, bidirectional normal/contact coverage, four-angle isolated art/UV or Foundry GLB performance benchmark; all UNVERIFIED. Do not apply modifier, replicate scene or call approved LOD.

## Next
Preserve v034 and all earlier saves. Extract actual distributed mating patches and manufacture a shared connector contract on an independent versioned Meshy derivative **before** certifying LOD. Retest masked Decimate candidate with direct vertex displacement and UV/shading measures + fixed player/structural/joint renders. No Meshy credits or Area8 changes. Installed skill v2.7.7 applies.
