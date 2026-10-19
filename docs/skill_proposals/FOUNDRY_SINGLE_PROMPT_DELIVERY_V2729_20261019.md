# Foundry one-prompt scene delivery v2.7.29 — draft skill update
Date: 2026-10-19
Status: DM-approved workflow policy, plugin release pending packaging/install verification

## Outcome
One DM prompt shall launch the entire source-to-review-ready, playable 3D Foundry scene. The assistant performs official source extraction, scene blueprint, approved asset registry reuse, per-asset Blender optimization when needed, native Foundry batch assembly, visual QA and repairs, gameplay/collision/reload QA, screenshot archive, documentation and final DM art review. Intermediate GLB exports, dry-run passes, 2D underlays or isolated models are INTERNAL checkpoints, not deliverables. Never conflate technical PASS, review-ready, and DM ACCEPTED.

## Source and live authority
Respect official Acquisitions Incorporated source, latest DM scope, GitHub docs/DOCUMENTATION_AUTHORITY.md, two handoffs, Drive state/change/roadmap/decisions, installed skill, live Blender and Foundry. Preserve Area8 and source/approved models and backups. Use one semantic blueprint; Foundry is the runtime and assembler. Blender is per-asset LOD/pivot/material/controlled derivative QA only, never a second full scene assembly.

## Fast execution gates
G0 read source; identify encounter roles, secrets, source constraints and design additions. G1 cohesive layout and player-eye world-feel plan. G2 check existing Meshy assets first; create source-preserving optimized GLB and verify task lineage/geometry, UV/PBR, 1K-first texture, model pivot, triangle count/size/hash; use pre-import gate references/FOUNDRY_PREIMPORT_LOD_GATE_V2727.md. G3 single-model real 3D Canvas smoke test and F5 before batching. Acq Bridge valid schema is {document:"Tile",semantic_id:"stable",data:{x,y,width,height,texture:{src:"icons/svg/cube.svg"},flags:{"levels-3d-preview":{model3d:"..."}}}}; empty objects array is a rejected call, not evidence of broken bridge. G4 use deterministic batch placement to assemble entire true 3D landscape (not merely a 2D map), props, actors/GM cues, lighting, paths, collision. G5 capture real overhead/hero/structural/player-eye renders, inspect them, correct floating/repeated/scaled/white/fallback assets; repeat without routine DM intervention. G6 actual scene reload/visibility/navigation/performance, source and GM secret check. G7 publish verified Google Drive captures and links, revision/manifest/known gaps, sync handoffs and ask for final DM art feedback.

## Outdoor exception
A large outdoor terrain composite or a few optimized source-derived terrain sections plus separate props can outperform grid microtiles. Validate actual runtime load, collision, texels and editability. Existing real Meshy assets first; no generated 2D reference map is equivalent to 3D terrain.

## Meshy authorization policy
DM grants editorial autonomy for selecting/generating appropriate assets without repeated creative permission prompts and requests credit thrift. **Tool/provider hard charge confirmation still applies**: before a Meshy credit-spending call, present model and actual listed cost, wait for required user confirmation if provider requires it. Do not interpret DM request as ability to bypass tool-enforced credit gate. No new paid Meshy asset unless necessary after inventory.

## Completion / safety
Do not return for routine iteration. Escalate only mandatory tool credit consent, actual inaccessible source/runtime, safety-critical or destructive scope changes. Stop/recover on corruption and report last safe checkpoint honestly. Preserve released work. Benchmark total elapsed production time and DM interventions.