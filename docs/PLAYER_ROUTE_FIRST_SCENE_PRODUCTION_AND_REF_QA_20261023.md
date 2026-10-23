# Player-route-first scene production and image-reference QA — 2026-10-23

Status: **process finding tested; plugin update staged but NOT published**. This document does not supersede the installed workflow's asset/geometry approvals.

## Failure found
Earlier Tresendar preparation devoted multiple sessions to parametric Area 6 while the party last reported reaching Phandalin. A good engineering joint in an unreachable later room is a poor next-session deliverable. The correct first playable environment is the damaged manor grounds, followed by the cellar stair/cistern area. Subsequent branches include the storage room, a blocked passage toward the pit hall, and an early secret branch to the chasm. Do not assume numeric room order predicts the players' choices. Source maps establish topology; exterior courtyard shape may need an explicitly designated authored choice if no official tactical map is provided.

## Corrective source-first sequencing
1. Retrieve latest verified party location and any approved scene/quest decisions from private GM handoff and official source.
2. Generate a **GM-only encounter access graph** with visible entrances, concealed portals, physically blocked openings, optional branches, and likely session stopping point. Differentiate source fact from staged spatial extrapolation. Do not leak spoiler nodes in player exports.
3. Prioritize first reachable real encounter and adjacent branch assets; postpone later rooms even if their parametric fixture already passes. Existing fixtures remain a construction library, not session readiness.
4. Require real player-eye, cutaway, edge-side/overhead and performance/collision before a scene is playable; runtime state is independent.
5. Publish and read back true images before sharing any link. A local synced folder is not independent cloud verification.

## Controlled visual reference failure
The DM requested free ChatGPT-made reference images before paid Meshy generation. Two attempts to generate **one isolated cistern object** returned fabricated, labeled campaign progress infographic boards instead. Neither is valid Meshy input and both are REJECTED. Do not pass them to image-to-3D, crop them into a false single object, or treat apparent 'completed' claims in generated pictures as evidence.

One local Meshy-library courtyard fixture (v046) used real imported stone floor, quake rubble, and limestone wall, rendered natively in Blender. It failed art QA: almost white rubble, detached rectangular wall, finite floor tile exposing sky/void, missing encounter structures and around **3,158,340 source polygons across only three meshes**. A Blender 5.2 sky enum failure occurred first and was corrected on **one isolated retry**. Technical import/render PASS, aesthetic and world-feel FAIL, mass replication BLOCKED. Original source meshes and unrelated runtime untouched. Reuse this observation to reject unsuitable art libraries promptly and consider appropriate purpose-built assets with separate provider per-task confirmation.

## Evidence and release
Private working source: `D&D/Foundry Bridge/assets/TresendarManor/Parametric_Resumption_v015/TRESENDAR_PLAYER_ROUTE_PRIORITY_v045_PRIVATE.json`, `Tresendar_Courtyard_MeshyLibraryArtQA_v046.json`, `TRESENDAR_PLAYER_ROUTE_GATE_v047.json`, and runnable `enforce_Tresendar_PlayerRoute_v047.py` (self-test exit 0; real release gate exit 3 blocked). Installed skill patch archive `ai_3d_skill_route_patch_v2760.zip` saved locally but **NOT published**; plugin updater rejected host upload arguments for Windows local archive path. Do not refer to draft v2.7.60 as installed. Preserve current installed release 2.7.59 until a verified upload/update/readback is possible.
