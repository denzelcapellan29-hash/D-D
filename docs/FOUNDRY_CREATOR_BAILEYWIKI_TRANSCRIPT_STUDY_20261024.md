# 3D Canvas creator + Baileywiki caption study — 2026-10-24

**Scope:** Source-linked study for Blender-authored 3D scenes imported to Foundry V14 + native 3D Canvas (GM-controlled in-person play). **Status:** SOURCE-RETRIEVED, NO PRODUCTION EDITS, native V14 behaviors separately UNVERIFIED unless independently passed in earlier QA. Videos largely predate the installed Foundry 14.368 / 3D Canvas 9.0.36, so their UI/API instructions are historical candidates, not deployment contracts.

## Retrieval method and exact evidence boundary
vidIQ `vidiq_video_transcript` returned **14 new complete English timestamped transcripts in this pass**. An additional standalone [Baileywiki Building Generator](https://youtu.be/k6V5UaE8ulU) transcript was retrieved in the preceding pass, on top of six Baileywiki captions already covered in [prior research](https://github.com/denzelcapellan29-hash/D-D/blob/main/docs/BAILEYWIKI_FOUNDRY_3D_CANVAS_TUTORIAL_RESEARCH_20261024.md). **21 distinct complete transcripts across the combined study.** YouTube playlist search identified the four supplied playlists, and channel/video discovery identified the below video IDs. **Individual playlist membership is not exhaustively verified**: do not represent this index as every episode in any playlist.

The video service then returned **insufficient vidIQ credits** when attempting [Baileywiki: Installing 3D Canvas](https://youtu.be/5VKs1Lul_Rg); no credits were charged on that failed attempt. It reported a Nov 24, 2026 refresh. Four short 3D Canvas clips have no caption tracks: `he9VmqMfiHg` (First Person), `WgNMPGs3A60` (Asset Browser & Merging), `XEr4r0QpF_0` (Stairway to Nowhere), `x9GQqQgE73Y` (Clipping/Illusory Wall). No visual-analysis tool was charged for these.

This document is an independently written **technical digest**, NOT a verbatim transcript repository; do not publish creator subtitle tracks or private campaign sources here.

## 14 newly retrieved video caption tracks

| Creator | Source video | Caption-derived practical scope |
| --- | --- | --- |
| TheRipper93 | [Easy 3D Dungeons with Blender and the Dungeon Pack](https://youtu.be/wvd7Wm7WvHQ) | Modular floors/walls/arches; grid snapping; Blender duplicate/array, applying modifiers and origin control. Early authoring examples are not source/geometry acceptance. |
| TheRipper93 | [3dify 2D battlemaps with Blender](https://youtu.be/n6FVHp3wr0I) | Subdivided 2D mesh, sculpt/mask/elevation, UV and face-normal checks, baked texture; older FBX route, not our current GLB contract. |
| TheRipper93 | [Room Builder](https://youtu.be/LYiFga661Qs) | Native add/subtract/knife room tools, separate room floors, presets/custom themes and door openings (0:32–3:25). |
| TheRipper93 | [Converting STLs with Blender (new Method)](https://youtu.be/j8sZ-VM0FoI) | Legacy STLs reduced with Decimate; UV preparation, GLTF/GLB and Draco compression. At 9:25–10:51 the tutorial reports a ~4.9 MB file compressed to ~775 KB with comparable viewed shape; case-specific, do not generalize to arbitrary GLBs or current renderer. |
| TheRipper93 | [Working with Heightmaps and Heatmaps](https://youtu.be/Tb-CSbKuOXM) | Paint terrain heights and separate trees/grass/rocks distribution masks, blend grayscale gradients, gravity placement; actual surface and provenance still need source-based QA. |
| TheRipper93 | [Blender 3.0 quick room layout](https://youtu.be/bM-Kf1GmUy8) | Extruded snapped wall polylines, Solidify and UV before glTF. Is a rapid technique, not permission for new unauthorized visible meshes. |
| TheRipper93 | [Donjon to 3D](https://youtu.be/OASEqDQidd8) | Grayscale cavern mask → native heightmap geometry and materials; demonstrated vision blockage on that generated terrain. Generic cavern generator is NOT source-faithful Tresendar geometry. |
| TheRipper93 | [Book of Shaders](https://youtu.be/R9mhwxXUO68) | Detailed native shader guide, incl. wind/ground blending (4:11–8:03), clipping around token/camera (19:31–24:56), slope-sensitive overlay masks (49:20–55:54), and tri-planar caveat (1:01:54 onward). Good art tools; not repairs for missing geometry or unsafe sockets. |
| TheRipper93 | [Map Generator](https://youtu.be/XsHeONzPPlY) | Native grid-cell height/materials, procedural layouts and themes, material randomization can break seamless texture continuity (5:19–5:49). Does not replace source-authored scene master. |
| Baileywiki, with TheRipper93 | [3D Combat Part 1: Optimization](https://youtu.be/DVv5IPOsYHE) | Most valuable operational transcript: mesh/draw-call complexity (4:24–7:51); instanced repeated grass (8:06–10:35); weather vs heavier volumetric particles (11:07–14:42); expensive stationary particle emitters (15:14–20:08); enabling 3D geometry for sight (27:58–30:42). Historical settings require 9.x validation. |
| Baileywiki | [Easy 3D Maps with Baileywiki 3D Assets](https://youtu.be/17qZ_hipfEg) | Modular scene/biome libraries, reusable decorated prefabs, gravity on real terrain, scene lighting, initial camera (28:06), movement/sight flags (40:33–40:49); presentation/asset fit ideas, not a fully automated importer. |
| Baileywiki | [Foundry Basics: Tiles](https://youtu.be/GtYiussF-q0) | Foundry 2D Tile coordinates, overhead/roof occlusion (5:45–8:28), separation of walls/roofs (9:15), hidden GM tiles (12:44). **Do not transfer 2D overhead semantics blindly to 3D GLB Tiles.** |
| Baileywiki | [Automated Animations Part 2: AA in 3D](https://youtu.be/3kbUVpnn45Y) | Optional automated animations with Sequencer/socketlib/JB2A and per-effect 3D projectile/beam/on-token controls (0:33–7:26); no new runtime module installed in this study. |
| Baileywiki | [3D Shop/Tavern Interior in Seconds](https://youtu.be/-BevtN61ei4) | Skybox projection inside cylinder, first-person and click hotspots using Monk's Active Tiles; presenter notes unsolved initial entry UX (5:12). **Not** physically authored source-faithful room geometry; not suitable as replacement for Blender Manor. |

Additional preceding-pass transcript: [Baileywiki 3D Building Generator](https://youtu.be/k6V5UaE8ulU) 0:07–2:31: automatic connected walls, floors, doors, furnishings and roofs, plus floor-aware roof fade and room furnishing. This is a demonstration of a separate Baileywiki product, not evidence that our existing bridge automatically supports it.

## What changes vs the existing project baseline

**KEEP (already superior or independently proven):** Existing source-hashed Blender chunk exporter; semantic GLB manifests; transform/elevation and placement checks; readback/rollback/lost-ack recovery; isolated seven-Tile Foundry native import/render/cleanup; GM first-person/free camera; native tested wall/sliding-door behavior. These tutorials do NOT establish reasons to abandon our importer or replicate tiny Tiles by hand.

**HIGH-PRIORITY improvement candidates (DESIGN_CHOICE, UNVERIFIED on installed runtime):**
1. **Per-role collision and vision flags.** Draft importer hardcodes `collision/sight/camera_collision=True` for all chunks (see as-built comparison). Native source and Baileywiki flags distinguish real blockers, floors, sight occlusion and decorations. Test floors as supporting collision but normally non-opaque, walls as opaque, small deco as non-blocking, roofs with elevation-aware visibility.
2. **Hinged-door source authoring.** Avoid whole-Tile animation of rigid frame + centered leaf. Use stationary frame, leaf/handle correct pivot and creator-supported per-mesh GLB extras where installed 9.x honors them; do a closed/open/reclosed collision, sight and player-eye pass, not just document metadata.
3. **True multi-level ownership.** Prior floor/stair BVH intersections are already verified, but imported token ascent/descent and roof disappearance during movement are still not certified; native route and supported floors/Levels semantics first.
4. **Performance budget based on mesh/draw call count, instances, shader cost, and FPS.** Do not judge readiness by triangles alone or sacrifice realistic stone/timber relief to force mesh-count optimization. Benchmark representative family fixture at default/reduced resolution and clear negative controls; keep animated/interactives out of unsafe merges.
5. **Art/render parity.** Source-appropriate PBR/UV texel scale, tile identity, shader overlays motivated by actual weather/use, sky/HDRI consistency; do not use clipping shaders, tint or skyboxes to disguise unsupported/absent physical geometry.
6. **Premium operational exposure.** Compare room/material/environment/editor and effects features against first-party bridge actions. Implement typed actions only for actual gaps; scene-edit ownership is the separate Foundry workstream and source Blender art stays with Manor owner.

## Boundaries
- **SOURCE:** creator's and Baileywiki's linked caption tracks, older software context, plus vendor 3D Tiles reference.
- **AS BUILT:** existing QA and unmerged PR8 only; no code/runtime/Manor modifications in this study.
- **DM_APPROVED:** one GM screen, source-faithful art+engineering on SAME decorated fixture, native Foundry 3D Canvas target.
- **UNVERIFIED:** tutorial-specific UI and operation on Foundry V14.368 + 3D Canvas 9.0.36; actual pivot, stair/door gameplay, load-soak still require tests.
- No credit-bearing provider actions, Meshy, vendor patching or scene writes were performed for this tutorial study.


---

## Additional targeted SOURCE study following DM preference: 3D Canvas FIRST, Foundry SECOND (2026-10-24)

**Scope constraint:** Only TheRipper93's creator videos/documentation and Baileywiki tutorial/session content. No unrelated YouTube channels, no general Foundry overview detour, and no claim of having exhaustively enumerated any YouTube playlist. vidIQ upgraded balance confirmed **2,000 credits available BEFORE this research**; retrieval is 5 credits per successful caption call. **10 additional video caption responses** were returned this pass (one music-only/no useful spoken instructions: `oOAusysEiXw`). No new paid video-watch or non-caption visual analysis. Multiple older short 3D Canvas videos lack captions; their absence is not proof a feature is unavailable.

### Targeted new transcript index: developer mechanics and real GM interoperability

| Priority | SOURCE | Specific researched behavior | Implication for current native v9.0.36 |
|---|---|---|---|
| P1 | [TheRipper93: 3D Canvas 3.5 Feature Roundup](https://youtu.be/X6IcVI-Z01k) | 3D Tile collision/vision configuration, native terrain/material browser, texture mapping, water shaders, live scene exposure/lighting, shader-vs-physical geometry; demonstrates older UI and shadow/resolution changes | Preserve 3D Tile semantics, current registered settings prevail over 2022 UI labels |
| P1 | [Baileywiki + TheRipper93: Levels, 3D Canvas, Tile Sort and Modules](https://youtu.be/6gzV5qfanSo) | 5:29–12:53: Levels handles vertically overlapping scenes and token/sight elevation, Wall Height and Better Roofs support Levels, floor heights need not form one uniform scene-wide stack | Separate **Levels visibility/elevation policy**, **native 3D geometry collision/sight**, **Foundry TokenDocument game state**; verify their agreement on same live fixture |
| P1 | [Baileywiki: 3D Canvas Feature Roundup Jan 2023](https://youtu.be/6bu3_ZIMcl8) | 1:03–2:24 duplicate floor/wall Tile merging and unmerge; 6:24–6:55 first-person token view noted primarily as immersion/sight inspection | Native merged instances are rendering optimization, *not* proof semantic Tile ownership/collision is preserved; current GM first-person proven, Game Camera optional |
| P1 | [Baileywiki: 3D Combat in the Throne Room](https://youtu.be/DJhaIzQk2AM) | Play footage: door/opening, sight changing as token crosses doorway (approx 4:53–5:43), native combat/targeting and overhead viewpoint (approx 38:38) | Positive **historical demonstration** of ecosystem-level 3D interaction, not proof of our exact imported Door GLB or D&D5e runtime |
| P2 | [Baileywiki: 3D Combat in a Warehouse](https://youtu.be/RFlHTKys-Ww) | Gameplay, token spatial moves and level/jump cases (around 56:14–56:49 mentions elevation/movement friction) | Recorded gameplay exposes edge cases but uses DC20—not substitute for D&D5e/our native test |
| P2 | [Baileywiki: 2026 Multi-Level Ship Workflow](https://youtu.be/Ur1FlKPFt5o) | Multi-deck authoring practice; treat as possibly hybrid 2D+3D until video mechanism is individually matched to our installed engine | May inspire a floor-aware fixture, not direct import specification |
| P2 | [Baileywiki: Colour Swap and Overlay Shader](https://youtu.be/F8i8QWsu_hM) | 0:19–3:51 multi-tone color replacement to preserve trim detail; 4:06+ overlay materials on 3D Tile geometry | Cosmetic adjunct only after good PBR and visible physical relief. No tint/overlay workaround for incorrect stone architecture |
| P2 | [Baileywiki: 20-Minute 3D Dungeon Design](https://youtu.be/98cMxiVxm78) | Practical 3D scene authoring and modular visual arrangement | Reference for art/editor workflow; source-defined geometry remains authoritative |
| P3 | [Baileywiki: 3D Canvas Cutscene Tool](https://youtu.be/3KnOl-Agc3I) | Cinematic camera orchestration demo | Our native Cutscene Panel is registered, but automated bridge coverage must be separately verified; not required for core scene acceptance |
| Exclude | [TheRipper93: 3D Canvas Foundry VTT montage](https://youtu.be/oOAusysEiXw) | Caption return is Thai auto-captions of music, not useful spoken technical content | No instruction derived, no engineering conclusion |

### Creator's current documentation: stronger authority for V14 than historical tutorial versions

1. [3D Canvas Tiles](https://wiki.theripper93.com/levels-3d-preview/info/entities/tiles): 3D Tiles (rather than 2D Foundry Walls) normally own fully 3D movement and sight blocking, plus native Tile doors. Tiles can be documented as Floor, Wall, Roof, Door or prop through their GLB and metadata. Tile role matters; unneeded Block Sight is wasteful. **Critical**: a 3D Tile has a Foundry 2D placeholder used by Levels for visibility, so our GLB importer must not omit/blank it. Native Levels option `Mirror Levels Tile Visibility` coordinates above-floor hiding with Levels defined elevations.
2. Same [Tiles: Blender custom properties](https://wiki.theripper93.com/levels-3d-preview/info/entities/tiles): mesh-level fields are **case-sensitive** and exact: `collision` integer 0/1, `sight` integer 0/1, `isDoor` integer 0/1/2, `doorId` string, `ds` integer 0/1/2, `doorStyle` integer 0/1, `doorAnimateAngle` integer degrees. Export GLB `extras` and inspect resulting GLB JSON to confirm correct mesh targeting; **do not assume** Tile-level door flags animate only one leaf. Frame immobile, door leaf hinge at physical pivot; test closed/open/reclosed physical collision and LOS.
3. [Fog of War & Vision](https://wiki.theripper93.com/levels-3d-preview/info/fow): Foundry Scene Token Vision/Fog Exploration are **separate settings** from 3D Canvas `Use 3D Geometry for sight calculations` and 3D fog render. Without 3D geometry sight, tokens can see through 3D Tiles while 2D walls still govern visibility. **Fog exploration remains 2D across vertical space**, not a volumetric multi-story reveal. 3D geometry sight can disable 2D vision when returning to 2D; weigh GM one-screen workflow and mode switching. Never claim `sight=true` proves LOS blocking while this feature or vision itself is disabled.
4. [Lights](https://wiki.theripper93.com/levels-3d-preview/info/entities/lights): Foundry Light documents are reused, but 3D Canvas supports only certain light animations; shadow-casting/wall-blocking on 3D lights can be very expensive. Avoid many shadow-casting lights; shader recompilation during light creation can stutter. Rendered illumination vs mechanical token vision are distinct.
5. [3D Canvas](https://wiki.theripper93.com/levels-3d-preview): `L` toggles first person, `Shift+X` focus token, native Game Camera optionally locks/top-down. This 3D presentation is separate from Foundry TokenDocument movement state. Prefer native tested free/FPS for DM; don't force Game Camera if optional.
6. [3D Canvas Mapmaking Pack](https://wiki.theripper93.com/levels-3d-preview/canvas3dcompendium): installed native Environment/Terrain/Props/Materials/Dungeons & Interiors/Effects/Cutscenes panels. Existence of buttons does not imply our MCP can safely perform all editing actions.
7. [Walls](https://wiki.theripper93.com/levels-3d-preview/info/entities/walls): Foundry Walls authored in 2D can show and block in 3D but creator discourages them as primary spatial geometry for fully native 3D scenes. Baileywiki 2D-to-3D demo is distinct workflow, not evidence a 2D Wall door is ideal for our Blender first-party leaf.

### Read-only AS_BUILT audit against current installed stack (new 2026-10-24 capture)

Runtime Foundry **14.368**, native 3D Canvas **9.0.36**, Mapmaking **10.0.1**, Premium **9.0.3**, first-party bridge **0.2.8**, seven QA source GLB Tiles in *inactive* QA Scene `3WNB3GURss8vPtua`, Scene revision `dd8676de454199188aee19d511717b8a93d50d3889fcf473b63e2e`. Read-only `inspect_3d_settings`, `inspect_3d_native_workflows`, `inspect_3d_scene` confirmed unchanged revision throughout. Blender Manor source saved/clean; Godot experimental, untouched.

- **ALL seven QA Tiles have `collision=true`, `sight=true` and `cameraCollision=true`**, even `lower_floor` and `stair_connector`. Exact current draft `tools/blender_to_3d_canvas/import_chunks_v02.py` source line 187 hardcodes all three. **CONFIRMED contract defect**, not tested player-observable sight defect yet.
- Current inactive QA Scene `tokenVision=false`, **zero Walls**, **zero QA Tokens**, **no controlled 3D Tokens**, and Game Camera disabled. Native collision flags cannot be interpreted as **actual** LOS acceptance in this configuration. No secret-sensitive player fog pass required by current DM one-screen operating mode.
- Draft importer lines 209–211 additionally writes whole Tile `doorType/doorState/doorStyle` on interactive bundles. Existing hinged door failed actual open collision. Exact Blender per-mesh `extras`, stationary-frame geometry and pivot still need validation **in 9.0.36 on a QA fixture**.
- Registered accessible native panel buttons: `props`, `environment`, `terrain`, `materials`, `roombuilder`, `effects`, `cutscenes`; native Props Browser instance is not currently open. **REGISTERED is not AUTOMATABLE and not acceptance.**
- Native free/first-person interactions previously passed in older QA; no new camera mode/movement/reload acceptance was performed here. Our `mcp__Foundry_MCP__token_move` is a Foundry token/pathfinding operation (2D scene/grid semantics); it is not on its own proof that the **3D Canvas engine** physically walked stairs/cleared a door.
- Strong checked production protections: accepted active Area8/source preserved; no native scene edits, no owner-crossing Blender/Godot work, no module update, no vendor patch, no new paid geometry generation.

### Prioritized bridge contract and release tests (for Foundry implementation owner, not executed by research)

| Priority | Owner/interface | Test/evidence |
|---|---|---|
| P0 | Blender exporter → GLB extras → native Tile renderer | Per-mesh metadata correctness; explicit role-based `collision/sight/cameraCollision` scene flags; native physical floor standability not weakened, actual 3D sight blocked by walls but not floor; unit tests for all role combinations |
| P0 | Blender leaf/frame GLB → 3D Canvas door handling → Foundry state | Real hinge pivot + doorId, `ds`, `doorStyle`; no redundant whole-Tile animation, state open/close changes actual geometry collision, token passage and sight, original QA/source revisions restored |
| P1 | Foundry TokenDocument/Levels → 3D Canvas native surface/camera | Stair ascent/descent via actual token path and elevation; above-floor roof hide with `Mirror Levels Tile Visibility`, no source changes, independent 2D fallback check if ever used |
| P1 | Foundry Scene vision/GM secrets → 3D Canvas visibility | Explicit readback of Token Vision, 3D geometry sight, Fog exploration, GM viewpoint; only DM-required one-screen safe visibility, no default non-GM fog benchmark |
| P1 | Scene lighting + GLB PBR + native renderer | Same fixture eye-level/reverse/overhead captures; native light/shadow behavior and exposure; no shader/tint hiding empty geometry; performance/FPS measured |
| P2 | Native panels + first-party bridge | Inventory registered vs actually callable safe methods, typed wrapper only if needed; keep user/native controls and vendor ownership |
| P2 | Release | Cold 3D reload, GM scene switching, saved Source and QA SHA, no black frames, DM visual signoff |

**Status:** Research+read-only capability auditing completed in this batch; physical behavior of new imports, door/stair passage, materials and loads remains UNVERIFIED. No runtime source/scene/code changes accepted or attempted here. This document **does not supersede** the Art+Engineering integrated gate, Scene-specific QA reports, or official adventure.
