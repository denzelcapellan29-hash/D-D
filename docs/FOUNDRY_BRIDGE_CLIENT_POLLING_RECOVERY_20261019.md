# Verified Foundry Acq Bridge / 3D Canvas capture recovery — 2026-10-19

## Symptom and scope
Foundry 14 / dnd5e 6.0.5 world `acquisitions-incorporated`, High Road scene `GEtOJxYA6Lwe7NG5`. Foundry's world-level commands, Tile writes, desktop client and the local Python bridge service still worked. `mcp__Acq_3D_Map__inspect_3d_scene` and `capture_3d_view` intermittently threw generic execution errors. This was NOT sufficient evidence of 3D Canvas or GLB corruption.

## Diagnosis (verified)
- Installed Acq Foundry Bridge code `scripts/acq-foundry-bridge.js` calls `startPolling()` after Foundry `Hooks.once("ready")` on the **active GM client**, conditional on `game.user?.isGM` and client `enabled` setting. `pollCommand()` reads `GET http://127.0.0.1:18747/bridge/next` and reports `/bridge/result`.
- Local Python `acq_bridge_agent.py` service was running; `GET /health` returned HTTP 200. A read-only `POST /rpc` ping timed out with HTTP 504, so agent healthy but no GM client polling.
- `G:\My Drive\D&D\Foundry Bridge\state\agent_status.json` `updated_at` was stale for over 7 minutes. This file's status string `connected` is NOT real-time proof of a live poller; compare timestamp.
- The agent scans `commands/*.json`, not `commands/pending/*.json`. Earlier diagnostic mistakenly placed a command in `commands/pending` and was not a valid test. Prefer `/rpc` health diagnostic.
- Foundry desktop Electron application window remained visible and showed High Road; a new Chrome `/game` session redirected to `/join` with 1/1 player seats occupied. Do NOT displace the active GM session or guess credentials.
- Simple WScript `AppActivate` and PostMessage F5 failed because foreground was Chrome, not the Foundry HWND. Foreground verification is mandatory before keyboard input.

## Recovery (performed and verified)
1. Preserve existing 32-Tile High Road scene, no vendor/module edits.
2. Find the Foundry Electron HWND using Win32 EnumWindows; actual target on this session 1573750 (not reusable).
3. Temporarily attach foreground and target window input threads using user32 `AttachThreadInput`; `ShowWindow(SW_RESTORE)`, `BringWindowToTop`, `SetForegroundWindow`; assert `GetForegroundWindow() == target HWND`.
4. Send one Windows F5 key press to confirmed foreground Foundry Electron client, not Chrome.
5. Verify fresh bridge agent status timestamp (changed from 20:30:23Z to 20:42:32Z); `inspect_3d_scene` returns OK; `capture_3d_view` produces actual WebP and `runtime_recovery.after.loading_count == 0`.
6. Confirm scene 32 tiles before building further. No server/module reinstall, no paid Meshy, no source file change.

This is a single empirically verified client-reconnect fix, not blanket permission to control user windows during play. Only perform when authorized, not during session safety lock. If a fresh F5 fails, stop and report; do not loop restarts.

## Additional current High Road art status
A no-credit actual 3D source-library terrain derivative `EP2_HighRoad_LibraryTerrain_v001_MapDrape.glb` (3,200 triangles) was staged with 4 x 3 x 0.12 Foundry runtime bounding size. It supports real topographic geometry and 3D camera capture but the detailed vegetation/water remains primarily image-projected, not physically modeled. Visually review as **experimental**, not a complete 3D environment or DM accepted. A visually mismatched Willow_Autumn_1 stock tree was rejected and its QA Tile deleted. NPC actors Thetsis (Lizardfolk SRD), Rasqel (Bandit SRD proxy), Jutt and Meff (Bugbear SRD) created in Foundry and token placement verified; source-specific stats not independently validated. Keep official source vs dramatic design separate.

## Reusable principle
For a working HTTP agent with `/rpc` timeout, test the **active GM client poller** and `agent_status.updated_at` before debugging WebGL capture code, reinstalling 3D Canvas, or modifying GLBs. Runtime screenshots still require direct 3D Canvas capture and actual visual inspection.
