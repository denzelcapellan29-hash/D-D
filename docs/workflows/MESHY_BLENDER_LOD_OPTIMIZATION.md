# Meshy -> Blender -> Foundry Mesh Optimization Workflow (draft v001)

Decision 2026-10-10: Preserve original high-resolution Meshy GLBs as immutable source assets; optimize copies in Blender before repeated-instance assembly and before any Foundry/3D Canvas export. Do not procedurally replace visible Meshy-authored architecture.

## Per-asset tiers
- SOURCE: untouched Meshy GLB, textures, task ID, approved reference, exact provenance, original bounds and triangle count.
- CINEMATIC: highest acceptable visual quality for close-up Blender renders; original or minimally cleaned mesh.
- SCENE: lower-poly mesh for repeated objects and mid-distance camera shots; linked instancing, normal preservation, texture/material consolidation.
- RUNTIME: stricter low-poly GLB for Foundry/3D Canvas after profiling; preserve UVs, bake normals/details and PBR textures from SOURCE/CINEMATIC, check silhouette and material response.

## Deterministic processing and QA
1. Inspect source dimensions, triangles, mesh parts, material slots, UVs, textures, normals, manifold status and license.
2. Make a versioned duplicate. Apply scale only to the duplicate, normalize origins and orientation, preserve snap geometry for architectural modules.
3. Trial decimation in reversible steps (e.g. 50%, 25%, 10% of source triangle count), using silhouette and texture distortion checks; do not assume a target is visually safe.
4. Bake tangent-space normals and material maps from high-resolution source to optimized mesh where appropriate. Ensure UVs remain valid; generate LODs as distinct versioned files.
5. Compare same camera, lighting, distance, exposure and resolution across SOURCE and optimized variants, including close-up and actual in-room views. Inspect renders, do not accept based solely on triangle counts.
6. Record source and optimized triangle counts, reduction %, bounds delta, material/texture differences, render times, file sizes, and visual QA outcome.
7. Publish only accepted GLBs to runtime/export manifest; retain source GLB and Blender QA checkpoint.

## Area 7 diagnostic note
Last successful render: v005 with 32 crawling-claw instances. v006a added 174 linked instances (206 total). Source crawling claw: 580,662 triangles; all 206 share one mesh datablock. At 206 instances, nominal scene triangle submissions from claws alone are ~119.6M; this is a performance concern, not a proven cause of black renders. On 2026-10-10, disabling all 174 new claws and rendering from the original camera **still produced black output**. Do not attribute the failure solely to instance count. Isolate by loading the last known render-good v005 checkpoint and comparing settings/output with v006a; use a tiny controlled diagnostic scene if necessary. Hard-stop production changes until an actual valid render can be captured.

## Art direction
Area 7 keeps checkerboard stone tile appearance, circular high chamber, suspended giant-foot crusher, no torches, dim blue footprint rune lighting. Sparse foreground hero claws plus lower-poly repeated background claws; do not need hundreds of expensive full-resolution visible models to communicate hundreds of remains.
