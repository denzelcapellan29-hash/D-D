# GM-operated native 3D Canvas regression — October 23, 2026 (ET)

**Status:** Native movement four-direction regression PASS; genuine native first-person render PASS; independent source/clone rollback PASS; combined Foundry V14 Region Surface creation + native movement BLOCKED; D&D5e Falling NOT TESTED; no comprehensive continuous-path claim.

## Scope and preserved authority
- The DM runs in-person sessions from one GM-operated Foundry screen. This run concerns *native integration testing*, NOT Tresendar Manor construction. No source world, visual geometry, Meshy, vendor module, global settings or unrelated Blender/Godot edits.
- Foundry 14.368, dnd5e 6.0.5, native 3D Canvas 9.0.36, Premium 9.0.3, first-party Acq bridge 0.2.8. All 14 Acq tools and 121 Foundry tools exposed.
- Protected original source Scene `NUEDEFAULTSCENE0` checksum `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`, exactly unchanged. Inactive GM-only QA clone `sW4aXZgKXj1cH0US` baseline/final checksum `05134d2c6debeb2ffb49d17b3f1c06e96dfa409c35a348d801157dd815a03e94`. GM local view switched to QA without activating for players, later restored to source; player pull false.
- QA clone baseline/final: 163 Tiles, 36 Walls, 13 Regions, 6 Lights, 2 QA Tokens. Monk original x1770,y300,elevation0.13,heading333.3798438225904; final EXACT same. No selected tokens at end.

## Native runtime and movement evidence (new live tests)
- Launched the installed native `preview3d` cube control once from Foundry desktop. 3D Canvas runtime `active=true`, `ready=true`, `loading_count=0`, and a genuine 1902x973 renderer capture produced, not a mock.
- Existing first-party QA session `acq-qa-mvlq09x9` selected the monk with native Token.control. The installed bridge source SHA `b25a35aa23c53e361222c53ab0518e7e30f2b17f70df3fef861db3b3151cd631` was read back. Existing guarded browser `/rpc` operation `qa_native_token_move_many` invokes Foundry `canvas.tokens.moveMany`, intercepted by real vendor libWrapper. It checks the exact inactive clone, GM/selection ownership, native renderer ready, source checksum and cardinal input, automatically restoring the original TokenDocument pose after EACH test. Rollback-only TokenDocument writes are never counted as locomotion.
- First input (dx0,dy+1): monk x1770,y300,elev0.13 -> native measured x1770,y200,elev0.12,heading180, then exact pose restore.
- Second input (dx-1,dy0): x1770,y300,elev0.13 -> x1870,y300,elev0.13,heading270; exact restore.
- Third input (dx+1,dy0): -> x1672.5517317392462,y300,elev0.13,heading90; exact restore.
- Fourth input (dx0,dy-1): -> x1770,y385.90413412970634,elev0.13,heading0; exact restore.
- All 4 calls actual HTTP200, native_api_invoked=true, native_move_succeeded=true, native_document_position_changed=true, restored=true, `native_move_error=null`. Exactly pinned QA clone checksum before/after. This tests four independent SINGLE steps, not continuous multi-step travel, and the +100px raw inputs do not guarantee +100px native travel. Current installed dry-run preview uses grid-absolute center coordinates; vendor moveMany remaps camera-relative heading. The preview is **not a trustworthy native direction or exact path predictor** until a tested first-party correction is deployed.
- Native roof/connector/floor downward BVH and wall rays already pass sampled static intersection tests; this session reconfirmed native collision groups move7/sight9/camera4. Previous real native wall-block/open-path and native sliding-door closed/open/reclosed tests remain independently documented separately; not rerun in this batch.

## Native first-person live visual check
- Guarded native `set_native_camera_mode(mode=first_person)` and exact owned session `acq-camera-mvlq4o1k` selected the recognized monk. Camera at (1.82,0.113,0.35), near clip 0.05. Actual 1902x973, nonblack 3D Canvas WebP image shows finished physical masonry, ceiling, two sewer pipes, central object, sewage pool and token placeholder. The QA capture was rendered in this conversation but was NOT independently uploaded to Drive.
- Guarded `mode=restore` succeeded. Original free camera returned; no change to GameCamera world settings. Historic GameCamera black visual failure still BLOCKED and not repeated. Free-camera and FPS suffice for presentational GM tests; avoid inventing a new camera engine.

## Combined Surface/Falling test: explicit blocker
- Read-only `inspect_native_floor_surfaces` returned 0 native movement Surfaces in unchanged QA scene, both test token Surface support probes null. Existing GLB BVH ground and D&D5e Falling are separate native mechanisms; the actual dnd5e world setting `disableFalling=true` was NOT changed, so no honest fall/damage automation certification.
- Tried one planned metadata-only `Region` creation via public typed `apply_semantic_objects` dry-run PASS followed by actual, then a single direct guarded first-party `/rpc` operation. Both actual operations reported `created:[{document:'Region',id:null}]`, no changed clone hash, Region count remained 13, and read-only getSurfaces stayed 0. This is **NO REGION CREATED/NO COMBINED SURFACE TEST**, not a pass. Do not endlessly repeat. Diagnose the silent zero-doc return or use a correctly versioned native fixture and explicit created-ID assertion before next QA.

## Recovery / cleanup
- Native selection restore initially produced wrapper error; independent readback later found token pose exact, selection empty, and QA clone checksum reverted to baseline. A single direct recovery attempt using observed transient checksum `8fd4495c...` returned revision mismatch because the actual scene had already converged to baseline `05134d...`. This confirms **asynchronous revision/heading settling**, not a permanent scene mutation. Do not mark the immediate-restore timing defect resolved.
- Exact later readbacks: source Scene still active/checksum unchanged; QA local view restored to source; clone 163 tiles/13 regions/two unchanged token poses; no controlled token; first-person false, GameCamera false and source 3D renderer inactive. Desktop foreground returned to pre-test window. No Meshy credits, no vendor/world/editor-code changes.

## Completion gates still outstanding
1. Native Core Surface fixture must return a non-null created Region ID, getSurfaces movement count >=1, and actual Core support height hit; then physically traverse multiple native 3D steps while that Surface is present, checking token elevation and genuine ground contact. The prior standalone Surface PASS is valid but does not complete integrated traversal.
2. D&D5e Falling is globally disabled, so legitimate fall/drop/damage/condition flow is NOT certified; do not change world rules without explicit scoped safety plan and user approval.
3. Existing native sliding-door pass is real but native mouse-click interaction is untested; hinge/rotation collision fails for the borrowed Door1.glb. This must be tested in a separate disposable fixture when needed.
4. Actual GameCamera black image cause and active camera wall/roof clipping remain unresolved; GM native FPS and free camera already render. Do not make GameCamera a blanket blocking requirement absent DM need.
5. Continuous, not rollback-per-step, multi-waypoint native traversal and cold reload/performance/camera behavior require a bounded, reversible fixture; current regression proves single-direction steps only.

Status classification: **technical regression saved, source/clone rollback accepted**, NOT whole-campaign, long-session, 3D physics or DM artistic acceptance. No user-facing stock image or fabricated asset evidence.

Prior validated evidence: docs/FOUNDRY_GM_SCREEN_NATIVE_DOOR_ACCEPTANCE_20261023.md, docs/FOUNDRY_NATIVE_WALL_BLOCK_AND_FPS_QA_PASS_20261023.md, docs/FOUNDRY_NATIVE_SURFACE_SUPPORT_PASS_20261023.md.
