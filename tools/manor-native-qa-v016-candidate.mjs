// Candidate only; source-only v016 fixture adaptation. NOT INSTALLED.
/** Scoped first-party QA around installed native movement; no replacement controller. */
export const MANOR_ID='Zbrn5EcZh6ZTLmgm';
export const SOURCE_ID='NUEDEFAULTSCENE0';
export const SOURCE_SHA='e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f';
export async function exerciseManorNativeMovement(scene,op,dryRun,ctx){
 const {game,canvas,l3d,revisionOf,selection}=ctx;
 if(!game.user?.isGM || scene.id!==MANOR_ID || canvas.scene?.id!==MANOR_ID || scene.active || scene.ownership?.default!==0 || scene.flags?.acq?.site_id!=='TresendarManor' || scene.flags?.acq?.purpose!=='source-faithful-manor-native-review')throw Error('Explicit owned inactive GM-only Manor QA scene required');
 if(game.scenes.active?.id!==SOURCE_ID || await revisionOf(game.scenes.get(SOURCE_ID))!==SOURCE_SHA)throw Error('Protected campaign source changed');
 if(!op.expected_qa_revision || await revisionOf(scene)!==op.expected_qa_revision)throw Error('Exact QA revision required');
 if(!l3d?._active || !l3d?._ready || l3d._pauseRendering || l3d.firstPersonMode || l3d.GameCamera?.enabled || l3d.cutsceneEngine?.isPlaying)throw Error('Ready native renderer and neutral camera required');
 const tokenId=String(op.token_id??'');
 if(!selection || selection.id!==op.session_id || selection.sceneId!==MANOR_ID || selection.tokenId!==tokenId)throw Error('Bridge-owned matching QA token selection required');
 const doc=scene.tokens.get(tokenId),token=canvas.tokens.get(tokenId),native=l3d.tokens[tokenId];
 if(!doc?.name?.startsWith('QA ONLY') || !native?.head || canvas.tokens.controlled.length!==1 || canvas.tokens.controlled[0].id!==tokenId || typeof canvas.tokens.moveMany!=='function')throw Error('One recognized native QA token required');
 const steps=op.steps;
 if(!Array.isArray(steps)||steps.length<1||steps.length>24||steps.some(s=>!Number.isInteger(s.dx)||!Number.isInteger(s.dy)||Math.abs(s.dx)+Math.abs(s.dy)!==1))throw Error('One to 24 cardinal native steps required');
 const poses=()=>({x:doc.x,y:doc.y,elevation:doc.elevation,rotation:doc.rotation});
 const before=poses();
 const tileIds=scene.tiles.contents.filter(t=>t.flags?.acq?.build_id==='Tresendar.Area01.v016').map(t=>t.id);
 const area02=scene.tiles.contents.filter(t=>t.flags?.acq?.build_id==='Tresendar.Area02.v002').map(t=>t.id);
 if(scene.tiles.size!==14 || tileIds.length!==10 || area02.length!==4 ||
    ![...tileIds,...area02].every(id=>l3d.tiles[id]?.mesh))
    throw Error('Exact ten A01 v016 and four A02 v002 loaded chunks required');
 const cameraToWorld=(step)=>{
   const p=l3d.camera?.position,t=l3d.controls?.target;
   if(!p || !t || ![p.x,p.z,t.x,t.z].every(Number.isFinite))throw Error('Live 3D camera axis unavailable');
   const angle=Math.atan2(t.z-p.z,t.x-p.x);
   const fa=Math.atan2(step.dy,step.dx)+angle-Math.PI;
   return {dx:Math.round(Math.sin(fa)),dy:Math.round(-Math.cos(fa))};
 };
 const preview={scene_id:MANOR_ID,token_id:tokenId,original_pose:before,steps,tiles:tileIds,native_api:'Foundry TokenLayer.moveMany intercepted by installed 3D Canvas libWrapper',pose_setup_counted_as_movement:false,los_height_scene_units:native.losHeight,token_height_scene_units:native.tokenHeight,world_step_preview:steps.map(cameraToWorld)};
 if(dryRun)return{dry_run:true,...preview};
 if(op.action!=='exercise_and_restore')throw Error('Only exercise_and_restore is supported');
 const traces=[];let error=null,restored=false;
 try{
  for(const step of steps){
   const old=poses(),center=token.center,los=native.losHeight??doc.elevation,worldDelta=cameraToWorld(step);
   const ray={x:center.x,y:center.y,z:los};
   const next={x:center.x+worldDelta.dx*canvas.grid.size,y:center.y+worldDelta.dy*canvas.grid.size,z:los};
   const hit=l3d.interactionManager.computeSightCollision(ray,next,'move');
   await canvas.tokens.moveMany({dx:step.dx,dy:step.dy,dz:0,ids:[tokenId],includeLocked:false});
   await new Promise(r=>setTimeout(r,350));
   const after=poses();const moved=after.x!==old.x||after.y!==old.y;
   const target={x:old.x+worldDelta.dx*canvas.grid.size,y:old.y+worldDelta.dy*canvas.grid.size};
   const axis_match=moved&&Math.abs(after.x-target.x)<1e-6&&Math.abs(after.y-target.y)<1e-6;
   traces.push({input:step,native_world_delta:worldDelta,expected_target:target,before:old,after,moved,axis_match,horizontal_ray_hit:Boolean(hit),native_head:{x:native.head.x,y:native.head.y,z:native.head.z}});
   if(!axis_match)break;
  }
 }catch(e){error=String(e?.message??e)}finally{
  const changes={};for(const k of ['x','y','elevation','rotation'])if(doc[k]!==before[k])changes[k]=before[k];
  if(Object.keys(changes).length)await doc.update(changes);
  await new Promise(r=>setTimeout(r,350));restored=Object.keys(before).every(k=>Math.abs(Number(doc[k])-Number(before[k]))<1e-6);
 }
 if(!restored)throw Error('QA token rollback failed; stop');
 if(await revisionOf(game.scenes.get(SOURCE_ID))!==SOURCE_SHA)throw Error('Protected source drifted during QA; stop');
 if(await revisionOf(scene)!==op.expected_qa_revision)throw Error('QA Scene revision did not restore exactly; stop');
 return{...preview,dry_run:false,traces,error,restored,final_pose:poses(),completed_steps:traces.filter(t=>t.axis_match).length,continuous_route_pass:!error&&traces.length===steps.length&&traces.every(t=>t.axis_match),source_unchanged:true};
}
