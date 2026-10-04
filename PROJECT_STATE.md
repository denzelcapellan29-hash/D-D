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
v0.3 structural cleanup is complete. Continue from this controlled coordinate world: improve urban grammar/material fidelity inside the authored envelope, then run end-to-end warehouse → fissure → dungeon QA before promotion.

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
