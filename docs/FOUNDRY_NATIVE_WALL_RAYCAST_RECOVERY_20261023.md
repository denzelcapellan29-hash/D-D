# Area8 live native wall raycast recovery — 2026-10-23
**Status:** Native 3D Canvas movement/sight/camera BVH raycast **PASS** for one north-wall sample; **actual TokenLayer.moveMany wall-blocking NOT TESTED**; suspected temporary/proxy collision mesh provenance remains to verify.

## Safety and source
All primary MCPs rediscovered: Foundry121, Acq_3D_Map14, Blender26, Godot91 and external GitHub/Drive. Protected original source `NUEDEFAULTSCENE0` revision `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f` unchanged. Inactive QA clone `sW4aXZgKXj1cH0US` 163 tiles /13 regions /2 QA tokens. Installed first-party bridge SHA `b25a35aa23c53e361222c53ab0518e7e30f2b17f70df3fef861db3b3151cd631`, active browser longpoll1, queues empty. Previous deployment attempt of new wall-collision adapter was blocked during stage transfer; incomplete local staged file was deleted, installed source remains verified. No vendor/scene writes.

## Actual live read-only inspection
- Successfully switched GM **local view only** to the inactive QA clone, without pulling players; clicked installed native Preview 3D toolbar. Runtime `active=true, ready=true, loading_count=0`.
- Invoked first-party existing `inspect_native_playability` read-only through GM browser RPC; HTTP200, `ok=true`, QA clone SHA preserved.
- Native Three/BVH collision group counts `move=7`, `sight=9`, `camera=4`.
- North-wall sample from Three coordinates `[1.92,0.12,0.55]` to `[1.92,0.12,0.03]`, native **movement ray hit** at `[1.92,0.12,0.16697797005]`, ray distance `0.38302`, object `TEMP_AREA8_WALL_ZERO_PIVOT`, parent `Area8_RADIAL_DATUMS_NONRENDERED`; native camera hit same object and position. Sight rays intersect at `z≈0.178` and `z≈0.166978`.
- QA Monk downward movement ray from y0.32 hits `AREA8_ROOF_DERIVED001` at y0.280568, plus `RADIAL_CONNECTOR_A001` at y0.012514. This can complicate player-eye camera positioning and movement support, but no new gameplay proof.
- **Provenance caution:** `TEMP_AREA8_WALL_ZERO_PIVOT` appears temporary/nonrendered in its names. Do not declare final approved architectural wall blockage until its approved GLB provenance, physical location and native movement interception are validated.
- GM view restored accepted source via `manage_vision_qa_scene(action=restore_view)` SUCCESS; original source revision unchanged, runtime on source inactive. No token session/pose mutated in this turn.
- User-facing result is a bounded raycast pass; blocked token movement remains unverified. Do not confuse these.

## Next safe gate
Inspect the wall Tile provenance, actual mesh flags and relative token approach position using native first-party read-only source/inspection. If grounded, execute **one** guarded QA-only native `TokenLayer.moveMany` movement at wall with strict token pose readback and rollback. Blocked-movement adapter is staged in GitHub `feature/native-wall-collision-qa-20261023`, isolated Node four tests PASS but **NOT DEPLOYED**. Prior transfer was safety-blocked; never bypass platform protections. Maintain original source and inactive QA clone as exact checkpoints.
