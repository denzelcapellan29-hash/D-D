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

**Foundry VTT + 3D Canvas** is the primary campaign runtime.

**Blender** is the deterministic 3D authoring/render/QA stage for geometry or assets that benefit from procedural construction, stronger materials/lighting, or independent visual validation. Blender is not canonical and does not own D&D mechanics.

**Minecraft Java + Fabric + WorldEdit** remains a verified procedural/export target and engineering reference, not the current visual target.

**TaleSpire** remains an optional fallback/export candidate and a useful reference for modular tabletop readability.

The active control split is:

```
ChatGPT
├─ hosted Foundry MCP -> generic Foundry/D&D5e documents and mechanics
├─ Acq 3D MCP -> 3D Canvas inspection/assets/semantic placement/camera/capture
└─ Blender MCP -> deterministic scene build/materials/lighting/render/export
```

The canonical data flow remains runtime-independent:

```
Adventure/source
→ Semantic Campaign + World Model
→ Deterministic Spatial / Geometry Engine
→ Platform-independent Scene
→ Blender authoring/QA when useful
→ Runtime exporters
```

## Current Episode 1 scope

The immediate quality gate is deliberately limited to the **lower Dock Ward**, not all of Waterdeep:

**harbor edge → lower Dock Ward streets → warehouse exterior/interior → earthquake fissure → subterranean transition → Area 1 → Area 2**

Full Waterdeep is a stretch goal.

## QA architecture

QA is layered and runtime-specific:

- **Semantic/structural validation:** dimensions, connectivity, clearance, provenance, stable semantic IDs and deterministic seeds.
- **Blender:** fixed overhead/isometric/player-height/wide-context renders validate geometry, materials, lighting and dressing before export.
- **Foundry/3D Canvas:** live Three.js inspection plus actual renderer capture is the player-facing acceptance test.
- **Minecraft:** VTK/BlueMap remain available for the Minecraft exporter.
- A blank, black, malformed or uninspectable visual result is a hard stop; API success alone never counts as visual acceptance.

## Release workflow

```
semantic campaign/world model
→ deterministic spatial build
→ platform-independent semantic scene
→ Blender procedural authoring + visual QA when required
→ versioned GLB/assets + export manifest
→ Foundry/3D Canvas semantic import
→ live 3D renderer QA
→ released campaign scene
```

Runtime exporters may also target Minecraft or a future TaleSpire path from the same semantic scene. Never convert Minecraft/Foundry/TaleSpire output into another runtime.

## Persistence

GitHub contains code, schemas, configs, tests, architecture and project tracking.

Google Drive `D&D` contains private/copyrighted source material, large generated assets, bridge transport, captures, review bundles and release binaries.

Do not commit copyrighted source PDFs or substantial copied source text to GitHub.

See [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md) for durable operating rules and [PROJECT_STATE.md](PROJECT_STATE.md) for current dynamic status.
