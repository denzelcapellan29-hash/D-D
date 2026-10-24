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
