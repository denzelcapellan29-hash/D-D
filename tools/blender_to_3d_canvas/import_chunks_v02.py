"""QA-only multi-chunk Blender GLB -> native 3D Canvas import v0.2.

--offline verifies immutable GLBs/manifest/source with ZERO Foundry operations.
--native-preview additionally calls native loader on the GM-viewed QA clone.
--apply requires preview, exact inactive QA clone, no existing semantic IDs,
and verifies all created IDs/real native Three.js bounds. No campaign writes.

This is a new source-safe experiment; v0.1 production proof remains unchanged.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
import pathlib
import struct
import sys
import urllib.error
import urllib.request
import uuid

SCHEMA="acq.blender-3dcanvas.multichunk.v0.2"
QA_SCENE="sW4aXZgKXj1cH0US"
PROTECTED_SCENE="NUEDEFAULTSCENE0"
PROTECTED_SHA="e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f"
QA_BASELINE_SHA="05134d2c6debeb2ffb49d17b3f1c06e96dfa409c35a348d801157dd815a03e94"
PREFIX="modules/acq-foundry-bridge/assets/blender_bundles/"
BRIDGE="http://127.0.0.1:18747/rpc"

def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for part in iter(lambda:f.read(1<<20),b""):
            h.update(part)
    return h.hexdigest()

def read_glb_metadata(path):
    with open(path,"rb") as f:
        header=f.read(20)
        if len(header)!=20:
            raise RuntimeError("GLB truncated header: "+path.name)
        magic,version,total,chunk_length,chunk_type=struct.unpack("<4sII I4s",header)
        if magic!=b"glTF" or version!=2 or chunk_type!=b"JSON" or total!=path.stat().st_size:
            raise RuntimeError("Invalid GLB2 header or file length: "+path.name)
        if chunk_length<100 or chunk_length>total-20:
            raise RuntimeError("Invalid GLB JSON length: "+path.name)
        meta=json.loads(f.read(chunk_length))
    meshes=meta.get("meshes",[])
    if not meshes or not meta.get("nodes"):
        raise RuntimeError("GLB is missing 3D meshes/nodes: "+path.name)
    return {"meshes":len(meshes),"nodes":len(meta["nodes"]),
            "materials":len(meta.get("materials",[])),
            "animations":len(meta.get("animations",[])),
            "has_extras":any("extras" in x for x in meta.get("nodes",[]))}

def safe_identifier(text):
    return (isinstance(text,str) and 1<=len(text)<=70 and text.isascii()
        and all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in text))

def verify(bundle, assets_root=None):
    folder=bundle.resolve(strict=True)
    manifest_file=folder/"manifest.json"
    doc=json.loads(manifest_file.read_text(encoding="utf8"))
    if doc.get("schema")!=SCHEMA:
        raise RuntimeError("Unsupported bundle schema, expected v0.2.")
    if len(doc.get("chunks",[]))<2 or len(doc["chunks"])>64:
        raise RuntimeError("Multi-chunk v0.2 requires 2..64 explicit chunks.")
    if not safe_identifier(doc.get("bundle")):
        raise RuntimeError("Invalid bundle ID.")
    grid=doc["foundry"]
    vals=[grid[x] for x in ("pixels_per_blender_meter","scene_grid_size_px","scene_grid_distance","native_3d_tile_scale")]
    if not all(isinstance(v,(int,float)) and math.isfinite(v) and v>0 for v in vals):
        raise RuntimeError("Invalid coordinate scale in manifest.")
    if abs(vals[0]/vals[1]-vals[3])>1e-9:
        raise RuntimeError("Inconsistent Foundry native scale.")
    source=pathlib.Path(doc["source_blend"])
    if not source.is_file() or source.stat().st_size!=doc["source_blend_bytes"] or digest(source)!=doc["source_blend_sha256"]:
        raise RuntimeError("Source .blend changed after export.")
    staging_root=None
    if assets_root is not None:
        root=assets_root.resolve(strict=True)
        if not folder.is_relative_to(root):
            raise RuntimeError("Native import bundle must be staged under authorized module assets.")
        rel=folder.relative_to(root)
        if any(p in ("..",".") for p in rel.parts):
            raise RuntimeError("Unsafe asset path.")
        staging_root=PREFIX+rel.as_posix()+"/"
    seen=set()
    rows=[]
    for index,item in enumerate(doc["chunks"]):
        cid=item["chunk_id"]
        if not safe_identifier(cid) or cid in seen:
            raise RuntimeError("Invalid/duplicate chunk id: "+repr(cid))
        seen.add(cid)
        asset=item["asset"]
        filename=asset["filename"]
        if pathlib.PurePath(filename).name!=filename or not filename.endswith(".glb") or "/" in filename or "\\" in filename:
            raise RuntimeError("Unsafe GLB filename.")
        glb=folder/filename
        if not glb.is_file() or glb.stat().st_size!=asset["bytes"] or digest(glb)!=asset["sha256"]:
            raise RuntimeError("GLB hash/length mismatch for "+cid)
        meta=read_glb_metadata(glb)
        if meta["animations"]:
            raise RuntimeError("Source contains unapproved embedded animation: "+cid)
        lo=item["source_bounds_m"]["min"]; hi=item["source_bounds_m"]["max"]
        if not all(isinstance(v,(int,float)) and math.isfinite(v) for v in lo+hi):
            raise RuntimeError("Non-finite source chunk bounds.")
        if any(hi[i]<lo[i] for i in range(3)):
            raise RuntimeError("Negative source bounding extent.")
        px=grid["pixels_per_blender_meter"]
        predicted=[(hi[0]-lo[0])*px,(hi[1]-lo[1])*px,(hi[2]-lo[2])*px]
        observed=item["expected_tile_footprint_px"]+[item["expected_tile_depth_px"]]
        if max(abs(a-b) for a,b in zip(predicted,observed))>1e-5:
            raise RuntimeError("Manifest dimension prediction inconsistent: "+cid)
        expected_elev=lo[2]*px*grid["scene_grid_distance"]/grid["scene_grid_size_px"]
        if abs(expected_elev-item["tile_elevation_scene_units"])>1e-6:
            raise RuntimeError("Elevation anchor inconsistent: "+cid)
        if item["kind"] not in ("static","interactive"):
            raise RuntimeError("Unsupported chunk kind.")
        if item["kind"]=="interactive" and len(item["source_objects"])!=1:
            raise RuntimeError("Interactive chunk must contain exactly one authored part.")
        for o in item["source_objects"]:
            mat=o["source_matrix_world_rowmajor"]
            if len(mat)!=16 or not all(isinstance(x,(int,float)) and math.isfinite(x) for x in mat):
                raise RuntimeError("Invalid authored world transform: "+cid)
        rows.append({
          "chunk_id":cid,"kind":item["kind"],"interactive_door":item["interactive_door"],
          "glb_file":str(glb),"glb_sha256":asset["sha256"],
          "glb":meta,"foundry_path":staging_root+filename if staging_root else None,
          "tile_center_xy_px":item["tile_center_xy_px"],
          "tile_elevation":item["tile_elevation_scene_units"],
          "expected_dimensions_px":observed,
          "semantic_id":"qa:multichunk:"+doc["bundle"]+":"+cid,
          "source_objects":len(item["source_objects"])
        })
    return doc,rows

def call(scene,op,dry_run=True,revision=None,timeout=90):
    p={"protocol_version":1,"scene_id":scene,"command_id":"v02-"+str(uuid.uuid4()),
       "dry_run":dry_run,"operations":[op],"_timeout_seconds":timeout}
    if revision:p["expected_revision"]=revision
    request=urllib.request.Request(BRIDGE,data=json.dumps(p).encode("utf8"),
        headers={"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(request,timeout=timeout+5) as response:
            result=json.loads(response.read())
    except urllib.error.HTTPError as error:
        raise RuntimeError("Bridge HTTP "+str(error.code)+" "+
                           error.read(1200).decode("utf8","replace")) from error
    entry=(result.get("operations") or [{}])[0]
    if not result.get("ok") or not entry.get("ok"):
        raise RuntimeError("Native command failed: "+str(result.get("error",entry.get("error"))))
    return result,entry

def inspect_guard():
    _,qastatus=call(QA_SCENE,
        {"op":"manage_vision_qa_scene","action":"inspect"},True,timeout=70)
    if (qastatus.get("source_scene_id")!=PROTECTED_SCENE
        or qastatus.get("source_revision")!=PROTECTED_SHA
        or qastatus.get("foundry_active_scene_id")!=PROTECTED_SCENE
        or qastatus.get("gm_viewed_scene_id")!=QA_SCENE
        or qastatus.get("qa_scene_id")!=QA_SCENE
        or not qastatus.get("qa_exists")
        or qastatus.get("players_pulled")):
        raise RuntimeError("Original accepted Scene or GM-only QA safety guard failed.")
    snap,scene=call(QA_SCENE,{"op":"inspect_3d_scene"},True,timeout=70)
    if snap.get("scene_id")!=QA_SCENE or not scene.get("levels3d_active"):
        raise RuntimeError("GM must view the inactive QA clone with native 3D Canvas active.")
    if snap.get("after_revision")!=QA_BASELINE_SHA:
        raise RuntimeError("QA clone diverged from pinned baseline; refuse v0.2 writes.")
    return snap,scene

def native_candidates(rows,manifest,revision):
    candidates=[]
    for row in rows:
        if not row["foundry_path"]:
            raise RuntimeError("Staging is required for native previews.")
        cx,cy=row["tile_center_xy_px"]
        if any(not math.isfinite(v) for v in (cx,cy,row["tile_elevation"])) or abs(cx)>100000 or abs(cy)>100000:
            raise RuntimeError("Invalid native Tile center/elevation.")
        preview_op={
            "op":"preview_native_asset_tile","foundry_path":row["foundry_path"],
            "x":cx,"y":cy,"scale":manifest["foundry"]["native_3d_tile_scale"],
            "elevation":row["tile_elevation"],"origin":"center","rotation":0,
            "collision":True,"sight":True,"camera_collision":True}
        _,preview=call(QA_SCENE,preview_op,True,revision,90)
        candidate=copy.deepcopy(preview.get("candidate") or {})
        expected=row["expected_dimensions_px"]
        if abs(candidate.get("width",-999)-expected[0])>1.1 or abs(candidate.get("height",-999)-expected[1])>1.1:
            raise RuntimeError("Native dimensions do not match Blender for "+row["chunk_id"])
        native_depth=candidate.get("flags",{}).get("levels-3d-preview",{}).get("depth")
        if not isinstance(native_depth,(float,int)) or abs(native_depth-expected[2])>0.3:
            raise RuntimeError("Native depth differs from Blender for "+row["chunk_id"])
        # Real 3D Canvas Tile x/y are *center* coordinates, not a corner.
        candidate["x"]=round(cx)
        candidate["y"]=round(cy)
        candidate["elevation"]=row["tile_elevation"]
        if row["interactive_door"]:
            attrs=row["source_objects"]
            authored=next(c for c in manifest["chunks"] if c["chunk_id"]==row["chunk_id"])
            extras=authored["source_objects"][0]["native_door_extras"]
            if not extras.get("doorId"):
                raise RuntimeError("Door has no native doorId.")
            # Keep the existing 3D Canvas vendor door engine/flags.
            flags=candidate.setdefault("flags",{}).setdefault("levels-3d-preview",{})
            flags["doorType"]=int(extras.get("doorType",1))
            flags["doorState"]=int(extras.get("doorState",0))
            flags["doorStyle"]=int(extras.get("doorStyle",0))
        candidates.append(candidate)
    return candidates

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bundle-dir",type=pathlib.Path,required=True)
    p.add_argument("--asset-root",type=pathlib.Path)
    p.add_argument("--native-preview",action="store_true")
    p.add_argument("--apply",action="store_true")
    a=p.parse_args()
    if a.apply and not a.native_preview:
        raise RuntimeError("Native apply requires full live native preflight.")
    doc,rows=verify(a.bundle_dir,a.asset_root)
    result={"ok":True,"stage":"OFFLINE_VERIFIED","schema":SCHEMA,
            "chunks":len(rows),"source_sha256":doc["source_blend_sha256"],
            "items":rows}
    if not a.native_preview:
        return result
    if not a.asset_root:
        raise RuntimeError("Native preflight requires authorized --asset-root.")
    snap,scene=inspect_guard()
    revision=snap["after_revision"]
    existing=[]
    for tile in scene.get("tiles") or []:
        if (tile.get("acq",{}).get("semantic_id") or "") in {r["semantic_id"] for r in rows}:
            existing.append(tile.get("id"))
    if existing:
        raise RuntimeError("No existing v0.2 semantic IDs allowed until idempotent update rollback certified: "+repr(existing))
    candidates=native_candidates(rows,doc,revision)
    records=[{"document":"Tile","semantic_id":row["semantic_id"],
             "build_id":doc["bundle"],"classification":"QA_ONLY_MULTICHUNK_V02",
             "provenance":{"asset_sha256":row["glb_sha256"],"source":doc["source_blend"]},
             "data":c}
             for row,c in zip(rows,candidates)]
    op={"op":"apply_semantic_objects","build_id":doc["bundle"],"objects":records}
    _,dry=call(QA_SCENE,op,True,revision,90)
    if len(dry.get("created") or [])!=len(records):
        raise RuntimeError("Native dry-run missing chunk create(s).")
    result["stage"]="NATIVE_PREFLIGHT_VERIFIED"
    result["native_dry_run"]=dry
    if not a.apply:
        return result
    # This is a non-production test fixture and must be fully reversible.
    wrote=False
    try:
        _,out=call(QA_SCENE,op,False,revision,100)
        wrote=True
        ids=[v.get("id") for v in out.get("created") or []]
        if len(ids)!=len(records) or any(not v for v in ids):
            raise RuntimeError("Native batch create returned null/partial Tile IDs; no acceptance.")
        _,loaded=call(QA_SCENE,{"op":"inspect_3d_scene"},True,timeout=80)
        tiles=loaded.get("tiles") or []
        for row,candidate in zip(rows,candidates):
            items=[v for v in tiles if v.get("acq",{}).get("semantic_id")==row["semantic_id"]]
            if len(items)!=1 or not items[0].get("runtime_bounds"):
                raise RuntimeError("Native runtime did not load exactly one chunk: "+row["chunk_id"])
            box=items[0]["runtime_bounds"]
            cx,cy=row["tile_center_xy_px"]
            expected=row["expected_dimensions_px"]
            residual=[abs(box["center"]["x"]*1000-round(cx)),
                      abs(box["center"]["z"]*1000-round(cy)),
                      abs(box["size"]["x"]*1000-candidate["width"]),
                      abs(box["size"]["z"]*1000-candidate["height"]),
                      abs(box["size"]["y"]*1000-expected[2])]
            if max(residual)>1.5:
                raise RuntimeError("Loaded runtime bounds mismatch "+row["chunk_id"]+": "+repr(residual))
        result["stage"]="QA_NATIVE_GEOMETRY_PASSED_NOT_ART_ACCEPTED"
        result["native_tile_ids"]=ids
        return result
    except Exception as error:
        if wrote:
            try:
                call(QA_SCENE,{"op":"delete_semantic_objects",
                               "semantic_ids":[r["semantic_id"] for r in rows]},
                     False,timeout=75)
            except Exception as undo:
                raise RuntimeError("Import failed: "+str(error)+
                                   "; rollback UNVERIFIED: "+str(undo)) from undo
        raise

if __name__=="__main__":
    try:print(json.dumps(main(),indent=2))
    except Exception as err:
        print(json.dumps({"ok":False,"error":str(err)}),file=sys.stderr)
        sys.exit(1)
