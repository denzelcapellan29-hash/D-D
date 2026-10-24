# Foundry V14 / native 3D Canvas 9.0.36 — model-door QA v05
**2026-10-24 | Status:** Source authored/GLB export PASS; seven-chunk manifest and live asset-loader preview PASS; full Python 47/47 PASS. Actual native import, hinge swing, token movement, level visibility and runtime visuals remain UNVERIFIED. PR: https://github.com/denzelcapellan29-hash/D-D/pull/8 (draft/unmerged).

## Why prior open-door test failed
Read installed vendor scripts/entities/tile3d.js read-only, without patches. The 9.0.36 setUpDoors function traverses GLB meshes with userData.isDoor + doorId. setDoorsMaterials reads Tile flags.levels-3d-preview.modelDoors[doorId].ds, and doorStyle=1 rotates the **mesh child** about its local Y pivot, then rebuilds native collision. Whole-Tile doorType/doorState instead makes setupDoor rotate mesh.children[0]. Previous importer wrongly applied whole-Tile door flags to a mesh-tagged leaf. Source GLB also had duplicate static wall_doorway_door mesh (source itself already labeled acq_excluded_reason), which could block portal after leaf opens. DoorHandle was not parented to Door. Native Tile doorAnimateAngle is converted from degrees, but mesh userData doorAnimateAngle is used directly; QA exporter now refuses unverified mesh-angle overrides.

## Code and disposable source changes
- Feature branch exporter: require per-mesh acq_role, preserve internal Door->DoorHandle parenting in glTF node hierarchy, reject visible excluded source objects, only permit explicit parented door attachments, reject unverified per-mesh angle override. No arbitrary geometry authored and no change to original Manor master.
- Feature branch importer and isolated QA runner: per-role movement/sight/camera collision matrix (floor/stair true/false/false; wall/roof and leaf true/true/true; visual foliage false/false/false); internal leaf uses modelDoors[doorId].ds rather than whole-Tile flags. Reconciler requires snapshot/readback of modelDoors or fails closed. New tests test_embedded_model_door_v02.py.
- Source fixture original, read-only: C:\Users\denze\AppData\Local\Temp\acq_foundry_import_v02\qa_two_level_dungeon_leafonly_v002_QA.blend; SHA256 25be3ebcccb49d857378abc4662b229cee7224bbdbf45c49a385c008e9e7fd4c.
- **New disposable** source: C:\Users\denze\AppData\Local\Temp\acq_native_door_v05_u235xpn1\qa_semantic_hinged_fixture_v05.blend; SHA256 2f26a428c5309adb1abaad3356e729b2237297c23e01d123890dd22dcd210fd0. Source-marked duplicate static doorway door hidden only in QA copy. DoorHandle parented to original Door with world transform preserved. Seven explicit chunk roles, no new visible geometry. Original source SHA rechecked unchanged.

## Actual exported/staged GLB evidence
Seven GLBs total 382,108 bytes. Staged under private local first-party module assets directory:
C:\Users\denze\AppData\Local\FoundryVTT\Data\modules\acq-foundry-bridge\assets\blender_bundles\qa-native-door-v05-20261024

GLB SHA256:
- lower_back_wall opaque_wall: ee44edd7c73b80dd7ccbbe668fcee45409ef98dfb0c0dbc7d9d92e776f6cc93e (54,020 bytes)
- lower_floor walkable_floor: c24d4c814dc6dc79c43d384b108c3467f7738c1b001d24ec7b39ab1b59cf5eba (29,004)
- lower_side_wall opaque_wall: b7d30840c5ca47bdbd728e7718af58b6a90334146746e0032d94cfc782baa54 (54,076)
- stair_connector stair: 734f0c1bff44ce81fcad156c45477d36cdbd09f78e4117b07ec83f46071df81e (44,276)
- upper_doorway opaque_wall: 5a98e91e135ae538d952fd934d2faf1d22dc3f158e8b976df2d0b352ced248a0 (46,904)
- upper_floor walkable_floor: e4739f4b73ef9e1bfac5eefaf93be3cb16f51bd6b52cb90fb4714b464e64d87d (29,008)
- upper_interactive_door door_leaf: 33948183ebb461f762035dbb3d783323e4ac140f29aaefef0e09aaff1f0e4975 (124,820)
Manifest SHA256 85926a053bb561433719f0b00f007d2e1712a50b555138832a0e997572993665. GLB2 JSON examined: Door node has child DoorHandle, native isDoor=true/doorId and style1 extras; no wall_doorway_door included in wall chunk. Exporter run exit0; importer offline verification 7/7 source SHA, asset SHA, coordinate/dimension and role semantics PASS.

Real Foundry port30000 HTTP GET of staged door/floor GLBs returned HTTP200 and exact byte lengths. Native first-party preview_native_asset_tile read-only calls returned ok=true, did_create_tile=false and **unchanged source revision**. Floor model bounds 300x300px, native depth11.25px, candidate flags movement true/sight false/camera false. Door bounds 120x24px, native depth201.0186px, candidate true/true/true. This confirms native loader & placement candidate ONLY, not actual door movement, collider or art QA.

Clean fresh external Blender-bundled Python v3 environment: 47/47 offline Python tests PASS, no syntax errors, GitHub source at commit 7ab251a3a44e97dd087841baea808cd79ea5ba1b (following patches only docs were authored). Earlier in-process Blender imported an old cached Python module, causing false failures; clean subprocess resolution verified. Full Node/browser and native gameplay test gates remain separate.

## Scene safety and remaining work
Foundry V14.368 + native 3D Canvas ready. Accepted Area8 Scene NUEDEFAULTSCENE0 is active; QA Scene 3WNB3GURss8vPtua inactive and still has 7 OLD untagged Tiles and no QA tokens. User stated first-person GM view was his inspection and explicitly authorized switching GM view. The source **document digest**, however, is 446136385eeae576bfb4abac199639b1f42b2a66e2e48883b06c96b2ea3c40dd, while current QA controller is pinned to e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f. Native preview readback showed digest unchanged. Because actual source digest changed, user permission to change the GM *view* is not permission to silently replace the accepted source-document baseline; guarded QA view remains blocked. No source or QA scene writes, no QA Scene activated for players, no tokens moved, no global Falling/vision/camera settings changed. Manor Blender file saved/clean; Godot untouched.

Next safe P0: reconcile source digest with existing accepted source/backups; establish fresh strictly pinned view-controller route without overwriting source, then view inactive GM-only QA, import only NEW role-tagged seven GLBs, compare before/after Tile modelDoors 0->1->0 and actual leaf + handle mesh pivot, moving/sight BVH raycasts and true controlled Token passage. Test stairs XY/elevation and negative wall crossing, upper floor/Levels roof fade, native renderer eye/reverse/overhead/PBR, cold reload and FPS, then semantic-ID rollback and exact revision checks. Do NOT claim playable/visual acceptance from export/previews.

The installed AI 3D Asset Workflow v2.7.67 was read back with native modelDoors section plus existing v2.7.65 art section preserved: https://chatgpt.com/plugins/plugins_6ac99807af3c81918a869eb5e2710a6b .
