# Acq Foundry Bridge read-only 3D diagnostic contract v0.1 — 2026-10-15

Status: PROPOSED SPECIFICATION, NOT CODE DEPLOYED. Applies to installed Acq Foundry Bridge v0.2.8, Foundry 14.368, 3D Canvas 9.0.35. No mutation authorized and no actual source-code readback completed. Connected Blender tool filesystem source-read attempt was blocked by safety controls and MUST NOT be worked around. Require DM-shared source copy or supported approved source-reader action.

## Proven live baseline
Custom Acq_3D_Map.inspect_3d_scene PASS: levels3d_active/available true, default scene NUEDEFAULTSCENE0, 0 3D tiles, camera position [2.88,1,1.92], target [1.92,0,.96], 5 lights. capture_3d_view produced 1920x992 actual WebP image inspected visually (default branded Foundry art surface), runtime_recovery ready, renderer/scene_graph/camera/controls true, loading_count 0. No scene edits; original revision d93c7518ac199375b7705715c1faf124b5cd35136ba8e8707ddc326ac15546ad. Intermittent command errors still observed.

## Proposed read-only `get_3d_runtime_health`
Schema: `{scene_id?, include_modules?:false}` -> `{ok,scene_id,scene_revision,server_timestamp,modules:[{id,version,active}],three:{ready,levels3d_available,levels3d_active,renderer,scene_graph,camera,controls,loading_count,errors},camera:{position,target,quaternion,fov,aspect,near,far,up,projection_matrix},canvas:{width,height,device_pixel_ratio},issues:[{code,message,stage,transient}],duration_ms}`. Redact sensitive paths/tokens. No eval, remote JS or arbitrary filesystem requests. Avoid reliance on single deprecated global without exact installed API verification.

## Proposed read-only `inspect_3d_object`
Input: `{scene_id, semantic_id?|tile_id?, include_mesh_children?:true}` (only scene-owned, allowlisted objects), no arbitrary code/path arguments. Output: `{document:{id,semantic_id,x,y,width,height,elevation,rotation,flags3d,model_path},model:{load_state,source_bounds,world_matrix16,world_quaternion,world_scale,world_AABB,world_OBB_or_corner_points,ground_offset,auto_ground,auto_center,material_summary,triangle_count},collision:{document_flags,engine_ready,measured_test_state:"UNVERIFIED"},revision,diagnostics}`. Call `updateMatrixWorld(true)` only if necessary (mutates in-memory matrix cache but not scene docs); explicitly disclose and isolate effects. Require cross-validation of matrix/Box3 with independent fixed fixture and exported Blender measured bounds. Do not claim AABB contact demonstrates actual mesh contact.

## Error/reporting and QA
Return typed errors `RENDERER_NOT_INITIALIZED`, `SCENE_NOT_ACTIVE`, `MODEL_LOADING`, `MODEL_NOT_FOUND`, `MULTIPLE_SEMANTIC_ID`, `VERSION_UNSUPPORTED`, `TUNNEL_FAILURE`, `STALE_REVISION`, `READ_TIMEOUT`, never generic `Error executing tool` without correlation token and safely redacted stage. Return readiness and timing per request. Invariant: read-only calls must leave scene document revision/hash unchanged, actor/token counts unchanged, camera pose unchanged unless explicitly requested. Test empty scene, no 3D runtime, loading GLB, one fixture, duplicate semantic IDs, client reconnect, repeated 10-call sequence. Nonblack actual screenshot and player-view visibility acceptance separate.

## Rollback prerequisite
Before scene writes, implement and test an isolated disposable scene snapshot/restore or scene clone with protected original; dry-run, revision guard, manifest diff and restore identity proof. Existing `snapshot` ack in Oct 5 archive is NOT tested restore. Strict authentic approved GLB-only visible mesh policy continues. Area8 v082 accepted preserved. Area9 discontinued.

## Next
Secure authorized installed module file copy from DM's Windows Foundry modules directory into Drive or upload; inspect v0.2.8 JS and 3D Canvas APIs, then implement minimal additive read-only command and fixture tests in version-controlled code (not blindly overwriting installed module).
