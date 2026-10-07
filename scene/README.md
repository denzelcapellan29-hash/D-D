# Platform-independent semantic scene

This directory defines the canonical scene contract used between campaign semantics, deterministic spatial generation, authoring tools and runtime exporters.

## Rule

The semantic scene is authoritative for generated world interpretation. Blender, Foundry/3D Canvas, Minecraft and TaleSpire are runtime/export targets. Never convert one runtime directly into another.

Pipeline:

Adventure/source -> semantic campaign/world model -> deterministic spatial engine -> semantic scene -> Blender authoring/QA -> runtime exporters.

## Coordinate convention

- Right-handed coordinates.
- Z is up.
- Semantic distances use the scene's declared distance unit.
- Grid size is explicit; no runtime may infer scale.
- Runtime adapters are responsible for axis/scale conversion.
- Stable semantic IDs survive every export.

## Layers

Spaces define inhabitable/world context and vertical envelopes.

Features define structural, tactical, decorative, atmospheric and GM-only objects.

Entities define PCs/NPCs/creatures/hazards/markers independently of visual assets.

Presentation defines art-direction profiles and fixed QA camera stations.

Runtime bindings contain only runtime-specific references and revisions; they must not become the source of authored facts.

## Provenance

Every authored feature/entity must identify one of:

- source-grounded
- procedural-interpretation
- platform-adaptation
- playability-change
- original-connective

This prevents visual/world-building additions from being confused with adventure facts.

## QA

A semantic scene is not accepted because an exporter succeeds. Each visual runtime requires an actual rendered acceptance view. Blender and Foundry/3D Canvas both use named QA cameras. A blank, black, malformed or uninspectable render is a hard stop.
