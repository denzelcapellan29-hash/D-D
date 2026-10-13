# Area 9 v040 — Narrow physical bearing-band trial (2026-10-13)

Reopened v039 joint-detail QA fixture (geometry inherited from v037), saved independent **clean** v040 `G:\My Drive\D&D\Foundry Bridge\assets\Area9_Prototype2x2_v040_BearingBandContractTrial.blend` (829,560,515 bytes), original Meshy GLBs unchanged, no new asset generation.

## Source-derived measured interface
The wider wall0 vs roof0 probe sampled 11×9 = 99 positions (x -0.6..0.6, y 1.78..2.30m) with 81 valid upper-wall/roof paired ray hits; 54 within 5cm, 23 positive gaps, 4 excessive penetrations, 14 missing wall hits, 4 lower-wall false hits. Those absent/exterior-front rock regions should not be automatically regarded as intended continuous bearing surfaces.

A tighter **central bearing strip** y=[1.975,2.040,2.105]m and x=-0.6..0.6m was found from actual `matrix_world` evaluated meshes: baseline v039 33 valid intersections, 29/33 within ±5cm, and **27/33 also with wall normal z>+.2 and roof underside normal z<-.2**. This is partial potential bearing support; it is not sufficient evidence for full physical join, distributed area load, contact continuity, or wall-floor support.

## Tested v040 geometry
New independent Meshy-derived wall0 mesh copy; four bounded Gaussian localized top-surface corrections near x=.12,.48,.60m and y=1.975..2.105m, affecting 30,888 vertices, max movement 0.0602m; prior decimation modifier unchanged/unapplied. v040 same central band: 33 valid points, **31/33 within ±5cm** and **30/33 additionally meet normal-facing z threshold**. Three remaining failures (x=.12,y2.04 excessive penetration -0.071m; x=.12,y2.105 roof normal z=-.08; x=.24,y2.105 penetration -0.054m and wall normal z=+.18). More distributed coverage tests and contact normal orientation required.

Actual closeup `G:\My Drive\D&D\Foundry Bridge\captures\Area9_v040_BearingBand_CloseupQA.png` generated, copied and pixel-inspected against fixed v039 closeup; **substantial black visible cavity above/between rock elements unchanged**, so G3 roof-wall and art quality FAIL. Do not promote as certified connector. Last better broad exterior/bearing visual geometry remains v037/v039; v040 is separately preserved as central bearing data experiment. No full-room replication, no new Meshy cost, Area8 approved v082 untouched. Capture cloud link not independently verified.

## Next design revision
Separate *load-bearing band* from *visible cave-rock transition*. Shared connector contract must specify hidden patch/collar/extension **from existing Meshy-derived geometry** (not arbitrary primitive fillers), normals and contact area, floor/wall/roof seams and the intentional overhang envelope. Before a new derivative, engineer actual surface coverage/mesh interface and check source volume and UVs; avoid further small Gaussian-only nudges. Retest robust per-patch bidirectional normals/area, fixed first-person/structural/joint images, evaluate UV/PBR and seam aesthetic. If original source volumes cannot provide enough rock for a credible joined silhouette, obtain DM review before new matched Meshy source assets.
