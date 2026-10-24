# Baileywiki Foundry + 3D Canvas tutorial study — 2026-10-24

**Status:** SOURCE-RETRIEVED / IMPLEMENTATION-UNVERIFIED. This is an original engineering digest of third-party tutorial captions, **not** a release acceptance report. Avoid distributing full copyrighted transcripts. Each citation below points to the creator's public video and a useful timestamp. The auto-captions can contain errors.

**Context:** Foundry V14 + native 3D Canvas is our primary runtime; in-person one-GM-screen; Blender-authored source-faithful GLB sections, native floor/wall/door/camera/vision when possible, and no manual micro-Tile rebuilds. Existing accepted Area8 runtime remains untouched. Godot experimental. Current artifact/runtime behavior and DM decisions supersede older video UI claims.

## Retrieved full timestamped caption tracks
| ID | Video | Published | Transcript |
| --- | --- | --- | --- |
| `cst7RRv8KHQ` | [Baileywiki: FoundryVTT Basics — Getting Started With Foundry in 2026](https://youtu.be/cst7RRv8KHQ) | 2026 | ACCESSIBLE |
| `RCzoblymlfM` | [How to 3D Part 2 — Using 2D Maps in 3D](https://youtu.be/RCzoblymlfM) | 2024 | ACCESSIBLE |
| `j9sRMW2naAE` | [How to 3D Part 3 — Tokens](https://youtu.be/j9sRMW2naAE) | 2024 | ACCESSIBLE |
| `zsQVGB0FJgU` | [2023 Ep. 3 — Scene Setup and Map Types](https://youtu.be/zsQVGB0FJgU) | 2023 | ACCESSIBLE |
| `6Qw4YrnmxoU` | [2023 Ep. 4 — Mapmaking (Exterior)](https://youtu.be/6Qw4YrnmxoU) | 2023 | ACCESSIBLE |
| `Izs7oC1JvNE` | [2023 Ep. 4.5 — Heightmaps and the Gradient Shader](https://youtu.be/Izs7oC1JvNE) | 2023 | ACCESSIBLE |

Original playlist: https://youtube.com/playlist?list=PLbNUuLLqMgaBfNAyYb6mhg4pR4bPcHXqM . Four playlist entries have not yet had transcripts retrieved in this study: Part 1 installation `5VKs1Lul_Rg`, 3D Automated Animations `3kbUVpnn45Y`, Colour Swap and Overlay Shader `F8i8QWsu_hM`, Cutscene Tool `3KnOl-Agc3I`. Actual playlist order/availability may change.

## Source-grounded lessons and engineering implications

1. **Keep native gameplay semantics distinct from visible geometry.** [Part 2, 01:04–02:41](https://youtu.be/RCzoblymlfM?t=64) demonstrates that a 2D scene's native walls, doors, lighting and fog can still function in 3D when the default rendered 3D walls/doors are hidden. **DESIGN HYPOTHESIS:** for our imported sections, native Foundry Wall doors should own passage/LOS when they can, while art GLBs need carefully defined non-blocking portal envelopes. This is **NOT** a demonstration of a moving hinged GLB or a proven fix for our failed `doorStyle=1` leaf.
2. **Use scene rendering controls rather than painting over geometry defects.** [Part 2, 03:14–04:21](https://youtu.be/RCzoblymlfM?t=194) shows lowering the native 3D resolution multiplier (example: 1440p to 1080p via 0.75) and recommends a Chromium-based runtime for performance. **VERIFY** an actual V14/3D Canvas 9.x setting and native FPS/memory before adopting the example value; do not hide clipping, gaps or missing PBR relief behind lower resolution.
3. **HDRI light is not the displayed skybox.** [2023 Ep. 3, 07:55–09:30](https://youtu.be/zsQVGB0FJgU?t=475) distinguishes environmental lighting from the panorama visible on the horizon. [Part 2, 11:35–15:40](https://youtu.be/RCzoblymlfM?t=695) also describes atmosphere/fog treatment for dungeon backdrops. **TEST** a matched HDRI/sky/background/exposure setup on the same real GLBs from eye-level, reverse, overhead and outdoor horizon. Do not use image/fog tricks to conceal source-architecture discontinuities.
4. **Lighting and vision are different layers.** [Part 2, 09:26–09:57](https://youtu.be/RCzoblymlfM?t=566) explains that changing 3D sun/shadow appearance does not automatically change token vision; native Foundry lights can continue working with the 3D presentation. **TEST** real GM screen light/vision/camera behavior on the imported fixture without converting non-GM fog inspection into a default blocker.
5. **Native camera and scene-load controls first.** [2023 Ep. 3, 02:51–07:24](https://youtu.be/zsQVGB0FJgU?t=171) discusses optional Game Camera constraints, maximum elevation and scene-entry camera capture. Our current first-person/free camera is already accepted, while an earlier GameCamera black-frame test failed. **VERIFY** these specific V14 controls before relying on them; GameCamera is optional unless the DM explicitly requires it.
6. **Protect complex tile scenes before merging or flattening.** [Part 2, 19:09–21:36](https://youtu.be/RCzoblymlfM?t=1149) discusses co-planar multi-tile z-fighting and warns that a tile-combiner operation changes scene documents and can flatten animated elements. Our project requires whole source-authored GLB sections and semantic manifests, **not** irreversible manual tile flattening of accepted Scenes. Use a disposable source-backed QA clone for any merge experiment.
7. **Source-driven terrain relief and slope-responsive materials.** [2023 Ep. 4, 00:15–03:46](https://youtu.be/6Qw4YrnmxoU?t=15) shows native terrain-from-heightmap and grass/dirt/rock blending according to slope. [Ep. 4.5, 02:13–09:27](https://youtu.be/Izs7oC1JvNE?t=133) explains black-to-white height correspondence, relief scaling, and gradient shader transitions by inclination **or** elevation; texel repeat and smoothing tune result. These are art-direction and native-feature references, **NOT** permission to manufacture arbitrary structural masters outside the DM-approved fabrication exceptions or replace source-specific elevation layouts with random terrain.
8. **Decorations must rest on real surfaces and preserve readability.** [2023 Ep. 4, 05:22–08:21](https://youtu.be/6Qw4YrnmxoU?t=322) places rocks relative to slopes and adjusts floating props using native transform controls. For our pipeline, source-backed assets and real connector tests take precedence over freehand scatter; use these techniques as visible QA criteria (no floating rocks, arbitrary seam disguises, repetitive geometry).
9. **Merging repeated assets is a conditional performance option.** [2023 Ep. 4, 08:21–09:23](https://youtu.be/6Qw4YrnmxoU?t=501) demonstrates reducing a repeated-prop scene from 37 native Tiles to 7 render objects. This is a version-specific example, not a performance guarantee or instruction to merge our semantic, collision or interactive assets. Only benchmark on a reversible fixture after native collision/door/roof ownership is preserved.
10. **Onboarding, backups and modules.** [2026 Basics, 04:06–10:56](https://youtu.be/cst7RRv8KHQ?t=246) covers setup warnings, backups/snapshots, system/module installation and module dependencies; [24:11–25:32](https://youtu.be/cst7RRv8KHQ?t=1451) covers Scene directories. This is useful operational literacy, but the tutorial itself discusses V14 as upcoming in the recorded walk-through. Our installed V14.368 is authoritative for UI/API specifics. **Never update Foundry, enable modules, or change world settings merely because the tutorial suggests it.**

## Prioritized verifications for the dedicated Foundry chat

**P1 — native portal ownership:** On an inactive isolated GM QA Scene with genuine floor/wall/door GLBs, evaluate native Wall door passage and sight separately from the rendered door Tile. Compare closed/open/reclosed, actual player-eye clearance, and actual native token traversal. The current centered hinged Tile/duplicate frame failure is NOT solved by a tutorial statement about 2D doors.

**P2 — supported GM presentation:** Verify whether current native scene controls allow independent skybox, HDRI, exposure, fog, initial camera and FPS/free camera. Render matched samples on one accepted geometry source. Preserve source art and scene-level secrets.

**P3 — outdoor shader/art parity:** Compare source-faithful approved outdoor GLB material transitions against native slope/height gradient presentation only on an authorized reversible decorated fixture. Reject random terrain reshaping, horizon cutoffs and props floating above actual ground.

**P4 — actual performance and reload:** Capture resolution setting, FPS and runtime/memory before/after controlled changes; inspect source model instancing vs a measured/native merge alternative only where reversible and semantic boundaries remain correct.

## Authority and handoff

- **SOURCE:** captions at the linked timestamps (creator tutorial observation).
- **DESIGN_CHOICE:** candidate engineering practices from these observations, subordinate to DM decisions and exact official map source.
- **UNVERIFIED:** all effects on our currently installed V14/3D Canvas 9.x until separately tested.
- **AS_BUILT:** original project's existing importer, GM Scene checksums, 7-GLB QA and door passability results in the current Foundry QA handoff; this note does not overwrite those outcomes.
- Full transcript text remains with the provider rather than in public GitHub. Do not publish private campaign source pages, GM lore or private Drive documents in this file.
