# CURRENT_HANDOFF — Acquisitions Incorporated
Updated: 2026-10-10 (based on latest explicitly recorded DM direction)
Status: Resume pointer, NOT an approval or production release.
## STARTUP / CONTEXT RESTORATION — MANDATORY
At the start of a new chat, work session, resumed task, or BEFORE substantial production changes:
1. Discover live plugin integrations with functions.exec -> ALL_TOOLS (never deny custom MCP access from abbreviated tool lists); health-check the needed integration.
2. Read GitHub D-D PROJECT_INSTRUCTIONS.md AND Drive PROJECT_INSTRUCTIONS (long-form rules). Read this CURRENT_HANDOFF, Drive PROJECT_STATE, CHANGELOG (latest entries), ROADMAP, DECISIONS. For code/config read relevant GitHub files; for assets consult official/private source, skill and Drive manifests. Do not trust chat summary alone.
3. Reconcile against newest explicit DM decision and live application state: confirm active goal, permitted scope, saved-vs-accepted status, exact checkpoint, newest QA artifacts, known failures/constraints, what not to touch and next reversible action. If documents disagree, flag the conflict; do not silently overwrite user decisions or treat old status as current.
4. Run one coherent batch, inspect actual result, capture/render, save/checkpoint only on verified success. Update this handoff + PROJECT_STATE/CHANGELOG/ROADMAP/DECISIONS and GitHub as appropriate. Leave a clear resumption pointer.
If any source cannot be fetched, record precisely which and use the remaining known-good information; ask the DM only if an essential unresolved detail blocks safe action. Do not ask them to recount past chat before searching persisted records.
## PROJECT BASELINE
Campaign: Acquisitions Incorporated Episode 1, Right Place, Wrong Heroes. Canonical: source -> semantic campaign/world model -> deterministic spatial engine -> platform-independent scene -> runtimes.
Primary future VTT Foundry + 3D Canvas; current isolated Blender/Meshy work does not involve Foundry.
General world-feel gate Waterdeep street/warehouse -> fissure -> subterranean transition -> Area 1 -> Area 2 remains in force; DM authorized Area 7 cinematic work as a separate scope. Area 2 basin approved asset pipeline: exact approved ChatGPT reference -> Drive signed raw URL -> Meshy 7.1 GLB -> isolated Blender multi-view real QA -> Drive for DM approval.
Skill: skills://plugins/ai-3d-asset-workflow/meshy-asset-pipeline (read current version for exact budget and asset rules).
## ACTIVE DM REQUEST
Area 7 "Stomp": focus ONLY on north/south footprint runes and ceiling/upper chamber, following DM-supplied approved first-person entrance reference. Runes must be scribed/recessed into masonry, evenly blue-lit from grooves, readable in entrance hero shot; ceiling should read imposing and cathedral-high. Preserve doorway framing, suspended granite foot, existing floor, dark-blue horror palette. Do NOT change crawling feet/claws in this pass. DM has rejected the v018 appearance as unlike reference; do NOT describe v018 as artistically accepted. User-supplied reference is in project conversation attachment; locate/verify a Drive copy before treating one as available there.
Current last VERIFIED SAVED (not accepted) Blender checkpoint:
G:\My Drive\D&D\Foundry Bridge\assets\Area7_Modular_Assembly_v018_ClawVisibility_QA.blend
Drive file: https://drive.google.com/file/d/1OQokYX-7qP_M_tl7x-ukBli5VO03ToYD/view
Previous v017 checkpoint preserved. Verify current open .blend/saved/dirty state via live Blender MCP BEFORE writing.
Last QA images (reference for rejected appearance, NOT acceptance):
Hero hi-res https://drive.google.com/file/d/14kaV81YuXUAmUWwztwW4wsJK1oTJiZAt/view
Floor https://drive.google.com/file/d/1-yrKvkZFV0RKDrUklUkINjyvDCSaN--w/view
Rune detail https://drive.google.com/file/d/1HOaQoOGwn82wMuHx8o1ZJMRC6UoAwAuQ/view
Captures: https://drive.google.com/drive/folders/1enIEdZ2KR4jKQwebagFcpeiEtsvUReHM
Assets: https://drive.google.com/drive/folders/1JxMgt6MqPDRitDRftLREHk0k0_qYyaqS
## KNOWN TECHNICAL FINDINGS / BLOCKERS
Area7_CrawlingClaw_Meshy71_v001.glb is real textured 3D geometry but contains multiple shallow disconnected foot forms bundled in one high-poly mesh; existing shared mesh is very flat and appears photographic. A heavy loose-parts mesh-separation operation crashed Blender/MCP (WinError 10054); never repeat against production without memory-safe isolated alternative. DO NOT touch feet during current rune/ceiling pass.
Floor has 185 visible Meshy floor-tile instances sharing one material, not confirmed missing/black tiles; checkerboard appearance should be diagnosed from actual geometry/lighting before edits, deferred for this pass.
Blender MCP has repeatedly been falsely reported absent when live ALL_TOOLS discovery would have found it; mandatory first step is functions.exec registry search + read-only get_blendfile_summary_path_info. Actual socket failure is different. Blender screenshot UI may show stale default cube; render to versioned PNG, read bytes via Blender MCP, and verify Google Drive cloud file.
Meshy asset reuse first; no unapproved new credit spending.
Area 7 v019 diagnostic claw test existed but was never accepted as checkpoint. Do not conflate diagnostic files with approved assets.
## NEXT SMALL REVERSIBLE ACTION
Inspect live v018 file, compare authored rune-wall meshes/materials and ceiling modules with official Area 7 source and approved entrance reference. Make rune/ceiling-only adjustment; render entrance hero, rune close-up and height shot; inspect actual bytes, verify Drive sync, save new numbered blend only after QA, report exact changes and remaining mismatch.
Expected acceptance: DM visual approval, NOT API success or saved file alone.
## CANONICAL LINKS
GitHub instructions: https://github.com/denzelcapellan29-hash/D-D/blob/main/PROJECT_INSTRUCTIONS.md
GitHub handoff: https://github.com/denzelcapellan29-hash/D-D/blob/main/CURRENT_HANDOFF.md
Drive instructions: https://docs.google.com/document/d/1IZmss9Dek0kWjYHD7-qQVpcNGw9szy-QxzOG_UHYL0A/edit
Drive state: https://docs.google.com/document/d/1QIPXGaH4KVFFvnZSMqEXXdk4DqjKRpxc90AeMwfwxG4/edit
Drive changelog: https://docs.google.com/document/d/1RKfbj4MK45Ha321bkbFQy8HXhvEUAR-0svLVyWJrGgQ/edit
Drive roadmap: https://docs.google.com/document/d/1GV62dDjojN13JtNVTRPh_GDSXSyTcwg2fMdDPzq1cH0/edit
Drive decisions: https://docs.google.com/document/d/1HpAlu11p9gf7eiNMwXvJIVEFCRCkH1cclYLGcS31VRo/edit
GitHub PROJECT_STATE.md, CHANGELOG.md and ROADMAP.md now include October 10 continuity pointers; Drive PROJECT_STATE and the newest handoff hold the fuller active-state record. GitHub remains canonical for code/config. Reverify both stores for freshness at each resume.