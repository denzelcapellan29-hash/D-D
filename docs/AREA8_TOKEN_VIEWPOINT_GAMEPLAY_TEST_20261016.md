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
