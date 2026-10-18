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