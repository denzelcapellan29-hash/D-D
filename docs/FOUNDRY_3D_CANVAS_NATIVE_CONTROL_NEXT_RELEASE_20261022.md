# 3D Canvas native control extension — source-staged checkpoint (2026-10-22)

Status: NATIVE TOOLS DEVELOPED AND MOCK TESTED, NOT INSTALLED, NOT LIVE QA/DM ACCEPTED. Existing Phase1 custom Acq 3D MCP 8 tools and Area8 saved Scene untouched.

## Real baseline
- Active client Foundry V14.368, 3D Canvas 9.0.36, Mapmaking Pack 10.0.1, Premium 9.0.3.
- Previous real `inspect_3d_capabilities`, `search_3d_assets`, `capture_3d_view` and `inspect_3d_scene` calls PASS. Baseline Area8 Scene `NUEDEFAULTSCENE0` 161 3D Tiles, six lights, 13 Regions, stable revision `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f` before this task; rechecked same at task start.
- The Blender runtime has an UNSAVED dirty blank-file buffer; do not overwrite or assume a current .blend scene. Godot runtime remains connected and primary until platform parity tests.

## Phase 2 code on `feature/3d-canvas-native-controls-20261022`
- `inspect_3d_native_workflows`: source-verified native 3D Canvas 9.0.36 BuildPanel Props vs Premium buttons and actual AssetBrowser opened-instance/closed-instance behavior. Read-only.
- `set_native_camera_mode`: verified source API calls `game.Levels3DPreview.GameCamera.toggle()`, `toggleFirstPerson()`, `setCameraToControlled(selectedToken)` with a bridge-owned session ID and matching restore. First-person requires specified **already-selected** live 3D token with a head anchor, and cuts are blocked while a cutscene runs. Dry-run defaults true; capture/restoration of camera/target/near clipping and original native GameCamera state; one bounded catch rollback. No persistent settings or documents changed.
- `preview_native_asset_tile`: resolve an allowlisted local module GLB/GLTF through native `helpers.loadModel`, inspect `THREE.Box3`, reproduce browser-native footprint conversion to a *proposed* Foundry Tile (x,y,width,height,depth,elevation,model3d etc). Return bounds and explicit seams/collision QA warning. It does NOT create a Tile. Default placement uses center coordinates with top-left derived; bounded scale, rotation, elevation, RGB, source path, collision flags. Never substitute fabricated or procedural geometry.
- All JS commands also use existing GM permission and active Scene guards in `executeCommand`.
- Python MCP wrappers/contract JSON updated, and mocked source-verified Node tests: `native-workflow-inventory.test.cjs`, `native-control.test.cjs` and CI hooks. **JavaScript V8 syntax PASS; independent V8 camera/GLB fixture 11/11 PASS; native browser stub fixture PASS.** Node CI runner for this branch has not been proven successful; there are no real Phase2 runtime screenshots yet.

## Guarded deployment-agent issue and v0.4 solution
- Existing Windows v0.3 watcher is *intentionally* pinned to the first old installed JS SHA256 `842e858751b50d765ac86c90665c29eaa59fd15b7562339fc2c67658615fa951` and refuses installed original Phase1 JS `0129dbefea404c56fb7d5206355f4f896fe26e30820fc824e8a38c305aed3ad9`. Its additive MCP patch also refuses `inspect_3d_capabilities` after Phase1 is already installed. Thus it is not safe/possible to submit a Phase2 deploy job to v0.3. Do NOT queue one there.
- Replacement conversation artifact `Acq_3D_Canvas_Guarded_Bootstrap_v0.4.zip` exact size **15015 bytes**, SHA256 `5ea2678d2f2aff16adccaa67f92f770276b54a8a61243cdc374e6c7c0534a50e`. Contains `Upgrade_3D_Watcher_v04.cmd`, PowerShell guarded backup/upgrader, 2 Python agent components, README, SHA256SUMS, 2 unittest files. It upgrades ONLY the first-party deployment watcher app, stopping/restarting only that watcher process, not Foundry or the active MCP. Prior v0.3 SHA pins and `--allow-deploy` process requirement must match. Native Windows execution unverified (no PowerShell parser in runtime).
- Python v0.4 worker provides strict allowlisted source branches, exact git source commit pin, exact installed hash comparison, **apply requires both candidate JS/Python SHA256 values from a passing preflight**, explicit local --allow-deploy, Node syntax check, Python AST check, allowlisted new tool names, additive local MCP preservation, protected FPS anchor checks, versioned immutable backups and digest-gated rollback. No arbitrary shell or third-party module writes.
- 14/14 disposable Python tests PASS including incremental subsequent release, unsafe source rejection, source commit drift rejection, unexpected candidate digest, and rollback. ZIP CRC / SHA256 verified in container.
- This is not an auto-updater: v0.4 must be installed **once locally by DM** because running v0.3 can only deploy two first-party Acq production files and cannot modify its own binary/source. Once installed, repeat Phase2/next approved allowlisted releases may use preflight/apply jobs with exact commit/checksum pins.
- DO NOT claim new native tools are live until local v0.4 bootstrap, preflight readback, guarded apply, restart of first-party MCP stack and GM browser refresh, tool schema refresh, and actual read-only native dry-run calls.

## Next actions
1. DM unpacks v0.4 artifact and launches `Upgrade_3D_Watcher_v04.cmd` once; if it fails, do not manually edit processes.
2. Assistant checks new worker health and queue/audit, then submits dry-run request **with pinned source commit SHA** and old installed SHA. Compare candidate new_js/new_mcp digests and stable scene revision. Only after PASS submit `dry_run:false` with both digests; watcher backups + immutable hash checks.
3. User idle-time restart Acq 3D MCP service and refresh Foundry GM client; refresh ChatGPT plugin tool registry. Confirm live 3 native tools and 3D scene stable.
4. Dry-run real GLB bounds on a known library prop and camera mode on explicitly selected QA token. Only perform live camera transition with reversible session ID and player-eye before/after renderer QA. Then design **disposable test scene** actual native GLB drop placement/movement/collision and benchmark versus Godot.
5. Preserve final-source/DM accepted rules: no new procedural visible geometry, no affected Area8/Area10 assets, no third-party vendor changes.

This document is a saved engineering milestone, not DM acceptance of final scene visuals.
