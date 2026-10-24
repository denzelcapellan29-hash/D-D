/** Read-only native 3D Canvas collision/BVH inspection on one explicitly
 * owned empty-QA Scene populated ONLY with the seven authentic library chunks.
 * This file makes no document, setting, movement or camera changes.
 * Not a substitute for actual token stair traversal / D&D5e Falling QA.
 */
import {isOwnedEmptyQaScene,SOURCE_SCENE_ID,SOURCE_SHA} from "./qa-empty-scene.mjs";

export const EXPECTED=new Set([
  "lower_back_wall","lower_floor","lower_side_wall","stair_connector",
  "upper_doorway","upper_floor","upper_interactive_door"
]);
const PREFIX="qa:multichunk:qa-twolevel-library-v02:";
const LEAF_PREFIX="qa:multichunk:qa-twolevel-doorleaf-v03:";
const LEAF_SHA=Object.freeze({
  lower_back_wall:"a7d7997840e3768a0a34daa7f533b6d3e542627d5bdc90cfef604122390f4749",
  lower_floor:"d2a5278ba360a3684f91151a3d5173543384be38bcf38c67df08ae93562847d1",
  lower_side_wall:"b05cdbb4f14f1ed27c7d499f7bf53f19527d0dfa644cd2ad274ca6717f53b679",
  stair_connector:"1c73c685fb18edb4fce77e437e02be22570f33af7248d087eb70eb3cfd26a149",
  upper_doorway:"87a62bb3da28facff1f07e6c6aa12ec4b30f027ea6322941638f1acb33615b43",
  upper_floor:"381d925eaa57e899e64a11897552c63e00245d09ce34b867d322bd95e0c51c95",
  upper_interactive_door:"2d58f8c6cf26ba72c399f01e40d624c55282e7741a9099c5bd3598661607f258"
});

// Native Three.js coordinate frame; 3D Canvas world units: scene pixels / 1000.
export const PROBES=[
  {name:"lower_floor_center",kind:"support",from:[1.92,0.22,1.41],to:[1.92,-0.08,1.41]},
  {name:"stair_lower",kind:"support",from:[1.92,0.35,1.22],to:[1.92,-0.10,1.22]},
  {name:"stair_middle",kind:"support",from:[1.92,0.46,1.11],to:[1.92,-0.04,1.11]},
  {name:"stair_upper",kind:"support",from:[1.92,0.54,0.99],to:[1.92,0.08,0.99]},
  {name:"upper_floor_center",kind:"support",from:[1.92,0.52,0.81],to:[1.92,0.14,0.81]},
  {name:"door_closed_horiz",kind:"door",from:[1.92,0.41,0.82],to:[1.92,0.41,0.53]},
  {name:"side_wall_cross",kind:"wall",from:[1.89,0.15,1.41],to:[2.16,0.15,1.41]}
];

function exactTaggedInventory(scene){
  const all=Array.from(scene?.tiles?.contents??scene?.tiles??[]);
  if(all.length!==EXPECTED.size||Number(scene?.tiles?.size)!==EXPECTED.size)
    throw new Error("Expected exactly seven exclusive QA-imported Tiles.");
  for(const spec of [
    {prefix:PREFIX,build:"qa-twolevel-library-v02",sha:null},
    {prefix:LEAF_PREFIX,build:"qa-twolevel-doorleaf-v03",sha:LEAF_SHA}
  ]){
    const names=all.map(t=>{
      const acq=t?.flags?.acq??{};
      const sid=String(acq.semantic_id??"");
      if(!sid.startsWith(spec.prefix))return null;
      const name=sid.slice(spec.prefix.length);
      if(acq.classification!=="QA_ONLY_MULTICHUNK_V02"||
         acq.build_id!==spec.build ||
         (spec.sha&&acq.provenance?.asset_sha256!==spec.sha[name]))return null;
      return name;
    });
    if(names.every(n=>n!==null&&EXPECTED.has(n))&&
       new Set(names).size===EXPECTED.size)return all;
  }
  throw new Error("QA imported chunk inventory or exact source provenance mismatch.");
}
export function classifyHits(hitList,board){
  if(!Array.isArray(hitList))throw new Error("Native collision helper returned non-array.");
  return hitList.slice(0,12).map(h=>({
    distance:Number(h?.distance),
    mesh:String(h?.object?.name??"").slice(0,130),
    parent:String(h?.object?.parent?.name??"").slice(0,130),
    board:h?.object===board,
    point:h?.point ? {x:Number(h.point.x),y:Number(h.point.y),z:Number(h.point.z)} : null
  }));
}
export async function inspectEmptyQaNativePlayability(scene,context,options={}){
  const {game,canvas,sourceRevision,l3d,THREE}=context;
  if(!game?.user?.isGM||!isOwnedEmptyQaScene(scene)||
     scene.id!==canvas?.scene?.id||scene.active||
     game.scenes.active?.id!==SOURCE_SCENE_ID||sourceRevision!==SOURCE_SHA)
    throw new Error("GM / owned inactive QA / source revision guard failed.");
  const tiles=exactTaggedInventory(scene);
  const manager=l3d?.interactionManager;
  if(!l3d?._active||!l3d?._ready||
     typeof manager?.computeSightCollisionFrom3DPositions!=="function"||
     typeof THREE?.Vector3!=="function")
    throw new Error("Native 3D Canvas collision raycast API is not ready.");
  if(l3d?.GameCamera?.enabled||l3d?.cutsceneEngine?.isPlaying)
    throw new Error("Neutral native QA camera required; no GameCamera/cutscene.");
  const mode=String(options.mode??"inventory");
  if(mode!=="inventory" && mode!=="ray")
    throw new Error("Explicit inventory or one-ray diagnostic required.");
  const groups=Object.fromEntries(["move","sight","camera"].map(
    type=>[type,manager?._sightCollisions?.[type]?.length??null]));
  // A one-request/one-ray limit prevents 21 potentially expensive native
  // raycasts from blocking the single-threaded Foundry client and bridge.
  const results=[];
  if(mode==="ray"){
    const probe=PROBES.find(x=>x.name===String(options.probe_name??""));
    const type=String(options.collision_type??"");
    if(!probe||!["move","sight","camera"].includes(type))
      throw new Error("Known probe name and exactly one collision type required.");
    const from=new THREE.Vector3(...probe.from);
    const to=new THREE.Vector3(...probe.to);
    const raw=manager.computeSightCollisionFrom3DPositions(
      from,to,type,false,true,false,true);
    results.push({...probe,collision_type:type,hits:classifyHits(raw,l3d.board)});
  }
  return {read_only:true,qa_scene_id:scene.id,source_scene_id:SOURCE_SCENE_ID,
    source_revision:sourceRevision,tiles:tiles.length,
    native_collision_groups:groups,mode,native_probe_count:results.length,
    native_ray_probes:results,
    physical_step_acceptance:false,door_hinge_acceptance:false,
    note:"One native BVH ray at a time; inventory mode runs ZERO collision rays. Actual token traversal remains a separate QA gate."};
}
