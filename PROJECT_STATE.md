# Project State

Updated: 2026-10-04

## Active runtime
Minecraft Java 26.3 + Fabric + WorldEdit is the primary campaign runtime.

## Bridge
- Fabric bridge v0.2.0 is installed and live in `Acq Waterdeep — Dock Ward`.
- Bridge agent v0.2.4 is the active control path.
- Google Drive commands/results transport now supports live filename-encoded query, fill, setblock, and region operations.
- Bulk `/region` inspection reads up to 500,000 live blocks using palette + run-length compression.
- Automatic waterfront inspection remains active.

## Dock Ward vertical slice
Live world editing is operational against the current save.
- Waterfront frontage: attached rowhouses, warehouse frontage, quay, piers, cranes, cargo, lamps, market awnings.
- Harbor: moored merchant vessel with mast/sails, cabin, cargo, gangplank, and mooring posts.
- Inland: second attached urban frontage with four multi-story buildings, interiors, doors, windows, varied rooflines/chimneys, market stalls, curbs, street lamps, and working clutter.
- North/south cross street was widened from a one-block pinch into a covered passage.

## Runtime QA
- Expanded QA region: x=-108..-48, y=96..125, z=-45..52.
- 179,340 live blocks inspected in the latest combined readback.
- Exactly two non-water connected components remain: one grounded city mass and one intentional moored vessel.
- Detached legacy roof strips, a floating chain, and the disconnected bowsprit were detected and repaired live.
- Street surfaces are continuous; both rowhouse pinch points were widened into covered passages.

## Immediate next milestone
Infrastructure bake-off is complete enough to select the authoring architecture.

**Selected authoring runtime:** local dedicated Fabric 26.3 server, using the existing 26.3 bridge code as the world-control substrate, WorldEdit for bulk edits/schematics, and BlueMap for actual-world visual QA. The semantic campaign/world model remains canonical above Minecraft.

This replaces the earlier assumption that a Paper/VibeCraft-style migration should be the default. Paper/IotA, VibeCraft, Clankercraft, Architect-Agent, Mineflayer MCPs and GDMC remain reference/fallback implementations, not the production dependency stack.

Next engineering work is to package and validate this dedicated-server path on a clone of v0.5 with no DM-side debugging:
1. server bootstrap with portable Java 25;
2. Fabric 26.3 + Fabric API;
3. existing Acq bridge adapted for dedicated-server operation and typed MCP facade;
4. WorldEdit 7.4.6 beta-02 for 26.3;
5. BlueMap 5.28 Fabric for 26.3;
6. explicit transaction snapshots/rollback and coordinate-envelope validation;
7. automated structural + BlueMap QA;
8. only then resume world-feel iteration.

The existing singleplayer world remains untouched until the dedicated-server clone passes equivalence checks.

## Scope gate
Do not expand to full Waterdeep or D&D gameplay systems until the Dock Ward waterfront → warehouse → fissure → dungeon vertical slice is convincingly playable and can be maintained autonomously.


## Coordinate working grid
The Minecraft runtime now has an explicit coordinate-based working-area contract in `integrations/minecraft-bridge/workspace.json`.
- Surface datum: Y=100.
- Planning origin: world (-80,100,0), giving local u=x+80, v=z, h=y-100.
- Primary Episode 1 controlled authoring envelope: x=-144..32, y=96..160, z=-96..96.
- Current verified corridor remains x=-108..-48, y=96..125, z=-45..52.
- Future writes should be rejected outside the controlled authoring envelope unless explicitly overridden; uncontrolled pregenerated terrain outside the envelope is not part of the authored world.
- Camera QA uses named coordinate stations rather than ad-hoc player movement.


## Headless voxel QA
Rendered Minecraft screenshots are no longer the primary visual-QA dependency.
- Live `/region` data is reconstructed outside Minecraft from XYZ occupancy + block/material identity.
- The current 179,340-block corridor has been successfully rendered into colored 3D voxel views without using the Minecraft camera.
- `integrations/minecraft-bridge/render_region.py` now exports a colored PLY point cloud and optional isometric PNG views from bridge region results.
- Minecraft camera/player automation is now secondary/diagnostic rather than required for normal QA.
- Next fidelity upgrade is richer block-state readback (stairs/slabs/panes/orientation), followed by entities/block entities where visually relevant.


## Visual material profiles
Appearance is now treated as independent from world geometry.
- Block/world coordinates remain stable while visual profiles map block IDs/block states to representative color, textures, opacity, emissive behavior, and optional model hints.
- Fast QA can swap hex/RGB palettes without touching the Minecraft save.
- Higher-fidelity QA will resolve resource-pack textures/models against the same block-state volume.
- `integrations/minecraft-bridge/visual_profile.schema.json` defines the profile contract.
- `integrations/minecraft-bridge/extract_resource_pack_palette.py` extracts representative texture colors from Java resource packs.
- Target delivery is a validated prebuilt world save plus an optional selected resource pack/profile, so the DM imports a finished release rather than assembling the world manually.


## Prebuilt world release v0.2
A new direct-import Minecraft save has been compiled offline from the existing validated Episode 1 world plus the latest live Dock Ward block readback.
- Release: `Acq_Waterdeep_DockWard_WORLD_v0_2.zip`.
- Drive artifact ID: `1fFokor3_ca_N_hqb0LBLZ3j32RY0Cw-c`.
- Latest live corridor patch: 179,340 cells reproduced exactly from runtime readback.
- Offline QA reopened all 300 pregenerated chunks successfully with zero NBT parse failures.
- Exact live-region comparison after compilation: 0 block mismatches.
- Authored context envelope contains 0 vanilla `grass_block` surface cells after cleanup.
- 16,134 previously vanilla surface columns were converted to harbor water or urban paving where safe.
- 35 non-playable background urban masses were added only in previously empty space to create skyline depth.
- 146 chunks were touched by the offline compiler.
- Existing Episode 1 v0.5.1 warehouse/fissure/dungeon content remains in the base save and was not regenerated from unsupported source assumptions.


## Prebuilt world release v0.3
Structural cleanup release: `Acq_Waterdeep_DockWard_WORLD_v0_3.zip`.
- Drive artifact ID: `1ydpXiCfN9KQxX6j4QFLddeL0AMaPoc5N`.
- Controlled world envelope: x=-144..32, y=96..160, z=-96..96.
- Cleared 177,238 blocks of uncontrolled terrain/legacy geometry above the neutral Y=96 datum outside the envelope.
- Removed 82 unsupported structural components / 6,258 blocks inside the envelope.
- Only two unsupported components remain, both explicitly classified small sail vessels over water.
- Replaced 23 obsolete `minecraft:chain` states with live 26.3 `minecraft:iron_chain`.
- 0 `grass_block` cells remain in the pregenerated surface volume.
- All 300 pregenerated chunks reopen successfully with 0 NBT parse failures.
- Verified live corridor remains an exact block match: 0 mismatches.
- Existing Episode 1 warehouse/fissure/dungeon content remains preserved.


## Prebuilt world release v0.4
World-feel/context-shell release: `Acq_Waterdeep_DockWard_WORLD_v0_4.zip`.
- Drive artifact ID: `1YEFlM2H_4jS62UBFrHacqkykeI5X6ddm`.
- Entire existing pregenerated footprint is now treated as authored city/harbor context: x=-144..175, z=-96..143.
- Added 111 deterministic background buildings, 3 skyline towers, 6 piers, 3 context vessels and 5 cranes.
- Added ~88k blocks of connected background architecture plus ~9.6k road cells.
- Replaced the large neutral sandbox plate with continuous urban ground and a broad harbor/shoreline shell.
- Default new-chunk flat worldgen no longer includes dirt/grass layers; it falls back to the neutral stone datum.
- Verified protected Episode 1 core is preserved exactly: 0 block mismatches over x=-120..40, z=-60..65, y=96..127.
- 300 pregenerated chunks reopen successfully with 0 parse failures.
- 0 grass blocks remain in the checked surface volume.
- Structural graph: 210 above-ground components, only 2 unsupported components / 29 blocks; both are the pre-existing explicitly allowed small sail vessels in the protected core.
- This is still procedural connective/background world-building, not canonical survey geometry for all of Waterdeep.


## Episode 1 geographic scope
Episode 1 intentionally targets only the lower Dock Ward required to make the warehouse/fissure/dungeon approach feel like a coherent lived-in district.
- Full Waterdeep is a stretch goal, not part of the Episode 1 quality gate.
- The current pregenerated footprint is context for the lower Dock Ward, not an attempt to represent the entire city.
- Expansion beyond this footprint should happen only when required by later episodes or explicit campaign decisions.


## Prebuilt world release v0.5
Organic lower-Dock release: `Acq_Waterdeep_DockWard_WORLD_v0_5.zip`.
- Drive artifact ID: `1akOelL6nL34XacJLNGTMVp--H8DE5go1`.
- Scope: Episode 1 lower Dock Ward only.
- Rebuilt procedural context around curved deterministic streets rather than a rectangular grid.
- Added frontage-driven attached rowhouses, terraced inland elevation, market/plaza dressing, a continuous quay, piers, ships, cranes and an inland skyline/fortification edge.
- 63 new context houses; 9,435 road cells; 4,861 sidewalk cells; 24 street lamps; 6 piers; 3 context ships; 4 cranes.
- Structural QA reports 0 unsupported components / 0 unsupported blocks after a boundary support repair outside the protected core.
- All 300 pregenerated chunks parse successfully.
- 0 grass blocks remain in the checked surface volume.
- Protected Episode 1 core remains exact: 0 block mismatches.


## Infrastructure QA v0.1
The promised tooling upgrade is now implemented and validated before further world-version churn.
- Added a read-only Java Anvil/NBT world reader that preserves block-state properties.
- Added a direct off-screen VTK visible-face renderer for fast engineering QA from the actual world save.
- Rendered the full v0.5 lower-Dock footprint headlessly: 540,080 non-air blocks, 263,057 visible faces, 262,349 mesh points.
- Added a BlueMap 5.28 standalone QA runner with optional resource-pack injection. BlueMap 5.28 CLI boot is CI-verified on Java 25 and targets Minecraft through 26.3.
- Added a non-destructive Amulet Core probe. Stable Amulet Core 1.9.49 installs/imports successfully on Python 3.11 in CI; it is not yet the production compiler until the real-world load/save/reopen probe passes.
- Added PyVista/VTK headless rendering smoke coverage. PyVista off-screen rendering is CI-verified under Xvfb.
- GitHub Actions run 37250767331 completed successfully across BlueMap, PyVista and Amulet jobs.
- Production fast renderer is direct VTK; PyVista is an optional higher-level convenience layer.
- Minecraft screenshots remain diagnostic only.


## Actual-world QA staging — 2026-10-04
- Explicit DM approval received for BlueMap to download the required Mojang client resources.
- BlueMap target remains 5.28 / Minecraft 26.3 / Java 25.
- A bounded `run_real_world_qa.ps1` runner is staged for the user machine because the current remote execution sandbox does not provide the required Java/network combination and the Minecraft bridge intentionally does not expose arbitrary shell execution.
- The runner snapshots the source world before QA; the source save is never written by BlueMap or Amulet.
- BlueMap renders the snapshot and publishes logs/web output/capture to the existing Minecraft Bridge captures folder when available.
- Amulet Core 1.9.49 probes load/save/reopen only on a disposable copy.
- Result review is pending the local run; no v0.6 world work begins before this gate is resolved.


## VibeCraft architecture evaluation — 2026-10-05
- VibeCraft was evaluated as an external MIT-licensed MCP-native Minecraft automation project.
- Its architecture is highly relevant: structured build tools, WorldEdit/vanilla fallback, spatial analysis, patterns, terrain generation, furniture helpers, and explicit AI-control safety.
- Its published client-mod compatibility currently stops at Minecraft 1.21.4, so it is not a drop-in replacement for the working Minecraft 26.3 runtime.
- Decision: keep the existing 26.3 Fabric bridge and adapt/port useful VibeCraft MCP-layer concepts, schemas and deterministic helpers above our bridge rather than replacing the runtime.
- DM-side manual infrastructure debugging is no longer an acceptable normal workflow. Local installs/restarts remain DM actions when truly required; routine QA and iteration must be bridge/repo/Drive automated.
- Amulet remains an optional candidate backend and is no longer a prerequisite for the next world-feel pass.


## Infrastructure bake-off conclusion — 2026-10-05
- Dedicated Fabric 26.3 is the preferred authoring/runtime control surface because it preserves the already-validated Fabric/WorldEdit world path while removing dependence on the player's client being the automation host.
- Fabric publishes a dedicated 26.3 server launcher; WorldEdit 7.4.6 beta-02 explicitly supports Fabric 26.3 server-side; BlueMap 5.28 supports Fabric 26.3 dedicated servers.
- The existing Acq bridge is already server-oriented internally (server lifecycle, ServerLevel/ServerPlayer, local HTTP) and therefore has a much shorter migration path to a dedicated Fabric process than a rewrite onto Paper.
- Standard WorldEdit is preferred over FAWE for now: FAWE's current stable compatibility stops at 26.2 and its 26.3 support is still in-flight.
- VibeCraft is a useful MCP/tool-schema reference but its published client-mod support stops at 1.21.4.
- IotA-asce/minecraft-mcp is a useful Paper/WebSocket/MCP reference, but its bridge is v0.1 and compiles against Paper 1.21.4; it is not adopted wholesale.
- Architect-Agent has an excellent staging/rollback/visual-loop design, but is extremely young and its dedicated-server docs target Paper 1.21.1.
- Clankercraft is comparatively mature and has strong WorldEdit/MCP tooling, but its player-bot protocol layer adds version/protocol dependency that this project does not need.
- Mineflayer-based MCP stacks are not selected because stable Mineflayer documentation still tops out at 26.1 while 26.3 protocol support remains under active PR work.
- minecraft-ai-build-server is a strong validator/compiler design reference but is pinned to 26.1.2 in its current stack.
- GDMC HTTP Interface currently targets Minecraft 1.21.11, so it is not a 26.3 candidate.
- No further DM-side Java/Python/PowerShell troubleshooting is part of the normal workflow. The next handoff should be a packaged, tested server launch or a single install/restart action only if unavoidable.


## Platform decision — 2026-10-05
After a fresh market/architecture review of Foundry + 3D Canvas, TaleSpire, The RPG Engine, RPG Stories, Menyr, Minecraft/Fabric, and emerging hybrids, **Foundry VTT + 3D Canvas is selected as the primary campaign runtime**.

Rationale:
- It is the only mature current option that combines high-quality 3D presentation with a documented/extensible campaign/rules platform and a control surface we have already proven end-to-end.
- Foundry V14 is stable and current; 3D Canvas is actively maintained and verified for V14.
- The existing Acq Foundry Bridge already proved scene/document CRUD, asset upload, lights/walls/regions/notes/journals, D&D5e compendium work, camera framing, captures, revision-checked writes and backups.
- TaleSpire remains visually excellent but its official Symbiote API still cannot persistently edit board state/place tiles, which is incompatible with the desired autonomous inspect/write/repair loop.
- RPG Engine and RPG Stories provide strong 3D building UX, but no sufficiently documented external automation/control API was found for the autonomous prep requirement. RPG Engine's public Steam binary branch has also not materially advanced since April 2025.
- Menyr is still beta/unreleased and explicitly has more VTT features coming later.
- Minecraft remains a deterministic/export/engineering target, not the player-facing visual runtime.

### Corrected Foundry implementation strategy
The earlier Foundry spike overused custom monolithic GLB generation and tried to solve geometry, materials, lighting and world-building simultaneously.

The production strategy is now **asset-first and semantic**:
1. semantic scene stays canonical;
2. semantic materials/objects resolve primarily to proven 3D Canvas tiles, props, materials, skyboxes and room-building assets;
3. 3D Canvas Advanced Tools and Mapmaking Pack provide terrain/interior/material/environment vocabulary;
4. custom GLB generation is reserved for source-specific geometry such as the earthquake fissure, bespoke carvings and unique set pieces;
5. the bridge creates/updates modular scene objects, lights, walls, regions, actors, journals and camera views rather than treating the world as one opaque model.

### Version pinning
For the next vertical slice, pin the runtime rather than auto-updating during campaign prep:
- Foundry VTT 14.368
- 3D Canvas 9.0.35
- 3D Canvas Advanced Tools 9.0.3
- 3D Canvas Mapmaking Pack 10.0.1
- compatible D&D5e V14 release

### Hard acceptance gate
One focused rebuild only:
Waterdeep lower-Dock street -> warehouse exterior/interior -> fissure -> subterranean transition -> Area 1 -> Area 2.

Foundry must demonstrate:
- convincing world/location/encounter-scale visual continuity;
- automated clean-scene reconstruction through the bridge;
- stable lighting/material response;
- automated canonical camera captures;
- working collision/sight/doors/regions;
- D&D5e actors/journals/encounter support;
- no routine DM-side file/script debugging.

If this asset-first vertical slice still fails the visual/world-feel bar after one bounded pass, stop Foundry work and move to TaleSpire. Do not return to Minecraft visual-polish work.


## Foundry infrastructure selection — 2026-10-05
A second-pass infrastructure review was completed specifically to avoid rebuilding generic Foundry functionality.

### Runtime
Pin the existing known-good line:
- Foundry VTT 14.368
- D&D5e 6.0.5
- 3D Canvas 9.0.35
- 3D Canvas Mapmaking Pack 10.0.1
- libWrapper
- Acq Foundry Bridge
- 3D Canvas Advanced Tools 9.0.3 only when its mapmaking conveniences materially help; it is not a required control-plane dependency.

The last persisted Foundry bridge state already reported Foundry 14.368, D&D5e 6.0.5, world `Acq WorldGen Test`, scene `Ep1 - World Slice`. Do not reinstall Foundry or D&D5e unless the live instance has since changed.

### Control plane
Use a hybrid rather than reinventing the entire Foundry API:
1. **Acq Foundry Bridge stays as the thin project-specific 3D authoring adapter** for 3D Canvas tile/model flags, environment controls, lights, semantic regions/levels, asset upload, camera framing/captures, revision checks and semantic build IDs.
2. **Foundry API Bridge / Foundry MCP is the preferred off-the-shelf generic campaign sidecar when the user's ChatGPT account supports custom MCP connections and the user elects its paid tier.** Delegate actors/items/journals/tables/compendiums/tokens/combat/time/UI to it instead of duplicating those generic APIs in Acq Bridge.
3. The vertical-slice rebuild does not depend on Foundry MCP availability. Existing declarative bridge operations remain sufficient to validate 3D authoring first.

Keep script/eval-style remote execution disabled. The custom bridge remains allow-listed and revision-checked.

### Foundry V14 architecture
- Use core **Scene Levels/Regions** for vertical organization. Do not restore retired Levels/Wall Height module architecture for a fresh V14 scene.
- Use 3D Canvas **Tiles** as the principal modular geometry primitive; they can carry collision, sight-blocking and door behavior.
- Build primarily from the Mapmaking Pack asset/material vocabulary; store only semantic references/metadata in the project and respect per-asset licenses.
- Generate custom GLB only for unique source-specific geometry.

### Transactions and persistence
- Each generated placeable receives stable `flags.acq.semantic_id`, `flags.acq.build_id`, and provenance/classification metadata.
- Before meaningful writes: duplicate/snapshot the target Scene and require `expected_revision`.
- Milestones use Foundry package backups plus versioned semantic manifests and generated/custom assets in project storage.
- Do not place the live Foundry User Data directory inside Google Drive/OneDrive/Dropbox synchronization. Drive remains bridge transport and artifact storage only.

### Performance/QA
- Keep authored geometry modular during iteration.
- On a duplicate/release candidate, use 3D Canvas tile merging for compatible static repeated assets after structural QA; never merge interactive doors.
- QA uses canonical camera stations and automated captures plus structural state assertions.
- Do not move to remote/dedicated Foundry hosting during the vertical-slice test; it adds infrastructure without improving the local 3D authoring loop.


## Direct ChatGPT MCP architecture — 2026-10-05
The DM confirmed this ChatGPT environment can create custom MCP connections. Infrastructure research is now explicitly scored against the actual product goal: autonomous Acquisitions Incorporated campaign prep and maintenance in a high-quality 3D VTT with minimal DM-side work.

### Research criteria
Any infrastructure choice must be evaluated on:
- direct ChatGPT read/write control;
- 3D world authoring, not merely campaign-document CRUD;
- semantic/idempotent rebuilds from the canonical campaign model;
- source-fidelity and GM-only hidden state;
- visual quality and world/location/encounter continuity;
- deterministic or revision-checked writes with recovery;
- asset discovery/reuse before custom modeling;
- D&D5e actors/items/compendiums/journals/encounters;
- programmatic camera/capture QA;
- runtime performance;
- maintenance/version risk;
- licensing/privacy/cost;
- and the amount of manual setup/debugging pushed onto the DM.

### Selected MCP topology
1. **Foundry API Bridge / Foundry MCP** is the preferred off-the-shelf generic Foundry control plane. It is current, Foundry V14 verified, D&D5e aware, supports ChatGPT OAuth, and exposes 121 tools at the Dungeon Master tier for actors/items/journals/scenes/tokens/combat/compendiums/time/UI. Use it rather than reimplementing generic campaign CRUD.
2. **Acq 3D MCP** will be a deliberately small private MCP server for project-specific 3D Canvas authoring operations that Foundry MCP does not expose: 3D Tile/model flags, semantic asset resolution, environment controls, semantic build IDs, specialized camera framing/capture, asset upload and idempotent scene-apply/repair.
3. Connect Acq 3D MCP to ChatGPT through **OpenAI Secure MCP Tunnel** rather than exposing a local port publicly. Reuse the existing Acq Foundry Bridge module/agent internals behind this MCP surface.
4. Google Drive is demoted from primary command transport to artifact/release/capture/private-source storage and emergency fallback transport.

### Safety
- Keep Foundry API Bridge "Allow Script Macros" off.
- Do not use generic code-mode scripts as the production write path because its documented execution is not transactional.
- Acq 3D MCP meaningful writes remain allow-listed, revision-checked, idempotent where possible, and backed by recoverable Scene snapshots.
- Full copyrighted adventure source remains in private Drive/project sources; Foundry and third-party MCP services receive only the concise campaign data needed to run/prep the world.

### 3D Canvas dependency correction
Published 3D Canvas documentation is inconsistent about legacy dependencies: the current V14 wiki still lists libWrapper/socketLib/Levels/Wall Height as required, while the current public source manifest lists only libWrapper as a hard requirement and marks Mapmaking Pack/Token Collection/Advanced Tools as recommendations. Therefore do **not** add or remove Levels/Wall Height/socketLib based on assumptions. Inspect the actual installed 9.0.35 manifest/runtime dependency state before changing the module stack.


## Live Foundry MCP validation — 2026-10-05
Direct ChatGPT -> Foundry MCP -> live Foundry has now passed end-to-end.
- `get-world-info` returned live world `Acq WorldGen Test`, Foundry 14.368, D&D5e 6.0.5, 9 scenes, 5 actors and 3 journals.
- A live `1d20` roll executed through Foundry and returned 7.
- The account is currently at **Guest**, not the free Patreon membership tier. Guest exposes only world-info and dice-level proof functions.
- Live permission probes confirmed:
  - Free Patreon membership: actors/items/folders/effects/chat/initiative family.
  - Adventurer (€3): journals and roll tables.
  - Dungeon Master (€10): scenes/doors, tokens, combat, compendiums/import, time/pause/UI.
- For this campaign's prep workflow the Dungeon Master tier is functionally justified because scene inspection, token/encounter setup and compendium import are core requirements, not conveniences.

### Important boundary discovered
The hosted Foundry MCP is not the 3D authoring engine.
- The 121-tool ChatGPT surface does not expose 3D Canvas-specific Tile flags/environment/camera controls.
- Its current scene screenshot path captures Foundry's 2D Pixi canvas (`canvas.app.view`), not the 3D Canvas renderer.
- The underlying bridge wire protocol has more generic Scene/wall/note CRUD than the current 121-tool ChatGPT surface, but it still does not replace project-specific 3D Canvas semantics.
- 3D Canvas itself exposes the live `game.Levels3DPreview` object, including the Three.js scene, renderer, camera and controls. Its own `export2d.js` demonstrates deterministic rendering through `game.Levels3DPreview.renderer`.
- Therefore the selected split remains correct: pay for generic Foundry/D&D5e automation; keep a small private Acq 3D MCP for 3D Tile/environment/camera/capture/idempotent semantic scene operations.

### Subscription recommendation
Upgrade to the Dungeon Master tier once the DM chooses to proceed. Connectivity is already proven, so the subscription is no longer an infrastructure gamble. Do not enable script macros. Do not make non-transactional code-mode execute the production world-build path.


## Foundry MCP Dungeon Master tier — ACTIVE (2026-10-05)
Direct DM-tier operations are now verified live through ChatGPT against `Acq WorldGen Test`.
- Scene enumeration succeeded: 9 scenes, with `Ep1 - World Slice` active.
- Active scene readback succeeded: 11 Tiles, 11 lights, 5 semantic Regions and 4 Notes.
- Compendium enumeration succeeded: 23 packs including SRD and 2024 D&D5e actor/item/spell/rules content.
- Token readback succeeded (currently no tokens in the active scene).
- World-time readback succeeded.
- No writes were performed during verification.
- The hosted MCP is now accepted as the generic Foundry/D&D5e control plane for this project.


## Acq 3D MCP implementation — staged in repo (2026-10-05)
The project-specific 3D control plane has now moved from design to implementation.

Implemented in `integrations/foundry-bridge`:
- direct loopback `POST /rpc` on the existing Python bridge agent, using the existing Foundry polling/execution path rather than Drive command files;
- 3D Canvas runtime inspection;
- installed 3D asset path search;
- ephemeral 3D camera positioning with optional initial-view persistence;
- true 3D capture from the 3D Canvas Three.js renderer;
- existing allow-listed environment control;
- idempotent semantic-object create/update keyed by `flags.acq.semantic_id`;
- semantic manifest validation;
- a narrow MCP Python server on loopback port 18748;
- Windows install/stack launcher;
- Foundry bridge smoke CI for JSON/Python/JavaScript/MCP import checks.

The hosted Foundry MCP remains responsible for generic campaign operations.

### Remaining gate before world writes
The new code is staged but not yet installed into the live Foundry machine. Before Episode 1 rebuilding:
1. pass CI/syntax checks;
2. package/install updated Acq Foundry Bridge;
3. start local bridge agent + Acq 3D MCP;
4. create and authorize an OpenAI Secure MCP Tunnel;
5. verify read-only 3D inspect/capture;
6. perform one disposable semantic Tile create/update/delete transaction;
7. only then permit production vertical-slice writes.


## Acq 3D MCP validated build — 2026-10-05
- Acq Foundry Bridge version bumped to **0.2.0**.
- GitHub Actions smoke validation passed on the current staged implementation: protocol JSON, Python syntax, JavaScript syntax, MCP SDK install/import and packaging.
- Validated workflow run: `37348107962`.
- Packaged release artifact persisted to Google Drive Foundry Bridge releases:
  - file: `Acq_Foundry_3D_MCP_build_2026-10-05.zip`
  - Drive ID: `1RiXGH7WKQ-74sEXVxvOnbtfAa1biEJpK`
  - artifact digest: `sha256:4e8ac0df4bf99d4e60a8222c4b735a52dfcf5846425787dea74ff01e9d22b11c`
- Windows installer now auto-detects the normal Foundry user-data locations and the known `G:\My Drive\D&D\Foundry Bridge` transport path when available.

The next step requires a bounded local install/restart/authorization action on the DM machine; no further remote implementation is needed before that runtime gate.


## Live Acq 3D MCP runtime validation — partial pass (2026-10-05)
With the bridge agent manually started and Foundry polling it:
- `inspect_3d_scene` passed live against `Ep1 - World Slice`;
- 3D Canvas reported active with live camera state, 11 3D Tiles, 11 lights and 5 regions;
- `search_3d_assets` passed and returned installed Mapmaking Pack assets from `canvas3dcompendium`;
- semantic manifest validation passed read-only;
- the Scene revision remained unchanged during these tests.

The first true-3D capture call returned a valid 1920x992 WebP payload but the pixels were black. Root cause is the capture implementation using `renderer.domElement.toDataURL()`, which is unreliable when the WebGL context does not preserve its drawing buffer. A v0.2.2 fix is staged to render into a Three.js WebGLRenderTarget and read pixels explicitly, following 3D Canvas's own export pattern. The same release also adds semantic cleanup so the disposable write gate can create and then remove a test object safely.

Current local runtime remains on the prior installed module until v0.2.2 is installed/reloaded.


## Acq 3D MCP v0.2.3 live read path — PASSED (2026-10-05)
After installing/reloading the v0.2.3 Foundry module:
- live 3D inspection still passes;
- the fixed render-target capture now returns a 1920x992 WebP payload of ~154 KB instead of the previous ~5 KB black frame, confirming that the WebGLRenderTarget/readRenderTargetPixels path is producing non-empty scene imagery;
- Scene revision remained unchanged during capture;
- semantic apply dry-run passed with the current revision and correctly planned creation of the disposable Tile.

The remaining infrastructure gate is a single actual disposable semantic Tile create/delete transaction. ChatGPT's current custom-plugin permission/safety layer blocks the non-dry-run write call even though dry-run is allowed, so the next user action is to allow low-risk writes for the Acq 3D Map plugin (or otherwise approve writes) and retry.
