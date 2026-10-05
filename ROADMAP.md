# Roadmap

## NOW — Foundry asset-first vertical slice

1. **Bring the existing Foundry instance back online; do not reinstall by default.**
   - Expected persisted baseline: Foundry 14.368, D&D5e 6.0.5, world `Acq WorldGen Test`.
   - Verify live module versions and current scene state through the bridge before changing anything.

2. **Verify the live 3D Canvas dependency graph before changing modules.**
   - Foundry 14.368
   - D&D5e 6.0.5
   - 3D Canvas 9.0.35
   - 3D Canvas Mapmaking Pack 10.0.1
   - Acq Foundry Bridge
   - libWrapper as indicated by current source manifest
   - Advanced Tools optional
   - Published 3D Canvas V14 docs and source disagree about Levels/Wall Height/socketLib; inspect the installed 9.0.35 manifest/runtime and preserve whatever it actually requires. Do not remove or add legacy dependencies by assumption.

3. **Recover/sync the most capable Acq Bridge implementation before extending it.**
   - Compare current repo v0.1 source with the previously proven v0.1.9-era Drive/release artifacts.
   - Restore only missing project-specific capabilities: camera/capture, semantic bounds, 3D environment/tile authoring, revision checks.
   - Do not rebuild generic actor/item/journal/combat/compendium APIs if Foundry MCP can provide them.

4. **Direct Foundry MCP connection — PASSED.**
   - ChatGPT OAuth + Foundry WebSocket linkage is verified live against `Acq WorldGen Test`.
   - Guest-tier `world-info` and live dice execution passed.
   - Permission probes confirmed Free / Adventurer / Dungeon Master boundaries.
   - **Next DM action:** upgrade to Dungeon Master (€10/month) if proceeding; it is justified by required scenes/tokens/combat/compendiums/time/UI access.
   - Keep Allow Script Macros off.
   - **DM tier active and validated:** scene enumeration/readback, compendium enumeration, token readback and world-time access all passed live. Next validate compendium search/import and combat on disposable/test content before first production use.
   - Generic MCP screenshots are 2D Foundry-canvas captures, not 3D Canvas truth; build the private Acq 3D MCP for 3D authoring/camera/capture.
   - Google Drive remains fallback transport/artifact storage rather than the normal command path.

5. **Build a machine-readable 3D Canvas asset catalog from installed modules.**
   - Resolve semantic roles to existing Mapmaking Pack asset paths/materials.
   - Dock Ward masonry/timber/roofing/cobbles/quay/harbor props.
   - Warehouse structure/clutter.
   - Fissure/rubble/cavern assets.
   - Area 1/Area 2 architecture and lighting/environment presets.
   - Store references/metadata, not redistributed third-party assets.

6. **Rebuild exactly one continuous vertical slice.**
   lower Dock Ward street -> warehouse exterior -> warehouse interior -> earthquake fissure -> descent -> Area 1 -> Area 2.

7. **Authoring rules.**
   - Core V14 Scene Levels/Regions for vertical organization.
   - 3D Canvas Tiles for modular geometry, collision, sight and doors.
   - Existing assets/materials first.
   - Custom GLB only for source-specific geometry.
   - Stable `flags.acq.semantic_id` and `flags.acq.build_id` on generated objects.
   - Revision-checked, idempotent scene application.

8. **Programmatic QA and release optimization.**
   - Structural scene manifest assertions.
   - Expected tiles/regions/lights/doors/actors/journals.
   - Six canonical close/medium/wide camera captures.
   - Performance sanity check.
   - Duplicate scene before bulk optimization; merge compatible static tiles only after QA and skip doors.

9. **Platform gate.**
   - PASS -> Foundry + 3D Canvas becomes campaign production runtime; propagate accepted grammar to Areas 3-10.
   - FAIL -> stop Foundry after this bounded pass and move directly to TaleSpire slab export. Do not resume Minecraft visual-polish infrastructure.

## Retained secondary targets
- Minecraft/Fabric: deterministic engineering/export target and procedural reference.
- TaleSpire: immediate fallback if the Foundry asset-first slice fails.
