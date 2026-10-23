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

## First actual native collider diagnostic — 2026-10-22 (engineering evidence)

**New DM direction:** Do not spend time revising the installed skill further now; the Blender → GLB → 3D Canvas procedure is already recorded in `docs/BLENDER_TO_3D_CANVAS_IMPORT_SPIKE_20261022.md` and in first-party GitHub scripts. Advance immediately to playable floor, physical walls and camera collision. Explicit original master art/source remains immutable.

**QA-only read-only runtime test:** The first-party bridge now has `inspect_native_playability` (GitHub feature source commit `e5f9a85048f08746eba1ff17ba0a6225e0a987d4`, first-party installed JS SHA `9057486a844fda12c73e15a662700f6f35357f5b4c50706d37bb8a1d1ce1d0fc`, backup `native-physical-qa-20261023T000640Z`). It is restricted to the GM-viewed inactive clone `sW4aXZgKXj1cH0US`; its guard was live-tested to reject the approved Area8 scene `NUEDEFAULTSCENE0`. 3D Canvas v9.0.36 native `interactionManager.computeSightCollisionFrom3DPositions` with its existing accelerated BVH provides actual hit coordinates and models. No ad-hoc collider meshes, no TokenDocument movement, no Scene/settings writes.

**Native hit results:**
- QA druid projected center (3D x=2.02,z=0.635), vertical movement-category ray from y=.32 to -.15 hit true 3D surface at **y≈0**. This is a meaningful actual source-geometry floor hit, but is not yet a physical walking/settling test.
- QA monk projected center (x=1.82,z=.35): same vertical ray first hit a real `AREA8_ROOF_DERIVED001` mesh at **y≈.28057**, then `RADIAL_CONNECTOR_A001` source-derived geometry at **y≈.01251**. Important: roof is above monk; floor-support probes must distinguish a ceiling hit from a foot-support hit.
- Test north wall ray from (1.92,.12,.55) toward (1.92,.12,.03) hit native `TEMP_AREA8_WALL_ZERO_PIVOT` at z≈**.166978** for **movement**. The **camera** collision ray hit the same mesh at the same world coordinate; native **sight** ray saw this plus additional masked geometry z≈.178. This passes **ray-level geometry inclusion**, not physical token-motion clipping or Game Camera visual behavior.
- Native collision ray service group counters after scoped ray tests: movement=7, sight=9, camera=4 (context-specific, **not total map collider counts**). QA clone has **13 Tile documents explicitly cameraCollision=true**, including one extra imported rim QA Tile; original source Area8 has 12.
- Two QA tokens' actor statuses currently empty, so no visible `falling` condition. HOWEVER actual native `game.settings.get('dnd5e','disableFalling')` returned **true**. Therefore `Falling absent` is **NOT a PASS**: world-wide automation is masking false positives and legitimate drops alike.
- Historic skill references `FOUNDRY_GAMEPLAY_MECHANICS_V2718.md` and `FOUNDRY_CAMERA_FALLING_VERIFIED_V2720.md` already verified the mechanism: D&D5e v6/v14 falling queries **Foundry Levels/Surfaces**, while a collidable 3D Canvas GLB does not automatically register a native supporting Surface. Official D&D5e 6.0 release note confirms that native Surface configuration is required and optional Falling automation can be disabled; source <https://newreleases.io/project/github/foundryvtt/dnd5e/release/release-6.0.0>. Foundry API `Scene.getSurfaces({type:"move"})` is documented at <https://foundryvtt.com/api/classes/foundry.documents.Scene.html>.
- Read-only original scene document check shows **one native Level** (`defaultLevel0000`, elevation bottom0/top4), 13 Regions dominated by difficult-terrain movement behaviors, and no explicit `surfaces` field on the Level record. This alone does NOT prove `Scene.getSurfaces` has zero derived surfaces; next QA should read that native API. Do not change `grid.distance`—previous attempt broke actual 3D roof elevation.

**Current acceptance statuses (required granularity)**

| Gate | Status | Reason |
|---|---|---|
| One-source static Blender-to-3D-Canvas geometry/placement | **PASS** | Native model loaded, bounds/center/checksum checked; source unmodified |
| Actual imported-source floor ray | **PARTIAL PASS** | Druid y≈0, monk lower structural surface y≈.0125, both genuine mesh hits |
| Floor traversal, seam crossing, foot contact | **UNVERIFIED** | Not a keyboard/mouse movement test |
| Wall movement obstruction geometry | **PARTIAL PASS** | Native BVH move ray hits northern wall |
| Attempted character walk into wall/through doorway | **UNVERIFIED** | No real in-client move trial this pass |
| Native Game Camera obstruction geometry | **PARTIAL PASS** | Camera ray intersects northern wall, but Game Camera disabled |
| Actual Game Camera and first-person clipping | **UNVERIFIED** | No dynamic active-camera test |
| Falling condition absence without global suppression | **BLOCKED** | `dnd5e.disableFalling=true`; supported native Surfaces not yet proven |
| Existing accepted Area8 map integrity | **PASS** | GM view and camera restored, source SHA unchanged |

**Required next QA, not a skill rewrite:** Test native `Scene.getSurfaces({type:"move"})` read-only, then validate a source-footprint-specific **Foundry-native Region Surface/Level** configuration on the QA clone only (metadata, NOT fabricated visible geometry). If native Surfaces cannot accurately represent Blender floors/holes/slopes, classify falling automation as DM adjudication limitation or require a different native-supported solution; do not quietly turn Falling automation off as proof of true support. With the native floor model settled, carry out physical drag/WASD-native movement along two adjacent walkable chunks and against a wall, verify camera blocking in the actually enabled camera mode, then cold reload and repeat. This is a release gate for every accepted imported room; not an excuse to rebuild the room with procedural primitives or Foundry 2D wall spaghetti.

**Recovery:** After read-only probe, the GM was returned to original source Area8 via native QA `restore_view`; one native renderer recovery succeeded. Source Scene was not activated/deactivated or document-edited by the probe.
