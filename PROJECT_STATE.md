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
