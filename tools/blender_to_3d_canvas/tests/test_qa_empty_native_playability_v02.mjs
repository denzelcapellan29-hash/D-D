import test from "node:test";
import assert from "node:assert/strict";
import {inspectEmptyQaNativePlayability,PROBES,EXPECTED,classifyHits}
  from "../bridge/qa-empty-native-playability.mjs";
import {freshScenePayload,SOURCE_SCENE_ID,SOURCE_SHA,QA_NAME} from "../bridge/qa-empty-scene.mjs";

function fixture(){
  const payload=freshScenePayload();
  const scene={id:"qa-isolated",name:QA_NAME,active:false,navigation:false,
               flags:payload.flags};
  const tiles=Array.from(EXPECTED).map(name=>({
    id:"qa-"+name,
    flags:{acq:{
      semantic_id:"qa:multichunk:qa-twolevel-library-v02:"+name,
      classification:"QA_ONLY_MULTICHUNK_V02",
      build_id:"qa-twolevel-library-v02",
      provenance:{source:"X:/read-only.blend"}
    }}
  }));
  scene.tiles={contents:tiles,size:tiles.length};
  const counts={move:0,sight:0,camera:0};
  const board={name:"native board"};
  const manager={
    _sightCollisions:{move:[{}],sight:[{}],camera:[{}]},
    computeSightCollisionFrom3DPositions(from,to,type){
      counts[type]++;
      return [{distance:.075,object:{name:type+" library mesh",
               parent:{name:"Source 3D Tile"}},
               point:{x:from.x,y:from.y-.075,z:from.z}}];
    }
  };
  const ctx={
    game:{user:{isGM:true},scenes:{active:{id:SOURCE_SCENE_ID}}},
    canvas:{scene:{id:scene.id}},
    sourceRevision:SOURCE_SHA,
    l3d:{_active:true,_ready:true,interactionManager:manager,board,
         GameCamera:{enabled:false},cutsceneEngine:{isPlaying:false}},
    THREE:{Vector3:class {constructor(x,y,z){this.x=x;this.y=y;this.z=z;}}}
  };
  return {ctx,scene,tiles,counts};
}
test("fixed source-backed stair/door ray table returns native hit categories",async()=>{
  const f=fixture();
  const r=await inspectEmptyQaNativePlayability(f.scene,f.ctx);
  assert.equal(r.read_only,true);
  assert.equal(r.tiles,7);
  assert.equal(r.native_probe_count,PROBES.length);
  for(const type of ["move","sight","camera"]){
    assert.equal(f.counts[type],PROBES.length);
  }
  assert.equal(r.native_ray_probes.find(p=>p.name==="door_closed_horiz").move_hits.length,1);
  assert.equal(r.physical_step_acceptance,false);
  assert.equal(r.door_hinge_acceptance,false);
});
test("non-GM denied",async()=>{
  const f=fixture();f.ctx.game.user.isGM=false;
  await assert.rejects(()=>inspectEmptyQaNativePlayability(f.scene,f.ctx),/guard failed/);
});
test("wrong original source hash denied",async()=>{
  const f=fixture();f.ctx.sourceRevision="STALE";
  await assert.rejects(()=>inspectEmptyQaNativePlayability(f.scene,f.ctx),/guard failed/);
});
test("wrong viewed scene denied",async()=>{
  const f=fixture();f.ctx.canvas.scene={id:"unrelated"};
  await assert.rejects(()=>inspectEmptyQaNativePlayability(f.scene,f.ctx),/guard failed/);
});
test("active for players denied",async()=>{
  const f=fixture();f.scene.active=true;
  await assert.rejects(()=>inspectEmptyQaNativePlayability(f.scene,f.ctx),/guard failed/);
});
test("missing Tile denied before any ray calls",async()=>{
  const f=fixture();f.scene.tiles.contents.pop();f.scene.tiles.size--;
  await assert.rejects(()=>inspectEmptyQaNativePlayability(f.scene,f.ctx),/exactly seven/);
  assert.equal(f.counts.move,0);
});
test("foreign Tile replaces one importer part and is rejected",async()=>{
  const f=fixture();f.tiles[0].flags.acq.classification="OTHER_BUILD";
  await assert.rejects(()=>inspectEmptyQaNativePlayability(f.scene,f.ctx),/ownership/);
});
test("native collision manager unavailable denied",async()=>{
  const f=fixture();f.ctx.l3d._ready=false;
  await assert.rejects(()=>inspectEmptyQaNativePlayability(f.scene,f.ctx),/not ready/);
});
test("GameCamera/cutscene must be neutral for test",async()=>{
  const f=fixture();f.ctx.l3d.GameCamera.enabled=true;
  await assert.rejects(()=>inspectEmptyQaNativePlayability(f.scene,f.ctx),/Neutral/);
});
test("malformed native ray return rejected",()=>{
  assert.throws(()=>classifyHits(null,{}),/non-array/);
});
