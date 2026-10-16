# Area 8 gameplay testing — token viewpoints (2026-10-16)

## Live verified
- Foundry 14.368, dnd5e 6.0.5; active scene `NUEDEFAULTSCENE0`, approved 161 source-derived 3D tile visual work preserved.
- Two explicitly temporary character Actors and tokens created for QA, **user authorized visible** because Area 8 has already been completed by players and is exclusively our test bed.
- Monk QA Actor `0RE9y8365cStS6x4`, token `iSbK8OUBuUEjIGGu`, at x1770,y300; test darkvision 60 ft (not assertion about actual monk sheet).
- Druid QA Actor `yLysDMnPJzM2WNeW`, token `KB7cUY9hXEXHeJqV`, at x1970,y290; test no darkvision (not assertion about actual druid sheet).
- Foundry `token_update({hidden:false})` succeeded for both, `token_list` independently verified both `hidden:false`; monk movement and multiple 1920x992 renderer captures succeeded. Eye-level temporary position captures DO NOT prove client-token camera binding, collision or player fog-of-war. The tokens currently have placeholder art `icons/svg/mystery-man.svg` and HP 0/0; do not use as completed encounter characters.

## Native Game Camera breakthrough — installed source read-only
Installed `levels-3d-preview/scripts/handlers/GameCamera.js` (private installed code; do not reproduce source) has `detectTargetPosition()` behavior: when Game Camera has `_forceTarget`, use the corresponding 3D token; in combat, prefer `game.combat.current.tokenId` if visible/owned; outside combat, select `canvas.tokens.controlled[0]?.id`; fallback to `game.user.character.getActiveTokens()[0]?.id`. This is **installed-code behavior**, not yet successful interactive selection/first-person test. The `update()` method can call parent `setCameraToControlled` when lock is set. Installed GameCamera also calls actual Three.js camera collision checks via the 3D interaction manager. Avoid inventing custom selection/turn switching until testing these native hooks.

## Next runtime gates
1. In a visible player/GM Foundry browser client, select monk, enable Game Camera, test view follows selected token; select druid and verify corresponding viewpoint. Then toggle true first person and return free tactical view. Capture true UI and camera state; no screenshot from arbitrary temporary camera position counts.
2. Check player-owned token configuration, vision-enabled scene, darkvision v normal character senses, ambient darkness, light visibility, solid-wall LOS blockers and fog explored-state using a player client, not only GM omniscient camera.
3. Test 3D movement/collision and floor support in each annular sector, controlled fall-through, roof and wall visibility, and route around the pool. Existing Foundry 2D token-move acknowledgement does not demonstrate 3D mesh collision.
4. Record exact native shortcuts/behavior and only add custom bridge control where necessary.

DM explicit priority: manual selection between monk/druid viewpoints, movement/collisions/character sight first; combat turn auto-follow optional. No autoplay task; hourly automation disabled.

## Follow-up QA readback (2026-10-16)
- Re-verified both visible tokens and unchanged clean approved Blender `.blend`; Foundry `actor_get` revealed both disposable level-0 characters initially had 0 HP and 0 ft speed. Corrected both via `actor_update` with `system.attributes.hp={value:12,max:12}` and `movement.walk=30`; reread both as 12/12 HP and 30 ft speed.
- Existing Foundry active default scene is 3840×1920, `grid.size=100`, `grid.type=0` (gridless), `grid.distance=1`; all two QA tokens currently have `disposition:-1` (hostile) despite standing in for PCs, and placeholder art. **Do not claim reliable 60 ft darkvision radius or player-specific fog until grid units and actor/token vision metadata are corrected and a non-GM test client renders them.**
- Installed native `GameCamera.js` uses `enableGameCamera`, `gameCameraDefaultGm`, `gameCameraAutoLock` and collision manager for camera/ground. Its `detectTargetPosition` prioritizes selected `canvas.tokens.controlled[0]` outside combat, current combatant token in combat, and user-character token fallback. This is read-only installed-code evidence, NOT exercised UI behavior. Current bridge camera tool moves a free GM camera by world XYZ but cannot select token, activate Game Camera or impersonate player.
- A latest diagnostic screenshot from elevated camera unexpectedly showed a close crop of the roof, obscuring tokens. A GM renderer capture is NOT proof tokens visibly render inside 3D Canvas or obey darkvision.
- Native turn-switch logic is already present, so do not build a competing selection mechanism. Next milestone requires UI-connected client-specific control and player-context vision verification. Preserve existing 161 source-derived Tile build.

## First-person native behavior verified from installed v9.0.35 implementation
- `main.js` `toggleFirstPerson()` refuses entry without `canvas.tokens.controlled.length`; entering stores old free camera and GameCamera state, changes near clip to 0.05, and disables GameCamera if enabled. Exiting restores prior camera/GameCamera state. This **confirms first person and Game Camera are mutually exclusive modes**; do not promise first person via GameCamera lock alone.
- During each renderer frame when `firstPersonMode` is true, implementation obtains `canvas.tokens.controlled[0]`, retrieves `this.tokens[controlled.id]`, and sets camera position from `token3d.headFast`. Therefore selecting a different token while first person is active should relocate viewpoint on subsequent frame, conditional on token having a loaded 3D representation. This is source-code-supported expectation, not verified player-client UI.
- `setCameraToControlled()` is a separate focus/third-person method and uses sight-collision check on the camera path. Avoid mixing it up with token-first-person mode.
- Actual client-side selection and toggle cannot be invoked by current Acq_3D_Map tools; `set_3d_camera` is an ephemeral GM free-camera adjustment, NOT first-person. Required user action for end-to-end test is minimal: in Foundry's active 3D Canvas, click a QA token, press L, select other token, and confirm follow; report if selection/toggle fails. No need to reinstall plugins or edit source.
- Read-only live inspect after this research: 161 3D Tiles, six lights, no regions, revision `2b107dfe95ccaf891f2192cc838aff9f7addda79200e74ef9898df4c1b79431a`. No architectural geometry edits. 3D tile flag summaries omit collision/sight flags and cannot certify them.
