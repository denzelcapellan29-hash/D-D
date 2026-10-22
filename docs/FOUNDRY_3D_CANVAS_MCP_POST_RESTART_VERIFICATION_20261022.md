# 3D Canvas MCP post-restart verification, 2026-10-22
Status: FILE DEPLOYMENT VERIFIED; OLD INSPECTOR RECOVERED; NATIVE 3D RUNTIME INACTIVE; NEW TOOL REGISTRY NOT REFRESHED. DO NOT MARK LIVE CAPABILITY MILESTONE COMPLETE.

## User report
DM: "restarted" after first-party guarded Acq 3D bridge JS/Python MCP deployment. They previously activated v0.3 Windows watcher and the staged deployment report `automation/deploy_results/deploy-3d-capability-apply-20261022.json` confirmed backup `capability-20261022T135404.612515Z` and safe first-party updates.

## Verified current state
- Discovered tool registry `mcp__Acq_3D_Map__` still exposes **seven tools**: `inspect_3d_scene`, `search_3d_assets`, `set_3d_camera`, `capture_3d_view`, `set_3d_environment`, `apply_semantic_objects`, `validate_scene_manifest`. The new `inspect_3d_capabilities` endpoint remains absent in THIS ChatGPT conversation's advertised tool metadata. Do not infer Python upgrade reverted; connector schema may be cached, or running service may still expose old tools.
- After restart, `inspect_3d_scene` NOW succeeds again, returning `levels3d_available:true` but `levels3d_active:false`. Active Foundry Scene `NUEDEFAULTSCENE0` has 161 3D tiles, 6 lights, 13 regions; before and after revision identical `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`. Thus main persisted Scene is unchanged.
- Native Foundry MCP `world_info` and `scene_get` independently succeed, including 162 Scene Tiles total, 36 wall segments, 2 QA tokens, 13 regions. This is normal semantic Scene health, not proof that renderer works.
- `capture_3d_view({scene_id:'NUEDEFAULTSCENE0',format:'webp',quality:.6,restore_camera:true})` reported generic `Error executing tool capture_3d_view` while 3D active=false. `search_3d_assets({query:'wall',limit:3,max_depth:3,scene_id:'NUEDEFAULTSCENE0'})` also returned generic `Error executing tool search_3d_assets`. DO NOT CLAIM these are definitely caused by the inactive 3D toggle: asset search may fail independently and no detailed error propagated.
- Previously checked Blender MCP is now connected, but its active filepath is blank and scene dirty. No edits to Blender. Godot editor also remains connected, unchanged.

## Safety disposition
No new 3D Canvas Document writes, no camera setting changes, no procedural geometry, no mesh imports, no service restarts commanded by assistant. Do not repeatedly force `capture_3d_view` or try restart loops. Live source scene preserved.

## Next required narrow checks
1. DM turns on **3D Canvas mode** (the 3D Canvas module toggle in Foundry GM client), ensuring actual 3D geometry loads. This is separate from enabling Game Camera/first-person.
2. Refresh/reconnect custom Acq 3D MCP connector in ChatGPT Settings > Plugins or reopen the connection to obtain a fresh tools/list. If ChatGPT tool list remains cached in this conversation, a new conversation may be required to discover new tools. Do not uninstall 3D Canvas or delete the bridge.
3. Re-run one read-only 3D inspector on active scene; verify `levels3d_active:true`, 161 loaded Tiles, no black/stale render, and revision unchanged.
4. Confirm new `inspect_3d_capabilities` exists in tool list, then invoke and inspect actual installed module version and native APIs. Only after that develop or deploy controlled camera + Asset Browser adapters. If generic errors persist after activation/reconnection, investigate GM client console and bridge agent logs rather than changing Scenes.
5. If 3D Canvas activation produces unexpected load/corruption, stop and use exact backup `capability-20261022T135404.612515Z` through guarded rollback mechanism.

Godot remains primary runtime pending fair 3D Canvas parity benchmark; no art acceptances implied.
