// Acquisitions Incorporated verified first-person camera tracking for 3D Canvas 9.0.35.
// Preserve token heading as its 3D head moves across genuine GLB floor tiles.
// Runtime-only camera/controls translation: no meshes, token elevation, or map edits.
function install(l3d) {
  const controls = l3d?.controls;
  if (!controls || controls.__acqAnchorInstalled || !l3d.camera) return;
  const original = controls.update.bind(controls);
  controls.update = function(...args) {
    if (l3d.firstPersonMode && l3d._active && l3d.tokens) {
      const token = globalThis.canvas?.tokens?.controlled?.[0];
      const head = token && l3d.tokens[token.id]?.headFast;
      if (head && Number.isFinite(head.x) && Number.isFinite(head.y) && Number.isFinite(head.z)) {
        const eye = l3d.camera.position;
        const dx = head.x - eye.x, dy = head.y - eye.y, dz = head.z - eye.z;
        // Keep target and eye translated together, preserving user's orbit/look bearing.
        controls.target.x += dx; controls.target.y += dy; controls.target.z += dz;
        eye.set(head.x, head.y, head.z);
      }
    }
    return original(...args);
  };
  controls.__acqAnchorInstalled = true;
}
if (globalThis.Hooks) {
  Hooks.on("3DCanvasPostInit", install);
  Hooks.on("3DCanvasSceneReady", install);
}
if (globalThis.game?.Levels3DPreview?.controls) install(game.Levels3DPreview);
