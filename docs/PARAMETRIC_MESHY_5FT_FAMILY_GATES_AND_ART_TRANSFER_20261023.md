# Parametric modular 5-ft fixtures: evidence and art-transfer failure modes (2026-10-23)

Status: **TESTED ENGINEERING FIXTURES / ART NOT ACCEPTED**. This is a process-learning addendum, not an installed skill release or scene acceptance. Never promote this document over the current installed AI 3D Asset Workflow skill, private sourcebook, approved scene, or DM decision.

## Method and authority

Follow `ai-3d-asset-workflow/parametric-meshy-fabrication` P0–P4: CAD/numerical structural geometry owns connectors and collision; original approved Meshy GLBs and existing accepted scenes remain immutable. New visible numerical structural masters are confined to the explicitly authorized parametric-construction lane; source-derived Meshy artwork is a separate layer. In a separate Blender process, save a fresh numbered fixture, never dirty or overwrite the live campaign master. No paid Meshy calls without provider-specific explicit approval.

## Verified small-fixture evidence

- 1.524m modular floor fixture: two exact male/female structural solids, .060m male key, .066m receiver, .002m lateral/vertical clearance; 189/189 floor-ray support, eight matched seam heights, aligned pair zero unintended solid overlap. +.015m axial and +.020m lateral offsets produce detectable intersecting volumes.
- Straight wall, through-door, right-angle corner and two flat-ceiling panels: individual manifold checks passed; positive joints zero unintended solid intersections, deliberate wall/roof offsets produce nonzero collisions or separation. Native ceiling-to-wall 18/18 sampled bearings zero gap; a +.012m lifted roof correctly fails support.
- Source-neutral adjoining-room fixture (two 10-ft rooms): exactly one shared physical partition, eight structural floor modules, eight removable ceiling modules; 561/561 floor rays, 29/29 seam test pairs, 39/39 ceiling bearing samples, 40/40 doorway clearance samples. Shared partition +.015m axial and +.020m lateral negative controls rejected, all structural mesh edges manifold. This is *not* a source-specific dungeon build or game-physics pass.

## Failed artistic-transfer methods (do not repeat unchanged)

1. **Projected dark limestone PBR** from prior Meshy-derived room: world-plane UVs on new CAD displayed dark cave-like repeat artifacts. Technical import != style suitability.
2. **Applying 2K image textures from a modular wall GLB onto arbitrary numeric wall UVs**: large broken-looking image patches appeared. Material existence and correct texture resolution do not prove compatible projection.
3. **Source-mesh geometry linked in an art cage**: real Meshy stone and native UVs substantially improved relief. A deliberate 66mm connector exclusion band each side produced a 132mm visible vertical strip. Bounds/cage PASS does not imply artistic contact.
4. **Narrow source-derived joint-cover via Decimate + Exact Boolean intersection**: manifold/art-cage/negative-spacing envelope can pass, and a 2,775-face GLB derivative can export, yet newly cut faces or empty material slots display as an obviously flat white ribbon. This method is visually **REJECTED** even when the structural connector is untouched. Do not keep recoloring or making more arbitrary filler strips after two nonimproving passes.

### Actionable reusable correction

For each *visual* connector interface define a purpose-built, named art role and exclusion mask **before** asset generation or clipping. Confirm both positive geometry AND installed-facing UV/PBR/material continuity from front, oblique, player eye and edge-on joint images. A successful 3D numerical socket does **not** guarantee a seamless ornamental face. Negative-control validators must fail shifted or missing geometry and art intrusions; preserve numeric manifests and actual render evidence. When existing artwork cannot serve the joint without visually flat edges, change the decorative-asset architecture or commission a purpose-built asset with its actual credit cost approved, rather than silently authoring unapproved geometry.

## Hard release rule

An automated gate must parse real source and QA records. Never count historical archive tests as newly rerun; never label locally synchronized files as independently verified cloud uploads. Generic two-room fixture passing is not permission to build the full adventure map; source-vector topology, room-specific door orientation, ceiling, corridors, art and engine traversal remain separate gates. Saved != artwork accepted != engine playable != DM approved.

## Continued v024–v029 evidence: *front-face-only* Meshy derivative and source-indexed chamber

- **v024 failed a strict clearance gate** by 0.000122m: front-facing source UV/PBR mesh derivative had 2,808/2,812 ray hits (99.858%), 12/13 seam pairs and unchanged CAD, but the decorative rear extended 0.122mm beyond the specified y=2.725m art exclusion plane. Do not classify fractional violations as pass merely because they look invisible.
- **v025 corrected only the artist-facing depth by 2mm**, with the original Area8 wall GLB still immutable. Real Blender repeat raycasts retained 2,808/2,812 coverage and 12/13 pairs; behind-CAD-wall-clear PASS, +20mm deliberate rearward shift REJECTED. Preserved original UVs and 24,318 source-derived faces per linked module, compared with 182,796 source faces. Front and seam camera images show a roughly hairline joint instead of a 132mm blank exposed strip. This is a technical artwork-cage improvement, not artistic approval.
- **v026 source-candidate Area6 and western passage**: the sourcebook describes the room as empty; map image tentatively resolves an approximately 2×3-cell room, west locked-door aperture, separate 1×3-cell corridor. Newly authored parametric room+passage fixture passed actual Blender 1,369/1,369 floor-support rays, 100/100 seams, 22/22 ceiling bearings, 20/20 portal clearance, manifold and positive/negative Boolean solids. It is a *partial source-specific engineering fixture*, not the 12-area dungeon, and the locked door leaf is explicitly missing, so release/traversal is blocked.
- **v027 mounted only the A6 north-facing wall art** from the v025 source-derived cladding. Structural geometry digest unchanged; 1,528/1,537 wall-facing ray samples (99.414%) contact UV-preserved Meshy art entirely outside CAD wall geometry, 6 linked instances. Other room walls, the locked door, and corridor art not completed; v027 is an unfinished partial art scene.
- **v028 controlled material tint comparison** from the same v027 scene changed only the PBR base-color multiply, while the full structural and art vertex digests remained equal. Genuine player-eye and oblique renders showed the wall is still pale/repetitive, despite a visually smaller seam. Neither v027 nor v028 is artistic acceptance.
- **v029 evidence-based gate** parses independent v025/v026/v027 manifests plus the earlier v017/v018/v021 proofs. Self-test exit 0; live gate exit 3 (`G4_BLOCKED`). Its required final art, complete map topology, target family corners and doors, actual locked door, four-view artistic acceptance and runtime checks must not be optimistically flipped. Preserve the source master and existing campaign scenes.

**Generalizable correction:** Test decorative surfaces *as open source-derived front-face geometry*, not a texture projected blindly onto arbitrary CAD UVs. Source geometry can fill the visible front almost continuously while remaining entirely outside the CAD mating volume. Require both dense surface ray coverage and a deliberate shift failing the clearance plane. This method reduces exposed seam width but does not fix the texture repetition, unfinished corners, or lockable doors; keep the structural/art gates independent.

