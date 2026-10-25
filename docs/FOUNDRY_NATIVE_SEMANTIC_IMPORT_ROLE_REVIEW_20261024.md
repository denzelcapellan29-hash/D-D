# Native 3D Canvas semantic import role correction — 2026-10-24

**Status:** SOURCE-ONLY PATCH + ISOLATED SEMANTIC TEST PASS. **NOT DEPLOYED TO FOUNDRY; LIVE PIVOT, FLOOR, STAIR, LOS AND CAMERA REGRESSIONS PENDING.** Per DM request, no change to accepted Area8, in-progress Manor Blender masters, installed 3D Canvas vendor, GameCamera world settings, or any campaign Scene. Existing strong centering/GLB hash and transaction recovery preserved. This is an unmerged feature branch PR [#8](https://github.com/denzelcapellan29-hash/D-D/pull/8).

## Baseline review before changes

Reviewed installed `ai-3d-asset-workflow` v2.7.64 and prior v2.7.65 art-owner release, the relevant native control and Surface QA skills, the technical study `docs/FOUNDRY_CREATOR_BAILEYWIKI_TRANSCRIPT_STUDY_20261024.md`, `docs/BLENDER_TO_3DCANVAS_TUTORIAL_VS_ASBUILT_REVIEW_20261024.md`, `docs/FOUNDRY_BLENDER_MULTICHUNK_IMPORT_V02_QA_20261023.md`, current `CURRENT_HANDOFF.md`, and actual read-only module/Scene status. Verified installed Foundry V14.368, 3D Canvas 9.0.36, Premium 9.0.3, Mapmaking 10.0.1, Bridge 0.2.8. Inactive seven-source-GLB QA scene `3WNB3GURss8vPtua` revision `dd8676de454199188aee19d511717b8a93d50d3889fcf473b63e2ed5fdb86e2e`: seven movement collision true, sight true and camera collision true Tiles **including floor and stair**. Token Vision=false, zero QA Tokens and zero core Walls: no actual token LOS acceptance possible from this state. Protected Area8 checksum `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`. Renderer ready at this pre-patch read-only check.

TheRipper93 [3D Tiles](https://wiki.theripper93.com/levels-3d-preview/info/entities/tiles) documents native 3D Tile movement and sight blockers, Blender extras and Levels 2D placeholder; [Fog of War/Vision](https://wiki.theripper93.com/levels-3d-preview/info/fow) explicitly separates Token Vision, Fog, 3D geometry sight and 2D fog; historical tutorial transcripts supplement this, do not govern V14 runtime. Foundry Core Region Surfaces and 3D Canvas BVH mesh physics are different, and D&D5e falling remains a different game mechanic.

## Code changes — no scene deployment

- `tools/blender_to_3d_canvas/export_chunks_v02.py`: requires user/source-authored `acq_role` on each visible mesh; rejects unsupported/missing role and door tags inconsistent with `door_leaf`. Manifest exports `acq_role`, explicit collision/sight and optional `camera_collision` hints; does not rewrite source Blender or emit new visible geometry. Existing untagged .blend fixtures must be explicitly role-tagged as *new disposable source versions* by the Manor/build owner or isolated fixture operator before using revised exporter.
- `tools/blender_to_3d_canvas/import_chunks_v02.py`: validates role-homogeneous chunks and role/door identity before any Foundry request; chooses Tile movement/sight/camera flags from explicit semantic role matrix, rejects mixed, missing, partial conflicting or invalid flag types and requires a written `semantic_override_reason` for nondefault settings. Import is fail-closed for legacy role-less bundles. **The old seven-Tile QA fixture is not retroactively modified or migrated.**
- Existing `tests/test_multichunk_manifest_v02.py` metadata fixture now declares `opaque_wall` and `door_leaf` roles, preserving old structural hashes/elevation and rejection tests. Added `tests/test_native_tile_semantics_v02.py` for floor/stair (movement only), wall/roof/leaf, prop/foliage, mixed and missing roles, conflicting hints and nonjustified source overrides. GitHub Actions discovers it using the existing `test_*v02.py` pattern.
- Five **isolated** local Python tests using the same semantic policy excerpt passed (roles and several negative controls). Full actual module in GitHub, Blender exporter, existing entire Python/Node GitHub Actions suite, live 3D Canvas role import and native gameplay have **NOT** been executed as passing checks. Do not treat them as such.

## Native test gates still open

| ID | Required verified check | State |
|---|---|---|
| P0-A | Export new explicit-role source GLB, verify actual GLB JSON nodes/extras, PBR, no unintended modification to Blender original, and native scene readback of collision flags | PENDING |
| P0-B | Closed/open/reclosed physically hinged leaf with *stationary* frame and proper pivot; dynamic native BVH collision and Token passage; not just a Tile document state | PENDING (prior opened-door obstruction FAIL) |
| P0-C | Floor support and actual stair ascent/descent with controlled QA token and independent TokenDocument XY/elevation + native mesh rays | PENDING |
| P1-A | 3D sight geometry with Token Vision enabled in disposable QA fixture; verify walls block, floors don't, 2D fog and Level visibility correctly isolated | PENDING; current Scene tokenVision false |
| P1-B | Levels roof hide, camera eye/overhead/collision, material and lighting parity of source-decorated assembly, native reload and FPS | PENDING |
| REGRESSION | Bridge source SHA/manifest, deterministic transforms, readback, negative control, rollback and original Area8 hash | Baseline previously passed; fresh regression PENDING |

**Live stop:** After the source-only patch and tests, first-party read-only `inspect_3d_capabilities` and `inspect_3d_settings` both returned errors, so no additional runtime testing, scene write, renderer reset, viewer switch or recovery was attempted. This is a transport/runtime blocker, NOT evidence the un-deployed code caused an error. Do not attempt repeated blind recovery. Reinspect runtime and scene revisions when connectivity is available.

## Skill release

The DM requested current skill review and corresponding gated guidance. The personal plugin [AI 3D Asset Workflow](https://chatgpt.com/plugins/plugins_6ac99807af3c81918a869eb5e2710a6b) was reviewed before edits. During preparation another agent published v2.7.65 with CAD Meshy skin variation/art changes; guarded upload stopped, re-read exact current release, then rebased changes to v2.7.66. Installed v2.7.66, readback verified both new `skills/foundry-3d-canvas-interop/SKILL.md` and `references/FOUNDRY_V14_3D_CANVAS_ROLE_AND_RUNTIME_QA_V2765.md` present, manifest routed to new skill and prior v2.7.65 art section preserved. This is binding *procedure*; does not imply actual runtime QA PASS.

## Next reversible action

Only once live GM/browser health and inactive QA revision are verified, construct a **new disposable explicit-role** floor/opaque wall/stair/leaf fixture using approved geometry. Native asset preview and snapshot before any write; apply only to an inactive GM-owned QA clone, real eye/overhead native capture, negative control, true token movement, closed/open door, then targeted revert and exact baseline Source/QA checksum verification. Keep full source and artistically accepted Manor untouched. Record statuses as SOURCE | STRUCTURE | ART | WORLD | NATIVE and the DM's final review separately.
