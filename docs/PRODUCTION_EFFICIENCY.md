# Faster production with the same quality bar

Use with the complete location recipe. The objective is fewer repeated decisions, exports, tool calls and repairs per playable area. These are process improvements, not permission to weaken source fidelity, visible art or native gameplay checks. No speed multiplier has been measured for a complete new build.

## Plan once, reuse explicitly
- Keep one location specification and source-feature crosswalk. Carry its registered coordinates, portal/elevation graph, source/DM decisions and required clues into geometry, dressing and runtime. Reopen relevant source for changes/conflicts rather than rereading all histories. Keep one concise current pointer and an incident archive.
- Triage assets before starting a room batch: usable now, derivative needed, new source-specific asset needed, or deferred with consent. Reuse approved source-matched material families, generators and standalone assets with known dimensions/provenance. Do not substitute a whole stock room for the source floorplan.
- Distinguish an individual reusable prop/structural family from a world-baked assembly section. A section GLB at fixed coordinates is not automatically a drop-in kit asset. Keep origin/scale, sockets, material/LOD variants and verification scope in the registry; reuse parameters and materials when the new source shape differs.
- Establish architecture, elevations and clearance before fine dressing. Prioritize player-visible identity, reachable routes and narrative-critical clues before low-impact ornament. Do not simplify a source-critical feature merely because it is small.

## Use dependable generators and stable adapters
Keep reusable area/terrain generation, export and native review tools driven by explicit project data rather than copying a new script with hardcoded live IDs for each revision. Reuse existing verified adapters first; parameterize a repeated operation only when it has a clear contract, rollback and representative tests. Do not claim a complete source-to-world compiler exists.

Share immutable mesh/material inputs and derive runtime textures/LODs once per source hash and options. Cache keys include source bytes, recipe/script version, transforms/material/role choices and relevant tool versions; a filename, size or mtime alone is insufficient. Avoid full mesh copies for every repeat instance. Retain independently moving doors and source-state/reveal ownership.

Group compatible changes into a connected-area batch, export only changed role sections and update stable semantic IDs. Use controlled lower-cost workbench previews during repair, then the required matched full views at review quality. Inspect corners/caps/back faces and portal clearance early enough to avoid decorating a defective family.

## Order cheap checks before expensive work
Check source layout/feature coverage, exact assembly membership, hashes and GLB scene/mesh integrity before staging large runtime assets. Import the representative real connection early, then reuse its validated interface and unchanged evidence. Run the existing bundle preflight and packaged GLB checker; neither grants art/playability approval.

Inspect native scene/Tile reports before optimizing. Measure the current limiting cost rather than reducing every asset: unique materials/draw calls, textures, lights/shadows, overdraw and geometry can have different effects. Do not regenerate a hero asset to solve an unrelated lighting/camera/export issue. Validate image/export/runtime assumptions before another paid job.

Prepare independent source extraction, references, manifests or approved assets while an asynchronous job runs. Batch independent reads and file inspections. Keep one writer per mutable Blender/runtime artifact. Do not benchmark FPS while competing Blender renders, texture baking or other heavy GPU work contaminates the measurement. Parallel work is useful only when resource limits and artifact ownership permit it; this is not authorization to create other chats or message agents.

## Retest affected dependencies, not unrelated work
The complete recipe's change matrix controls the actual tests. A prop color edit usually needs appearance/parity review; moving a bearing wall affects structure, neighbors, routes and camera; a light/environment change affects illumination/secrets and performance rather than automatically requiring every GLB to be exported again. If dependency impact is uncertain, expand checks rather than declaring them unaffected.

Preserve final assembled source/art review and representative native routes, doors, elevations, camera, secrets, reload and performance at meaningful milestones. Reuse older evidence only with exact unchanged inputs, settings, versions, test recipe and relevant context. A known FAIL remains FAIL even if rerunning the same test would be wasteful. DM acceptance is not a cache flag.

## Read-only incremental planner
The packaged skill includes the same helper. From the repository root:

```text
python tools/incremental_build/plan_incremental_build.py --manifest <plan.json> --previous <completed-stages.json> --root <build-root>
```

The helper hashes declared input/output files once per stable scan and computes fingerprints through a dependency graph. It reports REUSE, RUN or BLOCKED; it does not execute exporters, mutate a Scene, mark tests PASS or certify a release. An unchanged output may still contain a known quality failure. Missing dependency declarations are not inferred: the plan's coverage must be reviewed.

Manifest fields:
- `schema_version`:1; nonempty `project_id`; optional `context` object for genuinely global dependencies.
- `stages`: objects with unique `id`, a `recipe` object, optional `depends_on` stage IDs, optional `inputs` records (`path`, pinned lowercase SHA256), and nonempty unique `outputs` paths.
- Put generator/validator/script hashes, arguments, source/coordinate revisions and relevant tool versions in the recipe or input files. Native QA additionally needs the actual model manifest, source door/state/light/camera settings and test context. Performance evidence needs buffer/device/pass/route/lighting context. Avoid unrelated global fields that invalidate every stage unnecessarily.

Previous records contain `schema_version`:1, matching `project_id` and a `stages` object keyed by stage ID. Each successful execution record has `completed`:true, its exact `fingerprint`, and `outputs` records with `path`/actual SHA256. Record completion only after the operation really succeeds and its outputs exist; never copy a new fingerprint onto stale results. Keep semantic gate verdicts and their evidence separately. The planner intentionally cannot generate a completed cache from a plan alone.

Use relative paths for portable cache identity. Unchanged inputs/recipes/dependencies plus matching actual outputs allow REUSE. Dependency fingerprints include upstream output hashes, so even a regenerated output with unchanged source/recipe invalidates old downstream results. A changed input pin, recipe/tool version, output or upstream stage schedules RUN for affected descendants. Unexpected source bytes versus the pin, unreadable inputs or blocked dependencies produce BLOCKED. Cycles/invalid manifests and multiple producers for one output fail. Declare generated upstream artifacts through depends_on; pinned inputs represent the required existing inputs. Rerun the planner after upstream execution changes outputs before recording downstream completion. Exit0 means a usable plan was produced, not that RUN stages executed or quality passed; exit2 indicates blocking/invalid input. Recheck pins at execution time if writers could have changed files after planning.

## Measure useful throughput
At meaningful stage boundaries record elapsed time, rework cause and completed playable area/route. Compare source preparation, construction, asset wait/cleanup, export/import and QA separately. Prefer changes that reduce repeated effort or repair rate without removing a quality gate. Do not add mandatory paperwork per prop, repeat settled approvals or introduce a new engine/provider on a deadline. Evaluate Bonsai/new providers in their already chosen future-build lane.
