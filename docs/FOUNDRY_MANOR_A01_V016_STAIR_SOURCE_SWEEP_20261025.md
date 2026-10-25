# Foundry V14 / native 3D Canvas — current Tresendar A01 v016 source stair risk sweep
**2026-10-25, read-only native-scene snapshot and real source GLB BVH tests. Status: A01_V016_SOURCE_GRID_RISER_RISK_REPRO_PASS; actual 3D token traversal UNVERIFIED.**

## Scope, owner and live-state reconciliation

This test deliberately **did not reuse or alter the older v06 generic stair fixture** and did not touch the concurrently owned modular Manor production assets. The controlling Drive PROJECT_STATE header currently names the selected A01v011/A02v001 family, while the live GM-local **inactive QA-only** Foundry Scene `Zbrn5EcZh6ZTLmgm` currently contains the **newer as-built candidates** `Tresendar.Area01.v016` and `Tresendar.Area02.v002`. These are observed QA artifacts, **not a new DM approval or a replacement of PROJECT_STATE**; the sole desktop coordinator retains mutable ownership.

Read-only environment snapshot:
- Foundry **V14.368**, D&D5e **6.0.5**, native 3D Canvas **9.0.36**, Premium **9.0.3**; first-party bridge **0.2.8**.
- World/player **active** scene remains protected Episode1 sewer Area8 `NUEDEFAULTSCENE0`; **GM locally viewing** the *inactive* modular Manor QA scene `Zbrn5EcZh6ZTLmgm`, not the world-active scene.
- Actual 3D renderer `active=true`, `ready=true`, `loading_count=0`, `finalizing=true`. Actual nonblack 1902x973 native screenshot captured from the **unmodified existing camera**, which is looking close at a stone wall/wooden door; **not an acceptance-composition/art parity view**. Camera was not changed. Source-only asset analysis did not invoke Game Camera.
- QA Scene read-only revision before/after actual native capture: **`15a004bb13dc8ddce8e52c2bb696734dac0e046f0354448856b2ba7b5d3155d1`**. GM token selection empty. `tokenVision=false` and native `GameCamera=false`, so **vision/GameCamera acceptance not claimed**.
- Foundry base source scene listed **162 Tiles, 36 Walls, 13 Regions and two QA viewpoint tokens**, no source Scene writes. No fresh SHA recomputation for original Episode1 accepted source; do not substitute the historical source checksum for a newly verified digest.
- Blender MCP connected to historical `Tresendar_A1_8x7_Cistern_EastEntry_v107_G1_QA_PENDING.blend`, is_dirty **false both before/after**; this open file is **not** the selected A01 v016 source master. Godot project found; its editor disconnected, left untouched. Skill `ai-3d-asset-workflow` v2.7.70 read from Plugin Creator and current private Drive instructions/state read before action.
- Bridge `/health` direct readback HTTP200 with 4.61s browser-poll age, 1 active longpoll and a GM-local QA Scene ID. Earlier calls trying to force `inspect_3d_scene(scene_id=other_scenen_id)` returned generic connector errors; **no GM scene change was attempted**. Native default-current-scene inspection succeeds.

## Exact inputs and real as-built geometry

Live 3D Canvas QA Tile:
- Tile ID **`3BIMhv91xedDSlfK`**, semantic `Tresendar.Area01.stairs`, role `stair`, build `Tresendar.Area01.v016`.
- GLB source `G:\My Drive\D&D\Foundry Bridge\assets\TresendarManor\Coordinated_Production_v001\Area01_v016\A01_v016_stairs.glb`.
- **Independently read/verified source SHA256** `d8ab55e22488c69d64b100fd2ada832786669709321facd483702baad93769e6`, file **15,076,540 bytes**, **158,512 source indexed triangles**, two source Meshy mesh nodes `ART_SOURCE_MESHY_v103_N` and `ART_SOURCE_MESHY_v103_S` (79,256 triangles each).
- Transformed source GLB bounds X **[3.048,4.572]**, vertical Y **[-3.048,0]**, Z **[-3.81,3.81]** (meters).
- Native placed Tile footprint **100 x 500 px**, runtime bounds X **0.100000m**, vertical Y **0.200000m**, Z **0.500000m** (world under 3D Canvas). Derived three-axis placement scale **0.0656168** consistently across source X/Y/Z; one **100 px** native grid step in Z spans **1.524 source GLB units**. These are specific to this placed v016 Tile, **not a general conversion**.
- Source/placement hashes for related v016 GLBs also verified read-only: `A01_v016_floor.glb` SHA256 `29cac89a4e46a8ffa8b8887d83cf70a991b4439e60ccce04e5380df60f3ff5bd`; `A01_v016_roof.glb` `e6f9d66b8d58b9c11fc4d2aafd79c926d1891d8e02ee38df10e301bf1f98cce1`; `A01_v016_walls.glb` `238e2d8eb2d5a9333e9bc835e94cc6df0a10483c846dc6dffa23c9d7dab7f182`.

## Read-only geometric experiment (actually executed)

A new reusable, pinned GLB-to-native-grid read-only preflight was committed on the isolated Foundry feature branch as [`tools/foundry_manor_stair_source_sweep_v07.py`](../tools/foundry_manor_stair_source_sweep_v07.py); it imports the previously proven pure source mesh parser/BVH from [`foundry_stair_glb_ray_gate_v06.py`](../tools/foundry_stair_glb_ray_gate_v06.py). It enforces the exact source SHA and refuses nonuniform source→runtime scale, then shoots genuine Blender `BVHTree` triangles. **It never imports a mesh into the open scene, writes a file, or moves a token.**

Tested one upward +Z native grid-step `source_z=-3.000000 → -1.476000` at three independent interior lateral lanes. Downward source support sample (from +Y) and horizontal movement-segment rays were sampled at fixed **old-support + measured candidate clearance**; the clearance is *a parameter*, **not** a measured live native token LOS height.

| Source lateral X | Support rise over native 100px | Old-height horizontal rays intersect source stair | Old-height 120mm clearance ray |
|---|---:|---|---|
| 3.30 | **0.107983 m** | Collision at 20, 30, 40, 60, 80, **100mm** | CLEAR |
| 3.80 | **0.107243 m** | Collision at 20, 30, 40, 60, 80, **100mm** | CLEAR |
| 4.25 | **0.107375 m** | Collision at 20, 30, 40, 60, 80, **100mm** | CLEAR |
| Outside control X=4.90 | No supported start/end | No stair support path to classify | Not applicable |

**Executable QA regression: 6/6 positive assertions PASS; 2/2 negative controls PASS** (wrong SHA rejected, mismatched/nonuniform native scale rejected). The saved Blender session remained clean; this is independent of the previously failed v06 disposable stair and tests the **actual current modular Manor A01 v016 source**.

Interpretation: On the measured in-GLB support geometry, a 100px horizontal movement ray remaining 20–100mm above the old stair support collides with the ascending stair, while 120mm clears for the three measured interior lanes. This is a **high-priority native traversal risk** because the generic v06 stair test stopped under the installed old-height movement collision wrapper. But no native TokenLayer callback, selected token's real LOS height, camera-to-axis conversion or live A01 v016 ascent was executed. **Do not claim that v016's true native ascent has failed or succeeded.** Separate north/south start/exit positions and true flat-foot supports require representative route staging and negative controls.

## Engineering disposition / next authorized step

1. Preserve the existing QA Scene, v016 GLB, and all original accepted/manor artifacts. **Do not silently replace or reexport the v016 source stair or overwrite the current project state.** The installed bridge presently views the concurrently owned Manor QA scene; coordinate a bounded GM-only test before any token movement to avoid interfering with the sole desktop coordinator.
2. For real native certification, capture current QA revision and original token pose, select the QA monk using guarded session APIs, align camera to the actual intended entry direction, run actual 3D Canvas-intercepted `TokenLayer.moveMany` ascent **and descent**, wall negative and door passage controls, then strictly restore the owned token selection, camera, QA Scene and GM view. A `TokenDocument` teleport is not passage. Recheck exact revisions before/after; stop if concurrent changes are observed.
3. If real v016 ascent blocks, compare first-party native hit geometry to this pinned source gate and hand the owning Manor artist a new separately versioned candidate with correct socket elevations, source art and safe rise/run, then *repeat* the gate and the actual native movement. Changing Tile collision=false or source assets in place is prohibited. Subsequent gates: floors/roof/Levels visibility, cold reload, native camera, material/lighting parity, performance and full rollback.
4. Native **stair PASS, door TOKEN PASS for this scene, multi-floor, FPS, reload, performance and final DM art acceptance all remain UNVERIFIED**. Historical generic v06/door fixtures provide only their own scoped results.

**No Meshy/vidIQ costs, vendor patches, live scene/Token/Tile/setting writes, Manor mesh changes, camera changes or gameplay certification were performed.**
