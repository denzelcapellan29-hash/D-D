# D&D / Acq WorldGen

Platform-independent procedural 3D environment generation for D&D adventures, beginning with *Acquisitions Incorporated* Episode 1.

Canonical pipeline:

```
Adventure specification
→ Semantic World Model
→ Procedural Spatial / Geometry Engine
→ Platform-independent Scene
→ Exporters
```

Current exporter/feasibility work:
- Minecraft Java / WorldEdit `.schem`
- Foundry VTT + 3D Canvas GLTF/GLB
- TaleSpire remains a candidate

Project code, schemas, configuration, tests and documentation belong in this repository. Private/copyrighted source material and large generated artifacts belong in the connected Google Drive `D&D` folder.

## Current integration work

See `integrations/foundry-bridge/` for the Acq Foundry Bridge pseudo-connector.
