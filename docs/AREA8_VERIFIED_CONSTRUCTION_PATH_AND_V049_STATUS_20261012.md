# Area 8: validated construction path and current checkpoint (2026-10-12)

## Installed skill authority
The installed **AI 3D Asset Workflow v2.6.5** (release `pluginrel_6acd4df0d8408191bc9e9d8a4323740b`) was read back in this turn. Its binding reference `skills/meshy-asset-pipeline/references/AREA8_ROOM_ASSEMBLY_LESSONS_V265.md` already records the productive Meshy-to-Blender construction loop. Retain it; this document adds the later checkpoint and distinguishes observation from acceptance.

## Verified lessons to reuse
- Ground the plan and dimensions in the source, explicitly separating 10-ft walkway as source fact from radius and passage estimates.
- Meshy integrated image reference and textured GLB supply distinctive art style; reject the wrong silhouette before costly conversion.
- Preserve the provider GLB. Make a versioned, independent Blender mesh derivative for precision corrections; inspect texture/UVs after editing.
- Manufacture real connector faces on the derivative, rather than relying on angle placement or AABB overlap. In Area 8, tested plane trimming and radial parameter normalization replaced the earlier scalloped ring.
- Test just two modules using actual triangle-BVH surface sampling, then test every repeated seam and last-to-first closure before accepting a ring: 30/30 two-sector sampled crossings at max 2.82 mm and 312/312 full-ring sampled crossings at max 7.07 mm. These results are *sampled* and do not prove global watertightness.
- Reuse corrected assets with quaternion-aware evaluated world transforms, a common radial origin and exact source-tagged layout. Derive matching walls and roof only after their respective physical interface checks.
- Inspect actual PNG contents, not just render status or file size, with hero and structure views. Visually plausible does not equal DM approved or structurally certified.

## Current observed runtime
A read-only connected Blender inspection on 2026-10-12 reports saved clean `G:\My Drive\D&D\Foundry Bridge\assets\Area8_Rebuild_v049_CeilingPipeDerivative.blend`, active scene `Area8_RADIAL_DATUMS_NONRENDERED`, 184 visible scene mesh objects. Named components include `AREA8_ROOF_DERIVED`, three `SEWER_DISCHARGE_00..02`, `POOL_SEWAGE_SURFACE_v001`, `POOL_SHALLOW_SHELF_00` and `AREA8_PLANAR_TENTACLE_APPROVED_DECOR`; these named objects establish scene presence only, **not** that the pipes physically discharge into the pool, that roof bearing is sound, or that pool depths match the map.

## Remaining construction and QA gates
Review v049 from real hero and cutaway PNGs. Measure pipe outlet-to-flow-to-pool connection, roof-to-wall bearing/closure, navigability, pool depth bands and exits, texture health, visible geometry/missing faces and runtime performance. Save next numbered revision only after source checkout and backup. Preserve v014 visually accepted floor/wall/corner baseline and all intermediate scenes. Current DM feedback: 'looking much better'; final room acceptance has **not** been given.
