"""Create a disposable, versioned stair-geometry feasibility fixture.

Only the immutable generic v06 3D Canvas QA GLB is accepted. This copies its
existing faces, materials, UVs, textures, and glTF structure, stretching the
horizontal travel axis with inverse-transpose-corrected vertex normals.
It never writes an accepted source GLB or any .blend / Foundry Scene.
Native playability and art are NOT certified by this file.
"""
import hashlib
import json
import math
import struct
from pathlib import Path

PINNED_V06_SHA256 = "734f0c1bff44ce81fcad156c45477d36cdbd09f78e4117b07ec83f46071df81e"
STRETCH_Z = 1.5


def make_candidate(source, target, factor=STRETCH_Z):
    source, target = Path(source), Path(target)
    raw = source.read_bytes()
    source_sha = hashlib.sha256(raw).hexdigest()
    if source_sha != PINNED_V06_SHA256:
        raise ValueError("Source SHA mismatch: protected v06 file is immutable")
    if not math.isfinite(factor) or not 1 < factor <= 2:
        raise ValueError("Only 1 < horizontal stretch <= 2 is allowed")
    if raw[:4] != b"glTF" or struct.unpack_from("<I", raw, 4)[0] != 2:
        raise ValueError("Not a GLB v2")
    if struct.unpack_from("<I", raw, 8)[0] != len(raw):
        raise ValueError("GLB declared length mismatch")
    chunks, cursor = [], 12
    while cursor < len(raw):
        n, kind = struct.unpack_from("<I4s", raw, cursor)
        cursor += 8
        if cursor+n > len(raw):
            raise ValueError("Truncated GLB")
        chunks.append((kind, raw[cursor:cursor+n]))
        cursor += n
    if len(chunks) != 2 or chunks[0][0] != b"JSON" or chunks[1][0] != b"BIN\x00":
        raise ValueError("Unexpected GLB chunks")
    doc = json.loads(chunks[0][1])
    if any(doc.get(k) for k in ("skins","animations","extensionsRequired","extensionsUsed")):
        raise ValueError("Refusing modified or complex GLB")
    if len(doc.get("meshes",[])) != 1 or len(doc["meshes"][0]["primitives"]) != 1:
        raise ValueError("This tool only supports original one-primitive QA stair")
    primitive=doc["meshes"][0]["primitives"][0]
    if primitive.get("targets") or primitive.get("mode",4)!=4:
        raise ValueError("Unsupported mesh mode or morph targets")
    if set(primitive.get("attributes",{})) != {"POSITION","NORMAL","TEXCOORD_0"}:
        raise ValueError("Unexpected input attributes")
    buf=bytearray(chunks[1][1])
    transformed={}
    for kind in ("POSITION","NORMAL"):
        index=primitive["attributes"][kind]
        accessor=doc["accessors"][index]
        view=doc["bufferViews"][accessor["bufferView"]]
        if (accessor["componentType"],accessor["type"])!=(5126,"VEC3"):
            raise ValueError("Expected VEC3 float")
        if accessor.get("sparse") or view.get("buffer",0)!=0 or view.get("byteStride",12)!=12:
            raise ValueError("Unsupported accessor layout")
        start=view.get("byteOffset",0)+accessor.get("byteOffset",0)
        count=accessor["count"]
        if count < 1 or start+12*count>len(buf):
            raise ValueError("Accessor exceeds BIN chunk")
        mins=[math.inf]*3; maxs=[-math.inf]*3
        for j in range(count):
            offset=start+j*12
            x,y,z=struct.unpack_from("<fff",buf,offset)
            if not all(math.isfinite(a) for a in (x,y,z)):
                raise ValueError("Nonfinite vertex")
            if kind=="POSITION":
                z*=factor
            else:
                z/=factor
                norm=math.sqrt(x*x+y*y+z*z)
                if norm==0:raise ValueError("Zero normal")
                x,y,z=x/norm,y/norm,z/norm
            struct.pack_into("<fff",buf,offset,x,y,z)
            for c,val in enumerate((x,y,z)):
                mins[c]=min(mins[c],val)
                maxs[c]=max(maxs[c],val)
        if "min" in accessor:accessor["min"]=mins
        if "max" in accessor:accessor["max"]=maxs
        transformed[kind]=count
    # Source node translates the original 0..4 source-Z span by -2 to center.
    # A buffer-only stretch would shift its runtime origin: preserve the pivot.
    if len(doc.get("nodes",[]))!=1 or doc["nodes"][0].get("name")!="stairs":
        raise ValueError("Unexpected stair node: refusing unguarded pivot change")
    node=doc["nodes"][0]
    translation=node.get("translation")
    if translation is None or len(translation)!=3 or not math.isclose(translation[2],-2.0,abs_tol=1e-7):
        raise ValueError("Unexpected node pivot: refusing shifted candidate")
    node["translation"][2]*=factor
    docbytes=json.dumps(doc,separators=(",",":"),ensure_ascii=False).encode("utf8")
    docbytes+=b" "*(-len(docbytes)%4)
    binary=bytes(buf)
    payload=b"".join(struct.pack("<I4s",len(chunk),kind)+chunk for kind,chunk in
                     ((b"JSON",docbytes),(b"BIN\x00",binary)))
    out=struct.pack("<4sII",b"glTF",2,12+len(payload))+payload
    if target.exists():
        raise FileExistsError("A v07 QA candidate already exists: never overwrite")
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open("xb") as f:f.write(out)
    return {
      "immutable_original_sha256":source_sha,
      "candidate_sha256":hashlib.sha256(out).hexdigest(),
      "original_bytes":len(raw),"candidate_bytes":len(out),
      "horizontal_z_factor":factor,"accessors":transformed,
      "candidate_path":str(target),"scope":"generic QA stair only",
      "blender_scene_mutated":False,"native_certified":False,"art_accepted":False,
    }

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    print(json.dumps(make_candidate(a.source,a.output),indent=2,sort_keys=True))
