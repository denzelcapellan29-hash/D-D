# Area 8 — Reversible Electron cache reset trial (2026-10-18, EDT)

## Authority and context
DM ordered recovery of the previously working Area 8 3D Canvas scene before further Episode 2 construction. Last verified Area 8 first-person render was 2026-10-16 23:15 EDT. The earlier reversible comparison with untouched vendor camera scripts *also* failed to load 3D Canvas. Do not infer that custom camera scripts caused this regression. Both scene-building automations stay disabled; original Area 8 content is no-touch.

## Live preflight
- Blender MCP connected, clean saved `Episode2_HighRoad_WetBank_IsolatedQA_v010.blend`; NOT DM accepted.
- Foundry 14.368 / dnd5e 6.0.5 connected; original Area 8 scene `NUEDEFAULTSCENE0` active, Episode 2 `Test` inactive.
- Verified existing cold, offline world backup: `%LOCALAPPDATA%\FoundryVTT\AcqRecoveryBackups\Area8_PreRecovery_20261018T152210\Foundry_World_OFFLINE_VERIFIED`, 106 files / 3,564,332 bytes.
- Electron Chromium **user data profile** confirmed via live GPU process command line as `%APPDATA%\Foundry Virtual Tabletop` (Roaming), NOT `%LOCALAPPDATA%\FoundryVTT`. Earlier zero-cache search examined the wrong directory.
- Hardware enumerated AMD Radeon integrated and AMD Radeon RX 6550M dedicated GPU (~4GB), both driver 32.0.11020.6003. No HKCU DirectX UserGpuPreferences record explicitly selecting Foundry GPU. Active adapter not established; driver or GPU selection is a hypothesis, not an established failure.

## Cache trial — completed but FAIL
Preflight preserved complete world backup and native file hashes. Blender Python lacked `psutil` so the first script aborted before any file changes. A second script used Windows native process enumeration, graceful WM_CLOSE, verified **all** Foundry processes exited, then atomically moved the old Electron cache directories to:
`%LOCALAPPDATA%\FoundryVTT\AcqRecoveryBackups\Area8_ElectronCacheTrial_20261018T194829`

The archive has a manifest and preserves:
- `ORIGINAL_GPUCache`: 206 files, 11,198,228 bytes.
- `ORIGINAL_Code_Cache`: 790 files, 196,052,431 bytes.
- `ORIGINAL_Cache`: 318 files, 336,674,443 bytes.

The normal Foundry executable relaunched with `--world=acquisitions-incorporated`. Fresh caches were independently observed (5, 180 and 89 files respectively). Foundry world API reconnected, and Area 8 scene data remained present. Live installed patched scripts verified unchanged:
- `levels-3d-preview/scripts/main.js` SHA-256 `6abf61e2bc0b40203a989bf8bc0ac1918f63cea41f4ecae2abc2bfea1615817f`.
- `levels-3d-preview/scripts/handlers/GameCamera.js` SHA-256 `5930e69cbc302a655662ada5febfc594183c082e8ab1e4ff25882d0a8667b2f8`.

### Post-relaunch renderer QA
Using local Windows PrintWindow capture and user-interface 3D toggle, independently reopened Area 8 3D Canvas. The `Loading 3D Canvas...` overlay returned; Acq 3D inspector reported `levels3d_active=true` but **zero runtime tile bounds** out of 161 modeled tiles; true 3D capture continued returning RuntimeException. Client DevTools shows `WebGL: too many errors` and bridge `3D Canvas did not become ready within 15000ms`; earlier evidence identifies WebGL `uniformMatrix3fv` shader errors and Canvas3DCompendium 404 maps, but **root cause remains unproven**. DevTools width warning is a diagnostic confound, not original cause. One reversible cache-recovery attempt did NOT fix initialization. No further vendor, GLB, GPU-preference, cache or scene mutations performed. DevTools closed and Foundry returned to 2D; original Area 8 remains active. Artistically approved Area 8 is not currently visually operational.

## Guardrails and next reversible milestone
**STOP additional speculative resets** until a specific diagnostic target is identified. Next read-only evidence: capture earliest renderer JS exception and complete failed asset request URL in undocked DevTools, inspect shader/program initialization and GPU adapter. A later controlled device-selection test (dedicated RX 6550M) may require one additional restart, but should be independently authorized/justified and performed alone to avoid confounding changes. Always preserve original cache archive, versioned camera script backups, and cold offline world snapshot; do not regenerate road assets or touch accepted Area 8. Distinguish world API connection and `levels3d_active=true` from actual rendered frame and first-person movement PASS. Hourly automations remain disabled. No Meshy credits spent.
