# Foundry 3D watcher cold-start recovery — verified 2026-10-23
**Status: diagnosis PASS; deploy/restart NOT AUTHORIZED or performed.**

## Exact reason automatic v0.4 upgrade stopped
The pinned v0.4 Windows upgrade script at `C:\Users\denze\Downloads\Acq_3D_Canvas_Guarded_Bootstrap_v0.4\Upgrade_3D_Watcher_v04.ps1` was executed with `-DryRun`. All 14 package tests passed, but the script returned exit 1 with: `Expected exactly one running v0.3 watcher process; found 0. STOP.` The v0.4 script requires a currently running previous watcher **with the original explicit `--allow-deploy` flag**, checks its complete known CLI arguments, then upgrades only the deployment watcher—not the Foundry GM client, 3D Canvas, MCP or bridge processes. It intentionally does **not** support an absent previous process.

The expected installed files exist at `C:\Users\denze\Acq3DDeployAgent\app` and exactly match the previously pinned v0.3 SHA256:
- `acq_bridge_deployer.py`: `25065507f4ec54669ace7e232b8febb7bc9ae0b7ff5728265bec98d0f141181c`
- `acq_deploy_watcher.py`: `ccb845a4f43d08153b33d5242017d47451168bde8b022e29333a8fcc49e69b93`

The configured Windows scheduled task inventory, startup commands and services yielded no authorized watcher launcher. PowerShell command history yielded no prior `--allow-deploy` launch command. The independent `AcqDevAgent` process was confirmed running, but its `OPS` permit only health/list_files/read_file/hash_file and explicitly forbid file deployment or arbitrary shell commands. Therefore **no watcher restart and no privilege inference**. Do not convert user authorizing a functional goal into implied authorization for this script's `--allow-deploy` gate. No production scenes or modules changed.

## Correct cold-start recovery architecture (proposed, not installed)
1. Inspect only a previously approved, persistent local launch manifest/service definition, if found. It must pin repository checkout, Foundry user-data root, exact MCP Python source path, backup root, watcher script hash, per-operation privilege and `--allow-deploy` approval identity. The absence of any element rejects cold start. Never derive `--allow-deploy` from mere existence of `Acq3DDeployAgent` or a historical log.
2. Refuse automatic cold-start elevation without that recorded grant. If this grant does not exist, present exact required security decision and record a new, separately authorized persistent Windows task (only as explicitly approved) rather than starting with an inferred flag.
3. For approved recovery, verify the v0.3 SHA and path and no conflicting process; launch one pinned watcher; verify its arguments and PID/health (without queuing a deployment job); rerun the *unchanged* v0.4 `-DryRun` preflight. Abort on new mismatch.
4. Only after preflight and all tests pass, upgrade the **first-party watcher** with its guarded rollback. Any further first-party bridge deployment requires a separate pinned, backup/rollback-protected request, idle-time service restart and independent native GM browser polling proof.
5. Never silently upgrade third-party `levels-3d-preview` or Premium, create gameplay meshes, change global world settings or touch approved Scenes for this administrative recovery.

## Current alternatives before live deployment
- Run the already-committed **read-only** access selfcheck `tools/foundry_3d_access_selfcheck_20261023.py`.
- Preserve the first-party heartbeat/fail-fast patch as **staged** at draft PR https://github.com/denzelcapellan29-hash/D-D/pull/3 (four isolated tests passed), not installed.
- Tool schema mismatch is separate: the running Acq MCP `tools/list` advertises 14 tools, ChatGPT has eight. Resolve supported App tool-schema refresh when available; do not modify proprietary 3D Canvas to solve an App registry issue.
- Use existing native 3D Canvas read-only inspector through the live eight-tool MCP when stable; repeat browser-bridge calls only after safe checks.

## Evidence/cross-links
- Full native ownership: `docs/FOUNDRY_3D_CANVAS_OWNERSHIP_AND_FULL_ACCESS_GATE_20261023.md`.
- Previous operator and stop: `CURRENT_HANDOFF.md`.
- GitHub diagnostic: `tools/foundry_3d_access_selfcheck_20261023.py`.
