# Foundry and 3D Canvas tutorial library
Reviewed 2026-10-28. This is a research reference, not a new scene configuration or release certification.

Additional batch: [effects, shaders and native production tools](TUTORIAL_VFX_NATIVE_TOOLS_20261028.md) covers four more supplied videos through English captions, with current-documentation and installed-source checks.

## Evidence and use
Five new videos were reviewed through English captions; one through the vidIQ visual-analysis service because captions were unavailable. One supplied link was already covered and was not retrieved again. Service visual analysis is secondary evidence, not independent frame-by-frame inspection by this assistant. Topic labels below are descriptive unless marked as a verified title. Timestamp ranges are navigation aids from the retrieved evidence.

Tutorials do not override published adventure sources, current user decisions, or installed-version tests. Promote a technique into the production procedure only after checking its current API/UI and testing a reversible representative case with visual and gameplay evidence. Existing performance and asset contracts remain authoritative.

## Index
| Video | Topic | Evidence | Disposition |
|---|---|---|---|
| [hVOPxMKvO6Y](https://www.youtube.com/watch?v=hVOPxMKvO6Y) | General lag diagnosis | Captions | Separate load/UI/network problems from rendering |
| [g7Yig3dhLPk](https://www.youtube.com/watch?v=g7Yig3dhLPk) | Media organization | Captions; V10-era context | Reuse library discipline; validate format changes |
| [iZlrmoRJnRI](https://www.youtube.com/watch?v=iZlrmoRJnRI) | Performance troubleshooting | Captions; V10-era context | Controlled diagnosis; historical settings/modules |
| [5Ux6j4IVE54](https://www.youtube.com/watch?v=5Ux6j4IVE54) | Batch image optimization | Service visual analysis | Retain conversion concept; do not run old database recipe |
| [9cly27JMCEA](https://www.youtube.com/watch?v=9cly27JMCEA) | GPU/browser troubleshooting | Existing caption review | Reused; no duplicate retrieval |
| [DVv5IPOsYHE](https://www.youtube.com/watch?v=DVv5IPOsYHE) | 3D Canvas combat preparation, part 1 | Captions | Mesh/effect budgets and runtime diagnosis |
| [snMktFnbGnA](https://www.youtube.com/watch?v=snMktFnbGnA) | 3D Canvas combat and cameras, part 2 | Captions | Candidate combat acceptance fixture |
| [dnhTcLTrbyw](https://www.youtube.com/watch?v=dnhTcLTrbyw) | Particle presets, area and directional effects | Captions | Local effects recipes; detailed notes in additional batch |
| [PhncPae8Ydg](https://www.youtube.com/watch?v=PhncPae8Ydg) | Modular assets, shaders and environment; V10-era | Captions | Retain concepts; reject obsolete defaults |
| [6bu3_ZIMcl8](https://www.youtube.com/watch?v=6bu3_ZIMcl8) | Merging, asset browser, terrain and cameras | Captions | Compatible repetition of custom assets |
| [jP6QiqFWSVI](https://www.youtube.com/watch?v=jP6QiqFWSVI) | 3D toolbar and native production overview | Captions | Candidate tools; detailed workflows need validation |

## hVOPxMKvO6Y — Does Foundry VTT LAG? Here's 5 Quick Tips!
Verified title; caption-based notes.
- **0:31–1:36:** Graphics acceleration and GPU-selection suggestions. Diagnose the executable actually running Foundry; a Chrome setting does not automatically configure the desktop application.
- **1:53–2:58:** Module inventory and compatibility. The future-V13 discussion dates the advice; current compatibility requires current evidence.
- **2:58–4:06:** Avoid unnecessarily importing entire collections into a world; distinguish startup/document overhead from native 3D frame time.
- **4:06–5:32:** Performance-module and chat-cleanup suggestions are anecdotal, not proof of a scene-rendering improvement.

Application: preserve a backup, profile the failed layer, and compare one change at a time. Do not automatically install a recommended module, delete history, or enable experimental graphics overrides. No hardware purchase or quality reduction follows from these general tips alone.

## g7Yig3dhLPk — How to Organize and Optimize Your Foundry VTT Media Assets
Verified title; caption-based notes, explicitly V10-era.
- **0:17–1:54:** Separate shared resources from campaign-specific media and organize by purpose.
- **2:10–3:31:** Use predictable URL-safe filenames and creature prefixes for related token variants.
- **3:48–5:40:** Discusses WebP images, WebM video and OGG audio; example image densities are contextual, not universal standards.

Application: retain immutable source assets and named runtime derivatives, with stable paths and per-build manifests. Rename deployed resources only with corresponding reference updates and verification. Smaller image downloads do not by themselves demonstrate fewer draw calls or lower decoded GPU texture memory. Do not apply blanket 2D image conversion to embedded glTF PBR channels without checking the loader, color-space treatment and material parity.

The current [official media guide](https://foundryvtt.com/article/media/) supports organized paths, safe filenames and measured media-format choices.

## iZlrmoRJnRI — Performance troubleshooting (Dice & Easy)
Descriptive topic; caption-based notes, V10-era.
- **0:48–3:13:** Historical hardware requirements; do not repeat them as current purchasing guidance.
- **3:13–5:18:** Change one variable at a time; consider competing applications and graphics acceleration.
- **5:34–8:32:** Per-client graphics settings and module compatibility; resolution reductions have visible tradeoffs.
- **8:49–10:55:** Network/hosting issues and optional dice rendering concern different bottlenecks.
- **11:10–13:22:** Hardware upgrades and preset helpers are later options, not substitutes for diagnosis.

Application: classify slow loading, network latency, CPU/UI work and GPU rendering separately. Preserve current-quality captures and actual drawing-buffer dimensions during comparisons. A preset that lowers resolution cannot be reported as an equal-quality improvement. Named helper modules and old compatibility advice remain unverified for the installed runtime.

## 5Ux6j4IVE54 — Batch image optimization with FvttOptimizer
Descriptive topic; no captions were available. The following comes from the approved vidIQ visual-analysis service, not direct independent viewing.
- **1:47–2:04:** Service identifies FvttOptimizer and a Windows PowerShell workflow.
- **2:05–2:49:** Reports file/folder conversion controls, skipping existing WebP and using a minimum size-saving threshold.
- **2:50–3:40:** Reports recursive conversion and rewriting image references in legacy Foundry .db files.

Retain the concept of measured image derivatives and reference integrity. Do not adopt the reported command flags or automatic database edits as a current-world recipe. Foundry replaced NeDB with LevelDB in V11; verify supported current document APIs or packaging tools before any reference migration. [Official V11 release](https://foundryvtt.com/releases/11.299), [official packaging changes](https://foundryvtt.com/article/v11-leveldb-packs/).

The service's reported file-size saving is an example, not an FPS benchmark or evidence of identical visual quality. Originals, backups, representative material inspection and broken-reference checks remain necessary.

## 9cly27JMCEA — GPU/browser troubleshooting
Already reviewed in the 2026-10-26 custom-kit notes; reused without another paid call.
- **4:24–7:44:** Inspect the support report and actual renderer/GPU.
- **7:44–9:51:** Distinguish core frame settings and counters from native 3D measurements.
- **10:40–14:10:** Acceleration and experimental browser overrides; the latter were not adopted.
- **14:10–20:58:** Actual-executable GPU selection where applicable, followed by controlled restart and comparison.

Read the existing local research/tutorials/FOUNDRY_CUSTOM_KIT_NOTES_20261026.md for the earlier review. The tutorial's 2023 context does not establish present desktop behavior.

## DVv5IPOsYHE — Combat preparation and performance, part 1
Descriptive topic; caption-based Baileywiki/TheRipper93 discussion.
- **0:17–4:08:** Native content browsers and optional integrations; module/dependency names are historical.
- **4:24–10:35:** Inspect per-Tile mesh/submesh counts as well as triangles. Repetition/instancing can reduce overhead but repeated complex geometry still costs work.
- **11:07–20:24:** Weather, volumetric particles, persistent emitters and lights have different costs; first-use shader compilation can hitch. Claims that many lights are cheap do not establish the cost of shadow-casting lights.
- **21:45–26:21:** Shader categories vary in cost; benchmark the actual material/effect.
- **26:38–33:07:** Geometry-based sight, optional fog and nonblocking grass require deliberate semantics; 3D-only geometry does not create 2D wall coverage.
- **33:39–41:01:** Per-client graphics, shared context and shader preparation require full-frame inspection and stability checks.

Application: use native scene/Tile reports to locate costly content, then measure actual standing and walking frames with unchanged resolution and lighting. Keep source-matched geometry and interaction roles. Check sustained play and first-use effects separately. No tutorial claim certifies a universal light, mesh or FPS budget.

## snMktFnbGnA — Combat, cameras and animation, part 2
Descriptive topic; caption-based Baileywiki/TheRipper93 discussion.
- **2:13–5:35:** Associate a 3D model with a prototype token while preserving its actor and game mechanics.
- **5:50–12:10:** Projectile/effect macros and animation integrations; a visual projectile alone does not perform an attack or resolve damage.
- **13:01–20:51:** Selection and Free/Game Camera controls, tracking and lock behavior. Historical bindings may conflict with GM pause; verify actual bindings. Game Camera and character first-person are distinct modes.
- **21:08–24:31:** Elevation, blood effects and defeated poses; model origins/bounds and status integrations can affect grounding.
- **25:18–29:23:** Volumetric templates, elevation and system-aware effects require real targeting/mechanics checks.

Candidate fixture for future combat work: one PC and NPC; melee, ranged attack, elevated spell/template, turn-follow camera and defeated pose. Inspect source-appropriate visuals, actual rules results, ground contact and moving-frame performance. Validate only the integrations needed for that encounter instead of installing the entire tutorial stack.

## How these references enter future work
1. **Diagnose before optimizing:** identify rendering, UI, loading or network costs and maintain a matched baseline.
2. **Make assets reusable at acquisition:** consistent naming, physical scale, origins, material channels, immutable originals, hashes and stable runtime paths.
3. **Budget effects by encounter:** measure persistent effects, shadows, animation and first-use shader hitches in an assembled playable case.
4. **Promote tested findings only:** retain version, input assets, comparison images, movement/mechanics evidence and rollback with any adopted change.

These are research priorities and reinforcement of existing quality procedures. This ingestion made no changes to the playable scene, installed modules, camera settings, assets or packaged skill.

Further reading: [3D Canvas documentation](https://wiki.theripper93.com/levels-3d-preview), [production workflow](REPRODUCIBLE_BLENDER_FOUNDRY_WORKFLOW.md), [asset/library contract](ASSET_ACQUISITION_AND_LIBRARY_CONTRACT.md).


