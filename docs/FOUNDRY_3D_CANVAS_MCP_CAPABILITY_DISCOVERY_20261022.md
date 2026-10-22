# 3D Canvas MCP: capability discovery and bridge parity audit
Date: 2026-10-22
Status: CODE STAGED ON FEATURE BRANCH; NOT DEPLOYED; NOT DM ACCEPTED

## Authority and scope
This is a diagnostic and developer bridge milestone, not a change to primary 3D production. Latest DM decision: Godot is the primary 3D runtime; Foundry handles VTT mechanics. Preserve historical Foundry 3D Canvas environment and Area 8 161-tile visual checkpoint. No arbitrary eval, no vendor code modification, no scene writes.

## Verified live baseline BEFORE edits
- Foundry 14.368 / dnd5e 6.0.5 connected, 3D Canvas available and active.
- Scene `NUEDEFAULTSCENE0` active, 161 3D tiles, six lights, thirteen regions. Existing scene revision `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f` at discovery; these are source-backed inspection results, not release guarantees.
- `mcp__Acq_3D_Map__inspect_3d_scene` successful. `search_3d_assets` works with default roots; a custom root `["modules"]` failed (root validation likely).
- The currently connected MCP advertises SEVEN tools. Repo `integrations/foundry-bridge/agent/mcp_server.py` has TEN declared MCP tools on main (including reload_3d_scene, resize_scene, delete_semantic_objects). This indicates installed-server or exposed-tool-surface drift; DO NOT presume GitHub source equals the live agent.
- Blender MCP returned `UNAVAILABLE` on probe; Godot MCP editor connected. No Blender/Godot authoring changes.

## Authoritative source and API study
Published 3D Canvas version 9.0.36 exists in `theripper93/levels-3d-preview` (2026-10-16 release).
Important implementation paths:
- `scripts/main.js`: `game.Levels3DPreview`, `game.canvas3D` and `toggleFirstPerson()`.
- `scripts/handlers/GameCamera.js`: `GameCamera.toggle()`, `toggleTopDown()`, `getY()`, settings and camera collisions.
- `scripts/apps/buildPanel.js`: actual game camera, lock, fog, wireframe and performance buttons.
- `scripts/apps/assetBrowser.js`: 3D asset placement, orientation, scattering and normal alignment.
- `scripts/settings/config.js`: registered Scene and Tile 3D flags.

These names are from upstream public source, not yet matched to the installed module version. The installed version is not accessible in the old inspector; discovering it is the first purpose of the new operation.

## Implemented: read-only `inspect_3d_capabilities`
- Client-side Foundry bridge dispatcher: reports approved module IDs/versions, runtime readiness, selected token representation, Game Camera/first-person states, 12 allowlisted settings and boolean method availability.
- Python MCP wrapper forwards the command through existing synchronous loopback RPC; preserves active-scene guard and GM authorization.
- No arbitrary JavaScript execution, unrestricted settings reads, arbitrary filesystem access, camera toggling, or persistent writes.
- Updated protocol/tool surface and standalone Node contract test on this feature branch.
- Explicit behavior limitation: method presence is not proof that behavior works, and a different installed 3D Canvas version may expose different shapes.

## Tests and QA
- Successful independent V8 syntax compile of the full updated bridge source.
- Successful V8 stub-runtime smoke test covering the method matrix and fixed camera settings. No writes invoked.
- GitHub Actions workflow updated to run Node contract tests, but GitHub smoke runs on the feature branch fail within roughly two seconds and return zero job steps/logs; the hosted test is **UNVERIFIED**, not green.
- Python source change is a small typed MCP decorator forwarding the existing RPC helper; independent CI/import test still outstanding.

## Deployment and regression gates
1. Preserve working client bridge, Python MCP server, first-party module config and last safe scene; do not run `install_windows.ps1` blindly because it performs overwrite copies without versioned backup.
2. Independently inspect local installed module versions and bridge/agent hashes. Establish whether the 7-vs-10 registered-tool mismatch is installation drift or tunnel schema caching.
3. Create timestamped backup of first-party installed `acq-foundry-bridge` and running agent/MCP code; never alter `levels-3d-preview` vendor source.
4. Deploy first-party update to disposable/non-playing development client and restart only the necessary MCP/Foundry components.
5. Verify newly exposed tool listing, call `inspect_3d_capabilities`, compare exact Scene revision before/after, check 161 Tile objects unchanged and zero new Foundry error logs.
6. Exercise native first-person and Game Camera transitions on disposable QA tokens using screenshot/collision checks. ONLY THEN design write controls with revision/dry-run/recovery contract.
7. If load/connection regression: one verified rollback to backup, stop and report.

## Next independent milestone
Complete installed-code version discovery and camera-controller fixture (GM selected token, native first-person toggle, exit/restore, Game Camera lock/free modes, collision/eye-height). Create a separate controlled endpoint only after baseline proves it safe.

## 2026-10-22 live Windows preflight and additive upgrade preparation

The **already-running Windows v0.1 development agent** successfully processed fresh GitHub diagnostic requests through the default branch:
- `automation/results/health-20261022-mcp-upgrade.json`: ports 18747, 18748 and 8083 listening; installed `acq-foundry-bridge`, `levels-3d-preview`, `canvas3dcompendium`, `canvas3d-premium`.
- `automation/results/bridge-hash-20261022-mcp-upgrade.json`: installed client JS 37,532 bytes, SHA256 `842e858751b50d765ac86c90665c29eaa59fd15b7562339fc2c67658615fa951`.
- `automation/results/bridge-installed-read-20261022-mcp.json`: after line-normalized diff the installed JS matches repository main **except for the extra first line** `import "./fps-camera-anchor.mjs";`.
- `automation/results/bridge-fps-anchor-20261022-mcp.json`: installed 1,400-byte runtime-only FPS camera control stabilization source was recovered/verified as first-party. It has been committed to the feature branch and restored to the JS entrypoint. It remains part of the active installation; do not remove it.
- `automation/results/bridge-installed-manifest-20261022-mcp.json`: installed bridge version 0.2.8.

**Important operational blocker:** This proved the Windows diagnostic agent is running, but v0.1 supports only allowlisted read-only diagnostics. It does NOT provide guarded deployment, process restarts or arbitrary filesystem writes. No accessible MCP can safely replace the installed bridge/Python service. DO NOT claim deployment completed or improvise via Godot/Blender script execution or modify the third-party 3D Canvas module.

**Prepared guarded installer:** `integrations/foundry-bridge/upgrade_capability_discovery.ps1` (PowerShell, dry-run default, `-Apply` for guarded backup and first-party file replacement), with hard gate on the exact installed SHA, 0.2.8 manifest, original FPS anchor match, running Python MCP source discovery, and module/scene isolation. Python MCP modification is additive rather than overwriting unknown installed tools. Versioned backup and post-write integrity records are created under `%LOCALAPPDATA%\AcqBridgeBackups`. `rollback_capability_discovery.ps1` can restore the recorded original versions after integrity preflight.

**Current install status:** files STAGED IN GITHUB; NOT installed on Windows; no restart/refresh; new tool not yet live. The installer has not been run on Windows or verified with PowerShell parser/CI. Perform its dry run and correct any compatibility issues before its `-Apply` mode; then restart the MCP process and refresh the GM client when gameplay is idle. Tool discovery may require tunnel reconnection.

**Local user action when ready:** obtain feature branch files on the Windows PC, launch an ordinary PowerShell in the `integrations/foundry-bridge` folder, run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\upgrade_capability_discovery.ps1` for dry run and then with `-Apply` only after it reports **PRECHECK PASS**. If running MCP process detection cannot resolve the path, provide `-McpServerPath "C:\path\to\mcp_server.py"` explicitly. No user world edits are part of this installer. The assistant can then verify the new tool, active scene revision and physical camera APIs.

