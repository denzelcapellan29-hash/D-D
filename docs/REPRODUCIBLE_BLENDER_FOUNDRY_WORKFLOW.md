# Reproducible Blender → native Foundry workflow
Current production method, reconciled 2026-10-25. Blender is the editable master; native Foundry V14 + 3D Canvas is the playable target. Alternate engines require an explicit project decision.

This is a repeatable production procedure with an executable read-only bundle preflight. It does not claim that an inventory check creates artwork, certifies source facts, or replaces native gameplay testing.

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