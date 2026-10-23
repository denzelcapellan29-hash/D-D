# Foundry V14 native movement Surface: real QA support collision PASS
**Date:** 2026-10-23. **Classification:** ENGINEERING QA PASS (Foundry Surface API only). **NOT** a 3D Canvas real-time movement, D&D5e Falling, or DM visual acceptance.

## Strict layer ownership
- Foundry V14.368 Core: Region document `defineSurface` behavior, `Scene.getSurfaces({type:'move'})`, `Scene.testSurfaceCollision(from,to,{type:'move',mode:'closest'})`; native point fields are `x,y,elevation`, not Three.js `x,y,z`.
- 3D Canvas 9.0.36: Three.js GLB mesh and BVH raycast collision, 3D camera and renderer. It is **not proved** that 3D Canvas character movement automatically consults the Region movement Surface.
- D&D5e 6.0.5: Falling/conditions. Global `dnd5e.disableFalling=true` was observed and **not changed**, so Falling logic remains untested.
- First-party Acq bridge: typed region creation/deletion with expected revisions, GM-only view and read-only native inspection. It must **not** replace these native systems.

## Live fixture and provenance
- Source accepted Scene: `NUEDEFAULTSCENE0`, authoritative SHA `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f` throughout.
- Inactive GM-only QA clone `sW4aXZgKXj1cH0US`, baseline SHA `05134d2c6debeb2ffb49d17b3f1c06e96dfa409c35a348d801157dd815a03e94`, 163 Tiles / 13 Regions / two test Tokens.
- Before any write, checked browser bridge longpoll present, queues zero and a verified full QA Scene backup `QA_SCENE_PRE_SURFACE_FIXTURE_20261023.json` under private Google Drive folder `https://drive.google.com/drive/folders/1bfan6hyWbuWqi_kT89rB7GMRHiA-TTp1`. Backup byte count 295057, SHA256 `8956e5e8570145901d7469206a9db5ec59698ae66a7762848107d54022d8ce65`. Independently verified in Google Drive file ID `1mcTyOYaNWAdwwxxtd0FM7uFyNHLkFVTl`.
- Session after GM re-login: direct `Acq_3D_Map` discovery exposes 14 tools; Foundry_MCP 121; Blender/Godot connected. First-party browser script SHA256 `1d36a6e9aed966dec64e54811a8909317cd6b6be2b9fd906451f3ee4cd8c29ba` (guard for disabled native Game Camera plus corrected V14 Surface probe). GM local Scene switch to QA clone succeeded, players not pulled.
- Created temporary metadata-only QA Region `9WHadBS9YWSDdjN8` via `apply_semantic_objects`, semantic ID `qa:surface:monk-connector-20261023-retest`; rectangle x1807,y337,w26,h26; bottom/top elevation .125; enabled `defineSurface` with `system.placement='bottom'`, `move=true` (other sight/sound/light/occlusion/culling false), source GLB mesh unchanged.
- QA clone temporary SHA `f4be548ddd293fcaa70eec79ac613b0a14e927cd80179518b723539b91a7e83b`.
- Ran native GM-bound first-party read-only `inspect_native_floor_surfaces` through existing local bridge `/rpc`, **HTTP200, ok=true**. Foundry reported **1** movement Surface elevation **0.125**, associated with the temporary Region.
- Monk native `Scene.testSurfaceCollision` query from (x1820,y350, token elevation0.13) returned **support hit {x:1820,y:350,elevation:0.125}**, no error; Druid at (x2020,y635,elevation0) returned **null**, expected because temporary fixture did not cover the Druid.
- Thus **native Foundry movement Surface support is genuinely working** when configured, closing the diagnostic `z` vs `elevation` bug. `null` in the earlier QA had not established failure.
- Deleted the single temporary Region through its pinned semantic ID and expected temporary SHA. First-party `apply_semantic_objects` confirmed delete and QA clone SHA exactly reverted to `05134d2c6debeb2ffb49d17b3f1c06e96dfa409c35a348d801157dd815a03e94`. `manage_vision_qa_scene(action='restore_view')` returned GM to accepted source, source SHA unchanged and clone remained player-inactive. Independent GM-view and Scene count confirmed.
- Intermittent `inspect_3d_scene` on a **non-viewed** QA clone raised an MCP RuntimeException, while `manage_vision_qa_scene(action='inspect')` and source capability checks succeeded. Treat direct non-viewed-clone scene inspection as a separate bridge API limitation, not proof of clone mutation.

## Why this does and does not prove
**PASS**: Core Foundry V14 Region-defined Surface creation/discovery, height-aware closest movement collision for Monk, negative control for Druid, temporary metadata fixture cleanup/GM restore, accepted source unchanged, no visible geometry generation.
**NOT YET PASS**: Token locomotion by human/native controls, stop at BVH wall, opening native GLTF door, 3D Canvas and Foundry Surface integration during walking, D&D5e Falling while feature disabled, Game Camera visual QA (earlier black output), non-GM fog/vision and cold-load/performance.

## Next technically honest acceptance gate
Use an approved/source-proven GLB asset and QA-clone native Tile/Token controls, prove controlled character moves and is physically blocked by real 3D walls; inspect stable elevation before/during/after movement and player eye view. Validate Foundry native Regions support separately. Do not teleport TokenDocument and call that real movement, disable walls, change global Falling or introduce custom gravity. For Game Camera, first-party native world+Scene enablement guard is installed; world `enableGameCamera=false`, so avoid unsafe low-level toggle. Session end must restore GM view and source/checksum, and document both false positives and successful samples.
