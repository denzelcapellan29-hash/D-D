# Area 8 live restoration — offline backup and Foundry restart, 2026-10-18

Status: **cold world backup verified, Foundry world relaunched, GM login required; actual 3D renderer NOT yet verified working**. Do not claim restored Area8.

## DM authorization and safe baseline
- User requested attempt at last-known-good Area8 recovery now that Blender MCP was reconnected. Hourly Episode2 and Area8 automations remain disabled.
- Blender MCP get_blendfile_summary_path_info PASS, open clean saved `Episode2_HighRoad_WetBank_IsolatedQA_v010.blend` 270945686 bytes. Blender itself not edited.
- Foundry world initial original/default Scene `NUEDEFAULTSCENE0` active, Test inactive.
- Source authoritative last good **Oct 16, 2026 ~23:15 EDT Area8 first-person actual screenshot PASS** under the ALREADY patched native 3D Canvas `main.js` and `handlers/GameCamera.js`. Native code was untouched during these restarts; vendor original patch rollback would NOT reproduce last-good state.

## Verified pre-change backups
- Using newly connected Blender local file access, copied and independently SHA256 verified seven items: current 3D Canvas main.js, GameCamera.js, vendor originals, Acq Foundry Bridge main/anchor, and world.json. Recovery local folder under `%LOCALAPPDATA%/FoundryVTT/AcqRecoveryBackups/Area8_PreRecovery_20261018T152210/`.
- Initial world hot zip was explicitly labeled **NOT CERTIFIED** because the world was running.
- Gracefully shut down desktop app via normal Windows WM_CLOSE, verified **zero Foundry processes**, then created complete `Foundry_World_OFFLINE_VERIFIED` LevelDB directory copy. 106 files, 3,564,332 bytes; source/destination SHA256 readback matched for EVERY file. Manifest `world_offline_manifest.json` saved alongside. This is offline consistent at file-copy time, unlike hot zip. Did not replace any world file.

## Restart sequence
- First clean normal Foundry executable launch (no flags) returned to setup rather than joining world, so Foundry API Bridge MCP disconnected.
- Foundry documentation confirms supported `--world=<worldId>` startup option on Electron. Second graceful shutdown of setup instance and clean relaunch with `--world=acquisitions-incorporated` succeeded; process command-line verified and Foundry log reports World Launch 100%, server started port 30000, local GET title `Acquisitions Incorporated` HTTP 200.
- Captured actual local Foundry desktop join page through Windows screenshot. Only visible account was Gamemaster. Selected Gamemaster and made ONE normal attempt to join with blank password; UI displayed exact `Invalid password provided for Gamemaster!`. No password guesses, overrides, account edits, reset flags, API bypass, or credentials shared. **User needs to enter their own GM password locally**, not in chat; specialized 3D bridge cannot reconnect until an active GM client exists.
- Latest 3D Canvas `capture_3d_view` post-restart FAIL was while no GM was signed in; not evidence client render still broken after GM login. Do not claim success or failure post-authentication until actually inspected.

## Non-actions / pending gates
- NO native 3D Canvas script rollback, GLB/Area8 semantic tile change, Blender save, material repair, world backup restoration, Test deletion, or Meshy credit use. Verified original Area8 scene documents intact pre-restart.
- User instructed to join Gamemaster in reopened Foundry app directly. Do NOT request password in chat.
- After GM joins, immediately `world_info`, `scene_list`, `inspect_3d_scene` and actual `capture_3d_view` from Area8 with pixels; then true first-person camera movement/free-look QA. Keep or revert any subsequent native module recovery based on actual screenshot, preserving cold backup and Oct16 approved setup.

## Supplemental 2026-10-18 19:xx ET: GM joined; actual Area8 screenshot FAIL and reverted untested A/B
- DM signed in through normal private GM join; Foundry_MCP world_info and scene_list reconnected. Original Area8 scene active, Test inactive. Acq_3D_Map inspector returned `levels3d_active:false` and 161 scene 3D Tile model records; true `capture_3d_view` failed with RuntimeException.
- Independent actual Windows desktop PNG screenshot captured through connected Blender/PowerShell after foregrounding Foundry: actual Area8 dark viewport with permanent `Loading 3D Canvas...` modal (not successful 3D frame); game paused. This is a real visual FAILURE after GM login and proper world launch, so restart-alone remedy disproved.
- **One** reversible native-script A/B preflight: previously backed-up patched `main.js` SHA256 `6abf61e2bc0b40203a989bf8bc0ac1918f63cea41f4ecae2abc2bfea1615817f` and `handlers/GameCamera.js` SHA `5930e69cbc302a655662ada5febfc594183c082e8ab1e4ff25882d0a8667b2f8`, confirmed unmodified; vendor backup originals verified SHA `60cab83f15d1b84f986826807826cf8ff9d4e3f82c4edebb4052c0ff6531b52e` and `0d639c35f2305c9f2a99440d8de3368198c9bb8acbabeb99bd682e3250e1b9eb`. They were atomically staged as a hypothetical vanilla comparison. **The automated F5 reload was blocked by OpenAI safety checks. No new render was performed with the vendor files**, so do not claim comparison result. Both live native scripts were then immediately **restored from independent hash-verified saved copies of the Oct16 visually working patched config**, checked again byte-for-byte: hashes `6abf61e2bc0b40203a989bf8bc0ac1918f63cea41f4ecae2abc2bfea1615817f` and `5930e69cbc302a655662ada5febfc594183c082e8ab1e4ff25882d0a8667b2f8`. Blender .blend remained clean, Foundry world and Area8 data unchanged. The vendor vs patched comparison remains UNTESTED, not pass/fail.
- Recovery checkpoint path remains `%LOCALAPPDATA%\\FoundryVTT\\AcqRecoveryBackups\\Area8_PreRecovery_20261018T152210\\`; full offline world 106 hash-matched files; private local only. Hourly automations disabled. Next valid next-step requires GM to manually press F5 during a carefully staged test, or an explicitly authorized supported client reload, and direct visible result. No bypass of blocked programmatic UI action, no credentials stored.
