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


## ADR-005 — Keep Minecraft 26.3 runtime; adapt VibeCraft at the MCP/tool layer
**Status:** Superseded by ADR-006  
**Date:** 2026-10-05

### Context
VibeCraft is an MIT-licensed MCP-native Minecraft automation project with structured building tools, WorldEdit integration, spatial analysis, terrain/pattern/furniture helpers and explicit AI-control safety. Its published client-mod compatibility currently stops at Minecraft 1.21.4, while this campaign's validated runtime is Minecraft Java 26.3.

### Decision
Do not replace the working 26.3 Fabric bridge with VibeCraft's client mod.

Use VibeCraft as a reference/donor architecture for the higher-level MCP/tool layer above the existing bridge. Port or reimplement useful structured tool schemas, spatial-analysis ideas, deterministic build helpers, WorldEdit-aware batching and safety workflows while preserving the project's canonical semantic-world architecture.

### Consequences
- The validated Minecraft 26.3 world and bridge remain stable.
- We avoid a runtime downgrade or a second incompatible client-control stack.
- Higher-level build automation can mature without pushing repeated PowerShell/Python setup onto the DM.
- External code reuse must preserve attribution/license obligations where code is copied rather than reimplemented.
- Amulet remains optional; replacement of the validated low-level compiler is not a prerequisite for world-feel iteration.


## ADR-006 — Dedicated Fabric 26.3 authoring server with typed MCP control
**Status:** Accepted  
**Date:** 2026-10-05

### Decision
Use a **local dedicated Fabric 26.3 server** as the production authoring/control runtime for the Minecraft exporter.

Stack:
- Minecraft Java 26.3 dedicated Fabric server
- portable Java 25 bundled by project tooling
- Fabric API
- Acq Minecraft Bridge adapted to dedicated-server operation
- typed MCP facade above the bridge
- WorldEdit 7.4.6 beta-02 for bulk edits/schematics
- BlueMap 5.28 Fabric for actual-world visual QA
- deterministic semantic compiler and structural validators from this repository
- explicit region snapshots/inverse patches for transaction rollback

The existing singleplayer v0.5 world is not converted in place. Migration is first tested against a cloned save and promoted only after exact protected-core/block-state and QA equivalence checks pass.

### Why this over Paper
Paper 26.3 itself is viable, but changing server platform adds migration surface without solving a problem Fabric cannot solve. The current bridge is already written against Fabric/Minecraft server classes and has validated 26.3 behavior. Fabric dedicated-server mode removes the client-host dependency while preserving that implementation and the current world/toolchain.

Paper remains the fallback if a required server-only API or plugin cannot be provided cleanly on Fabric.

### Third-party bake-off
- **VibeCraft:** strong MCP schema/build-helper reference; published client-mod support currently stops at 1.21.4.
- **IotA-asce/minecraft-mcp:** strong Paper plugin/WebSocket/MCP reference with tests and player-less operations; useful donor/reference, not adopted wholesale.
- **Architect-Agent (TianYaYou):** best conceptual match for staging, token-compressed inspection, visual feedback and atomic rollback, but too young to be a production dependency and its dedicated-server documentation targets Paper 1.21.1.
- **Clankercraft:** mature MCP/WorldEdit tool surface, but uses a player-bot protocol layer that creates unnecessary version coupling for this project.
- **Mineflayer MCP implementations:** rejected for the 26.3 production path until stable protocol support catches up.
- **minecraft-ai-build-server:** validator/compiler and rollback concepts are strong references, but its current stack is pinned below 26.3.
- **GDMC HTTP Interface:** rejected for current runtime because its documented target is 1.21.11.
- **FAWE:** defer until 26.3 support is released/stable; use standard WorldEdit meanwhile.

### Operating rule
Routine infrastructure setup, QA, rendering and world iteration must not require the DM to debug Java, Python, PowerShell, browser capture or package compatibility. DM involvement is limited to a genuinely unavoidable install/restart/authorization action after the automation has been tested elsewhere.
