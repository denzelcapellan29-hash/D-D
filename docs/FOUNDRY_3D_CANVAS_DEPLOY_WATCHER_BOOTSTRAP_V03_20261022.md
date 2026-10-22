# Guarded Acq 3D Canvas deployment watcher v0.3 — 2026-10-22
Status: SOURCE BUNDLE CREATED AND TESTED IN CHAT; WINDOWS BOOTSTRAP NOT INSTALLED.

## Why
The current Windows diagnostic agent was verified live on 2026-10-22, but grants only read-only diagnostics. The existing custom 3D MCP advertises seven tools. The already-staged read-only capability discovery tool is not activated until two first-party runtime files (Foundry bridge JS, Python MCP server) are updated safely.

## Deliverables
User-facing conversation attachment: `Acq_3D_Canvas_Guarded_Bootstrap_v0.3.zip`, 13,685 bytes, SHA256 `2e9409e62368a8a95c2f3c3b5852eb950c9ebcb90899929200bca01e07d51cb2`.

ZIP contains first-party `acq_bridge_deployer.py`, `acq_deploy_watcher.py`, `install_deploy_watcher.ps1`, README, SHA256SUMS, two unittest modules. The ZIP is a **conversation attachment**, not a file in GitHub or independently Drive-hosted. Do not assert a downloadable GitHub binary link until separately uploaded.

The worker deliberately uses a separate queue `automation/deploy_requests/` and separate dedicated git clone from old read-only agent's `automation/requests/` diagnostics. It does not overwrite the old diagnostic agent or execute arbitrary shell commands from jobs.

Existing `feature/3d-canvas-capability-discovery-20261022` branch remains draft PR #1: native runtime discovery and first-person stabilization preservation. The new worker accepts exactly `deploy_3d_capabilities` on `feature/3d-canvas-*` branches, with explicit `dry_run` boolean, exact installed bridge SHA and version gate, and a locally opted in `--allow-deploy` flag before any file staging. It copies only first-party Acq bridge JS and additively patches the Python MCP server; protects original `fps-camera-anchor.mjs`, does not edit vendor 3D Canvas or scene objects.

## Live baseline
Foundry 14.368 / D&D5e 6.0.5, bridge module 0.2.8; exact installed JS SHA256 `842e858751b50d765ac86c90665c29eaa59fd15b7562339fc2c67658615fa951`. Existing Area8 161 3D tiles, six lights, 13 regions; last verified revision `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`. The installed first-party FPS anchor source was recovered; its import is preserved in the feature branch.

## Staged diagnostic request (DRY-RUN ONLY)
GitHub `main` commit `2c00cae1143eff8d9f3c4219632e7effb075abae` created:
`automation/deploy_requests/deploy-3d-capability-preflight-20261022.json`.
It requests `dry_run:true` and cannot change any files. The current read-only Windows agent does NOT process this separate queue, so it remains pending until the v0.3 watcher is locally bootstrapped.

## QA
A local disposable Python filesystem fixture ran 11 passing unittest cases: no-write preflight, file hash mismatch rejection, module-version rejection, installed camera-anchor protection, additive MCP patch, backup creation, hash-verified rollback, rejection of post-install tampering, unauthorised command rejection, --allow-deploy opt-in, and no local full path exposure in audit results. Locally verified ZIP CRC and SHA256. These are NOT Windows production validation and do not prove Foundry post-restart behavior.

## Explicit activation boundary
No current connected MCP can install an executable Windows deployment watcher or restart Foundry/MCP services. One-time user bootstrap:
1. Download/unzip attached v0.3 ZIP to Windows PC.
2. Run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install_deploy_watcher.ps1 -EnableDeploy` from inside the unpacked folder.
3. Installer locates verified Foundry user data, active Python MCP server and existing authenticated `$HOME\AcqDevAgent\repo`, clones a separate Git working copy, verifies JS version/checksum and starts watcher with explicit first-party-only deploy permission. If process path is ambiguous, supply `-McpServerPath`.

After its running result appears under `automation/deploy_results/`, assistant must inspect dry-run outcome and only then submit a **separate** `dry_run:false` job. On successful staged write, the assistant must coordinate restart/refresh during downtime, re-discover tool schema, call new read-only discovery endpoint and verify 3D Canvas camera, scene revision and unchanged saved geometry. STOP and restore immutable backup on regressions.

## Project decision
Godot remains primary 3D runtime until a genuinely feature-parity tested Foundry 3D Canvas scene demonstrates superior or comparable art, first-person traversal, efficiency and scene reliability. This diagnostic integration upgrade does not reverse that decision.
