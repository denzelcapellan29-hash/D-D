# Native Foundry + 3D Canvas gameplay QA — 2026-10-23
**Status: GM-only QA clone, PARTIAL PASS; Game Camera BLACK visual FAIL; floor/falling and physical traversal NOT CERTIFIED.**

## Why / exact scope
Follow-on to `docs/FOUNDRY_3D_CANVAS_LONGPOLL_MILESTONE_20261023.md`. Direct ChatGPT Acq_3D_Map 14-tool MCP + Foundry_MCP and first-party bridge used. Native Foundry V14.368/D&D5e6.0.5/3D Canvas9.0.36/Premium9.0.3. No vendor code patches, user world setting toggles, geometry generation, Meshy spend or accepted-source edits. Only existing inactive, GM-only Area8 QA Scene `sW4aXZgKXj1cH0US` was locally viewed; players were not pulled and accepted source `NUEDEFAULTSCENE0` stayed active. Original source SHA **`e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`** unchanged throughout.

## Exact test sequence & verified results
1. MCP discovery FIRST: Blender and Godot connections healthy; Foundry_MCP **121** tools; Acq_3D_Map **14**, native longpoll connection working. Source scene originally 3D runtime inactive.
2. Verified QA clone content via Foundry read-only: **163 Tiles, 36 Walls, 13 Regions, 6 Lights, 2 QA Tokens**, clone initially SHA `05134d2c6debeb2ffb49d17b3f1c06e96dfa409c35a348d801157dd815a03e94`. The source had 162 Tiles; the extra QA Tile is the source-derived GLB fixture. `manage_vision_qa_scene(action=view,dry_run=false)` **PASS** GM local view, active player Scene unchanged.
3. Determined native engine activation button from installed 3D Canvas `scripts/settings/config.js`: `getSceneControlButtons` tokens tool `preview3d` with native callback `game.Levels3DPreview.toggle()`. Safely clicked the Foundry UI control **once**, no programmatic replacement renderer. Runtime transitioned `active=true, ready=false, loading_count=163`, then `active=true,ready=true,loading_count=0`; environment/lights initialized. Readiness `finalizing=true` remained reported by native status, so this is a caveat. No crash.
4. Real Three.js renderer capture **PASS**: player/hero perspective shows 3D walls, pipes, central pool, creature object, ceiling and glossy sewage; placeholder 2D token face looked simplistic and full model art not accepted. Capture dimensions **1902 × 973**. Original clone revision unchanged.
5. `inspect_3d_native_workflows` when active/ready verified installed native UI actions: Props, Environment, Terrain, Materials, RoomBuilder, Effects and Cutscenes **registered=true/callable=true**. Registration is not actual operations test of each panel.
6. Two QA Token IDs from installed native inspector: Monk `iSbK8OUBuUEjIGGu`, Druid `KB7cUY9hXEXHeJqV`. Token selection dry run and actual native `Token.control` **PASS**; no TokenDocument write.
7. `set_native_camera_mode` native **first_person** dry-run and actual **PASS**, owned session `acq-camera-mvl29enf`; `first_person=true`, token head height camera `(1.82,0.113,0.350)`, actual 1902x973 renderer capture **PASS**. FPS camera restored via session ID and reported `first_person=false`.
8. One bounded native ArrowUp keyboard press in Foundry while QA monk selected and first person active. Read-only native token coordinates remained **x1.82,z0.35** afterwards. **NO MOVEMENT CERTIFICATION**; this does NOT prove obstruction or stability. Input may have been intercepted by native/core keybindings rather than 3D character traversal.
9. `set_native_camera_mode` **game_camera** actual ephemeral toggle **PASS** (GameCamera enabled, owned session `acq-camera-mvl2eb06`), **BUT live renderer capture was nearly black** with a thin strip of masonry. **GAME CAMERA VISUAL FAIL**; stop iterative camera tests per skill. Initial camera around (1.82,0.254,0.208), target (1.82,0.113,0.35). Hypotheses: occluding geometry at camera position, clipping or a camera pose close to roof/wall; **not proven**. Global settings have `enableGameCamera=false` and `gameCameraClipping=false`; do not silently flip these to claim success.
10. Existing first-party **read-only** operations `inspect_native_playability` and `inspect_native_floor_surfaces` were invoked via guarded Bridge loopback `/rpc` on GM-viewed QA clone, one batched call HTTP200; no writes:
   - Native Three/BVH collision groups: **move=7, sight=9, camera=4**.
   - Monk downward `move` hits roof at y0.280568 and approved connector at y0.012514; Druid downward hit around y0.0; sampled north wall move/sight/camera rays all hit near z0.167. True native BVH intersection **PASS** in sample, not real token movement/physical support pass.
   - CameraCollision explicitly true on **13**/163 QA Tiles; missing/unset flags are not proof of universal camera clipping.
   - Native Foundry V14 `Scene.getSurfaces({type:'move'})` returned **0** and `testSurfaceCollision` returned **null** for BOTH tokens; separate from GLB collisions.
   - `dnd5e.disableFalling=true`, so empty actor Falling statuses **masked/not meaningful**. Do not build new gravity or change global D&D5e without explicit decision.
   - Source QA sight angle=270 degrees for monk and druid (prior QA settings), vision source count in GM view initially 0; player fog and 3D sight cones **NOT CERTIFIED**.
11. Native Game Camera restored through owned session successfully. First selection restore returned transient bridge error `QA pose restoration did not persist: rotation` (strict immediate readback). Independent QA clone readback subsequently showed original revision `05134d2c...` and original monk rotation `333.3798438225904`; one verified cleanup repeat restored selection successfully with **no remaining fields changed** and no selected tokens. Thus **first-party bridge readback timing defect** remains a follow-up issue; do NOT treat it as an unresolved dirty scene.
12. `manage_vision_qa_scene(action=restore_view,dry_run=false)` **PASS**; independent `inspect_3d_capabilities` and Foundry Scene list confirmed original source viewed+active, 3D renderer inactive again, first-person and GameCamera both false, selected tokens empty, source SHA unchanged. QA clone inactive and SHA restored to `05134d2c6debeb2ffb49d17b3f1c06e96dfa409c35a348d801157dd815a03e94`.

## Evidence provenance — private Google Drive
Actual three renderer captures were retained by first-party Bridge `/results` and decoded byte-for-byte (original WebP files, no generated/staged artwork) into Drive Desktop mirror:
`G:\My Drive\D&D\Review Bundles\Foundry_3D_Canvas_Native_QA_20261023\`
- `01_qa_initial_native_render.webp`, 124284 bytes, SHA `cc1f96550da29cc60a5f5e69ef6127f7c7da7fbb04bb17c9d561347d160588ab`
- `02_qa_monk_first_person.webp`, 122034 bytes, SHA `c1ccced8626891abd3fb3902e43626966ac32e1b6f554e63e1447f18d5a56ba2`
- `03_qa_game_camera_BLACK_FAILURE.webp`, 12362 bytes, SHA `b202fcf247c5394d4eb643c4cd54731ceedc90569475f2a593e871ea5d4f0d45`
- `QA_EVIDENCE_MANIFEST.json`, local checksum `cba43abdde760cb8e7fa248e4d5e5a7be96817540bab11244c994393ceb3eccf`
- INDEPENDENT Google Drive tool `search` verified folder and `list_folder` verified all four files, exact names and byte sizes. Folder link: `https://drive.google.com/drive/folders/1bfan6hyWbuWqi_kT89rB7GMRHiA-TTp1`; not shared/public. User review captures are real 3D Canvas renderer results, not stock images.

## Acceptance status
- **PASS:** complete 3D Canvas renderer launch, load and live renderer capture in QA-only clone; native FPS toggle and real first-person image; native 3D GameCamera toggle; registered native editor UI actions; sampled true mesh raycast collisions; selected QA token and restored; source/clone scene safety; longpoll transport under larger scene load.
- **FAIL:** GameCamera **black render** from specific pose; immediate strict QA token-rotation readback (eventual consistency, cleanup later PASS).
- **UNVERIFIED:** 3D token movement or collision-blocked traversal, floor Surfaces / Falling behavior, player fog/vision cones, door mechanics, actual GameCamera collision/clipping, 3D scene FPS performance, visual art acceptance.

## Next safe engineering step
1. **STOP any more UI GameCamera rendering attempts until cause analyzed off-scene.** Inspect native GameCamera camera ray/near-plane setup, scene roof/wall proximity and current world setting `gameCameraClipping=false` **read-only**; propose reversible QA-only test architecture (no global setting change affecting campaign).
2. Refine first-party `native_select_qa_token.restore` to wait on native Foundry Document update + tolerant angular normalization, with bounded retry/rollback **on a branch and isolated fixtures** before any live deployment. Do not patch vendor 3D Canvas.
3. For actual playability, construct a SMALL *source/approved-GLB fixture* QA clone with correctly authored native Foundry V14 Surface metadata instead of touching accepted Area8 or inventing GLB floors. Test walking, doorway and genuinely valid Falling, independent from default disabled Falling. Separate native engine mesh BVH from Foundry's Surface model.
4. Capture multiple player-eye/overhead/collision-approach screenshots and inspect black/stale render regression; DM final visual approval required.

**Saved QA-only technical milestone, not DM acceptance.**
