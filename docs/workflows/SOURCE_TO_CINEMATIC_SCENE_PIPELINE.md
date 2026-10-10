# Source-to-Cinematic Scene Production Workflow — 2026-10-10

**Canonical reusable skill:** private ChatGPT plugin `ai-3d-asset-workflow` v1.3.0, `skills/meshy-asset-pipeline/SKILL.md`, plugin ID `plugins_6ac99807af3c81918a869eb5e2710a6b`. Source of truth for *execution rules* is that published plugin skill. This repository document is a durable project index / condensed policy, not a replacement for the skill.

**Canonical private campaign book:** Google Drive `Acquistions_Incorporated_Full_Source_Book.pdf`, file ID `1amfybsizYOvD_2VSfDfw8wX1wtjDUArk`. Source remains in Drive only. Supersedes isolated Episode 1 PDF if conflicting. Current area: Episode 1 Area 7, Stomp, until DM changes it.

## User-approved process
1. **Source QA:** review canonical book, official area map and nearby transitions; extract required features, dimensions, entrances, orientation, lighting, hazards, hidden/GM-only information; differentiate source facts from adaptation/interpretation.
2. **Asset inventory + exact reference images:** reuse existing accepted Meshy assets first; identify missing modular architecture/hero assets. Generate only the actual isolated images intended for Meshy. Show all finalized references together in a Drive gallery. Never generate decorative image previews to illustrate status or Blender-only changes.
3. **One reference-batch approval => one standard Meshy job per approved image:** stage exact versioned approved PNGs in Drive; use connector raw download URL for image-to-3D; standard Meshy 7.1 textured/PBR 2K, 30 credits per approved item. Record item/reference/task/cost. No repeated credit confirmation for the same approved batch; no unapproved additional paid retries/variants/surcharges.
4. **Build scene in Blender:** inspect latest accepted .blend, import/QA source GLBs, reuse linked instances, align axes/snaps/scale/materials, place art-directed hero props, stage lighting and cameras. Visible floors/walls/ceilings/doors are Meshy-authored, NOT Blender-procedural substitutes. Geometry/scenes reproducible and checkpointed.
5. **Visual QA + source QA at same time:** capture actual rendered PNGs (unique names), verify nonblack/nonstale, inspect pixels and actual screenshot, compare source-critical scene elements against official map/description, report PASS / CONDITIONAL / REJECT. Publish *actual* QA images to verified Drive folder with per-view results; never substitute concept art.
6. **Iterate until passes within safety gates:** solve Blender camera, orientation, lighting, staging and materials without repeated DM sign-off. New Meshy references require DM's exact-image approval and stated initial credit coverage. Reversible batch -> inspect -> render -> accept/revert. Stop after unexpected failure and one targeted recovery, report checkpoint and smallest DM action if needed.

## Specific acceptance contract, Area 7
- Roughly circular enormous high chamber with east/west approaches; large granite foot suspended near ceiling; recognizable *incised* bare-footprint runes in north and south wall masonry, with blue light emanating from carved grooves (not from added luminous panels); non-graphic crawling-claw/rotting-foot visual adaptation for hundreds of scattered severed feet.
- Main shot priorities: (1) foreground/midground crawling claws **readable**, (2) both footprint rune carvings visibly part of walls and motivating blue light, (3) readable vertical scale if unobtrusive. Retain approved checkerboard floor, giant foot and doorway framing. No torches/braziers.
- Reuse prior Meshy stone architecture, giant foot crusher and claw GLB. Replace only the deficient rune *wall module* using newly approved exact isolated reference. QA assets and scene through actual Blender renders; keep rejected versions archived.
- No Foundry/3D Canvas prep for the current cinematic session. Runtime mesh optimization is separately documented as future work.

## Persistence
- Original private PDFs, isolated reference PNGs, GLBs, .blend files, actual captures and releases: Google Drive D&D.
- This repository: concise source/asset IDs, configuration, semantic area model, workflows, logs and decisions.
- At milestones update Drive PROJECT_STATE, CHANGELOG, ROADMAP and DECISIONS as relevant; don't silently overwrite released assets.
- Render hard-stop: blank/black/mismatched capture or unavailable visual frame. Validate both actual image pixels and live screenshot path; don't claim visually successful until a real capture has been inspected.

## Outstanding policy question
Current safe default: **one paid standard Meshy generation per approved reference**. Any paid regeneration requires explicit prior approval or a preapproved capped retry budget. DM may choose a global auto-retry allowance to reduce back-and-forth.
