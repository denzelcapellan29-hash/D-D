# Foundry V14 / native 3D Canvas 9.0.36 — reversible QA v07 stair contact surface
**2026-10-25, source-only + native load-preview execution. Status: SOURCE_CONTACT_GATE_PASS / NATIVE_GLTF_PREVIEW_PASS / ACTUAL_NATIVE_STAIR_ASCENT_NOT_TESTED / FULL_CERTIFICATION_INCOMPLETE.**

## Authority, scope and immutable art

This work applies **only** to the disposable existing 3D Canvas library-stair v06 QA fixture, **not Tresendar Manor’s current modular stairs** and not the accepted sewer Area8 pilot. Installed source `modules/acq-foundry-bridge/assets/blender_bundles/qa-native-door-v05-20261024/qa-native-door-v05-003-stair_connector.glb`: **44,276 bytes, source SHA256 `734f0c1bff44ce81fcad156c45477d36cdbd09f78e4117b07ec83f46071df81e` unchanged**. Source art remains byte-for-byte untouched. The historical Blender v107 master was verified `saved=true, is_dirty=false` and left untouched; current selected modular Manor assets remain owned by the production coordinator.

Last native **actual** v06 TokenLayer ascent advanced three steps then collided at fourth grid move. Independent source/native ray evidence showed native BVH intersections at (2.77, 0.16, 1.45375) and (2.77, 0.20, 1.385), attributed to v06 Tile `qfbRiIKCFSix8yzP`. Installed vendor `levels-3d-preview/scripts/wrappers.js` SHA256 `16988fd4d67383c70ef368ba24948e7ea1eceac95c50e61c8416a9e8443f58a6` uses a **horizontal movement ray at previous `token3d.losHeight`** before downward support resolution; the v06 solid risers intersect that ray. Vendor module untouched. See [prior source reproduction](FOUNDRY_V06_STAIR_SOURCE_COLLISION_REPRO_20261025.md) and [native direct owner](FOUNDRY_V06_NATIVE_AXIS_ALIGNED_STAIR_QA_20261025.md).

## New artifact, generated and tested, not production-certified

**Separate immutable QA candidate:** `modules/acq-foundry-bridge/assets/blender_bundles/qa-stair-contact-v07-20261025/qa-stair-v07-tread-contact-only.glb`; 45,556 bytes; SHA256 **`0a6641be8446f2c0b7ae8d01fa347d09a409b4b294f43f173fc37dd34807bada`**.

Reproducible builder committed at [`tools/build_native_stair_tread_contact_v07.py`](../tools/build_native_stair_tread_contact_v07.py) (commit `b93d613c835613a946c0feb1a3fd30253e063c27`, independently fetched blob SHA `545c11527ea664146be05e6858b2375d23500667`). This strict SHA-pinned first-party Blender-host Python runs without importing/saving a Blender scene. It builds **eight near-original-elevation flat tread contact surfaces, 16 triangles**, in a separate glTF/GLB, retaining source PBR material/embedded texture and original glTF node transform. The source ornament, walls, handrails and visible staircase remain separate and unchanged. The design retains stair **walkable movement collision ON** on the new contact surface; a future **isolated QA** comparison would need the original visible stair Tile’s movement collision turned OFF solely to prevent the duplicate risers’ old horizontal ray hits, with walls/rail block controls and exact restore. This is an instrumented collision-substitution hypothesis, not permission to disable collision on a production staircase or claim general native support.

**Actually executed offline geometry gate, 9/9 checks PASS**:
- Source SHA guard and reproduced original riser ray hits: PASS.
- Candidate horizontal movements: **18/18 rays CLEAR** (3 lateral lanes × 6 vertical samples); this only tests static movement-ray geometry, not TokenLayer.
- Candidate vertical contact: **15/15 downward support samples HIT** (3 lateral lanes × 5 progress points), heights within **10 mm of source support**.
- Outside-stair negative control: no support at lateral X=2.5; eight steps/16 triangles; original material/image/texture records byte-identical; Blender `is_dirty=false` throughout.
- New GLB + JSON manifest staged in separate installed first-party module directory and mirrored into local Google Drive sync path `G:\My Drive\D&D\Foundry Bridge\captures\qa-stair-contact-v07-20261025\`, with hash readback. **Cloud Drive indexing not confirmed** (search returned zero results); do not represent cloud upload as verified.

**Actually executed Foundry HTTP and native loader checks**:
- `http://127.0.0.1:30000/modules/acq-foundry-bridge/assets/blender_bundles/qa-stair-contact-v07-20261025/qa-stair-v07-tread-contact-only.glb` returned HTTP200 `model/gltf-binary`, 45,556 bytes, exact candidate SHA; old fixture HTTP200 exact pinned source SHA.
- Native first-party `preview_native_asset_tile` returned `ok:true`, `dry_run:true`, `did_create_tile:false`. Loader parsed GLB bounds width2.8 × vertical3.5 × run4 source units, and proposed collision=true/sight=false/cameraCollision=false Tile at x2710,y1395,width21,height30, native scale0.075. It **did not** place a Tile or validate true overlap/support. Current GM viewed different inactive QA Manor scene, so preview coordinates must **NOT** be interpreted as an approved placement.
- Preview current GM scene revision unchanged, **`22f7a4b87ae0f22ad0a2e8450d25ab6bb95cbd336e84a650345f4ec83e069c36` before/after**.

## Live read-only ownership and safety

Foundry world V14.368 / D&D5e6.0.5; **player-active original Area8 scene** `NUEDEFAULTSCENE0` still active. GM currently views the separate **`QA ONLY - Tresendar Manor - Modular Build 20261025`** scene `Zbrn5EcZh6ZTLmgm` with native 3D Canvas **active=true, ready=true, loading_count=0**. This GM QA scene appears owned by concurrent Manor work; it and its camera, tokens, tiles, source/roof and material flags were **not modified or restored** by this Foundry certificate task. The isolated v06 stair QA Scene `3WNB3GURss8vPtua` still exists inactive with 14 Tiles/one QA Token from read-only Core MCP. The protected original Area8 SHA `e1c023a1...` and isolated v06 QA SHA `83566ac5...` are **historical last-verified pins, not newly recomputed this turn**.

Blender connected/clean, Godot editor disconnected and untouched. No production Area8 mutation, no Manor geometry, no vendor/global settings changes, no token movement, no Meshy/vidIQ credits. No active GM view switching; no in-person player screen interference.

## Exact next bounded actions / explicit release gate

1. **Coordinate exclusive GM view/QA-scene ownership**: the separate Manor GM QA Scene is currently open, so do not hijack its state. On authorized isolated v06 QA fixture, run source+QA hash verification, snapshot all mutable flags and camera, preview exact original Tile transform and new proxy registration, and independently verify relative bounds/offsets at all eight treads (not just default `autoCenter/autoGround`). Require a rollback plan before changing any QA-only movement flag.
2. Stage candidate **only on the disposable QA stair Scene**. The collision-enabled new tread Tile must support downward contact; original source visible GLB may be reclassified no-movement-collision only **within QA** to avoid duplicated riser collision. Verify **stair rail/wall negative control** remains blocking; rejecting an over-permissive collider is mandatory. Do not disable all stair movement collision, teleport TokenDocument, overwrite original GLB, patch 3D Canvas vendor, or edit selected Manor master.
3. Execute actual **camera-axis-aligned native `TokenLayer.moveMany` ascent and descent**, log every XY/elevation and real BVH hit. If blocked or bypasses walls, fail and rollback. Then physically test **open-door passage**, Levels upper-floor/roof visibility and reload, first-person/free-camera, renderer PBR parity, FPS, Falling/surfaces and exact source/QA/camera checksum restore.
4. Keep `SOURCE_PASS`, `NATIVE_LOAD_PREVIEW_PASS`, `ACTUAL_MOVEMENT_PASS`, `RENDER_QA`, `DM_ART_ACCEPTED` independent. **Actual v07 TokenLayer ascent/descent and full Foundry 3D playability are not certified**.

This is a concrete **staged, reproducible offline correction experiment and native GLB load preview**, not a final stair fix in the live game.
