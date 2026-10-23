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

## 2026-10-23 v077–v087: Two staircase failures that measured joints alone did not catch

A pair of descending parametric flights passed local rise checks, but a **published plan review** revealed that an end-to-end arrangement was architecturally false where the actual map depicted two side-by-side stair columns with a central route. A room-scale P1 check is not complete until the source map's *adjacency graph and orientation* are compared with the saved scene. Earlier numeric pass did **not** certify architectural source fidelity.

A revised two-column fixture set stair centers 3.048m apart and left a 1.524m aisle. Its initial wall/step geometry was dimensionally good, yet one upper landing had remained **3.048m detached** because its world matrix had been sampled before the parent transform was refreshed. Add explicit **top-stair-to-upper-landing** residuals, **last-step-to-lower-landing** residuals, full evaluated matrices after parenting, and a deliberate +30mm landing separation negative control to every parallel stair family. v081 correction attained ≤0.0000005m interface residual and rejected +30mm drift. Integration of both lower landings with a widened existing north room opening passed seven real floor support samples and the deliberately incorrect old-width wall blockage test. This is P1 construction evidence, not full source/directional or native movement QA.

Actual player-eye QA then showed stair textures dark, and the upper exit remains a void pending authored exterior. Two comparable lighting/material trials did not meet quality, so the source architecture/art role changes: four actual installed Foundry 3D Canvas staircase GLBs were imported and rendered in Blender, but looked too stylized for the richly carved Meshy cistern. These are useful as layout reference, not approved scene art. Do not mass-replicate native kit meshes purely because they are easy to snap.

A **no-cost** isolated Blender reference of the single 16-tread CAD source family was then rendered from 3/4 and side views. It passes strict one-object image composition validation, preserving original material source, and does not imply artistic approval. The proposed next image-to-3D call uses Meshy 7.1 Standard PBR2K at 30 credits, subject to the provider's explicit task-specific model+cost confirmation even where overall Meshy spending is generally authorized. Both original CAD and full artistic source remain immutable.

Preserved P1 evidence: private versioned QA manifests v081/v082. Executable release v087 gate self-test exit0, actual exit3, *blocked* pending source map pixel trace, genuine high-fidelity art, top-of-stair exterior architecture and 3D Canvas movement/collision. Source-specific map annotations stay GM private.
