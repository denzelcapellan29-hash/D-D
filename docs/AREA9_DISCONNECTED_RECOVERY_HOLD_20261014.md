# Area 9 recovery hold — 2026-10-14

## Latest verified
The latest confirmed saved and clean scene is `G:\My Drive\D&D\Foundry Bridge\assets\Area9_v065_OfficialGridBlueprintNoGeometry.blend`, derived from the preserved approved-visual `Area9_Prototype2x2_v064_FinalDarkmantleSideProfile.blend`. v065 contains geometry-free source-grid metadata, not completed large-room assembly. It records a **provisional** irregular north–south grid (22 rows, 124 occupied cells, x −4..4), which is an approximate working transcription, NOT a source-certified overlay. Actual Area 9 map PDF p15 establishes long N–S irregular cavern with rubble/recesses, brass wyrmling pinned north, two darkmantles and southern exit.

## Runtime failure and recovery check
Prior 124-cell room-wide assembly failed internally and did not return a saved checkpoint; subsequent health check timed out. Current follow-up read-only `get_blendfile_summary_path_info` returned `McpServerError: Session terminated`. Independent background-CLI path-info check on v065 also returned `Session terminated`. Thus this is disconnected Blender MCP **server**, not just a broken GUI session. Do not call the runtime and do not retry edits in this session. No new .blend, GLB, screenshot or cloud link can be verified, and no promise of current structural validation. Last known safe v065 and protected v064 must remain intact.

## Smaller safe restart plan
1. Restore Blender MCP server/add-on connection, read-only path + saved/dirty check. Verify v065 and v064 exist as clean checkpoints; save *new* v066 only after immutable backup. Do not reuse failed unsaved scene.
2. Re-check actual map outline and the hand-transcribed cell mask with official Map 1.3; distinguish source cells vs interpretation; register bounding shape, rubble alcoves, dragon and two darkmantle anchors.
3. First batch: instantiate real Meshy-derived floor in a *limited 2×3 or 3×4 new region* while preserving originals, then world-matrix and 5ft-pitch tests, raycasts, and rendered overhead player QA.
4. Second batch: expand only verified floor rows, recording total occupied cells and deviations; keep south exit open where map leaves continuation unspecified.
5. Third batch: roof/floor connector prototype using two walls + two roof tiles, verify actual bearing via evaluated matrices/rays and closeups. Never blindly ring-replicate. Quaternions before any rotations.
6. Add perimeter wall panels only where occupied cells border unoccupied source cells, preserving west/east alcoves and no unintended portal closures; avoid creating visible primitives.
7. Scale/position preserved genuine dragon boulder and darkmantles to source anchor cells; hero and topdown QA. Measure walkable floor continuity, roof-wall support, closure, texture repetition, image nonblack and file clean. Number checkpoints. Stop on repeated abnormal failure; report unknowns.
8. Full review only after successful hero + source overlay and structural-fixture QA; do not label DM approved or exported.

## Operational state
No work was executed after the disconnection other than read-only unsuccessful checks. No Meshy credits spent. Do not invent download links or claim recovery.