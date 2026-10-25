# Foundry V14 / native 3D Canvas — read-only stair preflight and connectivity checkpoint
**2026-10-25. Status: SOURCE_RAY_GATE_PASS; native full-session certification BLOCKED.**

## Action actually performed
Created and executed a reusable, **read-only** Blender-Python source-GLB ray preflight:
[`tools/foundry_stair_glb_ray_gate_v06.py`](../tools/foundry_stair_glb_ray_gate_v06.py).
It parses the GLB JSON/BIN directly, applies glTF node transforms, checks the
source triangles with Blender `BVHTree`, sweeps height/lateral samples
and independent vertical-support rays, validates the immutable source SHA,
and can be invoked by the source-asset owner before a revised QA fixture
is offered for native import. It **does not** import the GLB to the scene,
save a scene, modify geometry or mark a file release-approved.

Source fixture (disposable generic QA, **not** Tresendar Manor modular art):
`modules/acq-foundry-bridge/assets/blender_bundles/qa-native-door-v05-20261024/qa-native-door-v05-003-stair_connector.glb`.
SHA256 `734f0c1bff44ce81fcad156c45477d36cdbd09f78e4117b07ec83f46071df81e`;
44,276 bytes; 358 indexed triangles; glTF node `stairs`.
The placed-v06 mapping is **specific to this Tile**, scale 0.075, vertical
offset -0.02625m, world Z origin 1.46m; it is not an importer default.

## Executed source-geometry regression
Executed code in the connected Blender Python environment against the
actual installed immutable GLB and returned PASS on all five formal controls:
- **3 lateral lanes**, source X = -0.35, 0, +0.35, produce identical
  expected block/clear outcomes for actual native movement-ray samples
  Y = 0.12, 0.16, 0.20, 0.24m (12 sampled outcomes).
- At Y = 0.16m the source ray first strikes world Z = **1.453750m**;
  at Y = 0.20m it first strikes world Z = **1.385000m**,
  matching prior **live native BVH intersections within 1e-6m**.
  Y = 0.12 and Y = 0.24m are clear.
- **Outside-lane negative control** X = +2.5 source units: all four
  ray heights clear (4 more samples), excluding a global false blockage.
- **Actual riser support** at source Z = -0.0952 is world height
  **0.16089001m**; moving the sample +25mm in native Z onto the previous
  tread changes support to **0.12375000m**, a 37.14mm decrease.
  The support-ray control passes and reveals the sharp riser discontinuity.
- Pinned source SHA matches the installed source GLB; a different source
  cannot be silently tested as the accepted fixture.

Total diagnostic ray samples in this pass: **16 lateral movement rays and
six support rays**. This is an **offline source preflight** only;
we did not perform an actual new TokenLayer movement.
The gate deliberately outputs `native_runtime_certified: false`.

Executable tool was written/read back on the isolated feature branch;
latest tool content blob SHA `dd3434945f0e69a8cde321bcf7cd14d1ed53863c`,
commit `6447fd5f8d50367f4e09ac1ad12a9e28ba7d04e0`.
This adds a candidate-retest workflow without mutating current art.

## Live connectivity and preservation
- **Foundry MCP disconnected** on both attempts: connector reported the world
  had last been connected 8 minutes, then 16 minutes, previously.
  First-party bridge `http://127.0.0.1:18747/health` was HTTP 200,
  but reported browser poll age **635.35 seconds**, zero active browser
  longpolls and no outstanding RPCs; **HTTP 200 does not mean client or
  3D renderer is connected.** Last bridge Scene name was
  `QA ONLY - Tresendar Manor - Modular Build 20261025`, so neither the
  client GM's current view nor the protected scene checksum could be
  freshly verified. We made **no Foundry scene activation, GM-view restore,
  camera, Token, Tile, door, setting or vendor edit**.
- Blender connected; viewed historical `Tresendar_A1_8x7_Cistern_EastEntry_v107_G1_QA_PENDING.blend`
  `is_saved=true`, `is_dirty=false` before and after tool execution.
  **This is not the selected current modular Manor review master.**
- Godot 4.7 project metadata read-only, not used or modified.
- Private skill `ai-3d-asset-workflow` v2.7.70 read via Plugin Creator
  because `skills__list` returned empty. Controlling Drive
  CURRENT_HANDOFF / PROJECT_STATE identified current modular selected family
  A01v011/A02v001/A03v002/A04v002/A08-CharnelChasmv002; sole desktop
  coordinator owns mutable Manor artifacts. Historical sewer Area8 accepted
  source is **not** the Tresendar Charnel Chasm. No other branch/artifact
  ownership was exercised.
- No paid Meshy or vidIQ calls; no Manor source edit; no player activation.

## Next bounded native test
When the **Foundry world and browser client reconnect**, first inspect
GM-local Scene and source/QA revisions without writes. The scene owner
must separately supply a versioned, visually faithful, collision-enabled
supported-stair QA candidate (preserve entry/exit and original source hash).
Apply the new preflight to its GLB (use `expected_sha=None` only for
an explicitly new candidate, never to override the protected v06 SHA);
then import **only** the new QA semantic asset into an isolated inactive
Scene with source and rollback guards. Repeat **actual** camera-corrected
native TokenLayer ascent/descent, door token passage, Levels roof/upper-floor
visibility, cold reload, FPS/material parity, and exact rollback. No
manual TokenDocument teleport counts as traversal. Full NATIVE_PASS and
DM art acceptance are withheld.

**Use this checkpoint as technical evidence, not as proof of a corrected
staircase or a release-ready Manor scene.**
