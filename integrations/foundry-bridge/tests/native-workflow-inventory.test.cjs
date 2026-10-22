"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");
const code = fs.readFileSync(path.join(__dirname, "../module/acq-foundry-bridge/scripts/acq-foundry-bridge.js"), "utf8");
const start = code.indexOf("function inspect3dNativeWorkflows(scene) {");
const end = code.indexOf("async function set3dCamera(", start);
assert.ok(start >= 0 && end > start, "source must contain explicit native discovery helper");
const nativeCode = code.slice(start, end);
function fixture() {
  const buttons = [
    {id:"props", callback() {throw new Error("UI action must not be invoked by inspection");}},
    {id:"roombuilder",disabled:true},
    {id:"effects",disabled:false,callback() {throw new Error("Premium action must not be invoked");}}
  ];
  const runtime={
    _active:true, _ready:true,renderer:{},
    GameCamera:{enabled:false,toggle() {throw new Error("Camera must not move");}},
    toggleFirstPerson() {throw new Error("First person must not switch");},
    setCameraToControlled() {throw new Error("Token camera must not move");},
    BuildPanel:{BUILD_PANEL_BUTTONS:buttons},tokens:{monk:{}},
    CONFIG:{UI:{windows:{}}}
  };
  const canvas={tokens:{controlled:[{id:"monk"}]}};
  const game={Levels3DPreview:runtime};
  const context={game,canvas,Boolean,Array};
  vm.runInNewContext("function levels3d(){return game.Levels3DPreview};\n"+nativeCode+"\n globalThis.testProbe = inspect3dNativeWorkflows;",context);
  return {runtime,probe:context.testProbe};
}
test("closed browser is not an absent native editor", () => {
  const {probe}=fixture();
  const r=probe({id:"test"});
  assert.equal(r.native_browser.instance_open,false);
  assert.equal(r.native_browser.registered_props_action,true);
  assert.equal(r.native_buttons.find(x=>x.id==="props").callable,true);
  assert.equal(r.native_buttons.find(x=>x.id==="roombuilder").disabled,true);
  assert.equal(r.camera.controlled_3d_token_count,1);
  assert.equal(r.safe_inventory_only,true);
});
test("open browser instance supports source-derived tile data",()=>{
  const {runtime,probe}=fixture();
  runtime.CONFIG.UI.windows.AssetBrowser={buildTileData(){}};
  const r=probe({id:"test"});
  assert.equal(r.native_browser.instance_open,true);
  assert.equal(r.native_browser.can_build_tile_data,true);
});
