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
Continue visual/world-feel iteration inside the bounded Episode 1 corridor, continue bounded visual/world-feel polish, then restore reliable rendered-view capture for autonomous visual QA.

## Scope gate
Do not expand to full Waterdeep or D&D gameplay systems until the Dock Ward waterfront → warehouse → fissure → dungeon vertical slice is convincingly playable and can be maintained autonomously.


## Coordinate working grid
The Minecraft runtime now has an explicit coordinate-based working-area contract in `integrations/minecraft-bridge/workspace.json`.
- Surface datum: Y=100.
- Planning origin: world (-80,100,0), giving local u=x+80, v=z, h=y-100.
- Primary Episode 1 surface authoring envelope: x=-128..-32, y=96..160, z=-64..64.
- Current verified corridor remains x=-108..-48, y=96..125, z=-45..52.
- Future bridge writes should be rejected outside the authoring envelope unless explicitly overridden.
- Camera QA uses named coordinate stations rather than ad-hoc player movement.
