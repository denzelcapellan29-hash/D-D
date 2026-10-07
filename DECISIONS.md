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


## ADR-007 — Foundry + 3D Canvas is the primary campaign runtime
**Status:** Accepted  
**Date:** 2026-10-05

### Decision
Select **Foundry VTT + 3D Canvas** as the primary campaign runtime after a renewed comparison with TaleSpire, Minecraft/Fabric, The RPG Engine, RPG Stories, Menyr and emerging 3D VTTs.

### Why
The project requires all of the following simultaneously:
1. high-quality player-facing 3D presentation;
2. autonomous programmatic scene creation and repair;
3. structural/readback QA;
4. D&D5e campaign documents, actors, items, journals and encounters;
5. long-term maintainability and versioned automation;
6. minimal DM-side preparation.

Foundry + 3D Canvas is the only currently mature candidate that satisfies all six at once, and the project has already empirically validated most of its control plane.

### Important implementation correction
Do not repeat the earlier custom-GLB-first approach.

Use an **asset-first semantic resolver**:
semantic object/material -> existing 3D Canvas asset/material/environment whenever suitable -> custom geometry only when necessary.

Scene content should remain modular and bridge-addressable.

### Competitor conclusions
- **TaleSpire:** best out-of-box tabletop aesthetic; rejected as primary because the supported Symbiote API still cannot persist board-state edits/place tiles. Retained as immediate fallback.
- **The RPG Engine:** capable 3D world builder with terrain sculpting, campaign building and Workshop content; no sufficiently documented external automation API found, and its public Steam build has been unchanged since April 2025. Not suitable for the autonomous prep loop.
- **RPG Stories:** actively developed, strong procedural/auto-room builder, Workshop and UVTT export; useful map-building product but no comparable external programmatic control surface found.
- **Menyr:** visually ambitious and procedural, but still beta/unreleased with VTT features explicitly still arriving.
- **Minecraft/Fabric:** excellent deterministic control, but too much visual-engineering burden for the desired player-facing experience.
- **Merlin and other Foundry/Unreal hybrids:** architecturally interesting but not production-ready enough for this campaign.

### Runtime policy
Pin a known-good Foundry/3D Canvas version set for the campaign and upgrade only after clone-based compatibility testing.

### Final kill criterion
Perform one bounded asset-first vertical-slice rebuild. If Foundry still cannot meet the visual/world-feel standard without disproportionate engineering effort, switch directly to TaleSpire. No third round of Minecraft visual infrastructure work.


## ADR-008 — Thin 3D adapter + off-the-shelf generic Foundry APIs
**Status:** Superseded by ADR-009  
**Date:** 2026-10-05

### Decision
Avoid building a bespoke replacement for Foundry's entire campaign API.

Use:
- **Foundry V14 core** for Scenes, Scene Levels/Regions, documents and backups;
- **3D Canvas + Mapmaking Pack** for the player-facing 3D runtime and asset vocabulary;
- **Acq Foundry Bridge** as a thin, declarative, revision-checked adapter only where the project has genuinely specialized requirements: 3D Canvas tile/model/environment data, semantic build identity, asset upload, camera framing/capture and visual QA;
- **Foundry API Bridge / Foundry MCP** as the preferred optional generic campaign-management sidecar when account/plan/cost conditions allow it, rather than duplicating its actor/item/journal/table/compendium/token/combat/time/UI tool surface.

### Runtime baseline
Pin the vertical-slice test to the known-good/current stack:
- Foundry 14.368
- D&D5e 6.0.5
- 3D Canvas 9.0.35
- Mapmaking Pack 10.0.1
- libWrapper
- Acq Foundry Bridge
- Advanced Tools 9.0.3 optional

### V14 migration rule
Do not build a fresh V14 scene around the retired Levels/Wall Height module architecture. Use core Scene Levels/Regions. Legacy module installs may be used only for migration if required.

### Asset/build rule
Treat 3D Canvas Tiles as the normal geometry primitive. Resolve semantic scene objects to installed asset/material references first. Custom GLB generation is reserved for source-specific geometry not represented adequately by the asset ecosystem.

Every generated object must be addressable by stable semantic/build flags so scene application is idempotent and repairable.

### Safety
- No arbitrary remote eval/shell.
- Script macros remain disabled for generic remote bridges unless separately justified.
- Meaningful writes require scene revision checks and a recoverable pre-write state.
- Live Foundry User Data must not be placed inside bidirectional cloud-sync storage; Drive is transport/artifact storage only.
- Foundry package backups are supplemented by separately versioned generated/custom multimedia assets because package backups do not necessarily include assets stored outside package directories.

### Hosting
Stay local for the vertical-slice test. Dedicated/hosted Foundry is a later deployment concern and is not allowed to become another infrastructure project before the visual/runtime gate passes.


## ADR-009 — Direct MCP control optimized for autonomous 3D campaign prep
**Status:** Accepted  
**Date:** 2026-10-05

### Decision
Because the DM's ChatGPT environment supports custom MCP connections, make MCP the normal control plane rather than Google Drive command files.

Use two deliberately separated MCP surfaces:

1. **Foundry API Bridge / Foundry MCP** for generic Foundry/D&D5e operations. This is the wheel we do not rebuild: actors, items, journals, roll tables, scenes, tokens, doors, combat, compendiums/import, world time, pause and UI.
2. **Acq 3D MCP** for specialized campaign/world authoring operations that are unique to this project and 3D Canvas: semantic asset lookup, 3D Tile/model/environment properties, semantic IDs/build IDs, specialized asset upload, canonical camera framing/captures, idempotent scene application and repair, and visual-QA readback.

Connect the private Acq 3D MCP through OpenAI Secure MCP Tunnel. Reuse the existing Acq Foundry Bridge implementation behind it rather than writing another Foundry integration from scratch.

### Why
The infrastructure is being optimized for the actual product, not for generic VTT automation:
- ChatGPT should prepare and maintain the campaign;
- the semantic campaign/world model stays canonical;
- player-facing presentation must meet the 3D world-feel bar;
- source-grounded set pieces and GM-only state must survive export;
- writes need revision checks/recovery;
- visual QA must be machine-driven;
- and routine prep must not turn into DM-side scripting/debugging.

### Foundry MCP boundary
Use the hosted Foundry MCP service when the DM accepts its subscription/privacy tradeoff. Its current Dungeon Master tier exposes the broad campaign tool surface needed here and supports ChatGPT OAuth.

Keep script macros disabled. Do not depend on its code-mode execute path for transactional world-building; its own documentation states scripts are not transactional.

### Acq 3D MCP boundary
Do not expose arbitrary JavaScript, shell or database access. Provide small semantic tools such as:
- inspect_3d_scene
- search_3d_assets
- apply_semantic_objects
- place_or_update_3d_tile
- set_3d_environment
- set_or_update_light
- frame_semantic_region
- capture_3d_view
- validate_scene_manifest
- snapshot_scene
- restore_scene_snapshot

Each write carries scene/build identity and expected revision where applicable.

### Transport/persistence
- Direct MCP is the normal interactive control plane.
- Google Drive remains private-source, artifact, release, capture and backup storage plus emergency fallback transport.
- GitHub remains canonical for code/config/schemas/architecture/project tracking.
- Live Foundry remains runtime/play state, not canonical campaign semantics.

### Dependency verification correction
Do not assume V14 core Scene Levels eliminated every 3D Canvas legacy dependency. Current published sources disagree: the 3D Canvas V14 wiki still names Levels/Wall Height/socketLib while the public V14 source manifest lists only libWrapper as required. Verify the installed 9.0.35 manifest/runtime before changing dependencies.


## ADR-010 — Render-verified Foundry/3D Canvas authoring doctrine
**Status:** Accepted  
**Date:** 2026-10-06

### Decision
Treat `docs/FOUNDRY_3D_CANVAS_DOMAIN_KNOWLEDGE.md` as required project domain knowledge before any production Foundry/3D Canvas authoring.

The operational standard is:

1. use hosted Foundry MCP for generic Foundry/D&D5e operations;
2. use the actually connected Acq 3D MCP tool surface for specialized 3D Canvas inspection/authoring/QA;
3. use the underlying Drive bridge protocol only as an explicit fallback for capabilities not exposed by MCP;
4. use 3D Tiles as the normal 3D architecture primitive;
5. prefer installed assets/materials before procedural meshes and custom GLBs;
6. reproduce the supported 3D Canvas Tile initialization lifecycle instead of assuming arbitrary valid Tile JSON is runtime-equivalent;
7. require live runtime bounds and a visible 3D renderer capture before declaring visual work complete;
8. test new construction techniques on a disposable scratch Scene before production;
9. use revision-checked writes and recoverable state for meaningful changes;
10. treat V14 installed runtime behavior as authoritative when older tutorial material conflicts with current behavior.

### Why
The Episode 1 full-dungeon attempt demonstrated that Foundry document validity and Tile counts can coexist with a blank or malformed live 3D Canvas render. The project therefore requires render-verified acceptance rather than document-level acceptance.

### Consequences
- No production Area 3-10 rebuild resumes until a scratch Scene with a floor, model Tile, light, environment and camera passes live 3D capture.
- Serialized Scene JSON is useful for inspection/import/debugging but is not the canonical proof of a working 3D Scene.
- Camera targets are derived from live 3D runtime bounds, not raw Foundry Scene pixel positions.
- Bulk authoring follows small reversible proof batches before scaling.
- Tutorial concepts are retained, but version-sensitive UI/dependency instructions are checked against Foundry V14 and the installed 3D Canvas version.


## ADR-011 — Bridge owns 3D Canvas runtime recovery
**Status:** Accepted  
**Date:** 2026-10-06

### Decision
Camera and capture calls must not assume that 3D Canvas is already active. The Acq Foundry Bridge is responsible for ensuring the runtime is active and ready before operating on the 3D camera or renderer.

The recovery sequence is:
1. inspect runtime availability/readiness;
2. if already stable, continue;
3. if inactive, call the installed 3D Canvas runtime toggle API;
4. wait for active + ready + renderer + scene graph + camera + controls + zero loading Tiles;
5. if the first activation attempt does not stabilize, use the runtime reload/toggle-cycle recovery path;
6. fail with explicit runtime-state diagnostics rather than returning black/stale captures.

### Consequences
- The DM should not be asked to manually toggle 3D Canvas during normal prep.
- Black or unavailable captures are treated as control-plane/runtime faults first, not scene-art faults.
- Production build loops remain fail-fast: small write -> inspect -> rendered capture -> continue.


## ADR-012 — Fail-fast execution is the default prep standard
**Status:** Accepted  
**Date:** 2026-10-06

### Decision
Use fail-fast execution for Foundry/3D Canvas, bridge/infrastructure work, exporters, and other risky campaign-prep changes.

The mandatory loop is:
1. inspect current state/revision;
2. apply the smallest meaningful reversible batch;
3. inspect structural/runtime state;
4. validate the actual player-facing result;
5. accept the checkpoint before continuing.

For 3D Canvas, a rendered capture is the acceptance test. API success, valid JSON, document counts, and created Tiles are insufficient by themselves.

At the first unexpected failure, stop production changes and diagnose only the failing layer. Do not stack speculative fixes. Allow at most one targeted recovery/retry unless the DM explicitly authorizes deeper troubleshooting. If that retry fails or local DM action is required, return immediately with the last known-good checkpoint, exact failed operation, verified/uncertain state, and smallest required DM action.

Black/blank 3D captures or inability to inspect/frame/capture the live 3D runtime are hard stops.

Recurring manual recovery steps should be moved into bridge/tooling automation. Known local infrastructure paths, versions, launch commands, and bridge topology must be persisted and consulted rather than rediscovered.

### Rationale
This standard materially shortened fault isolation during the Episode 1 rebuild:
- stale revisions were separated from malformed scene objects;
- 3D runtime failures were separated from geometry failures;
- bad pool asset choices were caught before propagation;
- scene-bound coordinate clamping was discovered before later Areas were built on corrupted coordinates;
- bridge gaps were upgraded rather than repeatedly offloaded to the DM.

### Persistence
The same standard is recorded in the Google Drive `PROJECT_INSTRUCTIONS` document and should remain synchronized with the ChatGPT Project Instructions field.


## ADR-013 — Large-scene bounds and underground ground-first workflow
**Status:** Accepted
**Date:** 2026-10-06

### Decision
For large Foundry/3D Canvas scenes, scene dimensions must be validated before extending geometry beyond the initial footprint. Unexpected relocation, stacking, or compression of distant geometry must be treated as a spatial/control-plane fault until live Foundry coordinates and 3D runtime bounds prove otherwise.

For Episode 1 and similar underground builds:
1. resize the Scene to the intended footprint before large-area placement;
2. prove out-of-bounds placement with one test object and rendered capture;
3. establish believable environmental ground/context before completing all encounter rooms;
4. replace exposed white/tabletop surfaces early with broad dirt/rock/cavern context;
5. test one material treatment before promoting it scene-wide and reject obvious UV striping/repetition;
6. build each area in accepted layers: ground/shell -> structure -> source-visible dressing -> encounter/mechanics;
7. use rendered 3D captures as the acceptance test after each meaningful batch.

### Evidence
The `Example` scene originally clamped distant Episode 1 Tiles to x≈6000. After resizing the Scene to 22649×11218, x>6000 geometry rendered at the intended coordinates. A first ground material test produced obvious striping and was rejected; a simpler dirt texture treatment passed visual QA and was promoted across the underground footprint.

### Consequences
Do not compensate for scene-bound clamping with distorted geometry. Fix scene extent or bridge/tooling first. Underground environment context is now a first-class build layer, not post-polish.


## ADR-014 — Natural cavern construction and asset QA policy
**Status:** Accepted
**Date:** 2026-10-06

### Decision
Natural cavern visuals must use asset families that pass live 3D capture, not merely assets that exist in the installed library.

Current accepted Episode 1 approach:
- broad dirt/rock environment context;
- high-end boulder models for irregular cavern boundaries;
- source-visible dressing added only after the shell passes rendered QA.

Rejected for Area 5 after capture:
- stretched `small-cave.glb` terrain: white block;
- Kenney cave-cliff model: wrong/stylized silhouette;
- standing-bag cocoon surrogate: visibly a sack;
- dynamic `sphere` cocoon primitive: invalid wedge;
- white-egg cocoon surrogate: invalid wedge.

When an authored prop does not exist, prefer a purpose-built generated asset over an obviously wrong substitute.

### Runtime/tooling consequence
The bridge's generated-asset upload operation currently fails because `acq-foundry-bridge` does not enable Foundry package `persistentStorage`. Fix that bridge capability before relying on custom-asset upload in production.

A hidden Foundry Tile is not proof that its live 3D object was removed. If a hidden/rejected Tile remains visible after `reload_3d_scene`, treat the 3D runtime as stale and stop scene mutations until runtime state is clean.


### Verified implementation addendum to ADR-013/014 (2026-10-06)
For the accepted Episode 1 ground treatment, use six broad Dynamic Mesh boxes at elevation=1 and depth=4 with collision/sight disabled; set `imageTexture` to `modules/canvas3dcompendium/assets/TheMadCartographerTexturePack/Texture-Dirt.webp`, `fillType="stretch"`, `textureRepeat=4–6`, and muted dark earth tints. An earlier `Ground010_Color.webp` attempt with `fillType="tile"` and `textureRepeat=14` produced severe striping and was rejected. Check real runtime surface heights when adding props: 600px `Floor_Modular.glb` at elevation=-0.6 reached y≈0.588, occluding pools placed at y≈0.

Area 5's accepted cavern-floor/high-end-boulder boundary must remain unchanged while rejected cocoon test `ep1.a5.cocoon.test` remains hidden in the Foundry document but instantiated in live Three.js. Do not add cocoons until runtime cleanup and `persistentStorage`-enabled generated asset upload have been separately proven.
