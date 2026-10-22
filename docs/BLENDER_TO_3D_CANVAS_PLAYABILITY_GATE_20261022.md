# Blender → 3D Canvas: mandatory post-import playability gate
**DM architecture decision, 2026-10-22 — APPROVED SCOPE / TEST SPECIFICATION, NOT AN IMPLEMENTED RUNTIME PASS.**

## Production routing (newest DM decision supersedes older Godot-primary statements)
- IMPORTANT source-faithful campaign maps: author/accept in Blender using AI 3D Asset Workflow; export static architecture as coherent spatial chunks, retain independently interactive parts (doors, mechanisms, collision-specific submeshes); deterministic native Foundry 3D Canvas import and visual/playability QA. **Foundry + 3D Canvas is primary campaign runtime.**
- Low-priority generic 3D maps: prefer native [Baileywiki 3D Building Generator](https://foundrymods.com/modules/baileywiki-3d-building-generator) or approved reusable content when capable and available. Do not assume module installed or all generative outputs are accepted.
- Minor encounters: 2D maps, existing Foundry content, or theater of the mind. Do not waste high-fidelity art budget on every transitional location.
- Godot: preserve independent exploratory runtime and existing project/artifacts; it is *not* the primary campaign runtime unless a newer DM decision says so.
- DM may activate native first-person mode and move tokens manually; **do not block map completion on expanded camera/vision automation**. MCP priority is reliable scene import/QA and required native physics/camera inspection only. Extend full MCP only as justified by actual missing capabilities.

## Mandatory acceptance sequence
Existing Blender master/art quality acceptance remains separate. Import does not reach **PLAYABLE** status without all technical gates below. Status values **PASS / FAIL / UNVERIFIED** each, backed by actual runtime evidence; a Tile flag being true is only a configuration check.

**I. Source/visual import (highest priority, prerequisite):**
1. Export source-indexed sections (floor, wall, ceiling/roof, props, doors independently) with source GLBs/approved mesh provenance, parent hierarchy evaluated world matrices, quaternion rotations, scene scale, pivots and material textures.
2. 3D Canvas import idempotently into **duplicate disposable Scene** using native module API. Verify scene bounds and each landmark, entrances/exits and joins, model completeness and PBR textures, visual parity from matched player-eye/overhead/cutaway images.
3. Apply **per-function** collider/occlusion settings; DO NOT mark all geometry as collision/sight blocks. Native 3D Canvas Tiles favor authored geometry, not a replacement forest of 2D Walls. GLTF mesh custom properties are case-sensitive: `collision` INTEGER 0/1, `sight` INTEGER 0/1, `isDoor` INTEGER 0/1/2, `doorId`, `ds`, `doorStyle`, `doorAnimateAngle` per official v9 documentation. `cameraCollision` is Tile setting that applies to Game Camera and must not be conflated with token physics or normal first-person camera.

**II. Floor support / no falling (release BLOCKER):**
- From each intended character starting position, use an actual QA token of known footprint and eye height; spawn at intended ground contact, let native physics settle and measure token elevation, visible foot-ground contact, and **actual vertical support**.
- Test a short walk across every representative floor type and between adjoining chunks: especially seams, ramps, edges, raised walkways, stair changes and openings. Verify no fall through/collider tunnel, false `falling` status/condition, floating token, permanent stuck position or unjustified elevation changes.
- Sample native collider hits/raycast/proximity on the *real source-derived geometry* and actual token movement; do not rely solely on Tile `collision=true` or AABB. Do not create fabricated visible floor proxies or blindly patch with invisible surfaces; obtain/repair approved source geometry or calibrated native collider metadata as allowed.

**III. Wall collision and intended navigation (release BLOCKER):**
- Approach wall from both sides; normal character movement must stop instead of penetrating. Test corner/door frame, closed door, legitimate opening, and active doorway. Verify door open/closed changes blocking while traversable passages remain passable.
- Differentiate decorations, curtains, transparent foliage, water and floor from solid architectural walls; keep sight blocker `sight` separately from movement collider `collision`. Walls that look solid but are noncolliding FAIL; walls blocking intended entrances also FAIL.

**IV. Camera collision and usable first-person POV (release BLOCKER for 3D sessions):**
- Test third-person Game Camera against wall/roof/corner and zoom/clipping with installed module's actual `enableGameCamera`/`gameCameraClipping` settings. Official 3D Canvas docs state Tile **Camera Collider** is relevant **only with Game Camera enabled**; flag existence does not prove the default first-person camera will collide.
- Enter native first-person using documented module controls; verify the eye/camera stays at sensible character height, does not tunnel through walls/ceiling/solid surfaces, can look around and follows the token after real movement. Existing custom camera patches remain untouched; prefer native setting/API first.
- Camera tests must be repeated from inside and outside representative walls and after doorway transitions. An untested FPS/third-person mode is explicitly UNVERIFIED, not automatically accepted just because `cameraCollision=true`.

**V. Cold-start regression and release:**
- Close/reload or switch away/back to force native 3D GLB reload, then repeat at least one floor support, wall and camera collision route. Measure load completion/errors, token state retention, floor elevation, model counts, texture, and FPS frame budget.
- When any blocker FAILS, fix at the correct authored layer (Blender geometry/GLB custom metadata, importer flag/transform, or native module setting); rollback QA fixture and rerun. No hand placement repair on production scene and no unverified shortcut.
- Only export candidate and screenshot/metrics PASS together can be called **IMPORT PLAYABILITY PASS**. DM alone accepts final art. Approved Blender source and existing accepted Foundry Scene stay immutable while testing.

## Existing evidence vs missing evidence
- **ACTUAL PASS 2026-10-22**: one small Area 8 source-derived rim Blender MESH → 44MB GLB → Foundry-served native 3D Canvas Tile; model footprint/depth within pixel rounding, exact 3D world Tile center, idempotent updated document, one-command preview with GM QA Scene.view/restore and original Scene checksum unchanged. Full report `docs/BLENDER_TO_3D_CANVAS_IMPORT_SPIKE_20261022.md`.
- **UNVERIFIED**: a complete multi-mesh room architecture export, per-mesh collider tagging across combined GLB, actual floor support and `falling` condition, wall blocking, normal first-person and Game Camera collider correctness, native door cycling, visual parity and repeated cold-start gameplay. **No claim that a flag proves real collision**.
- **Next bounded test:** Export a **two-floor-chunk + wall/doorway** subset from approved-source Blender work into a fresh QA scene, with per-mesh collision/sight extras. Use one real QA token to walk across floor seam, hit wall, pass real opening and probe both camera modes. Compare native runtime results with inspected official 3D Canvas community sample settings and documented wiki. Preserve original Area 8 and Area 10 accepted masters.

## Sources
- Official 3D Canvas [Tiles](https://wiki.theripper93.com/levels-3d-preview/info/entities/tiles): 3D Tiles block movement and sight, separate Block Movement/Block Sight/Camera Collider; Camera Collider only relevant if Game Camera enabled; Blender GLTF custom properties are case-sensitive.
- Official 3D Canvas [Walls](https://wiki.theripper93.com/levels-3d-preview/info/entities/walls): 3D workflow prefers Tiles; 2D Walls may still work but should not be treated as necessary for every original Blender wall.
- Installed adaptive Blender-first skill v2.7.50 references current source-first art QA and scoped geometry policy; newest explicit DM decision supersedes earlier 2026-10-21 Godot-presentation prioritization.

**Ownership:** All test fixtures GM-only, new semantic IDs, revisable, with bounded rollback, no vendor source edit and no Meshy credit spend without provider-required approval.
