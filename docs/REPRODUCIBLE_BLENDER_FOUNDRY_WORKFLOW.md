# Reproducible Blender → native Foundry workflow
Current production method, reconciled 2026-10-25. Blender is the editable master; native Foundry V14 + 3D Canvas is the playable target. Alternate engines require an explicit project decision.

This is a repeatable production procedure with an executable read-only bundle preflight. It does not claim that an inventory check creates artwork, certifies source facts, or replaces native gameplay testing.

## Production reuse and current tool scope
Use [one source specification, component reuse and dependency-aware QA](REPEATABLE_PRODUCTION_AND_CHANGE_QA.md). Keep the [provider-neutral asset/custom-library contract](ASSET_ACQUISITION_AND_LIBRARY_CONTRACT.md) separate from provider endpoints. [Future tool evaluation](FUTURE_TOOL_EVALUATION.md) reserves Bonsai for the next build; no Tresendar migration or 3D AI Studio trial is on the critical path. Reuse working generators/export/native adapters. These procedures do not claim a complete build compiler already exists. Historical experiment reports are read for matching issues, not as mandatory startup history.

## Ownership and authorities
One coordinating task owns the selected build; delegate only isolated artifact scopes. Art, scene production and runtime integration are roles, not a requirement for three separate chats. Preserve originals and accepted releases. Current private project state selects exact artifacts; dated incident logs do not select a master.
Published source controls canon, latest DM decisions control adaptations, GitHub controls implementation/tests, private project records hold assets/evidence, skills supply the method, and live applications establish actual behavior. Never place private sourcebook text, hidden encounter data or real private build manifests in this public repository.

## Architectural review before expansion

Apply the [architectural-intent procedure](ARCHITECTURAL_INTENT_GATE.md) before connected-area expansion. Compare actual evaluated room, corridor, opening and elevation geometry against one calibrated source blueprint. Inventory checks, local seam contact and native token movement do not establish the source floorplan. A DM architectural rejection holds affected expansion and release; preserve originals and valid evidence while correcting the earliest source error in a versioned connected slice. Show matched overhead/source and player-eye/reverse views before resuming expansion. Reconcile the selected Blender assembly and runtime inventory; a stale visible file is not the current result.

## Repeat this sequence for each location
1. **Identify and freeze inputs.** Record adventure/site/map/area identity, source references, geometry interpretation/uncertainty, north, meters/grid scale, origin and coordinate transform. Select exact asset families, licenses and hashes. Distinguish source facts, approved changes, design choices and as-built results.
2. **Prepare one editable area.** For connected interiors, use one source-defined area per Blender scene in shared world coordinates. Keep continuous visible wall/floor finishes; use appropriate authored structure/terrain and verified source-compatible assets. Asset-only restrictions apply to their selected lane, not as a global ban on the approved modular method.
3. **Own interfaces explicitly.** Record neighboring area, portal plane, width/height, elevations, support, owner and intent. Shared walls/doors belong to one owner. Preserve source-intended blocked/hidden routes; a seam-height match does not prove an open route.
4. **Finish a representative section in context.** Retain physically meaningful relief, coherent PBR/UV density, material transitions and motivated wear. Use only applicable channels. Keep an editable art master and separate measured runtime derivatives. Reuse valid existing work; do not restart it as an unrelated pilot.
5. **Assemble and run preflight.** Link exact approved collections into a separate versioned master. Validate exact collection and intended visible object membership, source library paths, hashes, dependencies, units and known player/GM exclusions. Reopen the bundle. Never accept collection-prefix checks as proof of current artwork.
6. **Review real images.** Inspect matching approach, eye-height, reverse, doorway/seam and overhead views on that same revision. Record cameras, render engine, exposure/lighting, texture versions and any render seed. A nonblack image alone does not establish artistic quality.
7. **Probe native Foundry early.** Use sourced GLB sections and a semantic manifest with explicit roles and provenance. On a guarded GM-only QA scene, verify material/scale parity and actual token support, walls, doors, stairs/bridges, camera, roof/Levels as applicable, reload, performance and exact restore. Use native APIs. Inventory, rays, teleport and disabled Falling/collision do not substitute for actual traversal.
8. **Finish and release.** Repair affected failures, retest changed dependencies, then complete the location and remaining connected areas. Keep SOURCE, STRUCTURE, ART, WORLD, NATIVE and DM_ACCEPTED separate. Only the DM accepts final visuals. Record exact last accepted versus latest saved artifacts and the next action.

Known failures hold the affected release or repetition; independent reversible work may continue. Reuse the same area/family and valid evidence. Two comparable nonimproving attempts require a changed approach. Paid generation retains exact provider cost confirmation.

## Native measurement fidelity
For vertically connected exterior/interior builds on V14, read the [version-aware levels and underground review](V14_LEVELS_LIGHT_AND_FOG.md). Separate actual mesh support, core Scene Levels/Region surfaces, 3D visibility, lighting and fog. Legacy Levels UI instructions are not a current V14 configuration recipe; documentation availability is not a native acceptance result.

Read [native rendering and route evidence](NATIVE_RENDER_AND_ROUTE_EVIDENCE.md) before accepting runtime images or movement. Confirm real canvas readiness and the installed compositor/shared context, budget shadows against hardware limits, and verify each actual movement direction, initial floor support and expected elevation trace. Repair continuous relief surfaces with shared physical boundary vertices. Tool success, a nonblack image and a count of movement calls are not substitutes for these checks. AI3D Workflow2.7.72 carries the same procedure; its publication does not certify a campaign scene.

## Per-location private bundle
Keep the source directory tree and relative Blender library paths intact. A review bundle contains:
- private build manifest: identity, exact inputs/hashes, tool versions, coordinate system, chosen collections/visible objects, assets/materials, portal contracts and declared route states;
- editable per-area Blender files and a separate linked master;
- generation/assembly/export scripts and parameters where used;
- optimized player-safe GLB sections, semantic role/provenance manifest and separate GM reveal assets;
- fixed cameras, actual captures, structural/negative-control reports and native QA/rollback evidence;
- current status: last accepted, latest saved, open blockers, owner and next action.

Acquired AI-generated models/images are frozen inputs with recorded task IDs and hashes. Reproduction reuses those exact bytes; it does not promise identical future AI generations. Changes to source geometry, art, export roles or runtime version invalidate only their dependent evidence.

## Executable read-only preflight
Tools: `tools/scene_bundle/run_scene_bundle.py`, `validate_scene_bundle.py` and synthetic tests alongside them.

Supply an existing trusted Blender executable and the private manifest; no executable download or global configuration change is required.

```powershell
& '<python.exe>' tools/scene_bundle/run_scene_bundle.py --blender '<absolute Blender executable>' --manifest '<private bundle.json>' --output '<new report.json>'
```

Use `--asset-root` only for an explicit relocated bundle root. The runner uses a hidden background process, disables auto-execution, performs no scene saves, requires a fresh report filename, and rejects a PASS report from a failed process.

Run synthetic controls:
```powershell
& '<python.exe>' -m unittest discover -s tools/scene_bundle -p 'test_*.py' -v
```

Exit meanings:
- **0:** only the explicitly listed inventory checks passed; release remains UNVERIFIED unless independent records establish otherwise.
- **2:** inventory failure, such as omitted current art despite a matching legacy area prefix.
- **3:** inspection/launch failure.

Reports include observed file hashes, versions and a read-only inventory. Null expected hashes mean provenance is UNVERIFIED; pin selected input hashes in a new manifest revision before repeatability/release claims. Name/property checks do not prove secret-safe pixels. Declared OPEN/BLOCKED/NOT_MODELED routes are intent records, not physical passage tests.

## Resume and synchronization
Read one compact current status first, then only linked records needed for the job. Update that state after a meaningful milestone. Keep incident histories archived. Reusable method changes update this recipe and the skill; ordinary scene iterations update build state, not the generic plugin.
Project settings are durable pointers and require their own explicit update; editing Drive/GitHub does not change the settings UI.

The integrated art/engineering contract remains applicable, with the current routing and role-coordination clarifications above: [contract](INTEGRATED_ART_ENGINEERING_AND_AUTHORITY_CONTRACT_20261024.md).


## Native placement precision and portable delivery

Foundry stores Tile canvas positions and dimensions as integers and clamps negative positions. Preserve a world-baked GLB's intended center with the native model-offset flag: offset.x=desiredX−storedX, offset.z=desiredY−storedY, offset.y=0, in canvas pixels. Inspect the installed native implementation before adapting another version. Measure actual loaded vertices and floor intersections; a correct provenance coordinate alone does not prove placement. Bound dimension-rounding error from the scene grid/pixel scale, and keep structural interface tolerances separate from background foliage placement tolerances. Detect a deliberately shifted negative control on the actual native geometry.

For a portable private checkpoint, copy each selected area library without altering its original, make the master's library paths relative, pack all referenced images including unloaded files, and reopen it. Verify source/copy hashes, exact library membership, image dependencies and runtime GLB hashes. Archive the owned Scene/Actor resources and helper import closure, while recording licensed module dependencies rather than copying vendor miniatures. Distinguish the tested current-world restore from an untested fresh-world installer. Keep official private source material and campaign manifests out of public implementation repositories.

## Shared boundary enclosure and capture identity

A shared wall between rooms at different elevations must close against both adjacent ceilings. Check real evaluated inner and outer faces, wall thickness and miter corners; raising one side alone can leave a sloping wedge or exposed neighboring roof. Inspect player-eye entrance and reverse views after repair, and repeat affected support and open/closed-door checks. Do not cover an opening with trim or hide it with lighting.

When adapting a native QA scene, propagate its identity through capture, lighting, outline and controller helpers. A stale child-helper guard is an access/identity failure, not evidence of a black renderer. Version changed module imports explicitly, inspect actual completed native frames, and keep diagnostic lighting trials separate from adopted gameplay settings.
