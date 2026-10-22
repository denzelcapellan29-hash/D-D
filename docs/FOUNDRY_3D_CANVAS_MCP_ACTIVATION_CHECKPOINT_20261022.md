# Acq 3D Canvas MCP activation — verified 2026-10-22 09:55 EDT

**Status: FIRST-PARTY FILES STAGED; POST-RESTART RUNTIME UNVERIFIED. Do not call this an installed active MCP tool yet.**

## User action and worker
DM reported Windows bootstrap `ready`. New v0.3 guarded deployment watcher actually processed request and returned a passing preflight:
`automation/deploy_results/deploy-3d-capability-preflight-20261022.json`. This verified installed first-party baseline and candidate source commit `e003dc9b26c6c29e6489b55c58e495fc20e5980b` before writing.

Assistant then submitted one allowed `dry_run:false` job:
`automation/deploy_requests/deploy-3d-capability-apply-20261022.json`.

Worker confirmed successful staging in `automation/deploy_results/deploy-3d-capability-apply-20261022.json`:
- `ok:true`, `status:"staged_pending_service_restart"`, `scene_changed:false`, `requires_manual_restart:true`, `requires_gm_client_refresh:true`.
- First-party installed bridge JS prior SHA256 `842e858751b50d765ac86c90665c29eaa59fd15b7562339fc2c67658615fa951`; staged SHA256 `0129dbefea404c56fb7d5206355f4f896fe26e30820fc824e8a38c305aed3ad9`.
- Python MCP server prior SHA256 `d9c9b8e436110099cc010847ce658abbaaecc0532627c262f179cb5ca8e41b41`; staged SHA256 `16747c98e5a7ff1fc8e58be48f507ab8cc089b9ca4c3f92ce129ebc14bf7c55d`.
- Worker-created backup ID `capability-20261022T135404.612515Z`. Preserve backup. Audit GitHub commit `53471ddfbc433dc4f21cf8d867a58392e5e3cc92`.
- Separate v0.1 Windows diagnostic agent successfully re-read staged installed JS, **40,874 bytes, exact matching SHA256** `0129dbefea404c56fb7d5206355f4f896fe26e30820fc824e8a38c305aed3ad9`. It also confirmed ports 8083, 18747 and 18748 listening and installed 3D Canvas, Premium, Mapmaking Pack and Acq bridge modules.

## Runtime regression / no-touch
Before deployment, live scene `NUEDEFAULTSCENE0` returned 161 3D tiles, six lights, 13 regions; exact revision `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`, unchanged across operation. After file staging, original seven-tool 3D MCP inspector returned generic `Error executing tool inspect_3d_scene` twice (first check + one confirmation). This failure is NOT evidence of Scene corruption: Windows port tests and static file hashes continue to work. The GM poller or old-service runtime may be stale. Per safety policy stop repeated runtime calls; do NOT modify Scenes or 3D vendor source as a workaround. Root cause not yet verified.

The exposed Acq 3D MCP tool registry still shows only seven tools, so the new `inspect_3d_capabilities` cannot yet be called. The just-staged code requires an explicit restart of the local Python 3D MCP service and refresh of the existing GM Foundry client to execute newly loaded JS. A listening port alone does not mean the process reloaded its source.

## Next narrow action and release criteria
- When no live players are active, restart **only** the first-party Acq 3D MCP stack using its existing local launcher (`run_acq_3d_stack.cmd` / `run_acq_3d_stack.ps1` as applicable) after terminating the old stack. Refresh active GM client once (F5). Do not reinstall 3D Canvas, reset scenes, touch Meshy assets, or restart all Foundry infrastructure.
- Reconnect/refresh ChatGPT custom MCP connector if tool schema remains cached. Then inspect `inspect_3d_capabilities`, `inspect_3d_scene`, original first-person anchor behavior, Scene revision, loaded Tiles and capture.
- If restarted runtime still fails, pause and use the verified backup `capability-20261022T135404.612515Z` for guarded rollback; do not keep changing settings. The v0.3 worker does NOT implement process control or arbitrary shell commands; do not claim remote restart is available.
- The new runtime tool is code-staged only, **NOT end-to-end accepted**. Godot is still primary until 3D Canvas is fully evaluated with art/traversal/performance QA.

## Provenance
Feature branch: `feature/3d-canvas-capability-discovery-20261022`, draft PR https://github.com/denzelcapellan29-hash/D-D/pull/1 .
