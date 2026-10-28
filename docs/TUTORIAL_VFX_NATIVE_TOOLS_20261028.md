# 3D Canvas effects, shaders and native production tools

Reviewed 2026-10-28. Four user-supplied videos, all retrieved successfully through English captions. These are paraphrased research notes, with descriptive topic labels rather than independently verified video titles. Timestamps come from captions. No direct visual inspection, new runtime experiment or scene modification was performed in this ingestion.

Read with the [tutorial library](TUTORIAL_LIBRARY_20261028.md), [production workflow](REPRODUCIBLE_BLENDER_FOUNDRY_WORKFLOW.md) and [asset/library contract](ASSET_ACQUISITION_AND_LIBRARY_CONTRACT.md). Published source and current DM decisions still control design. A feature's presence in code does not prove its visual quality, compatibility with every asset, or performance in an assembled encounter.

## Video index

| Source | Descriptive topic | Useful reference points |
|---|---|---|
| [dnhTcLTrbyw](https://www.youtube.com/watch?v=dnhTcLTrbyw) | Particle-engine presets and effect tuning | 1:03 legacy emitters; 2:09 controls; 5:08 area; 7:20 mist; 9:28 directional effects |
| [PhncPae8Ydg](https://www.youtube.com/watch?v=PhncPae8Ydg) | Foundry V10-era 3D Canvas materials, modular assets and shaders | 5:27 modular set; 12:40 mesh overhead; 20:24 background/lighting; 29:50–43:25 shaders |
| [6bu3_ZIMcl8](https://www.youtube.com/watch?v=6bu3_ZIMcl8) | January feature roundup: merging, browsers and terrain | 1:03–2:24 merging; 3:28 placement; 4:47 terrain; 6:24 cameras |
| [jP6QiqFWSVI](https://www.youtube.com/watch?v=jP6QiqFWSVI) | Toolbar overview and native creation tools | 0:16 props; 1:18 atmosphere; 1:51 terrain; 2:24 materials; 2:55 interiors; 3:42 cutscenes |

## Particle effects — dnhTcLTrbyw

- **1:03–1:34:** An old emitter can render incorrectly after a particle-engine transition. The suggested repair is to reselect a suitable current preset and resize it. Treat this as a migration diagnosis, then inspect the actual effect; do not assume corrupted geometry or regenerate the prop.
- **2:09–4:17:** A native light can host an emitter. Presets, color gradients and custom settings supply variation; custom JSON is an advanced route. A preset's exposed controls can differ from the fully custom mode.
- **4:17–6:48:** Scale, effect area and intensity control different aspects of the result. The tutorial describes area as a multiplier on the light's configured extent, with zero concentrating the effect at a point. Confirm the installed interpretation before using physical dimensions; captions sometimes conflate radius and diameter.
- **7:20–8:07:** The mist example uses a thin horizontal layer at the light's elevation. Dense mist can behave poorly as the camera rotates. The speaker's low-intensity examples are starting points, not universal quality/performance settings.
- **9:28–11:05:** Emission angle, tilt and rotation orient directional fire, frost or cloud effects. Appearance alone does not create a damaging trap, weather rule or spell result.

Our use: test small local emitters before broad atmospheric layers. Deposited dust, rubble, tracks and physical construction must read correctly before adding airborne effects. Keep emitters away from critical sightlines and measure camera-motion overdraw. Record the preset, dimensions, intensity, gradient, elevation and current module version with a reusable effect recipe.

## Materials, construction and shaders — PhncPae8Ydg

This video explicitly covers Foundry V10 and an experimental contemporary 3D Canvas release. Its interfaces and performance opinions are historical.

- **5:27–10:33:** A modular family combines floors, walls, corners, doors, near-matching secret panels and channels. Props and dressing supply identity. The principle fits a custom source-matched kit; the example does not justify replacing an official floorplan with a stock dungeon.
- **12:40–13:46:** Excessive mesh subdivision/object overhead can matter alongside polygon count. Printing-oriented assets require runtime preparation. Merging compatible static content must retain separately controlled doors, reveals and other gameplay roles.
- **20:24–21:44:** The conceptual distinction is visible surroundings versus environment illumination. Actual field behavior must be checked in the installed loader, especially for source-dark interiors.
- **24:42–29:17:** Native generated shapes, texture repetition, material settings and separate movement/sight roles support rapid authoring. A decorative object does not automatically need all collision roles.
- **29:50–32:08:** Idle and wind shaders offer procedural visual motion. They do not establish a creature's feeding animation, skeletal rig, attack or physical displacement.
- **32:23–38:36:** Water/ocean and oil shaders demonstrate different fluid appearances. Small waves and restrained speed may suit contained water; an oily stylization is not automatically appropriate for clear water.
- **39:42–42:07:** Triplanar projection can help material scale on steep or displaced surfaces, while overlays can add controlled surface variation. Neither supplies missing construction or replaces a broken supporting mesh.

Do not inherit the video's preference for a20–30FPS cap: the current campaign target and measured client behavior govern performance. Its black-box room covers, provisional shader-preload advice and old nonanimated-door limitation are historical examples, not current defaults. Use verified native reveal/camera controls and test the delivered interaction.

## Repetition and rapid outdoor work — 6bu3_ZIMcl8

- **1:03–2:24:** Auto Merge All Tiles groups compatible repeated tiles; unmerge restores editable pieces. This is particularly relevant to individually placed copies of the same custom wall, floor or prop.
- **2:40–3:13:** Native3D text can support signs or GM labels. Keep private labels out of player-facing views.
- **3:28–4:31:** The asset browser combines search/previews with randomized placement and multiple selected models. Restrict variation to a curated family; random scale must preserve believable dimensions and clearance.
- **4:47–5:36:** Quick terrain, gradient materials and a separate water surface can accelerate a prototype or an unconstrained landscape. Registered source paths, portals and elevations still need deliberate construction.
- **5:52–6:24:** The roundup announces a threading improvement. That claim is release-specific; it is not evidence that a current setting can be enabled to gain a particular speedup.
- **6:24–7:57:** First-person inspection and depth of field have distinct uses. Use the actual installed bindings, and reserve photographic blur for optional presentation when it obscures gameplay detail.

Our use: design reusable custom assets so native repetition remains possible. Shared geometry/material identity can make repeated props eligible, whereas a unique world-baked section at fixed coordinates is a different asset. Preserve deterministic placement records when randomness is used. Evaluate native terrain on a separate future fixture rather than replacing an approved terrain master during a delivery deadline.

## Toolbar and production speed — jP6QiqFWSVI

- **0:16–1:03:** The prop browser may initialize slowly once per session. The presenter explicitly postpones detailed placement instruction because some behavior is being revised; this overview is not a complete browser contract.
- **1:18–2:24:** Environment and terrain panels collect atmosphere, sun, weather, terrain/fluid creation and common editing controls. They reduce navigation overhead, but generated content still needs source and playability review.
- **2:24–2:55:** Material browsing can speed controlled appearance trials. Save the chosen material and mapping settings so the result is reproducible.
- **2:55–3:27:** The interior builder paints enclosed spaces and the effects panel changes surface appearance. The clip introduces these tools; it does not specify a reliable source-map reconstruction algorithm or every effect's limitations.
- **3:42–4:14:** Cutscenes connect camera points into a sequence. They are a candidate for an arrival or reveal, with testing for secret exposure, collision/clipping, return of player control and input recovery.

Our use: keep Blender responsible for editable, source-registered architecture and use verified native tools where they save real work in placement, atmosphere or presentation. Record adopted runtime settings in the manifest so the result can be rebuilt. A rapid native sketch can be useful for a future incidental encounter; promoting that sketch to a final authored location requires the same integrated art/structure/gameplay gates.

## Current-version cross-check

Read-only inspection found installed3DCanvas9.0.36. This establishes code availability, not a new runtime PASS.

| Finding | Evidence | Consequence |
|---|---|---|
| Native shaders and per-entity configuration remain supported | [Official shaders guide](https://wiki.theripper93.com/levels-3d-preview/info/shaders); installed ShaderLib includes idle, wind, water, ocean, oil, overlay and triplanar | Reuse native features through a reversible visual/performance trial. First-use compilation and sustained cost are different measurements. |
| Lights can host emitters | [Official lights guide](https://wiki.theripper93.com/levels-3d-preview/info/entities/lights); installed particle system imports Quarks | A visible effect and illumination are related configuration concerns. Budget shadow casting separately; adding effects is not permission to add many shadowed lights. |
| Auto-merge has compatibility rules | [Official tile merging guide](https://wiki.theripper93.com/levels-3d-preview/info/entities/tiles#merging-3d-tiles); installed tile3d.js autoMergeTiles | Current code separates occlusion-link groups and groups by model, texture and generated-shape identity. It skips doors, already repeated/merged tiles, decals and heightmaps; selected tiles are skipped by the default all-scene call. Similar appearance alone is insufficient. Check all other per-instance flags before adopting a merge. |
| Native material, terrain, prop and cutscene tools exist | [Mapmaking Pack guide](https://wiki.theripper93.com/levels-3d-preview/canvas3dcompendium); installed QuickTerrain, assetBrowser and cutsceneEngine | Feature presence supports evaluation, not an automatic change of master-authoring method. |

## Practical priorities for this campaign

1. **Surface readability first:** reuse restrained, source-appropriate material/overlay recipes for wear, dust and wetness. Keep real relief, joints and tracks visible. Test procedural projection on a duplicate before replacing accepted UV/PBR work.
2. **Contained water next:** evaluate a shallow native fluid effect on an existing approved surface, preserving clarity and source dimensions. Visible motion does not certify real bubbling or mechanical depth.
3. **Sparse atmosphere:** test local motes or a narrow mist layer with the normal lantern/darkvision view and moving FPS. Fog should not hide architectural defects or reveal rooms through walls.
4. **Reusable custom kit:** carry common scale, origins, compatible material families, explicit collision/door roles and portable recipes into the next build. This supports faster native placement and eligible repetition without sacrificing source layout.
5. **Optional presentation:** try a short arrival camera sequence only after the playable route is complete. Keep normal walking and GM recovery controls readily available.

These are candidates and decision rules, not completed scene enhancements. This batch leaves the accepted construction direction and current playable build unchanged. The20-credit receipt and evidence limits are in the private/local retrieval record; full transcripts are not published.

