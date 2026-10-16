# Foundry 3D mesh loader patch (2026-10-15)

Installed module inventory via autonomous agent found levels-3d-preview/scripts/entities/tile3d.js. Proprietary source not published. Creator wiki Tiles says Dynamic Mesh not None ignores 3D Model path, and depth, width, height and auto-ground are separate settings.

Read-back of first-party Acq bridge v0.2.8 established existing inspect3dScene uses entity._worldBoundingBox, not evaluated descendant loaded meshes. Runtime Tile AABB alone cannot confirm successful GLB render.

The no-Draco material-free test Tile eIbwcCUdmuyNPfyE was removed by revision-guarded exact ID operation, returning original scene revision d93c7518ac199375b7705715c1faf124b5cd35136ba8e8707ddc326ac15546ad. Approved Area8 Blender v082 remains unchanged.

Staged NOT DEPLOYED first-party code: tools/foundry3d/acq-foundry-bridge-v029-mesh-diagnostics.js. Adds bounded read-only mesh_evidence field to existing inspect_3d_scene with Three.js Object3D root keys, descendant isMesh count, mesh geometry/material, vertex counts, visibility and local transforms. No module deployment, actual syntax test, or Foundry fixture PASS yet. This is diagnostic implementation candidate, NOT runtime feature.

Next: code validation, immutable installed-module backup and guarded deploy only outside a live session; Windows dev agent v0.1 cannot deploy, requires safe signed/guarded update. Then empty scene baseline, one small genuine GLB, loader evidence, fixed-camera screenshots, independent Box3 and 5ft grid calibration. Area9 remains frozen.
