# Foundry + 3D Canvas skill discovery — 2026-10-15

Status: read-only tool and archived-source audit. No scene modifications, no skill release published.

## Verified
Hosted Foundry MCP connected to world `acquisitions-incorporated` (Foundry 14.368, dnd5e 6.0.5). Foundry screenshot shows 3D Canvas 9.0.35 and Acq Foundry Bridge 0.2.8 enabled. Custom Acq_3D_Map remains unavailable end-to-end: tunnel client has not polled within 300 seconds. Historical local ports 18747/18748/8083 listening do not demonstrate remote connectivity.

## Tool boundary
Hosted Foundry MCP exposes 121 tools for RPG rules, tokens, actors, compendia, journals, basic scenes and 2D navigation. Custom 3D MCP exposes seven: inspect_3d_scene, search_3d_assets, set_3d_camera, capture_3d_view, set_3d_environment, apply_semantic_objects, validate_scene_manifest.

## Archived implementation inspection
User-provided Acq_Foundry_3D_MCP (3).zip is October 5 source, NOT independently verified as deployed bridge v0.2.8. Its MCP server forwards JSON RPC to localhost:18747; JS accesses game.Levels3DPreview private state. Camera modifies camera.position and controls.target directly; captures renderer.domElement.toDataURL, restoring camera by default. Inspection returns Tile x/y/width/height/elevation/rotation and selected flags, not evaluated Three.js world matrices. Environment changes write allow-listed levels-3d-preview flags. Semantic objects keyed by flags.acq.semantic_id are created/updated sequentially; manifest validation checks identity/counts only. Archive internal protocol also contains asset_upload, tile_set_model3d, generic CRUD, but those are not exposed as seven custom MCP tools. Snapshot op is not verified rollback. Archived code can NOT establish deployed v0.2.8 runtime behavior.

## Mandatory skill gates
1. Re-establish custom MCP full tunnel request/response read-only.
2. Audit actual installed module/agent v0.2.8 and verify v0.2.7 hotfix; distinguish from archived files.
3. Inspect installed 3D Canvas 9.0.35 coordinate units, tile/model transforms, camera, environment, GLB loader, collision, and renderer APIs with version proof.
4. Create disposable isolated low-poly GLB fixture ONLY after backup and confirmed connectivity. Test 1 unit/5ft grids, rotations/origins/scale and independent evaluated 3D readback.
5. Prove fixed camera captures, image fidelity, PBR/lighting baseline, navigability/occlusion, scene revision/rollback, performance budget and player safety.
6. Only then produce skill release and proceed to Area8 pilot. Area9 development frozen by DM decision.

Working detailed technical audit: conversation artifact `Foundry_3D_Skill_Discovery_Audit_2026-10-15.md`. No GM-visible scene writes made.