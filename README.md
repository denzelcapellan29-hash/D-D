# D&D / Acq Campaign Prep

Platform-independent campaign-prep tooling for D&D adventures, beginning with *Acquisitions Incorporated* Episode 1.

The target is a prep system that can build, maintain, inspect, QA, and release a playable campaign world while the DM focuses on running the game.

Canonical pipeline:

```
Adventure / campaign source
→ Semantic Campaign + World Model
→ Deterministic Spatial / Geometry Engine
→ Platform-independent Scene
→ Runtime / Exporters
```

## Active runtime

**Minecraft Java 26.3 + Fabric + WorldEdit** is the active primary campaign runtime.

The Acq Minecraft Bridge provides live-world control and inspection through:

```
ChatGPT
→ Google Drive command/result transport
→ local bridge agent
→ Fabric bridge mod
→ Minecraft world
→ live region state / QA results
→ ChatGPT
```

Current bridge capabilities include bounded live block edits, compressed region inspection, coordinate-controlled authoring, and automated structural readback.

Foundry VTT + 3D Canvas remains an evaluated exporter/runtime path rather than the current production target. TaleSpire remains a possible future exporter if a later campaign need justifies it.

## Current Episode 1 scope

The immediate quality gate is deliberately limited to the **lower Dock Ward**, not all of Waterdeep:

**harbor edge → lower Dock Ward streets → warehouse exterior/interior → earthquake fissure → subterranean transition → Area 1 → Area 2**

Full Waterdeep is a stretch goal.

## QA architecture

Minecraft client screenshots are diagnostic only. Normal QA is headless and layered:

- **Direct VTK renderer:** fast engineering views from the actual world save.
- **BlueMap:** resource-pack-aware visual truth check against the actual Minecraft world before release.
- **PyVista:** optional higher-level analysis/visualization layer.
- **Amulet Core:** candidate safer world-I/O backend, gated by a non-destructive real-world load/save/reopen probe.
- **Structural validators:** support/connectivity, terrain bleed, protected-core integrity, and block-state checks.

World geometry and visual appearance are intentionally decoupled: stable block/state geometry can be evaluated under multiple visual/resource profiles without rebuilding the campaign world.

## Release workflow

```
semantic world model
→ deterministic world build
→ Minecraft save compiler
→ structural QA
→ VTK/PyVista engineering QA
→ BlueMap resource-pack-aware QA
→ packaged direct-import world release
```

The DM should normally receive a finished world save rather than manually assembling schematics or debugging generated geometry.

## Persistence

GitHub contains code, schemas, configs, tests, architecture and project tracking.

Google Drive `D&D` contains private/copyrighted source material, large generated assets, bridge transport, captures, review bundles and release binaries.

Do not commit copyrighted source PDFs or substantial copied source text to GitHub.

See [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md) for durable operating rules and [PROJECT_STATE.md](PROJECT_STATE.md) for current dynamic status.
