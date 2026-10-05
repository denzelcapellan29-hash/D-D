# Roadmap

## NOW — Foundry asset-first vertical slice

1. Pin and snapshot the Foundry runtime stack:
   - Foundry 14.368
   - 3D Canvas 9.0.35
   - Advanced Tools 9.0.3
   - Mapmaking Pack 10.0.1
   - compatible D&D5e V14 system

2. Reconnect/verify the existing Acq Foundry Bridge against the pinned stack:
   - state readback
   - revision-checked writes
   - asset upload
   - tiles/lights/walls/regions/notes/journals
   - actors/compendium
   - 3D camera framing and automated captures

3. Build a machine-readable 3D Canvas semantic asset catalog:
   - Dock Ward masonry/timber/roofing
   - cobbles/quay/harbor props
   - warehouse structure/clutter
   - fissure/rubble
   - cavern/subterranean assets
   - Area 1/Area 2 architectural vocabulary
   - lighting/environment presets

4. Rebuild exactly one continuous vertical slice:
   lower Dock Ward street -> warehouse exterior -> warehouse interior -> earthquake fissure -> descent -> Area 1 -> Area 2.

5. Use existing high-quality 3D Canvas assets/materials first.
   Generate custom GLBs only for source-specific geometry that the asset library cannot express.

6. Programmatic QA:
   - structural scene manifest checks
   - expected object/region/light/actor checks
   - collision/sight/door checks
   - six canonical close/medium/wide camera captures
   - performance sanity check

7. Platform gate:
   - PASS -> Foundry + 3D Canvas becomes campaign production runtime; propagate accepted grammar to Areas 3-10.
   - FAIL -> stop Foundry after this bounded pass and move to TaleSpire slab exporter. Do not resume Minecraft visual polish.

## Retained secondary targets
- Minecraft/Fabric: deterministic engineering/export target and procedural reference.
- TaleSpire: immediate fallback if the Foundry asset-first vertical slice fails.
- RPG Stories: watch as a world-builder/export tool, not current primary runtime.
- Menyr/Merlin/other emerging 3D VTTs: watchlist only until production-ready APIs and runtime maturity exist.
