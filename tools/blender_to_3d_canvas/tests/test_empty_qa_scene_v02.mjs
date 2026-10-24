import test from "node:test";
import assert from "node:assert/strict";
import {manageEmptyQaScene, QA_NAME, QA_TAG, SOURCE_SCENE_ID, SOURCE_SHA,
        isOwnedEmptyQaScene, exactEmpty, freshScenePayload} from "../bridge/qa-empty-scene.mjs";
function fixture() {
  const canvas={scene:null};
  const game={user:{isGM:true},scenes:null};
  const files=new Map();
  let i=0;
  class Scene {
    constructor(data) {
      this.id=data._id || "qa"+(++i);
      this.name=data.name;
      this.active=data.active??false;
      this.navigation=data.navigation??false;
      this.flags=data.flags??{};
      this.ownership=data.ownership??{default:0};
      for(const kind of ["tiles","walls","lights","regions","tokens",
                         "drawings","sounds","notes","templates"])this[kind]={size:0};
      this.createdPayload=data;
    }
    toObject(){return this.createdPayload;}
    async view(){canvas.scene=this;}
    async delete(){files.delete(this.id);}
    static async create(data) {const result=new Scene(data);files.set(result.id,result);return result;}
  }
  const source=new Scene({_id:SOURCE_SCENE_ID,name:"Accepted Area 8",
                          active:true,navigation:true,flags:{}});
  files.set(source.id,source);canvas.scene=source;
  const scenes={get:(id)=>files.get(id),get active(){return source;},
                [Symbol.iterator]:function*(){yield* files.values()}};
  game.scenes=scenes;
  let rev=SOURCE_SHA;
  const ctx={game,canvas,get sourceRevision(){return rev;},
             revisionOf:async s=>s.id==="qa1"?"fixturehash1":"protected"};
  return {game,canvas,Scene,files,source,ctx,setRev:x=>{rev=x;}};
}
test("native Scene.create produces a zero-document inactive private QA Scene",async()=>{
  const f=fixture();
  const before=await manageEmptyQaScene({action:"create"},true,f.ctx);
  assert.equal(before.would_create,true);assert.equal(f.files.size,1);
  const done=await manageEmptyQaScene({action:"create"},false,f.ctx);
  assert.equal(done.created,true);assert.equal(done.qa_scene_id,"qa1");
  const qa=f.files.get("qa1");
  assert.equal(isOwnedEmptyQaScene(qa),true);assert.equal(exactEmpty(qa),true);
  assert.equal(qa.ownership.default,0);assert.equal(qa.createdPayload.width,4000);
  assert.equal(qa.createdPayload.height,3000);
  assert.equal(f.game.scenes.active.id,SOURCE_SCENE_ID);
  assert.equal(f.canvas.scene.id,SOURCE_SCENE_ID);
});
test("GM-only view and original restoration never activate players",async()=>{
  const f=fixture();await manageEmptyQaScene({action:"create"},false,f.ctx);
  const view=await manageEmptyQaScene({action:"view",qa_scene_id:"qa1"},false,f.ctx);
  assert.equal(view.now_viewed,"qa1");assert.equal(f.game.scenes.active.id,SOURCE_SCENE_ID);
  const ret=await manageEmptyQaScene({action:"restore_view"},false,f.ctx);
  assert.equal(ret.now_viewed,SOURCE_SCENE_ID);
  assert.equal(f.files.get("qa1").active,false);
});
test("only an exact owned empty QA Scene can be deleted",async()=>{
  const f=fixture();await manageEmptyQaScene({action:"create"},false,f.ctx);
  const qa=f.files.get("qa1");qa.tiles.size=1;
  await assert.rejects(()=>manageEmptyQaScene({action:"delete"},false,f.ctx),/not empty/);
  assert.equal(f.files.size,2);qa.tiles.size=0;
  const x=await manageEmptyQaScene({action:"delete"},false,f.ctx);
  assert.equal(x.deleted,true);assert.equal(f.files.size,1);
});
test("wrong source checksum blocks provisioning",async()=>{
  const f=fixture();f.setRev("wrong");
  await assert.rejects(()=>manageEmptyQaScene({action:"create"},false,f.ctx),/checksum changed/);
  assert.equal(f.files.size,1);
});
test("non-GM is blocked",async()=>{
  const f=fixture();f.game.user.isGM=false;
  await assert.rejects(()=>manageEmptyQaScene({action:"create"},false,f.ctx),/requires GM/);
});
test("reserved name collision is rejected",async()=>{
  const f=fixture();f.files.set("bad",new f.Scene({_id:"bad",name:QA_NAME,flags:{}}));
  await assert.rejects(()=>manageEmptyQaScene({action:"create"},false,f.ctx),/Ambiguous\/unowned/);
});
test("reserved flag collision is rejected",async()=>{
  const f=fixture();
  f.files.set("bad",new f.Scene({_id:"bad",name:"User scene",flags:{"acq-foundry-bridge":{[QA_TAG]:{}}}}));
  await assert.rejects(()=>manageEmptyQaScene({action:"create"},false,f.ctx),/Ambiguous\/unowned/);
});
test("unrelated Scene view and deletion forbidden",async()=>{
  const f=fixture();await manageEmptyQaScene({action:"create"},false,f.ctx);
  await assert.rejects(()=>manageEmptyQaScene({action:"view",qa_scene_id:"foreign"},false,f.ctx),/Exact QA Scene id/);
  f.canvas.scene={id:"unrelated"};
  await assert.rejects(()=>manageEmptyQaScene({action:"delete"},false,f.ctx),/not viewing original/);
  assert.equal(f.files.size,2);
});
test("payload does not inherit campaign Tiles, walls or tokens",()=>{
  const p=freshScenePayload();
  assert.equal(p.active,false);assert.equal(p.navigation,false);
  assert.equal(p.ownership.default,0);
  assert.equal(p.flags["acq-foundry-bridge"].qaEmpty3dFixture.schema,"acq-empty-scene-v1");
  for(const t of ["tiles","walls","regions","tokens","lights","playlist","journal"])assert.equal(t in p,false);
});
