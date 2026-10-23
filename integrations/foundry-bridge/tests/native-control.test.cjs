"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const test = require("node:test");

const bridge = fs.readFileSync(path.join(__dirname, "../module/acq-foundry-bridge/scripts/acq-foundry-bridge.js"), "utf8");
const start = bridge.indexOf("let nativeCameraSession = null;");
const end = bridge.indexOf("async function set3dCamera(", start);
assert.ok(start >= 0 && end > start, "native helpers must be present");
const helpers = bridge.slice(start, end);

function setup() {
  const calls = {camera: 0, first: 0, tile: 0, load: 0};
  let selected = [{id:"QA123"}];
  const camera = {
    position: {x:1, y:2, z:3, set(x,y,z){Object.assign(this,{x,y,z})}},
    near: 0.1
  };
  const controls = {
    target: {x:4, y:5, z:6, set(x,y,z){Object.assign(this,{x,y,z})}},
    update(){}
  };
  const runtime = {
    _active:true, _ready:true, camera, controls,
    firstPersonMode:false,
    GameCamera:{enabled:false,toggle(){this.enabled=!this.enabled;calls.camera++}},
    tokens:{QA123:{head:{x:9,y:9,z:9}}},
    cutsceneEngine:{isPlaying:false},
    toggleFirstPerson(){this.firstPersonMode=!this.firstPersonMode;calls.first++},
    setCameraToControlled(){camera.position.set(8,9,10)},
    THREE:{Box3:class {constructor(){this.min={x:-0.5,y:0,z:-1};this.max={x:0.5,y:2,z:1}}setFromObject(){return this}}},
    helpers:{async loadModel(){calls.load++;return {model:{}}}}
  };
  const canvas={grid:{size:100}, dimensions:{size:100},
    tokens:{get controlled(){return selected}}};
  const ctx={game:{Levels3DPreview:runtime},canvas};
  vm.runInNewContext("function levels3d(){return game.Levels3DPreview}; function vectorToObject(v){return v&&{x:v.x,y:v.y,z:v.z}};function setVector(target,v){target.set(v.x,v.y,v.z)};\n"+helpers+"\n globalThis.native={setNativeCameraMode,previewNativeAssetTile};",ctx);
  return {native:ctx.native,runtime,canvas,calls,setSelected:(x)=>{selected=x}};
}
test("native first-person dry run is non-mutating and restoration requires exact session", async () => {
  const v=setup();const scene={id:"QA_SCENE"};
  const preview=await v.native.setNativeCameraMode(scene,{mode:"first_person",token_id:"QA123"},true);
  assert.equal(preview.would_enter,true);
  assert.equal(v.calls.first,0);
  const enter=await v.native.setNativeCameraMode(scene,{mode:"first_person",token_id:"QA123"},false);
  assert.equal(enter.after.first_person,true);
  await assert.rejects(()=>v.native.setNativeCameraMode(scene,{mode:"restore",session_id:"wrong"},false));
  assert.equal(v.runtime.firstPersonMode,true);
  const exit=await v.native.setNativeCameraMode(scene,{mode:"restore",session_id:enter.session_id},false);
  assert.equal(exit.restored,true);
  assert.equal(v.runtime.firstPersonMode,false);
  assert.equal(v.runtime.camera.position.x,1);
  assert.equal(v.runtime.controls.target.x,4);
});
test("missing controlled token and non-ready runtime prevent first person", async () => {
  const v=setup();
  v.setSelected([]);
  await assert.rejects(()=>v.native.setNativeCameraMode({id:"QA_SCENE"},{mode:"first_person",token_id:"QA123"},true),/selected/);
  v.runtime._ready=false;
  await assert.rejects(()=>v.native.setNativeCameraMode({id:"QA_SCENE"},{mode:"game_camera"},true),/ready/);
});
test("native GLB model bbox yields source-derived centered Tile without Scene writes", async()=>{
  const v=setup();
  const r=await v.native.previewNativeAssetTile({id:"QA_SCENE"},{foundry_path:"modules/canvas3dcompendium/assets/Tiles/Medieval%20Dungeon/Decorative_Wall.glb",x:1200,y:1200,scale:1});
  assert.equal(r.did_create_tile,false);
  assert.equal(r.candidate.width,100);assert.equal(r.candidate.height,200);
  assert.equal(r.candidate.x,1150);assert.equal(r.candidate.y,1100);
  assert.equal(r.candidate.flags["levels-3d-preview"].depth,200);
  assert.equal(v.calls.tile,0);assert.equal(v.calls.load,1);
});
test("native preview rejects unsafe paths, bogus colors, and numeric sizes", async()=>{
  const v=setup();
  const p="modules/canvas3dcompendium/assets/A.glb";
  for(const vpath of ["https://remote.invalid/asset.glb","modules/canvas3dcompendium/assets/../unsafe.glb","modules/canvas3dcompendium/assets/%2e%2e/unsafe.glb","modules/canvas3dcompendium/assets/model.png"]) {
    await assert.rejects(()=>v.native.previewNativeAssetTile({id:"QA_SCENE"},{foundry_path:vpath,x:0,y:0}),/allowlisted/);
  }
  await assert.rejects(()=>v.native.previewNativeAssetTile({id:"QA_SCENE"},{foundry_path:p,x:0,y:0,color:"bad-color"}),/hex/);
  await assert.rejects(()=>v.native.previewNativeAssetTile({id:"QA_SCENE"},{foundry_path:p,x:0,y:0,scale:100}),/bounded/);
});
