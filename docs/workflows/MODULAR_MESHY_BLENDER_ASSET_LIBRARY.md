# Modular Meshy Asset Library and Blender Assembly — v1.0

Status: IMPLEMENTED FOUNDATION / STRUCTURAL ASSETS PENDING.

## Approved decision (2026-10-10)
- All visible architecture (floor, wall, corner, doorway, ceiling) is authored as reusable Meshy-generated GLB modules from exact approved reference images. Blender **does not** procedurally sculpt visible architecture.
- Blender is deterministic assembly, geometric calibration, snapping, instancing, lighting, camera placement, and render QA.
- Hero and dressing props are separate reusable assets. Keep original GLBs immutable and versioned.
- Whole-room Meshy models are concept/diorama references only, not production interiors.
- Area 7 remains active work; preserve prior experiments. Do not progress to further areas without DM approval.

## Structural kit contract
Each module must have: asset_id, version, source_reference_drive_id, meshy_task_id, glb_path, texture_paths, nominal_dimensions_m, actual_bounds_m, origin convention, snap_socket positions, orientation, material/style family, license/provenance, QA render folder, acceptance state.
Initial module pitch: 1.524 m (5 ft), **provisional until official Area 7 map dimensions are verified**. One floor module spans one grid cell; straight wall spans one cell; corners, doors and ceilings share compatible sockets. This pitch is a snap convention, not a claim about the adventure's dimensions.
Meshes can be linked-instanced (shared mesh datablock). Only hidden mating surfaces may be trimmed or capped; never replace visible Meshy geometry with procedural-looking Blender walls.
Validate bounds, manifold issues, flat/planar snap boundaries, texel density, seams, repeated-pattern artifacts, and first-person readability. Reject a module with exposed gaps or mismatched style. Add seeded tile variants after base kit acceptance.

## Asset pipeline
Official source/map -> source-critical feature checklist -> image reference of **one isolated module** -> exact-image approval -> Drive staging -> Meshy 7.1 standard textured GLB -> Blender import and bounds inspection -> isolate, orient, normalize and define snap sockets -> 3x3 test enclosure -> real first-person render -> Drive QA -> accepted module registry -> room assembly.
Use 30 credits per standard Meshy generation; never silently regenerate or add surcharges. An illustrated multi-asset workflow board is **not** an acceptable Meshy module input.

## Blender scene/checkpoint
`G:\My Drive\D&D\Foundry Bridge\assets\AcqInc_Modular_AssetLibrary_v001.blend`
Verified saved 2026-10-10; 9 named collections:
STRUCTURAL_FLOOR, STRUCTURAL_WALL, STRUCTURAL_CORNER, STRUCTURAL_DOORWAY, STRUCTURAL_CEILING, HERO_ASSETS, DRESSING, QA_CAMERAS, QA_LIGHTING.
Existing `Area7_GraniteFootCrusher_Meshy71_v001.glb` imported into HERO_ASSETS with asset metadata. Other structural slots are intentionally empty until approved Meshy assets exist; no placeholders misrepresented as completed.
Scene custom properties include module pitch and registry slot status.

## Reusable assembly algorithm (implementation contract)
1. Read canonical semantic room dimensions and doorway positions.
2. Validate required accepted structural asset IDs exist; fail closed on missing assets.
3. Instantiate floor linked meshes on grid with stable seed for tile variants.
4. Snap wall modules to outer grid edges; replace segments with door modules at source-defined openings.
5. Snap corner modules and ceiling segments; inspect overlaps and exposed seams.
6. Position hero assets using source-grounded semantic anchors.
7. Raycast walkable floor and test 3D camera frusta for obstructions; render entrance shot first.
8. Compare against source map, close/whole scene captures, and approve before more camera views.

## Experiment record
- Whole-room single-isometric Meshy v001: substantial volume, interior visual QA failed.
- Four-view Meshy v001: 1.662 x 1.736 x 0.079 bounds, rejected as flattened.
- Two-isometric Meshy v002: 1.634 x 1.898 x 1.356 bounds, volumetric but first-person camera QA failed.
- No additional full-room Meshy generation planned.

## Next acceptance gate
Generate **one isolated stone floor module** with the approved Area 7 style, verify reference, then one Meshy generation and 3x3 tile seam/eye-level QA. Follow with wall, corner, doorway and ceiling modules. Do not claim a finished room or finished structural library before these tests pass.

## Canonical source precedence — DM decision 2026-10-10
Primary private source: **Acquistions_Incorporated_Full_Source_Book.pdf**, Google Drive file ID `1amfybsizYOvD_2VSfDfw8wX1wtjDUArk`, https://drive.google.com/file/d/1amfybsizYOvD_2VSfDfw8wX1wtjDUArk/view. This supersedes the earlier Episode 1 extract where content conflicts. Preserve the source PDF in Drive only; do not commit scans, maps, or substantial copyrighted source text to GitHub. Before asserting source-grounded facts, consult this full book and identify the relevant passage; DM-provided notes below are approved briefing details, but have not yet been independently cross-checked against the new PDF.

## Area 7 — Stomp: DM-provided source notes and visual targets
- Enormous chamber, **roughly circular**, with **high ceiling**. The former rectangular 50x60-foot concept is **not** canonical and must not control the build. Verify actual dimensions/entrances against the full book's map before construction.
- Huge granite block suspended near the ceiling at the chamber center, **carved as a giant foot**.
- Runes scribed into the **north and south walls**, forming **outlines of bare footprints**. Preserve both as distinct spatially anchored features.
- Hundreds of rotting severed humanoid feet scattered across the chamber. For player-facing visual treatment, DM authorizes stylized **crawling-claw-like** props instead of graphic severed-foot imagery; this is a **visual adaptation**, not a change to the adventure fact.
- Crawling-claw reference: https://static.wikia.nocookie.net/forgottenrealms/images/1/1e/Crawling_claw_5e.jpg/revision/latest?cb=20161120044855 ; additional DM-uploaded visual reference available in conversation (do not claim the copyrighted image is owned/generated).
- Existing Meshy giant-foot crusher is reusable as hero asset. Review its suspension height in the final chamber.
- No source-grounded claims for braziers, chains, blue glow, or skull motifs unless confirmed from book; they remain optional creative art direction.

## Circular room modular assembly extension
- Meshy-generated structural library must include **curved wall wedges**, curved corner/transitions, doorway inserts, and radial/vaulted ceiling wedges, in addition to reusable floor tiles.
- Keep **one standard floor tile** reused across most of the interior; handle perimeter clipping or border trims as distinct Meshy-authored visible modules, with Blender-only hidden-edge fitting.
- Parameterize chamber center, radius, wall height, entry azimuths, ceiling apex/shape, segment count, and module snap transforms from verified semantic source.
- Deterministic radial placement and seam inspection; linked instancing for repeated wall wedges and floor tiles.
- QA acceptance includes actual ground-level Blender renders with chamber scale, overhead suspended crusher, two footprint outlines, and non-graphic crawling-claw dressing legible.
- Workflow graphic generated in the conversation is **conceptual**, not a verified actual Blender scene or accepted reference asset. The persistent source of truth for the workflow is this document.
