# Area 8 3D Canvas shared loading regression — vendor patch A/B negative; dual GPU diagnosis (Oct 18 2026)

STATUS: **UNRESOLVED**, Area8 game scene data and Oct16 camera-patch files preserved, automation disabled.

## Verified this run
- GM rejoined Foundry normally after confirmed offline backup + launch; original Area8 is the active scene, Test remains inactive, scene data existing.
- Last attempted renderer capture continued failing in Acq 3D MCP and actual Windows screenshot earlier showed perpetual `Loading 3D Canvas...`.
- A/B comparison: two **original vendor scripts** `levels-3d-preview/scripts/main.js` and `scripts/handlers/GameCamera.js` were staged for DM F5. DM explicitly reported **still stuck**, so the exact pair of camera patches cannot be the **sole** root cause. Immediately restored Oct16 last visually working camera-patched scripts from verified private snapshot:
  - main.js `6abf61e2bc0b40203a989bf8bc0ac1918f63cea41f4ecae2abc2bfea1615817f`
  - GameCamera.js `5930e69cbc302a655662ada5febfc594183c082e8ab1e4ff25882d0a8667b2f8`.
  Restored script readback confirmed exact SHA256. No scene/GLB/Area8 geometry changes.
- Local `3D Canvas v9.0.35` `build3Dscene()` source examined read-only. Loading gate tracks `loadingTokens`, `loadingTiles` and asynchronous `_envReady`; it transitions to `_ready` only after successful resource load and `renderer.compile(scene,camera)`. Shader errors or hung resource promises can keep loading UI visible. This is diagnostic architecture, not evidence which predicate actually failed. Existing browser console screenshot had repeated `WebGL INVALID_OPERATION uniformMatrix3fv` and three missing Canvas3DCompendium PBR maps.
- Both Area8 source EXR `canvas3dcompendium/assets/EXRs_1K/Lighting/Night/moonless_golf_1k.exr` (1.51MB) and Test WebP sky source (109KB) exist physically AND served HTTP 200 from Foundry. Core blank texture served HTTP 200. Therefore do not assert those known sky paths are missing. Truncated previous three material-map 404s remain unresolved; not proven fatal.
- **New read-only Windows GPU hardware audit:** two AMD adapters: integrated `AMD Radeon(TM) Graphics`, AdapterRAM reported 512MB, and dedicated `AMD Radeon(TM) RX 6550M`, AdapterRAM reported ~4GB; both report driver `32.0.11020.6003`, Status OK. Dedicated-GPU assignment is plausible renderer blocker. Foundry's official docs https://foundryvtt.com/article/ts-scene-loading/ recommend choosing high-performance GPU for Foundry on multi-GPU Windows machines and checking acceleration.
- Attempt to inspect app-specific Windows GPU assignment registry was BLOCKED BY OpenAI safety controls. Another read-only Foundry Electron cache-inspection call was also BLOCKED. **Neither GPU preference nor caches were edited, cleared, or reset.** Do not work around those blocks.
- Foundry user desktop Electron profile identified read-only at `%APPDATA%\Foundry Virtual Tabletop` including `GPUCache`, `DawnGraphiteCache`, `DawnWebGPUCache`, `Code Cache`. These are distinct from `%LOCALAPPDATA%\FoundryVTT\Data` containing the protected world. Corrupt shader/GPU caches are HYPOTHESIS only; no evidence/QA yet.

## Current next safe test (manual OS setting; no passwords in chat)
1. Windows 11 Settings -> System -> Display -> Graphics -> Add desktop app if absent -> browse `%LOCALAPPDATA%\Programs\Foundry Virtual Tabletop\Foundry Virtual Tabletop.exe` -> Options -> **High performance AMD Radeon RX 6550M** -> Save. Close all Foundry windows, relaunch world normally and join GM. On live Area8, try 3D Canvas and verify actual player-height view. This is Foundry official recommended route, changes an OS application preference but NOT scene assets or vendor files.
2. If that fails, a *separate* reversible offline graphics-cache reset may be considered ONLY after Foundry closed and complete backup of the exact Electron cache directories. Ensure no security blocked operation is attempted through alternative path. Preserve all world/3D asset backups.
3. If still stuck, use browser DevTools to inspect `game.Levels3DPreview._envReady`, `_ready`, counts of unfinished loadingTiles/loadingTokens and exact earliest JS exception or Three.js compile log; calibrate shader and resources rather than guessing. UI actions require supported path.
4. No asset placement or Episode2 automation until actual WebGL rendered viewport and first-person movement, tilt + GM visibility QA.

## Backups / no touch
Verified private recovery folder `%LOCALAPPDATA%\FoundryVTT\AcqRecoveryBackups\Area8_PreRecovery_20261018T152210` contains current/patched/native vendor JS and the COLD world copy (106 hash-verified files). Last DM-accepted Area8 Blender v082 and current GM Area8 scene untouched. Both campaign scheduled automations disabled.

No renderer fix claimed.
