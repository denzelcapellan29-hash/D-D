# Changelog

## 2026-10-08

### Area 2 visual workflow
- Area 2 remains the sole visual benchmark before any further Episode 1 production.
- Record every successful visual iteration as a repeatable process: numbered Blender checkpoint, QA render, exact visual delta, and relevant failure lesson.
- Current leading workflow: source/map for spatial truth, concept art for visual target, Blender for editable reconstruction, rendered QA for acceptance, Foundry/3D Canvas for runtime.


## 2026-10-04

### Minecraft Bridge
- Established live ChatGPT → local bridge agent → Fabric mod → Minecraft world mutation.
- Established Minecraft → bridge agent → Google Drive result/state readback.
- Added Fabric bridge v0.2.0 `/region` endpoint with palette + run-length compressed live block-state inspection.
- Added bridge agent v0.2.4 Drive filename-encoded live write transport, removing GitHub queue dependency for active world edits.

### Dock Ward
- Completed first live waterfront build and recovery pass.
- Added attached rowhouses, warehouse frontage, quay, piers, cargo, cranes, lamps, and market awnings.
- Added a moored merchant vessel with mast, sails, cabin, cargo, gangplank, and mooring posts.
- Extended inland with a continuous second street/frontage and four attached multi-story buildings.
- Added curbs, street lamps, market stalls, roofline variation, chimneys, and working clutter.
- Combined live readback covered 133,590 blocks.
- Structural QA detected a one-block north/south street pinch; repaired it live into a covered passage.

### QA / world-feel follow-up
- Expanded live QA to 179,340 blocks spanning harbor through deeper background context.
- Repaired four detached legacy roof strips, one isolated chain, and a disconnected bowsprit.
- Final structural graph contains exactly two intentional non-water components: city + moored vessel.
- Extended the cross street through the older background row and added a deeper skyline mass.
- Restored crane rigging with the correct 26.3 block ID: `minecraft:iron_chain`.

### Headless rendering / resource-pack workflow
- Formalized geometry/material separation for Minecraft world generation.
- Added visual profile schema for block color/texture/opacity/emissive metadata.
- Added resource-pack palette extractor for rapid aesthetic comparison.
- Changed intended release workflow toward prebuilt validated Minecraft world saves for direct import.

### Offline world compiler / release v0.2
- Compiled `Acq_Waterdeep_DockWard_WORLD_v0_2.zip` as a direct-import Minecraft save.
- Patched 179,340 live-readback cells into the prebuilt Episode 1 world with zero post-build mismatches.
- Removed visible vanilla grass from the authored context envelope without overwriting non-grass authored surfaces.
- Added 35 deterministic background urban masses in previously empty cells.
- Validated all 300 pregenerated chunks after rewrite; zero chunk/NBT parse failures.
- Persisted the release to Google Drive Build Artifacts.

### Offline world compiler / release v0.3
- Added strict support-graph validation for authored above-ground geometry.
- Removed 82 unsupported non-vessel components (6,258 blocks) from the controlled working envelope.
- Preserved only two explicit small sail-vessel components as intentionally unsupported over water.
- Cleared uncontrolled terrain and legacy above-ground geometry outside the coordinate-defined envelope, leaving a neutral lower datum instead of vanilla grass/legacy clutter.
- Eliminated all remaining `grass_block` cells in the pregenerated surface volume.
- Replaced 23 obsolete `minecraft:chain` block states with `minecraft:iron_chain`.
- Revalidated all 300 pregenerated chunks with zero parse failures.
- Confirmed the verified live corridor still matches exactly with zero block mismatches.
- Persisted `Acq_Waterdeep_DockWard_WORLD_v0_3.zip` to Google Drive Build Artifacts.

### Offline world compiler / release v0.4
- Replaced the visible neutral sandbox plate with a continuous city/harbor context shell across the full 320×240 pregenerated footprint.
- Added 111 deterministic background buildings, 3 skyline towers, 6 piers, 3 context vessels and 5 cranes.
- Added continuous street paving and irregularized harbor shoreline outside the protected Episode 1 core.
- Changed future flat-world generation to bedrock + stone datum only, eliminating new dirt/grass superflat bleed.
- Preserved the protected Episode 1 core exactly with zero block mismatches.
- Structural QA found only the two previously allowed small sail-vessel components unsupported; no new floating architectural components were introduced.
- Validated all 300 pregenerated chunks with zero parse failures.
- Persisted `Acq_Waterdeep_DockWard_WORLD_v0_4.zip` to Google Drive Build Artifacts.

### Offline world compiler / release v0.5
- Locked Episode 1 geographic scope to the lower Dock Ward rather than full Waterdeep.
- Rebuilt surrounding context using curved deterministic street fields instead of a rectangular street grid.
- Added frontage-driven attached rowhouses, terraced inland elevation, market/plaza dressing, harbor piers/ships/cranes and a contextual inland skyline edge.
- Preserved the verified Episode 1 core exactly with zero block mismatches.
- Structural QA finished at zero unsupported components and zero unsupported blocks.
- Validated all 300 pregenerated chunks with zero parse failures and zero grass blocks in the checked surface volume.
- Persisted `Acq_Waterdeep_DockWard_WORLD_v0_5.zip` to Google Drive Build Artifacts.

### Infrastructure QA v0.1
- Added a read-only Anvil/NBT world reader with block-state-property parsing.
- Added a direct off-screen VTK visible-face renderer and successfully rendered the actual v0.5 lower-Dock world: 540,080 blocks, 263,057 visible faces, 262,349 points.
- Added BlueMap 5.28 standalone QA automation with resource-pack support and explicit Mojang-download consent gating.
- Added a non-destructive Amulet Core load/save/reopen probe.
- Added GitHub Actions smoke coverage for BlueMap, PyVista and Amulet.
- Fixed Linux headless PyVista rendering with Xvfb/EGL/OSMesa dependencies.
- Validated the infrastructure stack in GitHub Actions run 37250767331: BlueMap success, PyVista success, Amulet success.
- No new Minecraft world release was produced as part of this infrastructure correction.


## 2026-10-05

### Foundry platform / MCP infrastructure
- Selected Foundry VTT + 3D Canvas as the primary campaign runtime after renewed platform research.
- Established a direct ChatGPT custom-MCP connection to Foundry MCP using OAuth.
- Fixed the Foundry-side key/account mismatch and proved full ChatGPT -> hosted MCP -> Foundry WebSocket connectivity.
- Live `get-world-info` returned `Acq WorldGen Test` on Foundry 14.368 / D&D5e 6.0.5.
- Executed a live d20 roll through the MCP path.
- Probed subscription boundaries: Guest, Free, Adventurer and Dungeon Master.
- Determined that the Dungeon Master tier is warranted for this project because scenes, tokens, combat and compendium import are required campaign-prep capabilities.
- Confirmed that hosted Foundry MCP does not replace the specialized 3D authoring layer: its standard screenshot path captures the 2D Pixi canvas, while 3D Canvas uses its own Three.js renderer.
- Retained the architecture split: hosted Foundry MCP for generic campaign/D&D5e automation + a thin private Acq 3D MCP for 3D Canvas semantic authoring and visual QA.

- Activated and verified the Foundry MCP Dungeon Master tier. Live scene enumeration/readback, compendium enumeration, token readback and world-time access all succeeded against `Acq WorldGen Test`; no writes were performed.

- Staged the first working Acq 3D MCP implementation: direct loopback RPC, 3D runtime inspection, asset search, camera control, true Three.js capture, semantic idempotent scene apply and manifest validation.
- Added a narrow Python MCP server and Windows stack launcher without exposing arbitrary JS/shell control.
- Added Foundry bridge smoke CI to validate protocol JSON, Python syntax, JavaScript syntax and MCP server import before live installation.

- Bumped Acq Foundry Bridge to v0.2.0, passed the Foundry bridge smoke workflow, and produced a validated install ZIP.
- Persisted `Acq_Foundry_3D_MCP_build_2026-10-05.zip` to Google Drive Foundry Bridge releases (Drive ID `1RiXGH7WKQ-74sEXVxvOnbtfAa1biEJpK`).

- Live Acq 3D MCP inspection and installed-asset search passed through ChatGPT → Secure MCP Tunnel → local MCP → bridge agent → Foundry/3D Canvas.
- Found and fixed the first 3D QA defect: renderer DOM-canvas capture produced black frames. v0.2.2 now captures via a Three.js WebGLRenderTarget/readRenderTargetPixels path.
- Added semantic-object cleanup to support a reversible disposable write test.

- Verified the v0.2.3 render-target capture fix live: 1920x992 WebP output expanded from the prior black ~5 KB frame to ~154 KB while preserving the Scene revision.
- Verified semantic Tile apply in dry-run mode. The only remaining infrastructure gate is an approved non-dry-run disposable Tile create/delete transaction.

- Completed the final Acq 3D MCP reversible write smoke test. Created and verified a disposable semantic 3D Tile, then removed it through the local bridge RPC.
- Verified the live Episode 1 scene returned to 11 Tiles and the original baseline revision `cbde9aa249e4a7bfb0c1b48034df6c38b7f88d81e7506cc9991cdd4572c23e70`.
- Closed the Foundry infrastructure gate; subsequent work moves to asset cataloging and the Episode 1 vertical-slice rebuild.

- Began Episode 1 production after closing the infrastructure gate. Reviewed the private Episode 1 source for the World Slice and recovered prior semantic/review artifacts.
- Added `vertical_slice_semantic_v1.json`, `asset_requirements_v1.json`, and `vertical_slice_build_v1.json` with stable semantic IDs, source/procedural classification, asset-first roles and phase QA.
- Live Foundry and the Secure MCP tunnel disconnected during the installed-asset catalog sweep; no production writes were made after the disconnect.

- Completed the first live Episode 1 installed-asset catalog and committed `campaign/episode1/asset_catalog_v0_1.json`.
- Validated disposable placements for building, wall, column, door and boulder assets in 3D Canvas.
- Patched Acq Foundry Bridge capture to hide 3D Canvas editor helpers and added per-Tile runtime bounds to inspection; bumped bridge to v0.2.4 and passed smoke CI.

- Applied the first real Episode 1 Phase A production write to `Ep1 - World Slice`: seven modular Dock Ward/Jolly's exterior Tiles added with stable semantic IDs; scene Tile count increased from 11 to 18.
- Persisted `campaign/episode1/phase_a_surface_context_state_v0_1.json` with Foundry IDs, asset paths and before/after revisions.
- Kept all legacy World Slice geometry in place and disabled collision/sight on new context assets during iteration.

- Expanded the live Episode 1 World Slice from the first surface pass to 61 Tiles and 10 Tokens while keeping all legacy geometry intact.
- Added warehouse-collapse rocks/timber/beams, Dock Ward lamp posts/carts, neutral City Watch tokens, and a player-safe Drunken Halfling Passerby cover token.
- Added Area 1 rubble/timber dressing and staged the source-grounded six green giant rats as two hidden waves of three.
- Added Area 2 blue/green/clear/cloudy pool surfaces, central columns, perimeter supports and provisional paired door shells.
- Recorded `campaign/episode1/live_vertical_slice_state_v0_2.json` and expanded the live asset catalog with validated timber, lamp and cart assets.
- Staged Acq Foundry Bridge v0.2.5 to correctly suppress nested 3D Canvas light helpers in QA captures and improve runtime model bounds; smoke CI passed.

- Validated Acq Foundry Bridge v0.2.5 live: runtime bounds became usable and large light-helper wireframes disappeared from QA captures.
- Rolled back an experimental cobble/floor/wall placement pass after visual QA showed it was not yet reliable; live World Slice returned to 61 Tiles / 10 Tokens.
- Staged v0.2.6 with `reload_3d_scene`, cheaper inspection bounds, and capture suppression for note/hidden-token/rangefinder editor overlays; smoke CI passed.

- Loaded and validated Acq Foundry Bridge v0.2.6 on the live World Slice.
- Full-scene inspection now completes reliably at 61 Tiles, and canonical 3D captures are clean enough for art-direction review.
- QA confirmed the remaining visual problems are scene-content problems, not capture-helper problems.
- Foundry MCP and the Secure MCP tunnel disconnected immediately before the next cobble-surface probe; no production write was made after disconnect.

- Resumed production after runtime recovery and confirmed both Foundry MCP and Acq 3D MCP live.
- Replaced the warehouse's white-grid opening with a three-piece irregular dark fissure mouth and retuned collapse dressing toward wood rather than metal.
- Added simple solid sidewalk slabs and replaced cyan generic shop shells with textured medieval building assets.
- Tested and fully rolled back unsuitable crater, thick cobbled-path and thin textured basin-lip probes after visual QA.


## 2026-10-06 — Foundry 3D construction method proven
- Added durable Foundry/3D Canvas domain knowledge and ADR-010.
- Built and visually captured a disposable `Example` scene using the supported model-backed Tile pattern.
- Verified modular Medieval Dungeon floor and wall GLBs through live Three.js runtime bounds and actual 3D captures.
- Established a measured coordinate mapping for the proven asset family.
- Opened the production gate for a modular Episode 1 rebuild; document/API success alone is no longer accepted as visual QA.


## 2026-10-06 — Acq Foundry Bridge v0.2.7 runtime recovery
- Bumped the Foundry bridge module to v0.2.7.
- Added automatic 3D Canvas runtime recovery before camera and renderer capture operations.
- Camera/capture now attempt direct 3D Canvas runtime activation, wait for a stable ready state, and perform one reload/toggle-cycle recovery before failing.
- Recovery is ephemeral UI/runtime behavior; it does not require persistent Scene `auto3d` changes.
- Capture results now include runtime-recovery diagnostics.
- Upgrade target remains the existing Windows stack layout under `Acq_Foundry_3D_MCP_build_2026-10-05\Acq_Foundry_3D_MCP` and the installed Foundry module under `%LOCALAPPDATA%\FoundryVTT\Data\modules\acq-foundry-bridge`.


## 2026-10-06 — Acq Foundry Bridge v0.2.7 runtime recovery
- Upgraded the project bridge module from v0.2.6 to v0.2.7.
- Added automatic 3D Canvas activation/readiness recovery before camera and capture operations.
- Verified recovery from `levels3d_active=false` to a valid 3D capture without manual DM intervention.
- Deleted 25 retired `Example` scratch/test Tiles.
- Resumed Episode 1 modular Area 2 construction; floor + perimeter walls passed live renderer QA.


## 2026-10-06 — Large-scene bounds + underground visual baseline
- Resolved Episode 1 scene-bound coordinate clamping by enlarging `Example` to 22649×11218.
- Verified x>6000 geometry renders at intended runtime coordinates.
- Established a dark dirt/rock underground ground layer across the Episode 1 footprint.
- Rejected a first-pass striped ground material and promoted the simpler accepted treatment only after rendered QA.
- Completed and visually accepted Area 4 broken-maze shell; added cave-in rubble after revision-checked retry.
- Documented the reusable scene-bounds, ground-first, and layered fail-fast workflow in ADR-013 and 3D Canvas domain knowledge.


## 2026-10-06 — Area 5 natural cavern QA
- Established high-end boulders as the accepted cavern-boundary asset family.
- Rejected stretched terrain/cave-cliff assets that failed live visual QA.
- Rejected bag, dynamic-sphere, and egg cocoon substitutes after rendered inspection.
- Generated a purpose-built cocoon GLB; upload exposed a missing `persistentStorage` capability in the bridge module.
- Recorded hidden-document/live-runtime divergence after a rejected Tile remained visible despite `reload_3d_scene`.
- Stopped further Area 5 production per fail-fast standard.


## 2026-10-06 — Formalized verified 3D construction domain knowledge
- Recorded the proven v0.2.8 `Example` scene resize and x>6000 clamp acceptance.
- Persisted exact underground Dynamic Mesh dirt-surface configuration and the rejected striped Ground010 texture attempt.
- Documented the stone-floor/pool-height calibration through live Three.js runtime bounds.
- Preserved the accepted Area 5 boulder-boundary method and the unresolved hidden-Tile/live-mesh divergence as a production hard stop.
- Synced detailed guidance to Google Drive `PROJECT_INSTRUCTIONS` and GitHub domain knowledge; ChatGPT Project Instructions still require the user's UI edit.


## 2026-10-07 — Large-scene + underground-context workflow
- Verified and documented Foundry Scene-bound coordinate clamping as the cause of missing/collapsed distant Episode 1 geometry.
- Resized `Example` to approximately 22649×11218 and verified x>6000 rendering.
- Replaced the white tabletop look with an accepted broad dirt/rock underground context layer.
- Rejected a striped high-repeat ground material mapping.
- Completed/accepted Area 4 broken-maze shell and cave-in rubble against the underground context.
- Adopted faster fail-fast cadence: one inspect, one coherent revision-checked semantic-layer write, one rendered acceptance capture.
- Area 5 initial cavern/cocoon visual pass rejected; subsequent correction halted on runtime inspection failure in accordance with fail-fast policy.


## 2026-10-07 — Blender semantic-authoring pipeline foundation
- Added runtime-independent semantic scene schema with spaces, structural/tactical/decorative features, entities, provenance, presentation profiles and fixed QA cameras.
- Added Blender authoring/QA contract and versioned Blender GLB export-manifest schema.
- Added a disposable, explicitly non-canonical Episode 1 pipeline smoke-test scene for scale/metadata/render/export validation.
- Recorded ADR-015: Blender is an authoring/render/QA stage; Foundry + 3D Canvas remains primary runtime.
- Corrected the stale repository README that still described Minecraft as the active primary runtime.
- Blender runtime execution remains gated until the local Blender MCP is exposed to this ChatGPT tool surface.
