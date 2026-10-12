# Area 8 v049 production and QA update (2026-10-12)

Current latest saved clean room: `Area8_Rebuild_v049_CeilingPipeDerivative.blend`, local Google Drive synced assets folder. Real hero PNG inspected and independently indexed in Drive: https://drive.google.com/file/d/16JpkYxfOgHQz9VeuI7UCYR3K1klEnxOc/view . Structural basin cutaway v044: https://drive.google.com/file/d/18YfBuBtI2RJ4P7c7MKTU-VEchzN23ix1/view . Room is visually promising **NOT DM accepted**; passages, true roof bearing and complete surface/physical connector certification outstanding.

## Construction successes

- v038 baseline: enclosed vaulted roof, three ceiling-discharge meshes, tentacle, radial wall, water surface and walkway.
- v043: manufactured 12 linked outer basin-wall sectors from independent Meshy-derived radial floor geometry, connecting to a 3-foot-shallow region, plus 12 inner basin-wall sectors to 10-foot-deep center; separate derived bottom disk.
- v044 inspected actual *water-hidden/roof-hidden* structural PNG: recognizable stepped basin, but bright stone repetition.
- v045 restored all visible room elements and rendered a real hero view.
- v047 corrected tiny repeated radial shallow shelf seam via copied mesh-angle factor 1.0065; BVHTree raycasts sampled 60 joins, 60/60 with surface hits on both copies, max sampled top-height delta 1.099 mm (10mm target).
- v049 roof/pipe extension: *local curved roof underside* at actual three pipe XYs z=4.224m, original pipes ended at z=3.100m and v048 naive global-AABB seating got z=3.135m, leaving a real ~1.089m gap. Independent 304,043-vertex Meshy-asset derivative smoothly elongated upper pipe parts by 1.14m, preserving lower discharge. Local actual geometry now pipe tops z=4.275m (~51mm nominal penetration into vault at sample coordinates), outlet bottoms z=-0.225m, submerged ~34mm below water surface. This is numerical placement evidence, not exact patch certification.

## Important QA process correction

BVHTree.ray_cast distance uses **object-local units**, not world units. On anisotropically scaled source GLBs, a 6-unit local ray can be too short to reach a bottom 3 meters below. Initial test falsely returned zero deep-basin hits, and an unnecessary face-reversal experiment was conducted in v046. v046 was **reverted**, never promoted. Retest from clean v045 using 40 local ray units gave center-bottom 12/12 hits at r=0,2,4m and z≈-3.047m, proving geometry present. Shallow annulus z≈-0.829m (upper walkable face of slab whose support level is -.9144m); seams narrowly open exactly at the angular boundary until v047 correction. Always transform ray endpoints into local space or choose adequate local-distance bound after scale accounting. Never infer geometry is missing from a short local ray.

## Next

Inspect remaining entrance passage alignments against printed map; test actual roof-wall physical bearing and first-person walkability; develop better sewage flow visuals and underwater material if supported by source; avoid unrelated procedural visible geometry. Retain all source GLBs and earlier approved visual v014.
