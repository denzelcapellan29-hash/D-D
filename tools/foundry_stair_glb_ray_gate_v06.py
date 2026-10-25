"""Read-only source GLB stair ray gate for Foundry V14 / native 3D Canvas.
Run inside Blender's Python interpreter; no scene import, save or mutation.
The fixture-to-world constants below are intentionally v06-specific, not global.
"""
import hashlib
import json
import math
import struct
from pathlib import Path
from mathutils import Matrix, Quaternion, Vector
from mathutils.bvhtree import BVHTree

EXPECTED_V06_SHA = "734f0c1bff44ce81fcad156c45477d36cdbd09f78e4117b07ec83f46071df81e"
FORMAT = {5120:"b",5121:"B",5122:"h",5123:"H",5125:"I",5126:"f"}
SIZE = {k:struct.calcsize("<"+v) for k,v in FORMAT.items()}

def _read_glb(path):
    raw=Path(path).read_bytes()
    if len(raw)<20 or raw[:4]!=b"glTF":
        raise ValueError("not a GLB file")
    magic,version,size=struct.unpack_from("<4sII",raw,0)
    if version!=2 or size!=len(raw):
        raise ValueError("GLB version/length mismatch")
    pos=12; chunks={}
    while pos<len(raw):
        n,typ=struct.unpack_from("<I4s",raw,pos);pos+=8
        if pos+n>len(raw): raise ValueError("truncated GLB chunk")
        chunks[typ]=raw[pos:pos+n];pos+=n
    doc=json.loads(chunks[b"JSON"].decode("utf-8"))
    if len(doc.get("buffers",[]))!=1 or b"BIN\x00" not in chunks:
        raise ValueError("expect one embedded BIN buffer; external buffers not allowed")
    return doc,chunks[b"BIN\x00"],hashlib.sha256(raw).hexdigest()

def _accessor(doc,binbuf,i):
    ac=doc["accessors"][i]
    if ac.get("sparse") or "bufferView" not in ac:
        raise ValueError("sparse/accessor without view is unsupported")
    view=doc["bufferViews"][ac["bufferView"]]
    if view.get("buffer",0)!=0: raise ValueError("nonzero buffer")
    ty=ac["type"]; components={"SCALAR":1,"VEC2":2,"VEC3":3,"VEC4":4}[ty]
    comp=ac["componentType"]; width=SIZE[comp]; rowbytes=width*components
    stride=view.get("byteStride",rowbytes)
    start=view.get("byteOffset",0)+ac.get("byteOffset",0)
    fmt="<"+FORMAT[comp]*components
    if stride<rowbytes or start+(ac["count"]-1)*stride+rowbytes>len(binbuf):
        raise ValueError("invalid accessor bounds")
    return [struct.unpack_from(fmt,binbuf,start+j*stride) for j in range(ac["count"])]

def _node_matrix(node):
    if "matrix" in node:
        a=node["matrix"]
        return Matrix(tuple(tuple(a[4*c+r] for c in range(4)) for r in range(4)))
    t=node.get("translation",(0,0,0))
    x,y,z,w=node.get("rotation",(0,0,0,1))
    s=node.get("scale",(1,1,1))
    return Matrix.Translation(t) @ Quaternion((w,x,y,z)).to_matrix().to_4x4() @ Matrix.Diagonal((s[0],s[1],s[2],1))

def load_triangles(path,expected_sha=None):
    doc,binbuf,sha=_read_glb(path)
    if expected_sha and sha!=expected_sha:
        raise ValueError("source SHA mismatch, refusing unverified geometry")
    vertices=[]; faces=[]; parts=[]
    def walk(index,parent):
        nd=doc["nodes"][index]
        mat=parent @ _node_matrix(nd)
        if "mesh" in nd:
            me=doc["meshes"][nd["mesh"]]
            for pi,prim in enumerate(me["primitives"]):
                if prim.get("mode",4)!=4 or "POSITION" not in prim.get("attributes",{}):
                    raise ValueError("nontriangle primitive")
                pts=_accessor(doc,binbuf,prim["attributes"]["POSITION"])
                ids=([x[0] for x in _accessor(doc,binbuf,prim["indices"])]
                     if "indices" in prim else list(range(len(pts))))
                if len(ids)%3: raise ValueError("indices not triangles")
                base=len(vertices)
                vertices.extend([tuple(mat @ Vector(v)) for v in pts])
                for j in range(0,len(ids),3):
                    trip=tuple(base+k for k in ids[j:j+3])
                    if any(k>=base+len(pts) or k<base for k in trip):
                        raise ValueError("index out of bounds")
                    faces.append(trip)
                parts.append({"node":nd.get("name",str(index)),
                              "mesh":me.get("name",str(nd["mesh"])),
                              "primitive":pi,"triangles":len(ids)//3})
        for child in nd.get("children",[]): walk(child,mat)
    roots=doc["scenes"][doc.get("scene",0)]["nodes"]
    for node in roots:walk(node,Matrix.Identity(4))
    if not faces: raise ValueError("no triangles in GLB")
    return vertices,faces,sha,parts

def _hit(bvh,orig,direction,length):
    hit,normal,tri,dist=bvh.ray_cast(Vector(orig),Vector(direction),length)
    if hit is None: return None
    return {"source_z":round(float(hit.z),8),"source_y":round(float(hit.y),8),
            "distance":round(float(dist),8),"triangle":int(tri)}

def run_gate(path,expected_sha=EXPECTED_V06_SHA,world_scale=.075,
             y_offset=-.02625,z_origin=1.46,start_z=0.0,
             travel_m=.1,lanes=(-.35,0,.35),
             sample_heights_m=(.12,.16,.18,.20,.22,.24),
             support_z=(0,-.0952,-.5714,-1.0476,-1.333333333333)):
    """Read-only BVH evaluation of one 100px move; returns reproducible JSON data.
    Heights are *samples*, not a measured native token LOS-height. A clear
    sampled ray alone never implies actual TokenLayer travel is certified.
    """
    if world_scale<=0 or travel_m<=0:raise ValueError("positive scale/travel required")
    vertices,faces,sha,parts=load_triangles(path,expected_sha)
    bvh=BVHTree.FromPolygons([Vector(p) for p in vertices],faces,all_triangles=True)
    distance=travel_m/world_scale
    lanes_out=[]
    for x in lanes:
        rays=[]
        for h in sample_heights_m:
            ly=(h-y_offset)/world_scale
            hit=_hit(bvh,(x,ly,start_z),(0,0,-1),distance)
            rays.append({"world_height_m":h,"hit":bool(hit),
                         "world_collision_z_m":round(z_origin+hit["source_z"]*world_scale,8) if hit else None,
                         "source":hit})
        lanes_out.append({"x":x,"rays":rays})
    supports=[]
    for z in support_z:
        hit=_hit(bvh,(0,10,z),(0,-1,0),20)
        supports.append({"source_z":z,
                         "world_support_y_m":round(y_offset+hit["source_y"]*world_scale,8) if hit else None,
                         "source":hit})
    # Calibrated fixture assertions are deliberately scoped to the immutable v06 hash.
    checks=[]
    if sha==EXPECTED_V06_SHA and world_scale==.075 and start_z==0 and abs(travel_m-.1)<1e-12:
        at={round(v["world_height_m"],4):v for v in lanes_out[1]["rays"]}
        for h,want,worldz in ((.12,False,None),(.16,True,1.45375),
                               (.20,True,1.385),(.24,False,None)):
            got=at[h]
            checks.append({"height":h,"expected_hit":want,
                           "expected_z":worldz,
                           "pass":got["hit"]==want and
                           (worldz is None or (got["world_collision_z_m"] is not None and
                            abs(got["world_collision_z_m"]-worldz)<1e-6))})
    return {"source_sha256":sha,"source_bytes":Path(path).stat().st_size,
            "triangles":len(faces),"parts":parts,"movement_length_native_m":travel_m,
            "source_ray_length":distance,"lanes":lanes_out,
            "support_samples":supports,"calibrated_checks":checks,
            "calibrated_pass":bool(checks) and all(v["pass"] for v in checks),
            "native_runtime_certified":False,
            "scope":"immutable disposable v06 GLB; not the current Manor staircase"}


def run_v06_regression(path):
    """Four actual source lanes and a 25mm shifted support negative control."""
    z_riser=-0.0952
    shifted_z=z_riser+(.025/.075) # +25mm in placed native world distance
    q=run_gate(path,lanes=(-.35,0,.35,2.5),
               sample_heights_m=(.12,.16,.20,.24),
               support_z=(0,z_riser,shifted_z,-.5714,-1.0476,-1.333333333333))
    expect=((.12,False,None),(.16,True,1.45375),
            (.20,True,1.385),(.24,False,None))
    checked={}
    checked["three_lateral_lanes"]=all(
        all(ray["hit"]==hit and
            (z is None or abs(ray["world_collision_z_m"]-z)<1e-6)
            for ray,(_,hit,z) in zip(lane["rays"],expect))
        for lane in q["lanes"][:3])
    checked["outside_stair_lane_clear"]=all(
        not ray["hit"] for ray in q["lanes"][3]["rays"])
    on,shift=q["support_samples"][1:3]
    checked["support_at_riser"]=abs(on["world_support_y_m"]-.16089)<1e-5
    checked["25mm_shift_negative_control"]=(
        shift["world_support_y_m"] is not None
        and on["world_support_y_m"]-shift["world_support_y_m"] > .03)
    checked["sha_pinned"]=q["source_sha256"]==EXPECTED_V06_SHA
    return {"pass":all(checked.values()),"checks":checked,
            "source_sha256":q["source_sha256"],
            "source_triangles":q["triangles"],
            "near_riser_support_m":on["world_support_y_m"],
            "shift_plus_25mm_support_m":shift["world_support_y_m"],
            "immutable_fixture_only":True,
            "native_runtime_certified":False}

if __name__=="__main__" and "--" in __import__("sys").argv:
    import sys
    from argparse import ArgumentParser
    parser=ArgumentParser(description="BVH source preflight; no native runtime claim")
    parser.add_argument("--asset",required=True)
    parser.add_argument("--regression-v06",action="store_true")
    parser.add_argument("--unpin",action="store_true",
                        help="candidate asset, source-only diagnosis (not native certification)")
    opts=parser.parse_args(sys.argv[sys.argv.index("--")+1:])
    if opts.regression_v06:
        output=run_v06_regression(opts.asset)
        print(json.dumps(output,indent=2,sort_keys=True))
        if not output["pass"]: raise SystemExit(3)
    else:
        output=run_gate(opts.asset,expected_sha=None if opts.unpin else EXPECTED_V06_SHA)
        print(json.dumps(output,indent=2,sort_keys=True))
