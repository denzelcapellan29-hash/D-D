# TaleSpire P1 — real native slab import, render and backend reload verified (2026-10-18 ET)

## Mission/authority
User notified "QA Board ready" after asking the assistant to continue the TaleSpire-native 3D pilot. The currently open new/disposable board is named **Unknown Realm 1** according to TaleSpire's own Campaign Boards menu; the desired proposed name "Acq QA Native Slab P1" was NOT shown. Treat it as disposable QA only on the user's confirmation, NOT a released campaign map. Preserve original Meshy assets, approved Area8 v082 Blender state and offline Foundry recovery. Source-first semantic blueprint, 1.524m pitch and existing installed AI 3D Asset Workflow connector/art policies remain binding.

## Exact validated artifact
Local staged code at `C:\Users\denze\Documents\AcqTaleSpireQA\P1_NativeSlab_20261018\four_piece_native_pilot.slab.txt` with SHA-256 `1f0992595d52eb4821c3ce77d502d18b9fae418729c926714cc4ae26fa72fc48`, 128 base64 characters (95 gzip bytes), 102 uncompressed bytes. Native published Slab v2 magic 0xD1CEFACE, version=2, 3 asset-layout groups, creature count 0, exactly FOUR instances:
1. abandoned_village_floor_2x2_01 UUID f5dbe998-db6d-407f-8738-ad7d0a33d18e at local grid x0,y0,z0 yaw0
2. abandoned_village_floor_1x1_01 UUID 65a07fe1-84b4-4d78-bb24-b49ad0cb6966 at local grid x2,y0,z0 yaw0
3. castle wall 1x1 half UUID 7f83ef67-8a96-4dcc-8df3-6bd5728743ee at local grid x0,y0.5,z0 yaw0
4. same castle wall x1,y0.5,z0 yaw0.
All UUIDs are verified entries in installed TaleSpire Medieval Fantasy native index, NOT custom Meshy tiles. Proposed semantic JSON → byte encoder + v002 14/14 local Python tests rerun PASS. Syntax, UUID, orientation encoded and local collider AABB checks pass; no full connector mesh certification.

## Live UI test and independent QA — PASS for core P1
- TaleSpire Steam build 25937418, already joined in GM role. After DM ready, read-only live screenshot established the blank QA board.
- Simulated keyboard events initially did not work: Windows Unity input required explicit keyboard scan codes via `MapVirtualKeyW` on keybd_event. Initial click to close Tutorial missed because separate PowerShell screenshot process has DPI virtualization (screenshot scaling differs from input physical screen); used native unscaled crop to identify Tutorial X at physical x385,y46. This is an automation input lesson, not a scene defect.
- Pressed **B** with scan code to actually enter BUILDING mode, loaded correct slab into Windows clipboard, Ctrl+V with key scan codes; screenshot eventually displayed a 3D moving preview, and game's Player.log recorded `Sending paste string chunks`, `Received paste string chunk` followed by `Pasting 4 assets`. Ghost initially showed wireframe before Unity finished instantiating textured models; don't call this a failure too early.
- Single left-click committed one group on the verified disposable QA board. ESC with native scancode cancelled an offered duplicate preview. Fresh actual screenshot confirmed ONE stationary real group; rotating/zooming camera produced oblique views.
- Observed **2 continuous light-stone wall sections** and **wood floor modules** in genuine TaleSpire native 3D, textured, nonblack, responsive. Wall-wall visual joint is coherent at this camera angle; floor-wall and proper walkability/path/true triangle-contact remain UNVERIFIED (AABB/render art alone insufficient). 3D asset count/log four rather than a mere document write.
- Persistent backend reload was ACTUALLY tested. In Campaign Boards panel the sole QA entry appeared as `Unknown Realm 1`. Expanded entry and selected **Reload Board**. Local Player.log confirmed `BoardSessionManager Active → TransitioningToLoadADifferentBoard → FetchingExistingBoard`, `Fetching board from the backend`, `FetchBoardState: ... Succeeded`, return to `Active`. Fresh independent screenshot shows the SAME 3D wall/floor asset arrangement survived reload. **Save/reload PASS**, not just assumption from autosave.
- No crash or board renderer stall in this small test. This is NOT a 3–4-hour stability benchmark and not a complete official dungeon, so those gates remain UNVERIFIED.

## Verified image/evidence
Real screenshot captured from TaleSpire client, 1536x864 PNG, 2,690,733 bytes, SHA-256 `d89c6b00c3ab06941c76f56a5040e2b859a81e9c0f2c434fb625347504e22c9d`.
Local preserved `C:\Users\denze\Documents\AcqTaleSpireQA\P1_NativeSlab_20261018\captures\P1_v002_TaleSpire_Actual3D_ObliqueAfterPlacement_20261018.png`; copied byte-identically to `G:\My Drive\D&D\TaleSpire QA\captures\P1_v002_TaleSpire_Actual3D_ObliqueAfterPlacement_20261018.png` and **Google Drive independently search-confirmed URL and size**:
https://drive.google.com/file/d/1lwLaTdWnYP2ltkOwPyf2q5zTZJqJsBVa/view?usp=drivesdk
Do not treat the file as an altered user-designed artwork; this is an unapproved technical four-asset QA fixture.

## Decision/gates
- P1-A format/data **PASS** (14 tests, binary parse, registered UUIDs).
- P1-B real native slab paste and rendered textures **PASS** (one placed set, 4 objects).
- P1-C game board backend reload/persistence **PASS**.
- P1-D exact connector patch metrics, walking/navigation, any moving token, player secrecy/fog/lighting, multiplayer joining, multi-hour resilience **UNVERIFIED**.
- DM scene/art approval **NOT REQUESTED/NOT ACCEPTED**.
- No Unity/TaleWeaver .tsMod or custom Meshy scene asset was imported, no Meshy charge, no Foundry/Blender scene write. Keep original P1 v002 zip sha `d767ef69ed7f4796aa11caa074bf9e7b161bde54b5c68803fa662a5557959ab5` downloadable in originating conversation artifact but not assume future sandbox path.

## Next reversible increments
(1) Extend native slab fixture only after measured floor/wall contacts and simple token movement QA, calibrated actual cell elevations; increase to 2x2 floor plus functional perimeter/door and performance batches.
(2) P2 independently derive user-approved Meshy tentacle into <60,000-vertex single-mesh textured creature FBX through validated TaleWeaver Lite Unity 2021.3-compatible pipeline; original approved GLB preserved, four-angle matched image and packed 3-texture QA; do not claim .tsMod until actual compiled and game displayed. Current tentacle export 190,669 vertices, 237,335 tris/9.3MB, so needs significant independent LOD. No credits without task confirmation.
(3) Canonical semantic room→native slab tile placement and separate Meshy hero-mini handling; do not use questionable TaleSpire native geometry extractor as Foundry bridge. No duplicate Blender assembly.
(4) Only after P2 and gameplay benchmark decide primary runtime, not from this isolated PASS.

No release of full campaign or blanket TaleSpire stability assertion.
