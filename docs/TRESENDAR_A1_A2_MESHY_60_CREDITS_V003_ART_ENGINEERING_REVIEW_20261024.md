# Tresendar Area 1–2 wall/floor CAD x Meshy rebuild: 60-credit generation and v003 fixture
**Date:** 2026-10-24. **Status:** REAL source GLBs SUCCEEDED; CAD preserved; v003 limited art fixture tested; **ART FAIL (incomplete room visual continuity)**; Foundry runtime UNVERIFIED; DM acceptance pending.

## Cost and provenance
DM confirmed 30 Meshy credits for each source GLB, 60 total. Meshy v7.1 multi-image PBR 2K tasks both SUCCEEDED and consumed exactly 30 credits each:
- Wall task `01a16ffd-71bb-7691-9d56-3dd832ee353b`, GLB 56,625,200 bytes, SHA256 `5244055079ca14ab76dfef03233c3c74e930d562deae381af3c5e8dfd21781e8`, original 852,403 vertices / 1,578,898 triangles, UV/PBR.
- Floor task `01a16ffd-b4ee-7588-9908-c99a26d27da6`, GLB 24,583,704 bytes, SHA256 `a36e924d9b9fde4ad06466e751b72319b451f5ae15c5f60e5a973d3925bd8b3d`, original 263,306 vertices / 498,054 triangles, UV/PBR.
- Input: eight hash-verified 3/4 isometric PNGs (four wall, four floor), private Drive: https://drive.google.com/file/d/1OPuJr_EbjDi6-47uxIGuyAUSrNZ6FV08/view . The original Meshy GLBs and texture maps are saved separately under synced `ART_Retrofit_v001/MeshySources/`; exact cloud GLB file links not independently confirmed.
- SOURCE: private Chapter 4 Tresendar Manor Area1–2 and Map2.2 reviewed. Built stone walls, distinct newer poor mortar blocker are source-grounded; exact limestone species and paver pattern are expressly DESIGN_CHOICE.

## Actual Blender construction, NEVER active GUI/source overwrite
Blender 5.2 background process opened and saved new derivatives of actual v125 architectural build; active GUI historical v107 untouched:
- Original v125 SHA `77a7568fb9a601843b0c024ff7abc3449c58f6d02db6afb338cb7e839f093f94` preserved.
- v002 `Tresendar_A1_A2_v125_MESHY_WALL_FLOOR_FIXTURE_v002_ART_QA_PENDING.blend` SHA `89c536085d76191dd884c5d3cd8e6f8d9d58f3a6d24801b75c6d5c64f4961638` tested two N-wall CAD bays and two adjacent floor bays using FOUR repeated art wall courses and two Meshy pavers. Its reproduced stone faces were obvious, dark exact panel seams remained, pale finish clashed: visual ART FAIL.
- v003 `Tresendar_A1_A2_v125_MESHY_WALL_TWO_BAY_FIXTURE_v003_ART_QA_PENDING.blend` 121,563,252 bytes SHA `a92fe9c430e4058cca57b0e4e3a8e3aa53c3d38c5228c349fd853d65ab52d4cc`. Replaced four repeated visual wall panels with ONE source-derived continuous 3.048-meter wall across TWO existing 1.524m CAD wall bays, retaining two visual floor bays. This removes the obvious wall panel grid but vertically stretches the source stone: assess material/proportions before art acceptance. Scene-use wall derivative 39,472 triangles with UV/PBR; floor 79,688 triangles each; fixture total 198,848 new visual triangles (still not a scene-wide LOD pass). Immutable source GLBs unchanged.

**Verified independent numeric v003 readback:** all 247 v125-stage objects present; every original object's mesh identity, vertex/face counts, transform and materials identical. Only four targeted CAD floor/wall objects were hidden from RENDER in this derivative (their collision/geometry remains). Actual evaluated vertex contact residual floor-wall 0 m (two instances), floor-floor 0.0000005 m, wall-wall 0.0000005 m. Deliberate +25mm seam shifts detected by both floor and wall checks at 0.0250006m. Meshy wall visual envelope matches original CAD pair bbox exactly, floor art top +12mm above CAD floor support. This proves the limited sampled geometry preservation/contact, **not** all full-room playability.

## Actual comparison and ART gate
Private image comparison explicitly extracted from real Blender renders: https://drive.google.com/file/d/1zY1KKLsSSUKR0xTH1g7AvKNiM6jYEYyN/view
Original v125 player eye: https://drive.google.com/file/d/1WgHMmGb1HbccQPpckBBB5Bxrv_Z2abCU/view
v002 repeated wall/ground art: https://drive.google.com/file/d/1cnJ0jwafSM8dsoyiru4ATOa8_RmlpDIA/view
v003 continuous Meshy wall/floor: https://drive.google.com/file/d/1gXYmJt5T_t4NmyD-JjfqaJHyi4EZ-2Dj/view
Independent full source front/back Blender PBR captures: https://drive.google.com/drive/folders/1Gdy3Dv58gMx7LYH9-uCfCL0b_boWhKu7

The new REAL geometry provides visible stone relief, more plausible material semantics and better player-eye reading than the old speckled placeholder. v003 is better than v002 at wall seam/tiling. However final ART still FAIL: very pale stone, abrupt mismatch to unchanged adjacent wall surfaces, overly similar floor modules, and unverified corner/doorway/roof context. Do not duplicate across Area1/Area2 before a real continuous room segment and native 3D Canvas parity pass. DM alone accepts final visual.

## Next safe action
Work in a separate v004 **derivative** only if needed: align PBR age/palette across wall/floor, create compatible genuine Meshy-derived corner and doorway returns or source-derived variation; inspect unchanged CAD portal/secret/roof envelopes, get player-eye/reverse/seam imagery, compare actual render with approved Area8 benchmark, and report keep/revert. Two unsuccessful aesthetic strategies trigger a different asset/fabrication strategy, not endless tinting. Foundry owner validates GLB camera/material/collision parity. No more Meshy paid tasks without their task-specific costs and DM confirmation.

## Independently verified private Drive artifact links (same 2026-10-24 milestone)
- **Wall original Meshy GLB (56.6 MB)**: https://drive.google.com/file/d/1gUFY5IKoE1GjvJfzdwU2vGzJ_Fp4YuY4/view
- **Floor original Meshy GLB (24.6 MB)**: https://drive.google.com/file/d/1a2CYlEBzFrqsMNgyOatRe35ze8jZsCU6/view
- **Reversible v003 Blender two-bay fixture (121.6 MB)**: https://drive.google.com/file/d/1GcBS0-vLpWHf2zJQP9_UKfE0Oh5AIaja/view
- **Preserved v002 four-panel comparison fixture**: https://drive.google.com/file/d/1_8Nzlf6uFKAWw9HP3TXW4O8oPVufB8-w/view
- **Evaluated-vertex contact, 25mm negative controls, hashes, triangle budgets**: https://drive.google.com/file/d/1xllrDVk4YPEabm2bdey2Ae1ux-ySPi0w/view
- **Actual rendered three-stage art comparison (v125 / v002 / v003)**: https://drive.google.com/file/d/1zY1KKLsSSUKR0xTH1g7AvKNiM6jYEYyN/view

The above Drive file IDs were independently resolved from containing private Drive folders; hashes computed in connected Blender. No full room art acceptance or native Foundry parity implied.
