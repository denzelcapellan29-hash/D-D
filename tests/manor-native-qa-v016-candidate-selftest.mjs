import assert from 'node:assert/strict';
import {exerciseManorNativeMovement as run, MANOR_ID, SOURCE_ID, SOURCE_SHA} from './acq_manor_native_v016_candidate.mjs';
const records=[];
function makeHarness({wrongBuild=false,sideways=false,blocked=false,drift=false,sourceDrift=false}={}){
 const tokenId='WFTbaMsg6sFNPblG';
 const doc={name:'QA ONLY — Area 8 Monk Viewpoint',x:1650,y:1550,elevation:.06,rotation:0,async update(c){Object.assign(this,c)}};
 const token={id:tokenId,get center(){return {x:doc.x+50,y:doc.y+50}}};
 const chunks=Array.from({length:14},(_,i)=>({id:'tile'+i,flags:{acq:{build_id:i<10?'Tresendar.Area01.v016':'Tresendar.Area02.v002'}}}));
 if(wrongBuild)chunks[0].flags.acq.build_id='Tresendar.Area01.v015';
 const scene={id:MANOR_ID,active:false,ownership:{default:0},flags:{acq:{site_id:'TresendarManor',purpose:'source-faithful-manor-native-review'}},tiles:{size:14,contents:chunks},tokens:{get:()=>doc}};
 const l3d={_active:true,_ready:true,_pauseRendering:false,firstPersonMode:false,GameCamera:{enabled:false},cutsceneEngine:{isPlaying:false},tokens:{[tokenId]:{head:{x:1,y:2,z:3},losHeight:4.02,tokenHeight:4.45}},tiles:Object.fromEntries(chunks.map(x=>[x.id,{mesh:{}}])),camera:{position:{x:2,z:1}},controls:{target:{x:-1,z:1}},interactionManager:{computeSightCollision(){return null}}};
 const canvas={scene:{id:MANOR_ID},grid:{size:100},tokens:{controlled:[token],get:()=>token,async moveMany({dx,dy}){
   if(blocked)return;
   const a=Math.atan2(l3d.controls.target.z-l3d.camera.position.z,l3d.controls.target.x-l3d.camera.position.x);
   const fa=Math.atan2(dy,dx)+a-Math.PI;
   const wx=sideways?dx:Math.round(Math.sin(fa)),wy=sideways?dy:Math.round(-Math.cos(fa));
   doc.x+=wx*100;doc.y+=wy*100;
 }}};
 const source={id:SOURCE_ID};
 const game={user:{isGM:true},scenes:{active:source,get(id){return id===SOURCE_ID?source:scene}}};
 let qaReads=0;const revisionOf=async d=>{if(d.id===SOURCE_ID)return sourceDrift?'source-drift':SOURCE_SHA;qaReads++;return drift&&qaReads>1?'qa-drift':'qa-sha';};
 const ctx={game,canvas,l3d,selection:{id:'sess1',sceneId:MANOR_ID,tokenId},revisionOf};
 const op={token_id:tokenId,session_id:'sess1',expected_qa_revision:'qa-sha',steps:[{dx:1,dy:0}],action:'exercise_and_restore'};
 return {scene,op,ctx,doc};
}
function record(k){records.push(k)}
{const h=makeHarness();const result=await run(h.scene,h.op,true,h.ctx);assert.equal(result.dry_run,true);assert.deepEqual(result.world_step_preview,[{dx:0,dy:-1}]);assert.equal(result.los_height_scene_units,4.02);record('PREVIEW_CAMERA_REMAP_AND_LIVE_HEIGHT')}
{const h=makeHarness();const r=await run(h.scene,h.op,false,h.ctx);assert.equal(r.continuous_route_pass,true);assert.equal(r.completed_steps,1);assert.equal(r.traces[0].axis_match,true);assert.deepEqual([h.doc.x,h.doc.y,h.doc.elevation,h.doc.rotation],[1650,1550,.06,0]);record('NATIVE_INTERCEPT_MOCK_AXIS_AND_ROLLBACK')}
{const h=makeHarness({wrongBuild:true});await assert.rejects(()=>run(h.scene,h.op,true,h.ctx),/Exact ten A01 v016/);record('V015_PROVENANCE_REJECT')}
{const h=makeHarness({sideways:true});const r=await run(h.scene,h.op,false,h.ctx);assert.equal(r.continuous_route_pass,false);assert.equal(r.completed_steps,0);assert.equal(r.traces[0].axis_match,false);assert.equal(r.restored,true);record('WRONG_CAMERA_DIRECTION_REJECT_AND_ROLLBACK')}
{const h=makeHarness({blocked:true});const r=await run(h.scene,h.op,false,h.ctx);assert.equal(r.continuous_route_pass,false);assert.equal(r.completed_steps,0);assert.equal(r.restored,true);record('BLOCKED_NATIVE_STEP_REJECT')}
{const h=makeHarness({drift:true});await assert.rejects(()=>run(h.scene,h.op,false,h.ctx),/QA Scene revision did not restore/);assert.deepEqual([h.doc.x,h.doc.y],[1650,1550]);record('POST_ROLLBACK_QA_SHA_DRIFT_REJECT')}
{const h=makeHarness({sourceDrift:true});await assert.rejects(()=>run(h.scene,h.op,true,h.ctx),/Protected campaign source changed/);record('SOURCE_SHA_DRIFT_REJECT')}
{const h=makeHarness();h.op.expected_qa_revision='wrong';await assert.rejects(()=>run(h.scene,h.op,true,h.ctx),/Exact QA revision required/);record('EXPECTED_QA_SHA_REJECT')}
process.stdout.write(JSON.stringify({passed:records.length,tests:records})+'\n');
