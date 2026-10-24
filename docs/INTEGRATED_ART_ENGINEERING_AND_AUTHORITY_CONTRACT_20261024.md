# Integrated Art–Engineering Production and Authority Contract
**DM decision:** 2026-10-24. **Scope:** Acquisitions Incorporated, custom 3D environments, Blender master -> Foundry VTT V14 + native 3D Canvas primary playable target. Godot is separate experimental work.

## Governing principle
**Structural truth and visual truth must agree in the SAME actual asset arrangement before mass repetition.** A structural test passing while its material family looks generic is a valid engineering result and a FAILED production-art gate. A pretty render with false connections, wrong source-map orientation, or invisible out-of-camera void is a FAILED production-scene gate. Neither is ready for use. Preserve prior structural fixes; solve visual mismatch at the correct asset/material/art-direction layer without dismantling sound architecture.

### Five linked gates, one common fixture
One immutable-source-preserving, reversible fixture: **2 adjoining walls + true corner/door opening + connected floor + supported ceiling/roof + one defining narrative/wear element**, plus appropriate entrance/stair/courtyard connector when essential to the player route. Use one source-tagged semantic layout and identical source revisions across tests. Exterior/outdoor uses representative continuous terrain/bank/entrance instead of a literal room roof.

1. **Source/meaning:** official published plan, approximate vs exact sections, route graph, openings and 5–8 environmental identity anchors; maintain SOURCE / DM-APPROVED / DESIGN / AS-BUILT labels. Wrong source topology is hard FAIL independent of appearance.
2. **Structural/mechanical:** physically measured evaluated geometry joins, supports, wall/door/stair clearances, sealed intended boundaries, real negative shifted controls, no disguised seams or impossible traversal. Only actual valid measurements count, not AABB proximity or script exit0.
3. **Art/physical integration:** source-appropriate silhouette, real stone/timber relief where visible, material continuity over structural interfaces, coherent texel density, plausible PBR (albedo/normal/roughness), motivated aging/wetness, varied yet consistent adjacent modules, no gray void/unfinished backs. Art cannot intrude into collision, portals or bearing patches. Different artistic families may need different structural interface contracts; revise BOTH sides together in a reversible independent derivative, not by flattening art to fit bad sockets.
4. **Player experience:** actual matched-view Blender renders at approach, inside eye height, turn to side/back, doorway/exterior transition, and overhead/connector diagnostic; inspect real pixels. Three-second environment recognition, coherent lighting, terrain/ceiling support, no repetitive slabs, no clipping/black view. Camera fixes cannot disguise geometry defects.
5. **Target runtime:** early small native Foundry 3D Canvas import and image parity, correct units/transforms/materials; real token wall/opening/ground/step tests, native doors, measured FPS/load/cold reload as applicable. Playability PASSES are scene/version-specific. D&D5e Falling disabled globally is NOT proof of floor support or legitimate drops. Optional Game Camera failure need not block normal native first-person/free-camera presentation unless the DM requires that feature.

### Mandatory bidirectional design loop
- **Design fixture:** site story/architecture AND art identity at the same time, BEFORE mass module production; choose structural master and candidate art family together.
- **Engineer + art:** measure sockets/bearings, visualize decorated interfaces at character height, quantify relief UV/texture family mismatch and preserve passage clearances; update a common `FAMILY_CONTRACT`.
- **A/B candidate:** same perspective/exposure/render/material context; target one root cause; record geometry residual + image before/after together. A PASS on one dimension cannot silently replace a FAIL on another.
- **Runtime probe:** import representative fixture early; if renderer changes art drastically, classify it as asset/PBR/export/runtime mapping rather than rebuilding correct geometry.
- **Expansion:** only when SOURCE, ENGINEERING, ART, ASSEMBLY and REPRESENTATIVE_RUNTIME each have evidence; otherwise retain engineering checkpoint and hold production replication. Some source-accurate layouts require context-building before artistic acceptance; record blockers explicitly rather than inventing geometry or abandoning source fidelity.
- **Cost/practicality:** no paid Meshy task without that provider's per-task cost confirmation; any visible geometry exception follows its explicitly approved construction lane; originals and DM-accepted scenes remain immutable.

### Small machine-readable-compatible handoff for all three chats
One record `FAMILY_REVIEW` per art/engineering fixture:
```
artifact_id, scene_id, source_pdf_map_ref, source_status,
blend_path, blend_sha, asset_family_id, original_GLBSha,
art_pbr_version, structural_contract_version, render_config_id,
fixed_cameras, source_gate, geometry_gate, art_gate,
assembly_gate, foundry_gate, sample_sizes_and_tolerances,
actual_image_links, foundry_native_evidence_links,
decision: KEEP_FIXTURE | REJECT_ART | REJECT_GEOMETRY | HOLD_RUNTIME | DM_ACCEPTED,
top_blocker, next_single_action, owner, verified_at
```
Gate values PASS/FAIL/UNVERIFIED and don't mislabel saved as accepted. A source/art or PBR change invalidates only affected downstream visual/runtime proof, not unrelated proven geometry. A connector/portal geometry edit requires reconfirming its adjoining art, passage and native movement. Report those exact dependencies.

## Documentation authority and synchronization
| Layer | Owns | Does NOT own |
|---|---|---|
| **ChatGPT Project instructions UI** | Compact, durable mission/authority/workstream routing; *pointer to this contract* | Live revisions, narrative lore, screenshots, long technical incidents |
| **Official private adventure in Drive** | Published canon, maps and GM-only specifics | Automation source or public GitHub text copies |
| **Private campaign story register in Drive** | DM-approved narrative deviations and undecided proposals | Visual art acceptance for unbuilt models |
| **Drive PROJECT_INSTRUCTIONS + DECISIONS** | Long-lived private policy and explicit DM choices; pointer to this contract | Source code mechanics and ephemeral build status |
| **Drive PROJECT_STATE/ROADMAP/CHANGELOG/CURRENT_HANDOFF** | Latest checked status, handoffs, acceptance, and review artifacts; canonical Drive links/hashes | Retroactive acceptance from file presence |
| **GitHub D-D** | This technical contract, semantic schemas, code, fixtures, unit and runtime tests, change reviews, engineering audit | Private sourcebook text, spoilers, large binaries |
| **Installed AI 3D Asset Workflow** | Executable method and gate criteria; refer to this contract and actual current policies | Independent campaign decisions, new geometry authorization, runtime state |
| **Blender/Foundry live** | Actual current scene/runtime objects, renderer, collision and view state | Adventure/story policy or DM approval |

**Conflict resolution:** official source controls published facts; latest explicit DM decision controls authorized deviations/target/scope; current source-tagged semantic contract controls layout hypotheses; GitHub source controls code/test procedure; installed skill controls execution only where it does not conflict with higher authority; Drive current state controls artifact release/acceptance; live Blender/Foundry controls what actually happened. Historical statements in long files are NOT automatically latest policy. A doc edit does not alter ChatGPT Project UI or already-running chat context.

**Sync procedure:** after a verified DM decision or actual tested skill change, update THIS contract or referenced canonical record once, then place short dated cross-links and version/acceptance information in appropriate Drive/GitHub handoff records. Avoid copying full policy into three systems and drift. On a conflicting instruction, emit `CONFLICT: source A, source B, newest decision, proposed resolution`; never silently improvise. Preserve last-accepted versus latest-saved distinctions. Each parallel chat reads latest linked rules at safe checkpoints; no cross-owner file writes.

## Three fixed workstreams
1. **Art/skill chat**: own visual methodology, integrated art/engineering gates, shared skill edits and document-policy pointers; does not touch Manor .blend/Foundry importer.
2. **Manor scene chat**: own source-aligned Blender geometry, asset intake, actual art execution, measured joint fixtures and real image evidence.
3. **Foundry integration chat**: own multichunk exporter/importer, runtime native QA, lighting/material parity and scene rollback; report relevant parity defects to Manor/Art.
All three inspect shared evidence read-only; the DM alone confers final art acceptance. A positive read from a QA fixture does not release an entire room.

## Current evidence motivating this policy (no new acceptance granted)
Tresendar Area1-to-Area2 saved v112 G3 structural fixture and latest v119 layout comparison improved actual connections; v114 pale masonry, v115 tint, v116 pastel props and v117 cave-looking stone failed art quality. Area8 v082 is an approved visual benchmark but earlier architecture had limitations. This contract is POLICY only. It does not mark the Manor, any new modular family or the full Foundry pipeline as ART ACCEPTED or playable.

### Verified coordination references
- Previous three-chat handoff: https://github.com/denzelcapellan29-hash/D-D/blob/main/docs/ART_FIRST_WORKSTREAM_SKILL_V2761_20261024.md
- Private build audit: https://docs.google.com/document/d/1EyA1b45f_JgIyzV-fBZHfR9b55znV8Et5cuFmNbzBqk/edit
- AI 3D Asset Workflow: https://chatgpt.com/plugins/plugins_6ac99807af3c81918a869eb5e2710a6b
- Private sourcebook: https://drive.google.com/file/d/1amfybsizYOvD_2VSfDfw8wX1wtjDUArk/view
- Private approved narrative changes: https://docs.google.com/document/d/1ht8lVcRc0KaERYRb9yL0G0MSVk8SIgBpvY-J28EO_po/edit
