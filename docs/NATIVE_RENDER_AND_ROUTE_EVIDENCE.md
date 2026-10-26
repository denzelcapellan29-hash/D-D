# Native render and route evidence

Use the actual installed engine and the selected scene revision. These checks improve measurement; they do not authorize vendor patches, replace native mechanics or grant scene acceptance.

## Render pipeline and GPU budget
- Inspect current shader errors and renderer capabilities before treating missing surfaces as broken export geometry. PBR textures and shadow samplers share hardware limits; budget active shadow lights against the actual shader and device. A fixed universal shadow count is inappropriate.
- After a confirmed shader failure, reduce the offending budget in the owned QA scene and use one justified fresh-renderer recovery. Check that real materials return. Do not repeatedly alter geometry or relight to conceal missing surfaces.
- A raw renderer.render(scene,camera) may omit the installed composer pipeline. In a shared WebGL context, renderer.domElement can be an unused canvas; renderer.getContext().canvas identifies the actual context canvas. Capture the completed native frame from that canvas and visually compare it with the live window. A bounded one-frame hook must restore itself on success, failure and timeout. Blank, repeated-identical or partially rendered images fail the capture check even if the tool returns ok.
- Keep matched Blender/native camera poses, height, FOV/aspect, illumination assumptions and scene/model hashes. QA illumination is not automatically source-faithful gameplay lighting.

## Native readiness
A grid/scene change can redraw the canvas and close the 3D view asynchronously. Await the actual canvas-ready transition before starting the native renderer. Use the installed open/toggle API once and wait for stable active/ready state and complete inventory. A timeout shorter than asset loading can trigger a harmful reload race. Diagnose pending loading and real state before choosing a bounded recovery; do not repeatedly restart.

## Meaningful traversal
- Independently verify the starting feet hit the intended floor rather than a pit, shaft wall or lower surface. Record setup placement separately from locomotion.
- Installed camera-relative keyboard movement can turn cardinal inputs into diagonals. Use native stopCameraAnimation and a neutral fixed yaw for deterministic QA; temporarily preserve/restore camera panning and damping when needed. Verify each actual XY displacement matches the declared world direction and distance.
- Check expected endpoint heights and the whole elevation trace. A route that falls onto a shaft wall and later recovers is not a floor-support pass.
- Retain ordinary collision/falling settings. Native mesh rays, abstract token footprint, Foundry Region Surfaces and D&D5e Falling are distinct evidence. Do not infer a swept character collision volume from center rays.
- Include source-intended blocked controls and open/reclosed door checks, actual ascent/descent and reverse connections as applicable. Restore token pose/selection, door state, grid and the full authored scene; verify the protected source independently.
- Keep incident IDs and project results in private handoffs. Reuse generic procedure here, not historical asset acceptance.

## Architectural seams
For adjacent relief surfaces, fade displacement at shared boundary samples and genuinely join/weld the common vertices where the intended construction is continuous. Inspect the real evaluated joins from both directions. Verify actual seam distances/topology and a physically displaced negative control. Covering a gap with trim, dark lighting or camera framing does not repair the interface.
