# Reproducible 3D environments — 2026-10-29

## Production decision

Keep Blender as the editable master and Foundry + native 3D Canvas as the playable target. Use numerical architectural contracts, reusable components, connected assembly checks and art direction together. A new CAD application is not required to implement this. Bonsai remains a measured next-build trial: compare source tracing, revision effort, export cleanup and native parity against this baseline before adoption. No new provider, purchase or engine migration is implied.

This workflow covers the whole environment. Constructed interiors use exact physical dimensions; caves, chasms, ruined silhouettes and terrain retain source-shaped geometry. Their interfaces share coordinates, elevations and clearance contracts. Never square off a natural feature to fit the kit. Preserve successful exterior/artwork and fallback scenes.

## What changes after the Manor experiment

- Author rooms, openings, stair flights and level changes from one registered location plan. Do not independently infer their adjoining caps or coordinate offsets in later repair scripts.
- Define the token-centre lattice and doorway centre lines in that same plan. Snapping wall boundaries to a quarter-grid does not guarantee that a four-foot opening admits an ordinary five-foot token step. Audit the lateral phase of each opening, preserve source-required exceptions, and test an oblique camera approach as well as a centred cardinal crossing. A review alignment helper is a scoped usability aid, not proof that a mismatched grid has been repaired.
- Prefer a small set of useful floor sizes and masonry runs. Use fitting pieces only at real boundaries. A finer tracing grid is not a requirement to manufacture a component for every tiny square.
- Check whole enclosures, including floor thickness/bearings, wall backs/returns, stair sides, unequal ceiling transitions and pit shafts. Component socket tests and center-point movement tests alone missed defects.
- Keep exact common geometry/material paths reusable. UV phase, random color and wear should not silently create a unique GLB per placement. Prove exported/native material support before choosing a variation strategy. Derive visible relief and finishes from approved art inputs; plain structural boxes are a technical stage.
- Fix a failed rule in the shared generator or adapter, add a meaningful failure case, and rebuild the affected branch. Keep exceptions explicit; repeated scene-specific patches are not a reusable system.
- Include native effects, clue images, interactive masonry, doors and encounter relationships in the feature crosswalk. A geometry-only retention filter lost required content.
- Separate editable component assembly from runtime packaging. Test native repeated assets and Auto Merge/Unmerge; compare local batches or static sections only where compatible with the requested editing workflow. Fewer Tile documents do not prove fewer draw calls or higher FPS.

## The build sequence

1. **Source specification.** Read the relevant source/map and current DM decisions. Record adventure/site identity, source hash and page/map locators, calibrated transform, north, physical dimensions, room/terrain boundaries, elevations, routes, portal ownership/state, material families and every source feature. Mark SOURCE, DM_APPROVED, DESIGN_CHOICE and UNVERIFIED. Interpreting a map remains expert work; the compiler does not infer canon from an image.
2. **Choose and reuse.** Search the verified registry before generating assets. Architecture uses numerical masters and suitable sourced relief/PBR. Props, creatures and signature damage use inspected approved assets. Preserve immutable originals, provenance, licenses and paid-job consent. Establish 3–5 coherent material families and source-specific identity anchors.
3. **Prove the actual connection.** Use the existing accepted representative slice when applicable. Otherwise build a reversible decorated slice containing floor, two walls/corner, an operating door, roof/ceiling, a real level transition, a meaningful wear/hero cue and an irregular boundary if required. Check source alignment, exact support/clearance, UVs/relief, entrance/reverse/overhead images and early native scale/material/movement parity on that same geometry. Do not mass-produce a failing interface.
4. **Expand connected branches.** Produce reachable area batches from the location plan, one editable area scene plus linked master at common coordinates. Reuse standard components with boundary fittings. Doors, traps, clues, blocked masonry and independently changing levels remain separable. Structural edits invalidate affected neighbors and routes.
5. **Finish the world.** Apply continuous source-compatible finishes, correct UV density on treads/risers/caps/undersides, true relief and caused wear. Compose arrival → encounter → descent, ground enclosure and a coherent horizon. Inspect the same current assembly at player height, reverse, edges and overhead. No mist, darkness or camera angle may hide geometry defects. Final artistic acceptance belongs to the DM.
6. **Export and integrate.** Generate content-addressed GLBs plus stable semantic placements, axes/units, pivots, role/state and feature inventory. Check real exports and actual loaded placements; do not rely on Blender names or document counts. Preserve native effects/clues in their native form. Use a versioned inactive candidate and exact rollback; protect accepted scenes and selected production pointers.
7. **Play every required interaction.** Ordinary movement both ways, body/camera clearance, stairs/support, closed blocking, real rendered Open/Close buttons, secret reveal/restore, pit descent/exploration/recovery and reload. Relocation and direct API state changes do not substitute for walking or clicking. Record the tested token/body size, lighting, state and coverage. Whole-site visual review requires a position/heading coverage ledger, including borders, not just route endpoints.
8. **Optimize measured costs.** Inspect scene/Tile reports and actual draw calls/materials/textures/lights/shadows/overdraw/triangles. Compare baseline and candidate with identical viewport, render scale, quality, visibility, lighting, hardware, route, warmup and FPS cap. Measure moving and stationary frame times and matched images. Protect silhouettes, clue readability, water, secrets, collisions and support. No universal 60 FPS or modular speedup is claimed.
9. **Release a reproducible checkpoint.** Pin source, recipes/tool versions, assets, native scene revision, captures and rollback. Require separate source, structure, export, art/world, native gameplay, performance and DM acceptance results. UNVERIFIED never means PASS. Record throughput and rework per connected playable area so future tools are evaluated against measured effort.

## Units and library standard

Use metres in the master. Five physical feet = 1.524m; ten feet = 3.048m. Each asset records its actual dimensions, local origin/axes, sockets, collision/sight/camera roles, material/UV scale, LODs and immutable source hash. Doors have an independently tested hinge; stairs specify rise, run, risers, landings and body clearance as one interface. A category or thumbnail is not a compatibility certificate.

Map grid distance is a conversion, not permission to scale all actors, doors and stair risers. A 25ft map cell may contain several physical floor modules; a 50ft world map uses a different level of detail. Preserve source dimensions and physical character clearance. Match native grid/placement conversion separately.

## Implemented reference toolchain

`tools/environment_workflow/` contains a deterministic rectilinear architecture compiler, independent contract checks, Blender asset/master exporter, release-evidence audit, tests and an original example plan. The plugin carries the same files in `skills/modular-area-scene-production/scripts/`.

```text
python -m unittest discover -s tools/environment_workflow -p "test_*.py"
python tools/environment_workflow/workflow.py build --spec tools/environment_workflow/connected_example.json --out builds/my-new-revision --blender "<Blender executable>"
python tools/environment_workflow/workflow.py audit builds/my-new-revision
```

Choose a new output directory per revision. Build success creates a technical candidate; audit exits 2 while release gates are held. The runner writes no Foundry documents, does not modify the open Blender session, and never overwrites an existing bundle. It saves source/recipe fingerprints, editable master/area scenes, shared content-addressed component GLBs, exact placements and check reports. It is not an installer or a completed native importer.

Supported reference geometry: axis-aligned rectilinear rooms, straight positive-axis stair flights, rectangular internal pits and two-neighbor openings. It rejects unsupported/invalid input rather than approximating it. It does not generate caves, terrain, arbitrary roofs, high-quality PBR, relief, furniture or source interpretation. Use the existing outdoor/map reconstruction/art/asset lanes for those. The example is DESIGN_CHOICE technical geometry, not a Manor replacement or artistic sample.

The checker compares exact intermediate solids and continuous surface/volume coverage, plus triangle rays and finite sampled body clearance. These solids are exact boxes, not bounds used as a proxy for arbitrary meshes. Arbitrary imported meshes need their actual evaluated geometry checks. A finite body route does not certify every continuous stance, creature size or native locomotion system.

The Blender adapter reimports every family GLB: exact local corners, outward closed triangle topology, noncollapsed UVs, one populated scene and door extras. It reopens the master and checks all instance positions against the plan. This verifies the simple reference meshes, not finish quality, renderer parity or native hinges/collision semantics.

## Evidence and cache rules

Use the existing dependency-aware incremental planner for larger projects. Declare source/generator/material/export/native/test dependencies; run only affected stages. That planner schedules work and reuses hash-matching outputs; it does not execute them or award quality passes. The new runner demonstrates one complete reference stage, not a general world-build scheduler. Its release digest is deliberately conservative: any changed bundle file invalidates its external review attestations.

`release.json` has STRUCTURE, GLB, SOURCE, ART, NATIVE, PERFORMANCE and DM_ACCEPTED gates. ART includes assembled world/horizon review. Review attestations in `evidence/reviews.json` must name the exact bundle digest, reviewer, basis and local evidence paths/hashes. The software verifies identity/completeness, not whether a person actually inspected an image. Native records additionally require scene revision, ordinary UI/movement/door/stair/pit/secret/reload checks and verified feature IDs. Performance records require the matched measurement context. DM acceptance must be supplied by the DM; never manufacture it.

Example record shape (all values below are placeholders, not approvals):

```json
{"ART":{"status":"PASS","bundle_sha256":"<digest from release.json>","reviewer":"<actual reviewer>","basis":"<what was inspected and limits>","artifacts":[{"path":"evidence/eye.png","sha256":"<actual file hash>"}]}}
```

Native `checks` labels are `rendered_controls`, `forward_return`, `stairs_support`, `closed_blocking`, `pit_explore_recovery`, `secret_reveal_restore`, `reload`, `native_features`; include `scene_revision` and `features_verified`. Unsupported checks may only be waived by an explicit scoped source/DM decision documented in evidence; do not silently omit them. This reference policy has no automatic waiver path.

Performance `measurement` fields are `viewport_px`, `render_scale`, `quality`, `visibility`, `lighting`, `hardware`, `route`, `warmup`, `baseline_revision`, `candidate_revision`, `moving_frame_ms`, `stationary_frame_ms`, `quality_parity` (true), `accepted_target`. DM acceptance adds `reviewer_role: "DM"`. Required feature omissions remain a release hold until resolved or explicitly approved and reflected in the source plan.

## Verification on 2026-10-29

- 26 regression/policy tests pass. Negatives detect missing surfaces/returns/treads, thin edge gaps, missing pit shafts, paper-thin walls, blocked body routes, disguised obstructions, missing door leaves/features, stale specs/assets/reviews and placement mismatches. Policy mocks are not Blender/native evidence.
- Actual Blender 5.2.2 export/reimport and master reopen: 153 placements, 41 shared dimension families pass. Family count includes boundary fittings; this is not a production catalog size target.
- Independent forward testing exposed six missed failure cases; each was corrected in the generator/checker and regression tests. Final independent retest confirms both last failures are detected and a non-grid revised layout with 12 risers passes (173 parts, 3,070 checks).
- Source/art/native/performance/DM gates remain UNVERIFIED for this technical fixture. No new Manor repair, native performance gain or whole-site certification follows from these tests.

The workflow and tooling are reusable now within the stated scope. The next application should repair the paused Manor's affected connected architecture from its existing plan and preserve its successful artwork, then satisfy the actual decorated/native gates before any promotion. Do not restart a third whole-Manor rebuild or reinterpret the technical example as permission to replace its visuals with boxes.

## Measured modular batching

Separate architectural reuse from runtime grouping. A consistent kit accelerates editing but does not guarantee higher FPS. Native Auto Merge may instance one repeated asset across a large location; inspect the installed Three.js/native implementation and actual culling behavior before assuming each instance is culled. Do not patch vendor code.

Benchmark a few difficult representative views first, including movement and stationary frames. Record draw calls and triangles together: splitting every cheap floor or wall batch can save geometry while increasing calls enough to make the scene slower. Try spatial grouping only for the expensive repeated opaque static families, leaving cheap batches alone. Derive family thresholds and group dimensions from measurements rather than a universal tile budget.

A render-only candidate must preserve exact placement matrices, instance colors/custom attributes, materials, source membership and conservative bounds. Keep the registered native collision sources and interactive doors, secrets and effects independent. Check ordinary forward/return movement, support and rendered controls with the candidate installed. Require version and scene guards, cleanup on free view/exit, safe fallback on relevant edits and exact restoration. A scene-specific successful adapter is not automatically portable to the next native version.

Matched-image tests need unchanged pose, actual first-person eye position, hidden review body, lighting, dimensions, focus and settled native shadows. If images differ, capture an unchanged A/A pair before blaming the candidate. Spinning native condition icons can change both pixels and shadows without an asset defect. Any scoped presentation-only suppression must apply equally to both images, preserve Actor conditions and restore on exit; do not change world settings merely to improve a test. Report exact equality separately from small render-rounding differences.

For hillside coverage, recompute floor height after rounding or changing XY. A stale elevation can put a sample below intact terrain. Keep captured, occupied/excluded and unresolved positions separate. Finite torso/head rays can miss a camera inside thick masonry; inspect recaptures and use a reasoned nearby stance in the same review square when appropriate. Do not label finite samples continuous-volume or all-creature-size proof.

Portable UV0 atlases and matching terrain bounds/support do not establish native art parity. Inspect the actual full-world result from both sides of a transition. Reject candidates that leave the original defect or expose new wedges; restore the source rather than adding tint, fog or camera masking.
