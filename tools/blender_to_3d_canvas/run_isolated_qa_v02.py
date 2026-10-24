"""Source-owned isolated GM-only 3D Canvas native import and visual QA runner.

OFFLINE mode performs immutable source/GLB checks only and requires no login:
  python run_isolated_qa_v02.py --bundle-dir STAGED --asset-root MODULE_ASSETS

Live mode requires a freshly authenticated GM client and the first-party
manage_empty_qa_scene browser operation installed and responsive:
  python run_isolated_qa_v02.py --bundle-dir ... --asset-root ... --live

It creates or reuses only an EXACTLY owned empty inactive Scene, never alters
an existing campaign/Manor Scene, never activates the new Scene for players,
and returns the GM to the accepted original. Temporary imported QA Tiles are
deleted unless --retain-import is requested. Scene deletion is deliberately
separate: empty fixture QA Scenes can be inspected and reused safely.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import pathlib
import sys

from import_chunks_v02 import verify, call, PROTECTED_SCENE, PROTECTED_SHA

SEMANTIC_PREFIX = "qa:multichunk:"
REQUIRED_CHUNKS = {
    "lower_back_wall", "lower_floor", "lower_side_wall",
    "stair_connector","upper_doorway","upper_floor","upper_interactive_door"
}
REQUIRED_COUNTS = ("tiles","walls","lights","regions","tokens",
                   "drawings","sounds","notes","templates")

def provision():
    _,check=call(PROTECTED_SCENE,{
        "op":"manage_empty_qa_scene","action":"inspect"},True,
        PROTECTED_SHA,timeout=80)
    if (check.get("source_revision")!=PROTECTED_SHA or
        check.get("foundry_active_scene_id")!=PROTECTED_SCENE or
        check.get("gm_viewed_scene_id")!=PROTECTED_SCENE or
        check.get("players_pulled")):
        raise RuntimeError("Source GM ownership violated, refuse provisioning.")
    if check.get("qa_exists"):
        if not check.get("qa_owned") or not check.get("qa_empty"):
            raise RuntimeError("Existing isolated QA Scene is occupied/unowned.")
        if not check.get("qa_scene_id"):
            raise RuntimeError("QA Scene ID missing.")
        return check["qa_scene_id"],False
    _,created=call(PROTECTED_SCENE,{
        "op":"manage_empty_qa_scene","action":"create"},False,
        PROTECTED_SHA,timeout=85)
    if not created.get("created") or not created.get("qa_empty"):
        raise RuntimeError("QA create outcome unverified; STOP and inspect.")
    return created["qa_scene_id"],True

def owned_inspect(scene_id):
    # manage_empty_qa_scene reports ownership from the immutable ORIGINAL,
    # not from mutable imported Tile flags.
    _,q=call(PROTECTED_SCENE,{"op":"manage_empty_qa_scene","action":"inspect"},
             True,PROTECTED_SHA,timeout=80)
    if (not q.get("qa_owned") or q.get("qa_scene_id")!=scene_id or
        q.get("foundry_active_scene_id")!=PROTECTED_SCENE or q.get("players_pulled")):
        raise RuntimeError("Owned scene isolation failed.")
    return q

def native_preview(scene_id,manifest,rows,sha):
    got=[]
    grid=manifest["foundry"]
    for row in rows:
        x,y=row["tile_center_xy_px"]
        op={"op":"preview_native_asset_tile",
            "foundry_path":row["foundry_path"],
            "x":x,"y":y,"scale":grid["native_3d_tile_scale"],
            "elevation":row["tile_elevation"],"origin":"center",
            "rotation":0,"collision":True,"sight":True,
            "camera_collision":True}
        _,preview=call(scene_id,op,True,sha,timeout=95)
        cand=preview.get("candidate") or {}
        exp=row["expected_dimensions_px"]
        if abs(cand.get("width",-1000)-exp[0])>1.1 or abs(cand.get("height",-1000)-exp[1])>1.1:
            raise RuntimeError("Native Tile 2D size mismatch "+row["chunk_id"])
        flags=cand.get("flags",{}).get("levels-3d-preview",{})
        depth=flags.get("depth")
        if not isinstance(depth,(int,float)) or abs(depth-exp[2])>.35:
            raise RuntimeError("Native 3D depth mismatch "+row["chunk_id"])
        cand["x"]=round(x);cand["y"]=round(y)
        cand["elevation"]=row["tile_elevation"]
        if row["interactive_door"]:
            authored=next(it for it in manifest["chunks"]
                         if it["chunk_id"]==row["chunk_id"])
            entries=[obj["native_door_extras"]
                     for obj in authored["source_objects"]
                     if obj["native_door_extras"].get("doorId")]
            if len(entries)!=1:
                raise RuntimeError("A single native door identity is required.")
            extra=entries[0]
            flags["doorType"]=int(extra.get("doorType",1))
            flags["doorState"]=int(extra.get("doorState",0))
            flags["doorStyle"]=int(extra.get("doorStyle",0))
        got.append(cand)
    return got

def collect_owned(scene_id,semantics):
    envelope,s=call(scene_id,{"op":"inspect_3d_scene"},True,timeout=80)
    items=(s.get("tiles") or [])
    found=[t for t in items if (t.get("acq") or {}).get("semantic_id") in semantics]
    # Revision is attached to the command envelope, not the inspect
    # operation itself. Preserve the operation's native geometry fields.
    return {**s,"after_revision":envelope["after_revision"]},found

def import_once(scene_id,manifest,rows,sha):
    candidates=native_preview(scene_id,manifest,rows,sha)
    ids={r["semantic_id"] for r in rows}
    before,exists=collect_owned(scene_id,ids)
    if before["after_revision"]!=sha or exists:
        raise RuntimeError("QA pre-import revision drift or duplicate semantic Tile.")
    objs=[{"document":"Tile","semantic_id":r["semantic_id"],
           "build_id":manifest["bundle"],
           "classification":"QA_ONLY_MULTICHUNK_V02",
           "provenance":{"asset_sha256":r["glb_sha256"],
                         "source":manifest["source_blend"]},
           "data":c}
          for r,c in zip(rows,candidates)]
    _,dry=call(scene_id,{"op":"apply_semantic_objects","build_id":manifest["bundle"],
                        "objects":objs},True,sha,timeout=85)
    if len(dry.get("created") or [])!=len(objs):
        raise RuntimeError("Native creation preflight missing items.")
    _,created=call(scene_id,{"op":"apply_semantic_objects",
                 "build_id":manifest["bundle"],"objects":objs},
                  False,sha,timeout=125)
    if len(created.get("created") or [])!=len(objs) or any(
        not v.get("id") for v in created["created"]):
        raise RuntimeError("Ambiguous native batch creation; manual safety inspection required.")
    after,actual=collect_owned(scene_id,ids)
    if len(actual)!=len(objs) or any(not t.get("runtime_bounds") for t in actual):
        raise RuntimeError("Imported real 3D bounds not verified.")
    return after["after_revision"], actual

def cleanup(scene_id,owned,expected_count):
    _,s=call(scene_id,{"op":"inspect_3d_scene"},True,timeout=80)
    semantics=set(owned)
    tiles=s.get("tiles") or []
    owned_tiles=[t for t in tiles if (t.get("acq") or {}).get("semantic_id") in semantics]
    if len(owned_tiles)!=expected_count:
        raise RuntimeError("Exact importer-owned deletion cardinality changed.")
    if any((t.get("acq") or {}).get("classification")!="QA_ONLY_MULTICHUNK_V02"
           for t in owned_tiles):
        raise RuntimeError("Unowned Tile among cleanup targets.")
    _,deleted=call(scene_id,{"op":"delete_semantic_objects",
                 "semantic_ids":sorted(semantics)},
                 False,s["after_revision"],timeout=90)
    if len(deleted.get("deleted") or [])!=expected_count:
        raise RuntimeError("Native cleanup incomplete.")
    final,remaining=collect_owned(scene_id,semantics)
    if remaining:
        raise RuntimeError("Imported Tiles remain after cleanup.")
    return final["after_revision"]

def view_original(qa_id):
    _,r=call(qa_id,{"op":"manage_empty_qa_scene",
                   "action":"restore_view"},False,timeout=90)
    if r.get("now_viewed")!=PROTECTED_SCENE or r.get("players_pulled"):
        raise RuntimeError("Original GM view restoration failed.")
    return r

def execute(args):
    manifest,rows=verify(args.bundle_dir,args.asset_root)
    if set(r["chunk_id"] for r in rows)!=REQUIRED_CHUNKS:
        raise RuntimeError("This v0.2 QA runner accepts exactly the seven verified library chunks.")
    if not args.live:
        return {"ok":True,"phase":"OFFLINE_VERIFIED",
                "chunks":len(rows),"source_sha":manifest["source_blend_sha256"],
                "source_blend":manifest["source_blend"],
                "scene_mutated":False}
    qa_id,created=provision()
    viewed=False
    imported=False
    baseline=None
    error=None
    report=None
    try:
        owned=owned_inspect(qa_id)
        if not owned["qa_empty"] or any(owned["qa_counts"].get(k)!=0 for k in REQUIRED_COUNTS):
            raise RuntimeError("Expected totally empty QA Scene.")
        baseline=owned["qa_revision"]
        _,v=call(PROTECTED_SCENE,{"op":"manage_empty_qa_scene",
                 "action":"view","qa_scene_id":qa_id},False,
                 PROTECTED_SHA,timeout=90)
        if v.get("now_viewed")!=qa_id or v.get("players_pulled"):
            raise RuntimeError("GM-only QA local view failed.")
        viewed=True
        _,capture=call(qa_id,{"op":"capture_3d_view",
                  "format":"webp","quality":0.4,"restore_camera":True},
                  False,timeout=130)
        if not capture.get("image_base64"):
            raise RuntimeError("Native 3D renderer did not initialize.")
        empty_envelope,empty=call(qa_id,{"op":"inspect_3d_scene"},True,timeout=70)
        if empty.get("tile_count")!=0:
            raise RuntimeError("Unexpected Tile in reserved empty QA Scene.")
        loaded_sha,objects=import_once(qa_id,manifest,rows,
                                      empty_envelope["after_revision"])
        imported=True
        # Real nonblack visual QA belongs to an actual capture. This runner
        # returns captured metadata but not DM artistic acceptance.
        _,viewshot=call(qa_id,{"op":"capture_3d_view",
                       "format":"webp","quality":0.8,"restore_camera":True},
                       False,timeout=130)
        image_b64=viewshot.get("image_base64","")
        report={"ok":True,"phase":"NATIVE_IMPORT_AND_CAPTURED",
                "qa_scene_id":qa_id,"qa_created":created,
                "chunks":len(objects),"loaded_revision":loaded_sha,
                "capture_bytes_encoded":len(image_b64),
                "visual_art_accepted":False,"movement_accepted":False,
                "retained_import":bool(args.retain_import)}
        if not args.retain_import:
            clean=cleanup(qa_id,{r["semantic_id"] for r in rows},len(rows))
            imported=False
            report["empty_revision_restored"]=clean==baseline
    except Exception as e:
        error=e
        # A partially applied uncertain write is NOT automatically replayed,
        # deleted or hidden. Leave exact recovery evidence for manual check.
    finally:
        if viewed:
            try:view_original(qa_id)
            except Exception as restoration:
                raise RuntimeError("STOP: GM view restoration UNVERIFIED: "+
                                   str(restoration)+"; prior error="+str(error)) from restoration
    if error:
        raise error
    if not report:raise RuntimeError("No acceptance report produced.")
    final=owned_inspect(qa_id)
    if not args.retain_import and not final["qa_empty"]:
        raise RuntimeError("QA scene did not restore to an empty state.")
    if final["gm_viewed_scene_id"]!=PROTECTED_SCENE:
        raise RuntimeError("GM is not viewing the approved original.")
    report["gm_view_restored"]=True
    report["protected_source_revision"]=final["source_revision"]
    return report

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--bundle-dir",type=pathlib.Path,required=True)
    parser.add_argument("--asset-root",type=pathlib.Path,required=True)
    parser.add_argument("--live",action="store_true")
    parser.add_argument("--retain-import",action="store_true")
    args=parser.parse_args()
    try:print(json.dumps(execute(args),indent=2))
    except Exception as error:
        print(json.dumps({"ok":False,"error":str(error)}),file=sys.stderr)
        sys.exit(1)
