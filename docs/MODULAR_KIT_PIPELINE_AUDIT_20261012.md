# Area 8 — Modular Kit Pipeline Audit (2026-10-12)
Status: proposed skill amendment, not a certified builder.

## Source audit
Installed skill v2.3.0 already specifies blueprint, actual connector patches, constrained assembly, two-wall+roof+floor prototype, strict GLB-only visible geometry and structural QA. The missing capability is EXECUTABLE ENFORCEMENT: we repeatedly bypassed these gates and rendered large assemblies with holes. GitHub document authority opening still says v2.2.0; reconcile with installed v2.3.0 before next release.

## Proposed hard gates
1. Blueprint a logical structural shell: complete floor regions, wall perimeter except intentional portals, roof coverage and bearing, basin boundary, wall pipe penetrations and connected sewage outflow. Explicit 2D coverage topology before 3D.
2. Define a modular kit grammar: each approved structural GLB must carry verified mating connector IDs, counterparts, local frames, topology-backed physical contact patches, units, geometry provenance/hash, allowable transforms and tolerances. Nonconforming assets are decorative or rejected, not silently pressed into structural service.
3. Separate structural kit geometry from decorative dressing. Every visible object remains from approved GLBs or verified existing models; no Blender procedural substitute.
4. Demonstrate assembly fixtures before replication: two floor tiles, two walls with supported roof and adjoining roof piece, pipe penetration/wall joint, basin edge, plus straight and curved closure fixtures.
5. Deterministic assembly from kit connectors and adjacency graph. Bounded optimizer solves remaining tolerances only; no unbounded ring placement or blind scaling. Incompatibility becomes new asset specification.
6. Structural validators report floor coverage holes, wall boundary gaps, roof enclosure/support, pipe outlet-to-pool continuity, navigability, portal exclusions, source compliance. AABB/ray hits/nearest-point distance individually cannot PASS a joint. PASS/FAIL/UNVERIFIED explicitly recorded with units/confidence.
7. Never promote a room for DM acceptance or art-review-as-if-complete on failed structural gates. Separate labels: technical prototype, visual-only comparison, structurally validated candidate, DM accepted. Include fixed hero and defect close-ups.
8. Automated regression tests include missing tile, suspended roof, false-positive AABB intersection, incomplete circular closure, nonconnected pipe, intended doorway, valid straight fixture, valid curved fixture, and imported real GLB performance.

## Tool decision
Existing Blender MCP + bpy + NumPy + GitHub are sufficient for first fixture implementation. Blender mathutils.bvhtree supports real surface proximity/raycast/overlap; combine with connector contract rather than treat overlap as support. Add SciPy optionally for bounded least-squares fitting; OR-Tools CP-SAT later only if discrete module selection becomes difficult; Trimesh/Open3D only if native Blender mesh queries insufficient. Blender 5.2.2 has NumPy, not SciPy/NetworkX/OR-Tools/Trimesh/Open3D at last verified inspection. Another generic Blender MCP offers little value. Blender Asset Browser is optional kit organization, not structural solver.

## Minimum runnable milestone
Version generic connector manifest/schema, kit-adjacency solver, floor/wall/roof/pipe validator and pytest/unittest fixtures in GitHub. Run on actual approved GLB assets in isolated Blender checkpoint; render first-person and cutaway only once structural fixture passes. Return an incompatible asset family to Meshy approval and paid-task cost gate, not a full room placement loop.
Area8 v020 saved clean and not DM approved; no Blender changes as part of this audit.