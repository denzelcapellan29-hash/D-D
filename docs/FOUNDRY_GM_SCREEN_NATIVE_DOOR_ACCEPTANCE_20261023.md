# GM-only Foundry 3D Canvas: native door, movement and camera presentation QA — 2026-10-23

**DM runtime choice (latest):** Sessions are conducted **in person** from the **GM Foundry screen**. Do **not** gate map preparation on separate player accounts, per-player fog/vision or player-client tests. Prioritize GM-controlled native doors, first-person/free-camera presentation, physical movement, supported floor transitions and the actual exploration route. Preserve GM-only secrets outside any display-facing view; a GM session can reveal GM-visible objects if indiscriminately projected.

**This milestone:** Native 3D Canvas **closed/open movement collision works** for a borrowed QA-only door GLB. Distinguish 3 tested native door styles below. No accepted campaign geometry was changed and no vendor 3D Canvas source was modified.

## Runtime and provenance
- Foundry V14.368 / D&D5e6.0.5 / native 3D Canvas9.0.36; 14 specialized Acq 3D MCP tools, 121 Foundry MCP tools; native first-party agent browser command transport healthy.
- Accepted original Area8 Scene: `NUEDEFAULTSCENE0` SHA **`e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`**, unchanged throughout.
- GM-viewed only, inactive QA clone: `sW4aXZgKXj1cH0US`; baseline and final checksum **`05134d2c6debeb2ffb49d17b3f1c06e96dfa409c35a348d801157dd815a03e94`**; 163 Tiles/36 Walls/13 Regions/2 test Tokens after cleanup, no players pulled.
- Pre-change immutable full QA Scene checkpoint `QA_SCENE_PRE_SURFACE_FIXTURE_20261023.json`, SHA256 **`8956e5e8570145901d7469206a9db5ec59698ae66a7762848107d54022d8ce65`** in private Google Drive QA folder.
- Asset: **preinstalled library** `modules/canvas3dcompendium/assets/Tiles/Furniture/Door1.glb`. This library is approved for studying *construction/operation*, **not** accepted Acquisitions Incorporated appearance. Native `preview_native_asset_tile` loaded the GLB, found model bounds 1.5944m wide x 3.0814m tall x 0.3199m depth. Preview auto-generated 159×32 Foundry footprint and depth308.139 px.
- Created one temporary QA-only Tile with stable semantic ID `qa:gm-native-door-20261023`, actual ID **`vo1aEuaBUngxwzgH`**, x3121,y1584,w159,h32,elev0, model above, flags `doorType=1`, `doorState=0`, `collision=true`, `sight=true`, `cameraCollision=true`. Source style mismatch/freestanding placement explicitly non-production.
- Test monk initially (x1770,y300,elev0.13,heading333.3798438225904°) temporarily staged via **TokenDocument update for setup only** at (x3071,y1600); selected with bridge-owned QA session `acq-qa-mvlf38k8`. **Only** real `canvas.tokens.moveMany` counts as movement result; setup and rollback TokenDocument writes do not. Native movement input (dx0,dy+1) mapped camera-relatively across door from center x3121,y1650 toward y1550.

## Three native door styles: actual gameplay results

| Native style (vendor flag) | Document state | Actual native moveMany result | Real 3D render |
|---|---|---|---|
| `doorStyle=0` transparent | `doorState=0` closed | **BLOCKED** x3071,y1600 unchanged | Full intact door visually |
| `doorStyle=0` transparent | `doorState=1` open | **ALLOWED** y1600→1500 | Door still partly visible/translucent; presentation unclear |
| `doorStyle=1` swing (90°) | `doorState=1` open | **FAILED: STILL BLOCKED** despite native toggle and visibly rotated model | Model swung edge-on; collision did not clear |
| `doorStyle=2` slide (angle0°, slidePercent100) | `doorState=1` open | **ALLOWED** y1600→1500 | Model moved laterally out of the passage; visibly distinct open |
| `doorStyle=2` slide | `doorState=0` reclosed | **BLOCKED AGAIN** x3071,y1600 unchanged | Reliable closed collision |

All movement results were actual native 3D Canvas-intercepted Foundry `TokenLayer.moveMany`, HTTP200/ok=true/adapter-restored=true; elevation remained 0.13 in the successful single steps. The same QA token was restored after every step; readback scene checksum returned to its pinned staged checksum per test. **Native interaction by clicking the door in the GUI was not tested**; state changed via native Foundry Tile document's `flags.levels-3d-preview.doorState`, which installed vendor `Tile3D.setHooks` translates to its own `setupDoor`, collision rebuild and animation. Do not call this mouse-click acceptance.

The 90-degree swing collision failure applies to **this library GLB / placement**, not all doors. It suggests a model-pivot/worker collision difference that needs an actual **hinge-correct purpose-built approved GLB** for production swinging doors. Do not globally substitute sliding fantasy doors where the source calls for hinged doors. The native sliding style 2 is a validated *functional GM presentation option when architecturally appropriate*, not a blanket visual rule.

## Camera presentation and visual evidence
- Captured **five actual 1902×973 WebP renders** at temporary GM free-camera position `(3.121,0.15,1.04)` targeting `(3.121,0.15,1.584)`. The `capture_3d_view` call restores the prior GM camera automatically. Closing/opening states show measurable visible differences; swing open was clearly edge-on but physically failed; sliding open clearly moved laterally and passed movement.
- Visual background around this isolated QA door is dark/outdoor void with floating proxy token placeholder. **These are not final art**, because door was staged intentionally outside Area8 production architecture; do not present as recommended in-world atmosphere.
- Actual screenshot IDs, saved and **independently indexed** in private Drive:
  - [QA closed, transparent style](https://drive.google.com/file/d/1rWKrACxSHqwFUY-6eS0YFyfeR-oj64Qi/view)
  - [QA open, transparent style](https://drive.google.com/file/d/1bRqhzRXdKv27jV7SoMd_EMCkBfOez6w3/view)
  - [QA closed, swinging configuration](https://drive.google.com/file/d/1d11tAx6KEIGkoNJefQ3FONPd0Okj5Ub1/view)
  - [QA swing open — collision failure](https://drive.google.com/file/d/1fSvWH3Dlmu0X-UEm2F-ON73v8ZwpDuf1/view)
  - [QA sliding open — collision pass](https://drive.google.com/file/d/1SXV1U6pRgCWJXmBSmFfKFpYJk_fH6_Hi/view)
  - [Exact QA data manifest](https://drive.google.com/file/d/1UXdLhYLhHaD7Y9V4yLVQQhkWbRmZaFAf/view)
- Files are private in [Drive QA folder](https://drive.google.com/drive/folders/1bfan6hyWbuWqi_kT89rB7GMRHiA-TTp1), manifest SHA256 **`ab0733699b9c05de7ca47ead96c16eac91eaf6652e520cdd36915e3095e3ce99`**. Image bytes and manifest read-back verified locally, Google Drive list_folder verified six indexed filenames and sizes.

## Native ownership reviewed against actual vendor source
- Native `levels-3d-preview/scripts/entities/tile3d.js` sets `isDoor = doorType !=0`; a doorState-only Tile update via `updateTile` invokes native `setupDoor`. Style0 changes visibility and collision/sight; style1 rotates the mesh; style2 slides the mesh, then native code regenerates 3D collision/sight. Native GM layer retains ownership, no bridge-generated physics.
- Foundry V14 Core owns the Tile document and Token document; D&D5e does not own 3D door animation. The first-party bridge orchestrated setting a native Tile flag and native TokenLayer moveMany rather than inventing an independent door system.

## Cleanup and GM-specific next priorities
- Released QA token selection (no controlled tokens); removed the single temporary door via its pinned semantic ID; restored QA monk to original x1770,y300/elev0.13/rotation333.3798438225904. **QA clone SHA exactly baseline** and GM view restored to original Area8; accepted original SHA unchanged, no players pulled and no global settings changed.
- **Priority A:** Move from engineering clone to source-map-correct **upcoming Tresendar exploration areas**, source-verified approved GLB assets, exact entrances/joints and visual QA. Don't spend another build cycle on redundant player-client fog tests.
- **Priority B:** Preserve GM-friendly controls: first-person token camera, GM free/overhead camera, native display and screen-safe framing; handle private GM spoilers off the projected display. GM-operated view does not require a separate player account. Current native GameCamera is disabled by world setting and its prior black frame failed; do not blindly enable or duplicate it—GM's ordinary free camera and FPS may be sufficient.
- **Priority C:** Build and test a purpose-built hinged door GLB *only when the source architecture calls for it*, with real native closed/open movement and visual camera QA. No Meshy spend without provider-required approval. Otherwise use documented passing native DoorStyle=2 when suitable.
- **Priority D:** Test elevation transitions and sustained traversal for GM movement, while D&D5e's `disableFalling=true` remains unchanged. No need for separate player-account vision/fog as a gameplay-release gate in this in-person use case.

**Verdict:** Native GM Tile-state control, collision-aware open/closed access, two rendering modes and camera positioning **technically demonstrated** on temporary fixture; production art/architectural integration not accepted. 
