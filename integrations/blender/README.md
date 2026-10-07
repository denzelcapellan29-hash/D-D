# Blender authoring / QA stage

Blender is an authoring, procedural-generation and visual-QA stage. It is not the canonical campaign model and it does not own D&D mechanics.

## Responsibilities

Blender may:
- build structural geometry from semantic spaces/features;
- resolve approved modular assets and material families;
- generate constrained decorative scatter;
- create lights/atmosphere;
- place visual creature markers/miniatures from semantic entities;
- render fixed QA cameras;
- export GLB/glTF plus a machine-readable export manifest.

Blender must not:
- invent adventure facts silently;
- alter encounter mechanics;
- move tactical entities for composition without an explicit playability-change;
- become the only location where geometry/intent is stored;
- overwrite released assets silently.

## Required object metadata

Every generated Blender object should carry:
- acq.semantic_id
- acq.build_id
- acq.classification
- acq.provenance
- acq.asset_role when asset-backed

Collections:
- STRUCTURE
- TACTICAL
- TERRAIN
- PROPS
- LIGHTING
- CREATURES
- FX
- CAMERAS
- EXPORT

## Safe MCP surface

The connected Blender MCP should expose the smallest practical set of operations:

1. health/version/current-file inspection
2. inspect semantic objects and collection bounds
3. execute an idempotent semantic build/update
4. search/link approved local assets
5. apply material/lighting profiles
6. render a named camera to an image
7. validate scale/bounds/object metadata
8. export selected semantic roots to GLB
9. save a versioned .blend checkpoint

Arbitrary viewport clicking is not part of the production path.

## Fail-fast cycle

For each meaningful change:

inspect current state -> apply one reversible batch -> structural validation -> render named QA camera -> visually accept/reject.

At the first blank/black/malformed render, stale semantic revision, invalid scale, missing asset, or unexplained runtime state: stop production changes and diagnose only that layer. Allow one targeted retry.

## Export contract

Blender export output must include:
- GLB path
- semantic scene id
- build id
- source semantic revision/hash
- axis/scale transform
- world-space bounds
- exported semantic IDs
- collision intent where relevant
- material/texture dependency summary
- QA render references

Foundry/3D Canvas consumes this output as a runtime artifact. It must not infer geometry from Blender object names alone.
