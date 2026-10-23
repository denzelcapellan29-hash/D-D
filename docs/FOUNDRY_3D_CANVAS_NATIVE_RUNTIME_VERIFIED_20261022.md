# Acq 3D Canvas native runtime verified — 2026-10-22
Status: PHASE 1 ACCEPTANCE = FIRST-PARTY RPC LIVE AND VERIFIED; PHASE 2 NATIVE EDITOR ADAPTER STAGED ONLY, NOT DEPLOYED/DM ACCEPTED.

## User-supplied visual evidence
GM DevTools screenshot showed `gm:true`, `bridgeModuleActive:true`, `bridgeLoaded:true`, `bridgeEnabled:true`, `canvas3DActive:true`, and local agent `reachable:true / status:200`. 3D Canvas rendered Area8 sewer cistern environment. Foundry V14 window-size warning explicitly said effective viewport 982x794 below 1024x768 minimum; docking DevTools caused reduced available width. Undock DevTools or close and maximize when evaluating visual quality. Console also had a 3D Canvas `Performance Grade E` report, FPS ~25 bottom left, 130 warnings; this is a performance-optimization signal, not evidence RPC failed or proof of a representative benchmark. Do not conflate viewport issue with bridge failure.

## Actual MCP calls VERIFIED after user screenshot
- `inspect_3d_scene`: ok, 3D active true, 161 3D Tiles, six lights, thirteen Regions; no scene revision change.
- New `inspect_3d_capabilities`: ok. Installed versions: 3D Canvas 9.0.36; Mapmaking Pack `canvas3dcompendium` 10.0.1; Token Compendium 2.0.20; Premium 9.0.3; lib-wrapper 1.13.5.1; first-party Acq bridge 0.2.8. The runtime reports active/ready, renderer/camera/controls/lighting/scene-graph true, loading_count 0.
- Runtime APIs identified: 3D Canvas toggle, runtime reload, `toggleFirstPerson`, `setCameraToControlled`, `GameCamera.toggle`, `GameCamera.toggleTopDown`, `GameCamera.getY`, live Three renderer, runtime Token/Tile registries, cutscene engine and interaction manager all present. `GameCamera.enabled:false` in GM session; `firstPersonMode:false`; zero controlled tokens. `enableGameCamera` setting false despite GameCamera controller existing. Do NOT call camera operations blindly; first-person toggle in upstream 9.0.36 is a no-op without selected token and can alter prior GameCamera state and restore it when disabling.
- Asset search `search_3d_assets(query='wall',limit=8)`: ok, retrieved genuine Mapmaking Pack `Banner_wall.glb`, `Decorative_Wall.glb`, `Stairs_SideCoverWall.glb`, `Sword_WallMount.glb`, with texture neighbors.
- 3D Canvas renderer capture `capture_3d_view(format='webp',quality=.65,restore_camera=true)`: ok, 1227x992 image, nonempty base64 103632 characters, `runtime_recovery.action='already-ready'`. Camera auto-restored, no Scene revision change.
- Scene revision baseline `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`, before==after all calls.
- Connected Foundry 121-tool MCP separately healthy. Native bridge has 8 tools after connector refreshed.
This proves the new first-party endpoint truly executes inside GM Foundry context after earlier transient tool failures; exact reason for earlier failures not established. Do not restart/reinstall based on old generic errors.

## Source-derived Asset Browser correction
Current v1 `inspect_3d_capabilities.available_apis.asset_browser_class=false` was a mistaken interpretation: upstream 3D Canvas 9.0.36 `scripts/apps/assetBrowser.js` constructor assigns **instance** to `game.Levels3DPreview.CONFIG.UI.windows.AssetBrowser=this` ONLY WHEN THE PROPS WINDOW IS OPEN. Upstream `scripts/apps/buildPanel.js` Props callback instantiates `new AssetBrowser().render(true)`. Browser function/class is imported within vendor module, not advertised in the same namespace. The false flag DOES NOT mean unavailable. The native `buildTileData` helper depends on current raycast hit and UI selection; direct calls absent browser state may not work. For programmatic placement use validated native drop functions with GLB measured footprint and separate runtime QA; no fabricated simple JSON placement.

## Phase 2 staged code
Branch `feature/3d-canvas-native-controls-20261022` from source-equivalent Phase1 deployed branch, not installed:
- New allowlisted read-only `inspect_3d_native_workflows` JS handler, Python MCP tool, protocol and tool-surface manifest.
- Inspect native BuildPanel `BUILD_PANEL_BUTTONS` by fixed known IDs (`props`, `environment`, `terrain`, `materials`, `roombuilder`, `effects`, `cutscenes`); distinguish missing, disabled, callable; no callbacks invoked.
- Distinguish actual open browser instance and `buildTileData` method from separate Props callback registration.
- Inspect Game Camera/first-person capability and selected token runtime readiness. Pure read-only/no world/UI effects.
- Source V8 syntax check PASSED; mocked closed/open Props and premium action fixture PASSED. Added Node test with CI hook, but hosted CI is not yet independently passing. Python import/Windows runtime not tested for Phase2.
- DM-approved visible geometry remains from approved Meshy GLB or verified library. No automatic scene or vendor module changes.

## Next gates
1. Finish native editor inventory tests, review installed Premium actions and design allowlisted idempotent camera mode control. First-person requires selected QA token and verifying genuine head anchor and movement; never simply set arbitrary camera coordinates.
2. Inspect native Asset Browser placement via core `dropFunctions.Tile` and `interactionManager._onDrop` and match its actual model-derived bounding box/autoGround contract. Stage disposable test Scene transaction before mass assembly.
3. Upgrade using existing guarded Windows watcher only after deployment preflight, backup, rollback and zero Scene mutation checks. Preserve `fps-camera-anchor.mjs`.
4. Capture player-eye, overhead, side/rear and performance evidence. Do not call successful renderer capture alone final art/traversal acceptance.
