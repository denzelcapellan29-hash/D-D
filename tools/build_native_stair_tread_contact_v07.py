"""QA-only v07 staircase walkable-tread contact prototype. No source or .blend edits.
Native certification requires separate guarded import, real token movement, and rollback.
Keeps original GLB as immutable visible art; substitutes a separate collision-ON tread
surface only on a disposable QA scene. All eight step supports remain physically tested.
"""
import copy, hashlib, json, os, pathlib, struct
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
SRC=pathlib.Path("C:/Users/denze/AppData/Local/FoundryVTT/Data/modules/acq-foundry-bridge/assets/blender_bundles/qa-native-door-v05-20261024/qa-native-door-v05-003-stair_connector.glb")
SHA="734f0c1bff44ce81fcad156c45477d36cdbd09f78e4117b07ec83f46071df81e"
DEST=SRC.parents[1]/"qa-stair-contact-v07-20261025"
GLB=DEST/"qa-stair-v07-tread-contact-only.glb"
MAN=DEST/"qa-stair-v07-offline-gate.json"
DRIVE=pathlib.Path("G:/My Drive/D&D/Foundry Bridge/captures/qa-stair-contact-v07-20261025")
raw=SRC.read_bytes()
if hashlib.sha256(raw).hexdigest()!=SHA: raise ValueError("pinned original GLB changed")
if raw[:4]!=b"glTF" or struct.unpack_from("<I",raw,4)[0]!=2:raise ValueError("not glTF 2")
jn,jtype=struct.unpack_from("<I4s",raw,12)
if jtype!=b"JSON":raise ValueError("invalid JSON chunk")
j=json.loads(raw[20:20+jn]);bo=20+jn;bl,bt=struct.unpack_from("<I4s",raw,bo)
if bt!=b"BIN\x00":raise ValueError("missing BIN")
b=raw[bo+8:bo+8+bl]
if len(j.get("meshes",[]))!=1 or len(j["meshes"][0]["primitives"])!=1:raise ValueError("source layout changed")
prim=j["meshes"][0]["primitives"][0]
node=j["nodes"][0]
if node.get("name")!="stairs" or node.get("translation")!=[0,0,-2] or [round(x,4) for x in node.get("scale",[])]!=[.8,1,1]:
 raise ValueError("source transform changed")
def accessor(i):
 a=j["accessors"][i];v=j["bufferViews"][a["bufferView"]]
 fmt={5121:"B",5123:"H",5125:"I",5126:"f"}[a["componentType"]]
 n={"SCALAR":1,"VEC2":2,"VEC3":3}[a["type"]];f="<"+fmt*n
 off=v.get("byteOffset",0)+a.get("byteOffset",0);stride=v.get("byteStride",struct.calcsize(f))
 return [struct.unpack_from(f,b,off+k*stride) for k in range(a["count"])]
oldpts=[Vector((x*.8,y,z-2)) for x,y,z in accessor(prim["attributes"]["POSITION"])]
oldidx=[x[0] for x in accessor(prim["indices"])]
oldfaces=[tuple(oldidx[i:i+3]) for i in range(0,len(oldidx),3)]
# Individual face collision masks are not supported on a one-Tile mesh in native
# 3D Canvas. A physically present, collision-enabled top-only Tile avoids vertical
# front risers intercepting a previous-height movement ray. No wedge or teleport.
v=[];inds=[];n=[];uv=[]
for step in range(8):
 y=4.0-.5*step-.11
 z0=.5*step-(.001 if step else 0.)
 z1=.5*(step+1)-(.0001 if step!=7 else 0.)
 a=len(v)
 v.extend([(-1.75,y,z0),(1.75,y,z0),(1.75,y,z1),(-1.75,y,z1)])
 n.extend([(0.,1.,0.)]*4);uv.extend([(.17,.105+.01*step)]*4)
 inds.extend((a,a+2,a+1,a,a+3,a+2))
new=copy.deepcopy(j);newbin=bytearray(b)
def add(buf,comp,typ,count,mi=None,ma=None,target=None):
 while len(newbin)%4:newbin.append(0)
 off=len(newbin);newbin.extend(buf)
 vw={"buffer":0,"byteOffset":off,"byteLength":len(buf)}
 if target:vw["target"]=target
 nv=len(new["bufferViews"]);new["bufferViews"].append(vw)
 acc={"bufferView":nv,"componentType":comp,"count":count,"type":typ}
 if mi is not None:acc["min"]=list(mi)
 if ma is not None:acc["max"]=list(ma)
 ai=len(new["accessors"]);new["accessors"].append(acc)
 return ai
def pack(rows,fmt):return b"".join(struct.pack(fmt,*x) for x in rows)
p=add(pack(v,"<fff"),5126,"VEC3",len(v),
      [min(x[i] for x in v) for i in range(3)],
      [max(x[i] for x in v) for i in range(3)],34962)
nn=add(pack(n,"<fff"),5126,"VEC3",len(n),[0.,1.,0.],[0.,1.,0.],34962)
tex=add(pack(uv,"<ff"),5126,"VEC2",len(uv),[.17,.105],[.17,.175],34962)
ind=add(b"".join(struct.pack("<H",x) for x in inds),5123,"SCALAR",len(inds),[0],[max(inds)],34963)
new["meshes"]=[{"name":"QA_v07_eight_walkable_treads",
 "primitives":[{"attributes":{"POSITION":p,"NORMAL":nn,"TEXCOORD_0":tex},
                "indices":ind,"material":prim["material"],"mode":4}]}]
nnod=copy.deepcopy(node);nnod["name"]="qa_v07_collision_on_tread_support"
nnod["extras"]={"acq_role":"stair","qa_only":True,
"source_sha256":SHA,"movement_collision_required":True,"contact_geometry":"8 source-height treads"}
new["nodes"]=[nnod];new["scenes"]=[{"nodes":[0]}];new["scene"]=0
new["buffers"][0]["byteLength"]=len(newbin)
while len(newbin)%4:newbin.append(0)
js=json.dumps(new,sort_keys=True,separators=(",",":")).encode()
js+=b" "*((-len(js))%4)
binary=(struct.pack("<4sII",b"glTF",2,12+8+len(js)+8+len(newbin))+
        struct.pack("<I4s",len(js),b"JSON")+js+
        struct.pack("<I4s",len(newbin),b"BIN\x00")+bytes(newbin))
new_sha=hashlib.sha256(binary).hexdigest()
B0=BVHTree.FromPolygons(oldpts,oldfaces,all_triangles=True)
newpts=[Vector((x*.8,y,z-2)) for x,y,z in v]
B1=BVHTree.FromPolygons(newpts,[tuple(inds[i:i+3]) for i in range(0,len(inds),3)],all_triangles=True)
def ray(bvh,x,world_y):
 y=(world_y+.02625)/.075
 hit,normal,tri,dist=bvh.ray_cast(Vector((x,y,0)),Vector((0,0,-1)),.1/.075)
 return hit is not None
def down(bvh,x,z):
 hit,normal,tri,dist=bvh.ray_cast(Vector((x,10,z)),Vector((0,-1,0)),20)
 return None if hit is None else -.02625+.075*hit.y
rays=[{"lane":x,"height":y,"source_blocked":ray(B0,x,y),"proxy_blocked":ray(B1,x,y)}
      for x in (-.35,0.,.35) for y in (.12,.16,.18,.2,.22,.24)]
samples=[]
for x in (-.35,0.,.35):
 for z in (0.,-.0952,-.5714,-1.0476,-1.333333):
  a=down(B0,x,z);c=down(B1,x,z)
  samples.append({"lane":x,"local_z":z,"source":a,"proxy":c,
                  "deviation_m":None if a is None or c is None else round(c-a,8)})
checks={
 "original_SHA":hashlib.sha256(raw).hexdigest()==SHA,
 "original_riser_reproduced":ray(B0,0.,.16) and ray(B0,0.,.2),
 "proxy_rays_clear":all(not a["proxy_blocked"] for a in rays),
 "all_support_samples":all(a["proxy"] is not None for a in samples),
 "support_matches_original_10mm":all(a["deviation_m"] is not None and abs(a["deviation_m"])<=.010 for a in samples),
 "outside_lane_unsupported":all(down(B1,2.5,z) is None for z in (0.,-.57,-1.33)),
 "tread_faces_16":len(inds)//3==16,
 "original_PBR_metadata":new["materials"]==j["materials"] and new["images"]==j["images"] and new["textures"]==j["textures"],
 "blender_clean":not bpy.data.is_dirty
}
report={"status":"OFFLINE_GEOMETRY_QA_ONLY","source":str(SRC),
 "source_sha256":SHA,"candidate":GLB.name,"candidate_sha256":new_sha,
 "candidate_size_bytes":len(binary),"source_faces":len(oldfaces),"proxy_faces":16,
 "source_steps":8,"source_node_transform":nnod["scale"],
 "qa_runtime_collision_configuration":{"visual_source_asset":"MUST be QA-only movement collision OFF to avoid old riser blocking; original GLB bytes never changed",
 "candidate_tread_asset":"movement collision ON, sight OFF, camera collision OFF",
 "note":"Walkable stair collision retained. Rail/wall blocking, camera and native token traversal still unverified."},
 "checks":checks,"ray_checks":rays,"support_checks":samples,
 "native_traversal_certified":False,"production_certified":False,
 "requires_native_alignment_and_guarded_rollback":True}
if not all(checks.values()):
 result={"pass":False,"report":report}
else:
 payload=(json.dumps(report,indent=2,sort_keys=True)+"\n").encode()
 def stage(path,content):
  path.parent.mkdir(parents=True,exist_ok=True)
  if path.exists():
   if path.read_bytes()!=content:raise RuntimeError("Refuse overwrite nonidentical "+str(path))
   return "UNCHANGED_SAME_SHA"
  tmp=path.with_suffix(path.suffix+".staging-tmp")
  if tmp.exists():raise RuntimeError("stale temp "+str(tmp))
  with tmp.open("xb") as h:
   h.write(content);h.flush();os.fsync(h.fileno())
  os.replace(tmp,path)
  if path.read_bytes()!=content:raise RuntimeError("Readback mismatch "+str(path))
  return "CREATED"
 stages={str(p):stage(p,x) for p,x in ((GLB,binary),(MAN,payload),
      (DRIVE/GLB.name,binary),(DRIVE/MAN.name,payload))}
 result={"pass":True,"checks":checks,"candidate_sha256":new_sha,
 "source_sha256":SHA,"output_paths":stages,
 "native_traversal_certified":False,"production_certified":False}
