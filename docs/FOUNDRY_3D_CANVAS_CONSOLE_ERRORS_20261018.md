# 2026-10-18 — Foundry 3D Canvas shared loader: actual browser console evidence

Status **UNRESOLVED / no root-cause proven / no campaign scene edited**. DM screenshot in current chat of Foundry desktop DevTools Console in active Test after 3D Canvas spinner; Foundry v14.368 / dnd5e6.0.5 / 3D Canvas9.0.35. Screenshot exists as user conversation attachment, not yet a verified Drive file.

## Actual displayed errors, with proper interpretation
1. **WebGL graphics-state error, repeated 256 times**: `WebGL: INVALID_OPERATION: uniformMatrix3fv: location is not from the associated program`, followed by `WebGL: too many errors, no more errors will be reported to the console for this context.` A uniform is submitted under a mismatched compiled shader program / WebGL state. This is serious graphics runtime evidence, but is NOT by itself proof our native FPS camera patch or 3D Canvas module shader is the unique cause.
2. **Three 404 file requests** under `modules/canvas3dcompendium/..._Metalness.webp`, `...AmbientOcclusion.webp`, `...Emissive.webp`. These are real missing texture resource requests in Canvas3DCompendium/associated material. The full request path is truncated by console width; need DevTools Network request URL / module asset audit to determine whether source files missing or references stale. Do not invent replacements or modify vendor libraries blindly. Some PBR missing maps may use defaults but these errors must be addressed before 3D render acceptance.
3. **Deprecation WARNINGS** `Scene#background` use `Level#background` and `Level#textures`, stack `Levels3DPreview.createBoard(main.js:979:39)`. Compatibility deprecation since Foundry 14; warning alone doesn't prove a fatal loader exception. Relevant to upstream compatibility but do not misclassify.
4. **UI viewport minimum error** `Foundry Virtual Tabletop requires a usable window dimensions of 1024px by 768px or greater; current 982px by 794px; zoom factor may be applied.` The screenshot has DevTools docked on right, reducing effective width below Foundry minimum; this can introduce an additional rendering/UI obstacle during diagnosis and may not explain earlier full-window spinner. Close/undock DevTools and use 100% zoom for actual load attempt.
5. `Worker TextureCompressor of FogExtractorCanvas3D | Initialized Worker` indicates only that a worker started, not that renderer initialized.

## Live readback
- Foundry ordinary `scene_list` remains responsive and returns Test active, Area8/default inactive; Area8 original scene documents previously verified 162 Tiles + 36 Walls + 13 Regions, source kept.
- Read-only Acq_3D_Map inspect briefly succeeded and returned `levels3d_active:true`, Test scene environment `exr=modules/canvas3dcompendium/assets/Beautiful-Sky/2K/Sky_LowPoly_01_Day_a.webp`, `renderTable=matpaper`, single optimized road Tile source and remaining three hidden/blank, runtime bounds null. `capture_3d_view` subsequently returned RuntimeException; follow-up `inspect_3d_scene` also returned RuntimeException, so client bridge still unstable and 3D renderer cannot be certified.
- Attempt to empty the remaining QA GLB in Test could not be made, because guarded modification needs fresh revision and fresh inspector was invalid. Last independently verified normal Foundry scene readback 4 Tiles / 1 visible. Do NOT claim scene empty, no successful user-visible GLB render.
- Blender MCP now reports `Session terminated`; do not infer active .blend has changed. No local shared-module JS edits, GLB changes, Meshy charges or Area8 changes were performed in this diagnostic.

## Next safe A/B diagnostic
1. With DevTools **undocked or closed** and Foundry zoom 100% in a window >=1024×768, restart 3D Canvas in Test to see if viewport-size issue materially contributes. Earlier full-window spinner means no guarantee.
2. In a non-invasive Network tab (Preserve log on), click the first missing `*.webp` 404 and copy **Request URL**; identify one precise Canvas3DCompendium texture path that is absent, compare module physical file with expected reference. Do not fabricate files or overwrite a vendor module.
3. Capture the **earliest genuine uncaught red JavaScript error** after full reload (not just warning or 404). WebGL `uniformMatrix3fv` repeated errors may reflect GPU shader state, library conflict or context handling; neither cause nor specific fix established.
4. When safe Acq inspect and exact revision recover, reversible QA-only one-road blank/hidden Test Tile to test empty scene; do not modify Area8, original GLBs or vendor patched `main.js`. If empty Test fails, prioritize engine/module/GPU config. A/B original vendor JS only in controlled rollback with full backups and user-approved safe plan; preserve working FPS mouse-look.
5. Pause all Episode2 asset placement. A manifest PASS is never a renderer PASS.

Canonical incident reference: `docs/FOUNDRY_SHARED_3D_CANVAS_LOADING_INCIDENT_20261018.md`; installed private AI 3D skill v2.7.27. 
