# Area 8 native 3D Canvas 9.0.36 — settings and first-person QA
**Date:** 2026-10-22. **Status:** live first-party native settings + first-person QA PASS; 3D collision/vision/player traversal and cutscene QA UNVERIFIED. No Scene document, accepted Blender source or vendor module modifications.

## Decision and intent
DM requested testing the **native** 3D Canvas camera on existing Area 8 and warned that 3D Canvas module settings can diverge from Foundry defaults. Respect approved native-first policy: discover installed module settings before building custom camera behavior. Blender remains authoritative source; Godot and 3D Canvas compete as playable runtimes.

## Recorded baseline
- Active Foundry v14.368 world `acquisitions-incorporated`, Scene `NUEDEFAULTSCENE0`; 3D Canvas `levels-3d-preview` v9.0.36, Mapmaking 10.0.1, Premium 9.0.3, bridge v0.2.8.
- Saved scene revision before and after read-only bridge inspections, GM camera control, and native mouse input: `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`.
- 161 tagged 3D Tiles/162 total Tiles, six lights, 13 Regions, 36 Foundry Walls, two QA token documents. Saved and visually accepted Blender v082 Area8 source untouched.
- Scene Foundry `tokenVision=true`; `environment.darknessLevel=0.55`; `fog.mode=0`, `grid.size=100`, `grid.distance=1`. No assumptions that the numeric '60' token range represents correctly calibrated feet in a scene with grid.distance=1.
- Source skill: `FOUNDRY_SIGHT_DARKVISION_V2724.md` and `FOUNDRY_FPS_FREE_LOOK_V2723.md`. Historic v9.0.35 third-party camera vendor patch is NOT automatically reapplied on v9.0.36.

## LIVE settings from new first-party read-only `inspect_3d_settings` GM handler
All observed values are actual `game.settings.get('levels-3d-preview', key)` with source registration/scope, not assumed defaults.

| 3D Canvas setting | Scope | Observed |
|---|---|---|
| enableGameCamera | world | false |
| gameCameraDefaultGm | world | true |
| gameCameraAutoLock | world | true |
| gameCameraMinAngle / MaxAngle | world | 45 / 45 |
| gameCameraMinAzimuth / MaxAzimuth | world | -180 / 180 |
| gameCameraMaxZoom | world | 1 |
| gameCameraClipping | world | false |
| cameralockzero | world | true |
| altCameraControls | client | **true** |
| screenspacepanning | client | true |
| enabledamping | client | false |
| exactTokenVisibility | world | true |
| dynamicTokenVisibility | world | false |
| allTokens | world | false |
| preventNegative | world | true |
| enableShaders / enableEffects | client | true / true |
| sharedContext | world | true |
| lightCacheSize | world | 4 |
| regionsAlwaysFlat | world | false |

3D Canvas **Tile** flags: `cameraCollision` explicitly true on only 12 of 162 Tiles, false on zero, absent on 150. `collision` explicitly false on one Tile and absent on 161 (native default true); `sight` absent on all 162 (native default true). Missing flags represent *default behavior*, NOT verified physics/occlusion. Scene `showSceneWalls=false` hides the visually procedural 3D Wall rendering while maintaining invisible 2D sight Walls.

Two QA Token sight profiles (source-backed historical):
- Druid `KB7cUY9hXEXHeJqV`: sight.enabled true, `basic`, range 0, angle 120°, elevation 0.
- Monk `iSbK8OUBuUEjIGGu`: sight.enabled true, `darkvision`, range 60, angle 120°, elevation 0.13.
- GM had 0 controlled tokens; `canvas.effects.visionSources.size=0` in the GM view. This is expected unless a vision-providing token is selected, not a failed feature. Non-GM token ownership and true player vision have not passed QA.

## Source-grounded native mouse mapping root cause
Exact installed upstream 3D Canvas tag `9.0.36`, `scripts/handlers/GameCamera.js`, `setControlPreset()`: with `altCameraControls=true`, native `OrbitControls.mouseButtons = {LEFT: undefined, MIDDLE: THREE.MOUSE.ROTATE, RIGHT: THREE.MOUSE.PAN}`. With setting false: `LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN`.
Thus native first-person left-drag correctly did **nothing** (yaw 0.099° → 0.099°, pitch -3.551° → -3.551°). It was an invalid input for the current module setting, NOT proof a custom camera patch is needed. NO setting change required for native rotation.

## Live v9.0.36 first-person tests and rollback
- Via first-party QA-only `Token.control({releaseOthers:true})` and native `l3d.toggleFirstPerson()`/`setCameraToControlled`, entered first-person with the existing druid. Native runtime reported `first_person=true`, `GameCamera=false`, druid controlled and loaded 3D head anchor. Exact bridge-owned camera session restored pretest position `(1.92,0.15,0.31)`, target `(1.92,0.112681,0.916432)`, near clip `0.01` and firstPerson false. QA token `release()` restored zero selections. Full enter/restore 5.64 seconds; no document revisions changed.
- Actual Windows mouse left-button drag inside the client canvas 150 px right / 70 px up produced yaw change 0°, pitch change 0°; expected, because LEFT is unbound under `altCameraControls=true`.
- Actual Windows mouse **middle-button** drag, 170 px right / 80 px up, while native first-person on druid: actual 3D renderer camera yaw `0.099° → -62.751°` (**-62.85°**) and pitch `-3.551° → 20.917°` (**+24.468°**). These values were measured from GM bridge `inspect_3d_scene` before and after input. Camera and token selection were restored by exact owned sessions. No persistent setting, document or GLB writes.
- This technically validates FIRST-PERSON CAMERA ROTATION in GM on the installed 9.0.36 with **native controls, no custom camera patch**. Does NOT validate keyboard token movement, follow target during movement, wall/camera collision across the entire room, physical elevation, non-GM player eye or cinematic control after cutscenes.

## MCP engineering
- First-party bridge read-only `inspect_3d_settings` and temporary bounded `native_select_qa_token` native input adapter installed with GitHub source commit `0930820c04288a07c62a5269b392959647728758`, local first-party JS SHA256 `87853c5e552faebcf74494564d5e7e934e040a459764c728a13f94ca6ef7660f`, immutable backup `native-qa-selection-20261022T192119Z`. Settings-inspector previous build backup `module-settings-inspector-20261022T191736Z`. Node syntax and a dedicated native control/select/restore fixture passed.
- Running Python MCP extended by exactly two tool wrappers `inspect_3d_settings` and `native_select_qa_token`, using pinned GitHub source `ce26b2b4c2abf21c1e280281cd458a74b2dea143`, source SHA `9c961ca9f4e81e46ca9a13da90c335690a5c1f48e2be3ee0485fa14eaa6c8e34`, immutable backup `mcp-native-settings-20261022T192758Z`, controlled Python-only MCP restart. Live Streamable HTTP protocol `2025-06-18` `tools/list` returns **13 tools**, both new registrations, and actual `tools/call('inspect_3d_settings')` PASS with unchanged saved Scene revision. Existing ChatGPT conversation may still advertise stale eight tools; runtime service is independently verified, no manual installer.
- Third-party 3D Canvas files `main.js` and `GameCamera.js` unchanged in this work. Protected first-party FPS camera anchor preserved. No need to set `altCameraControls=false` unless DM specifically wants native left-drag instead of middle-drag.

## Next bounded native-first gate
1. Compare native keyboard character motion/follow yaw/pitch and actual floor support on a DUPLICATE Scene with QA token, no accepted Area8 scene data changes. Use genuinely native input, not only TokenDocument teleport.
2. Test native cameraCollision against walls and ceilings; only 12 wall Tiles explicitly enabled, 150 unset. Test Game Camera clipping separately from first-person camera: the `gameCameraClipping` toggle does not stand for all possible camera occlusion.
3. Test QA monk/druid native vision with selected token and a non-GM player account; verify 120° direction, light cutoff, elevation/roof occlusion and fog caveats; don't claim true 3D volumetric fog.
4. Test native cutscene author/play/restore, then compare Area8 and Area10 GLB/manifest fidelity and FPS vs Godot.
5. Decide whether old 9.0.35 mouse-look vendor patches are unnecessary (for rotation, now proven) separately from token-follow compensation (still requires v9.0.36 movement test).

**Artifact classification:** Tested native settings/mouse-look = ENGINEERING PASS. Full player-ready Area8 = UNVERIFIED; DM art acceptance remains only Blender Area8 v082. No scene or Blender source edits.
