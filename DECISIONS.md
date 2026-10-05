# Decisions

## ADR-001 — Decouple Minecraft geometry from visual material profiles
**Status:** Accepted  
**Date:** 2026-10-04

### Decision
Treat Minecraft world geometry/block-state placement as a stable spatial/runtime layer and treat appearance as a separate visual profile.

A visual profile maps Minecraft block IDs/block states to:
- representative RGB/hex color for fast headless QA,
- one or more texture references for higher-fidelity headless rendering,
- transparency/emissive flags,
- optional model/face metadata when a resource pack changes block geometry.

The same canonical scene/world geometry may therefore be evaluated against multiple resource packs without rebuilding the world.

### Consequences
- Fast QA uses colored voxel reconstruction directly from bridge `/region` data.
- Higher-fidelity QA can resolve actual pack textures/models later.
- Resource-pack iteration does not require regenerating the semantic world or changing coordinates.
- Minecraft screenshots are diagnostic only, not the primary QA loop.
- Final delivery can be a prebuilt Minecraft world save plus an optional chosen visual/resource profile.

### Delivery strategy
The target workflow is:
semantic campaign/world model → deterministic world build → world-file/chunk output → structural QA → headless visual QA → optional resource-pack comparison → release ZIP.

The DM should normally receive/import a finished world rather than manually constructing it in Minecraft.


## ADR-002 — Coordinate-controlled construction envelope
**Status:** Accepted  
**Date:** 2026-10-04

### Decision
Treat the active Minecraft build as a coordinate-controlled authored volume rather than inheriting arbitrary vanilla terrain outside the current campaign workspace.

Current Episode 1 surface envelope:
- X: -144 .. 32
- Y: 96 .. 160
- Z: -96 .. 96
- Surface datum: Y=100
- Neutral lower datum outside authored space: Y=96

Uncontrolled above-ground geometry outside the current envelope may be cleared in compiler releases. The authored envelope expands deliberately as the semantic world grows.

### Consequences
- Vanilla grass/legacy procedural clutter cannot leak into the visible working world by accident.
- Structural QA has an exact spatial contract.
- World expansion becomes a deterministic compiler operation rather than uncontrolled exploration/worldgen.
- Neutral space outside the envelope is temporary construction context, not canonical Waterdeep geography.


## ADR-003 — Episode 1 targets the lower Dock Ward, not full Waterdeep
**Status:** Accepted  
**Date:** 2026-10-04

### Decision
For Episode 1, generate only enough of Waterdeep's lower Dock Ward to support a convincing persistent approach from harbor/street context to the warehouse, fissure and subterranean encounter chain.

Full-city Waterdeep generation is explicitly a stretch goal.

### Consequences
- Generator effort prioritizes density, continuity, visual polish and playability over geographic breadth.
- Non-playable background context may imply a larger city without requiring full simulation or construction.
- Later episodes may expand the semantic city/world model outward from the same coordinate system.


## ADR-004 — Layered Minecraft QA stack
**Status:** Accepted  
**Date:** 2026-10-04

### Decision
Use separate tools for different QA responsibilities rather than forcing the Minecraft client to be the inspection surface.

- Direct VTK renderer: primary fast engineering renderer from actual world-save block/state data.
- BlueMap: resource-pack-aware renderer of the actual Minecraft save and visual truth check before releases.
- PyVista: optional higher-level analysis/visualization layer, not a hard production dependency.
- Amulet Core: candidate world-I/O backend only after a non-destructive real-world load/save/reopen compatibility probe passes.
- Minecraft screenshots/client camera: diagnostic fallback only.

### Consequences
- World generation and QA can run headlessly.
- Material/resource-pack experiments do not require manual Minecraft screenshots.
- Low-level compiler replacement is gated by compatibility tests rather than assumption.
- New world releases should follow tooling validation, not precede it.
