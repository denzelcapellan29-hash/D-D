# D&D / Acq Campaign Prep

Platform-independent campaign-prep tooling for D&D adventures, beginning with *Acquisitions Incorporated* Episode 1.

The project has evolved beyond procedural map generation. The target is a prep assistant that can build, maintain, inspect, and QA a playable 3D campaign so the DM can focus on running the game.

Canonical pipeline:

```
Adventure / campaign source
→ Semantic Campaign + World Model
→ Deterministic Spatial / Geometry Engine
→ Platform-independent Scene
→ Runtime / Exporters
```

## Active runtime

**Foundry VTT + 3D Canvas** is the active primary campaign runtime and prep target.

The Acq Foundry Bridge provides programmatic access to the live world through:

```
ChatGPT
→ Google Drive transport
→ local bridge agent
→ Foundry module
→ Foundry / 3D Canvas
→ state, results, and pixel captures
→ ChatGPT
```

Verified bridge capabilities include scene/world manipulation, generated asset upload, programmatic pixel capture, semantic Regions and Notes, Journals, D&D5e compendium search, and direct 3D Canvas camera framing.

Minecraft Java / WorldEdit remains a verified procedural/export target. TaleSpire remains a serious candidate if Foundry does not pass the visual/world-feel quality gate.

## Design goal

Environments should work at three scales:

- **World:** districts, roads, landmarks, travel context.
- **Location:** streets, warehouse districts, buildings, caves, ruins, surrounding terrain and architecture.
- **Encounter:** combat rooms, traps, boss chambers and set pieces.

The immediate quality gate is a high-fidelity vertical slice:

**Waterdeep street / warehouse district → warehouse exterior/interior → earthquake fissure → Area 1 → Area 2**

This slice determines whether Foundry can achieve the desired world feel before broader Episode 1 polish continues.

## Persistence

GitHub contains code, schemas, configs, tests, architecture and project tracking.

Google Drive `D&D` contains private/copyrighted source material, large generated assets, Foundry bridge transport, captures, review bundles and release binaries.

Do not commit copyrighted source PDFs or substantial copied source text to GitHub.

See [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md) for the durable operating rules.

## Integration

See `integrations/foundry-bridge/` for the Acq Foundry Bridge pseudo-connector.
