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

5. **Install and validate the staged Acq 3D MCP control plane.**
   - Updated bridge code now includes direct loopback RPC, 3D inspect/camera/capture, asset search, semantic idempotent apply and manifest validation.
   - **CI/syntax gate PASSED**; validated package is in Google Drive releases.
   - Package/install updated Foundry module and local MCP stack.
   - Connect it with OpenAI Secure MCP Tunnel.
   - **PASSED:** read-only 3D inspection, asset search, true 3D render-target capture, revision-checked semantic Tile create, verification, and cleanup all succeeded. Scene returned to 11 Tiles and the original baseline revision. Infrastructure gate is closed.
   - No production scene writes until this passes.

6. **Build a machine-readable 3D Canvas asset catalog from installed modules.**
   - Source roles and query vocabulary are defined in `campaign/episode1/asset_requirements_v1.json`.
   - **Live candidate sweep completed:** `campaign/episode1/asset_catalog_v0_1.json` now records validated installed candidates and explicit gaps.
   - Install/load Acq Foundry Bridge v0.2.4 so clean helper-free captures and runtime model bounds are available before production placement.
   - Resolve semantic roles to existing Mapmaking Pack asset paths/materials.
   - Dock Ward masonry/timber/roofing/cobbles/quay/harbor props.
   - Warehouse structure/clutter.
   - Fissure/rubble/cavern assets.
   - Area 1/Area 2 architecture and lighting/environment presets.
   - Store references/metadata, not redistributed third-party assets.

7. **Rebuild exactly one continuous vertical slice.**
   - **STARTED:** Phase A surface context has its first production placement: 7 new semantic 3D Tiles, taking the scene from 11 to 18 Tiles without deleting legacy geometry.
   - Surface dressing expanded: warehouse rubble/timber, diegetic lamps, carts, neutral City Watch/cover NPCs.
   - Area 1 now has source-grounded debris and six hidden rats staged 3 + 3.
   - Area 2 now has four distinct pools, columns/supports and provisional double-door shells.
   - Next: load v0.2.5 for clean automated captures, visually tune placements, then build the remaining source-specific rope/bootprints/reliefs/lock details before any legacy swap.
   lower Dock Ward street -> warehouse exterior -> warehouse interior -> earthquake fissure -> descent -> Area 1 -> Area 2.

8. **Authoring rules.**
   - Core V14 Scene Levels/Regions for vertical organization.
   - 3D Canvas Tiles for modular geometry, collision, sight and doors.
   - Existing assets/materials first.
   - Custom GLB only for source-specific geometry.
   - Stable `flags.acq.semantic_id` and `flags.acq.build_id` on generated objects.
   - Revision-checked, idempotent scene application.

9. **Programmatic QA and release optimization.**
   - Structural scene manifest assertions.
   - Expected tiles/regions/lights/doors/actors/journals.
   - Six canonical close/medium/wide camera captures.
   - Performance sanity check.
   - Duplicate scene before bulk optimization; merge compatible static tiles only after QA and skip doors.

10. **Platform gate.**
   - PASS -> Foundry + 3D Canvas becomes campaign production runtime; propagate accepted grammar to Areas 3-10.
   - FAIL -> stop Foundry after this bounded pass and move directly to TaleSpire slab export. Do not resume Minecraft visual-polish infrastructure.

## Retained secondary targets
- Minecraft/Fabric: deterministic engineering/export target and procedural reference.
- TaleSpire: immediate fallback if the Foundry asset-first slice fails.


### QA-control follow-up
- v0.2.5 bounds/helper fix validated live.
- v0.2.6 is staged and CI-passed to add deterministic 3D runtime reload plus cleaner player-neutral captures.
- After loading v0.2.6: reload the active 3D runtime, capture the canonical surface/warehouse/Area 1/Area 2 views, then continue visual tuning. Do not delete legacy monolithic geometry until those captures pass.


### v0.2.6 live QA result
- **PASS:** full-scene inspection on the 61-Tile production scene.
- **PASS:** clean player-neutral capture path; large light helpers and hidden rat meshes are suppressed.
- **ART DIRECTION FAIL (expected at this stage):** legacy white/grid surface, sparse warehouse rupture dressing, and schematic Area 2 still require replacement/tuning.
- Runtime disconnected before the next reversible cobble probe could execute. Restore connections, then continue small visual probes before destructive legacy replacement.


### Runtime-back continuation
- **DONE:** recover live Foundry + Acq 3D MCP.
- **DONE:** reversible fissure-mouth and surface-context visual pass.
- **REJECTED/ROLLED BACK:** stretched-texture sidewalk/basin strips, crater model as fissure, thick cobbled-path model tiles.
- **NEXT:** refine Area 2 basins/door with solid/model geometry, then source-specific rope/bootprints/reliefs; legacy monolith remains until canonical QA passes.


### Episode 1 modular rebuild — ACTIVE
The `Example` scratch-scene renderer gate has passed. Resume production using the proven modular model-backed Tile method.

Immediate order:
1. replace/hide legacy full-dungeon visual Tiles while preserving Regions/notes/tokens/lights;
2. rebuild Areas 1–10 on their existing Region footprint coordinates using modular floors/walls;
3. add source-grounded landmarks per room;
4. capture and visually accept each major room/cluster;
5. preserve `Ep1 - World Slice` as the polished surface/warehouse transition and return scene;
6. finish Acquisitions Incorporated HQ after dungeon visual acceptance.

Do not return to monolithic GLB-first construction.


## Bridge / Area 5 follow-up
- Enable Foundry package `persistentStorage` for `acq-foundry-bridge`, validate `asset_upload`, and release as a versioned bridge upgrade before depending on generated runtime assets.
- Add a deterministic runtime cleanup/delete path that proves rejected/hidden 3D objects are removed from the live Three.js scene.
- After runtime cleanup is proven, resume Area 5 with five purpose-built hanging cocoon assets, then webs, hidden spider encounter state, and final QA capture.


## Resume gate — Area 5 after domain-knowledge persistence
1. Clear rejected `ep1.a5.cocoon.test` from the **live** Three.js runtime via a deterministic, targeted bridge cleanup (not merely `hidden=true`).
2. Verify absence with inspect + actual 3D capture; if it persists after one recovery, stop.
3. Fix the bridge package `persistentStorage` capability through a versioned upgrade and validate upload of an original cocoon GLB.
4. Place five source-grounded hanging cocoon props + webs and stage giant spider/occupants as GM-only encounter state. Run close + wide visual QA before continuing.


## Immediate visual next steps — 2026-10-07
1. Restore/verify healthy live 3D inspection on `Example`; no scene mutations until this passes.
2. Rebuild Area 5 with proven boulder-based cavern boundaries and organic cocoon props; one coherent write + one capture.
3. Continue Areas 6–10 using the same underground-context visual language and fast fail-fast cadence.
4. Revisit warehouse/fissure presentation after underground Areas 1–10 reach coherent visual completeness.


## Blender authoring/QA integration — 2026-10-07

1. **Expose the existing Blender MCP to this ChatGPT project.**
   - Verify health/version/current .blend and enumerate actual MCP operations.
   - Do not design around assumed Blender tool names.

2. **Run the disposable semantic smoke test.**
   - Input: `campaign/episode1/pipeline_smoke_test.scene.json`.
   - Build structural room, doorway, raised platform, one light and one medium-scale marker.
   - Preserve stable semantic IDs as Blender custom properties.
   - Render all four named QA cameras.
   - Hard stop on black/blank/malformed output.

3. **Validate Blender export contract.**
   - Export a versioned GLB.
   - Produce `blender_scene_contract.schema.json`-conformant manifest with bounds, scale/axis transform, semantic IDs, collision intent and QA references.
   - Re-open/inspect exported artifact when the MCP permits.

4. **Validate Foundry round-trip on disposable content.**
   - Upload/place the accepted GLB through Acq 3D MCP.
   - Use revision-checked writes.
   - Inspect live Three.js bounds.
   - Capture the actual 3D Canvas renderer.
   - Compare orientation/scale/material read against Blender reference.

5. **Promote only after PASS.**
   - Adapt the real Waterdeep street -> warehouse -> fissure -> subterranean -> Area 1 -> Area 2 vertical slice into semantic scene data.
   - Keep source-grounded, procedural, adaptation and original-connective provenance explicit.
   - Use Blender where it materially improves world-feel; retain proven native 3D Canvas assets where they are already superior.
