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
  const found=Array.from(scene?.tiles?.contents??scene?.tiles??[])
    .filter(t=>String(t?.flags?.acq?.semantic_id??"").startsWith(PREFIX));
  if(found.length!==EXPECTED.size || Number(scene?.tiles?.size)!==EXPECTED.size)
    throw new Error("Expected exactly seven exclusive QA-imported Tiles.");
  const names=found.map(t=>String(t.flags.acq.semantic_id).slice(PREFIX.length));
  if(new Set(names).size!==EXPECTED.size || names.some(n=>!EXPECTED.has(n)))
    throw new Error("QA imported chunk inventory mismatch.");
  if(found.some(t=>t.flags.acq.classification!=="QA_ONLY_MULTICHUNK_V02"||
                   t.flags.acq.build_id!=="qa-twolevel-library-v02"))
    throw new Error("Unexpected Tile ownership or build provenance.");
  return found;
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
export async function inspectEmptyQaNativePlayability(scene,context){
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
  const run=(probe,type)=>{
    const f=new THREE.Vector3(...probe.from);
    const t=new THREE.Vector3(...probe.to);
    const raw=manager.computeSightCollisionFrom3DPositions(
      f,t,type,false,true,false,true);
    return classifyHits(raw,l3d.board);
  };
  const rows=PROBES.map(probe=>({
    ...probe,
    move_hits:run(probe,"move"),
    sight_hits:run(probe,"sight"),
    camera_hits:run(probe,"camera")
  }));
  const groups=Object.fromEntries(["move","sight","camera"].map(
    type=>[type,manager?._sightCollisions?.[type]?.length??null]));
  return {read_only:true,qa_scene_id:scene.id,source_scene_id:SOURCE_SCENE_ID,
    source_revision:sourceRevision,tiles:tiles.length,
    native_collision_groups:groups,native_probe_count:rows.length,
    native_ray_probes:rows,
    physical_step_acceptance:false,door_hinge_acceptance:false,
    note:"Native 3D Canvas BVH ray evidence only; does not execute TokenLayer.moveMany or D&D5e Falling."};
}
