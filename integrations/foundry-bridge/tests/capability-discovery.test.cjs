// Read-only contract tests. The real source is evaluated with inert Foundry Hooks.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const bridge = fs.readFileSync(
  path.join(__dirname, "../module/acq-foundry-bridge/scripts/acq-foundry-bridge.js"),
  "utf8"
);
// The live custom first-person stabilizer is preserved as an ESM import.
// Node vm.Script parses classic scripts; test the module body without executing that import.
const protectedImport = 'import "./fps-camera-anchor.mjs";';
assert.ok(bridge.startsWith(protectedImport), "protected first-person module import must remain");
const bridgeBody = bridge.slice(protectedImport.length).replace(/^\\r?\\n/, "");

function fixture(active) {
  let writes = 0;
  const settingValues = {
    enableGameCamera: true,
    gameCameraDefaultGm: false,
    gameCameraAutoLock: true,
    gameCameraMinAngle: 10,
    gameCameraMaxAngle: 80,
    gameCameraMinAzimuth: -180,
    gameCameraMaxAzimuth: 180,
    gameCameraMaxZoom: 4,
    gameCameraClipping: true
  };
  const definitions = new Map(
    Object.keys(settingValues).map(key => ["levels-3d-preview." + key, {scope: "client"}])
  );
  const gc = {
    enabled: true, lock: true, topDown: false,
    toggle() { writes++; }, toggleTopDown() { writes++; }, getY() {}
  };
  const l3d = active ? {
    _active: true, _ready: true, _envReady: true, _lightsOk: true,
    _finalizingLoad: false, loadingTiles: new Set(),
    renderer: {}, scene: {}, camera: {position: {x: 1, y: 2, z: 3}},
    controls: {target: {x: 4, y: 5, z: 6}},
    tokens: {monk: {}}, tiles: {wall: {}},
    GameCamera: gc,
    toggle() { writes++; },
    reload() { writes++; },
    toggleFirstPerson() { writes++; },
    setCameraToControlled() { writes++; },
    cutsceneEngine: {}, interactionManager: {},
    CONFIG: {UI: {windows: {AssetBrowser: function AssetBrowser() {}}}},
    firstPersonMode: false
  } : null;
  const scene = {
    id: "test-scene",
    tiles: [
      {flags: {"levels-3d-preview": {model3d: "safe.glb", cameraCollision: true}}},
      {flags: {"levels-3d-preview": {roughness: 0.3, privateToken: "secret-NEVER-RETURN"}}}
    ],
    flags: {"levels-3d-preview": {enablePlayers: true, superSecret: "secret-NEVER-RETURN"}},
    update() { writes++; }
  };
  const modules = new Map([["levels-3d-preview", {active: active, version: "9.0.36"}]]);
  const game = {
    version: "14.368", world: {id: "test-world"}, modules,
    settings: {settings: definitions, get(_scope, key) {
      if (key === "apiKey") throw new Error("no secrets");
      return settingValues[key];
    }}
  };
  if (active) {
    game.Levels3DPreview = l3d;
    game.canvas3D = l3d;
  }
  const canvas = {scene, tokens: {controlled: [{id: "monk"}]}};
  const context = {game, canvas, Hooks: {once() {}, on() {}}, console};
  context.globalThis = context;
  vm.runInNewContext(bridgeBody + "\n globalThis.__capProbe = inspect3dCapabilities;", context);
  return {report: context.__capProbe(scene), getWrites: () => writes};
}

test("active 3D Canvas: detailed runtime methods and selected token", () => {
  const f = fixture(true);
  const r = f.report;
  assert.equal(r.world_id, "test-world");
  assert.equal(r.camera.game_camera_enabled, true);
  assert.equal(r.camera.game_camera_lock, true);
  assert.equal(r.available_apis.first_person_toggle, true);
  assert.equal(r.available_apis.game_camera_top_down_toggle, true);
  assert.equal(r.available_apis.asset_browser_class, true);
  assert.equal(r.camera.selected_tokens[0].rendered_3d, true);
  assert.equal(r.camera_settings.find(s => s.key === "gameCameraMinAngle").value, 10);
  assert.equal(f.getWrites(), 0);
  assert.equal(JSON.stringify(r).includes("secret-NEVER-RETURN"), false);
});

test("inactive 3D Canvas: discovery reports missing runtime without mutation", () => {
  const f = fixture(false);
  const r = f.report;
  assert.equal(r.available_apis.first_person_toggle, false);
  assert.equal(r.camera.game_camera_present, false);
  assert.equal(r.modules[0].installed, true);
  assert.equal(r.modules[0].active, false);
  assert.equal(r.runtime.active, false);
  assert.equal(f.getWrites(), 0);
});

test("all surfaced camera setting names are on a fixed allowlist", () => {
  const r = fixture(true).report;
  assert.equal(r.camera_settings.length, 12);
  assert.equal(r.camera_settings.some(s => s.key === "apiKey"), false);
  assert.ok(r.config_inventory.tile_flag_keys.includes("cameraCollision"));
});
