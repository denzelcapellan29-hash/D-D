"""Transactional QA-only native Tile create/update/reconciliation for v0.2 chunks.

The previously verified import_chunks_v02.py remains the default create-only
implementation. This opt-in helper supports exact native no-op, update and
rollback of tagged, exclusively importer-owned QA Tiles. It never writes to
the accepted scene, vendor modules or user Blender sources.

Only managed fields are updated; unrelated Foundry Tile metadata is preserved.
Rollback journal is stored on the local GM disk BEFORE writes and checkpointed
after each successful operation. On ambiguous connectivity, inspect journal and
STOP rather than attempting uncontrolled retries.
"""
from __future__ import annotations
import argparse
import copy
import json
import math
import os
import pathlib
import sys
import tempfile
from import_chunks_v02 import (QA_SCENE,PROTECTED_SCENE,PROTECTED_SHA,
      QA_BASELINE_SHA,verify,native_candidates,call)

CLASSIFICATION="QA_ONLY_MULTICHUNK_V02"
SCALAR=("x","y","width","height","elevation","rotation")
ALLOWED_FLAGS=frozenset({
 "model3d","material","color","scale","collision","sight","cameraCollision",
 "doorType","doorState","doorStyle","doorAnimationDuration","doorAnimateAngle",
 "doorSlidePercent","imageTexture","fillType","castShadow"})
METADATA_SCOPE="flags.acq.provenance"

def scene_guard():
    _,q=call(QA_SCENE,{"op":"manage_vision_qa_scene","action":"inspect"},True,timeout=65)
    safe=(q.get("source_scene_id")==PROTECTED_SCENE and
          q.get("source_revision")==PROTECTED_SHA and
          q.get("foundry_active_scene_id")==PROTECTED_SCENE and
          q.get("gm_viewed_scene_id")==QA_SCENE and
          q.get("qa_scene_id")==QA_SCENE and
          q.get("qa_exists") and not q.get("players_pulled"))
    if not safe:raise RuntimeError("Original Scene and GM-only QA ownership guard failed.")
    snap,scene=call(QA_SCENE,{"op":"inspect_3d_scene"},True,timeout=70)
    if snap.get("scene_id")!=QA_SCENE or not scene.get("levels3d_active"):
        raise RuntimeError("QA renderer not active in GM-only clone.")
    return snap,scene

def prepare_plan(doc,rows,candidates,scene,offset_x=0,offset_y=0):
    tile_list=scene.get("tiles") or []
    if len(tile_list)!=len({t["id"] for t in tile_list}):
        raise RuntimeError("Native inspector returned duplicate Tile IDs.")
    plan=[]
    for row,candidate in zip(rows,candidates):
        sid=row["semantic_id"]
        matches=[t for t in tile_list if t.get("acq",{}).get("semantic_id")==sid]
        if len(matches)>1:raise RuntimeError("Duplicate owned semantic id: "+sid)
        expected=copy.deepcopy(candidate)
        expected["x"]+=offset_x
        expected["y"]+=offset_y
        proposed3d=expected.get("flags",{}).get("levels-3d-preview",{})
        relevant={k:v for k,v in proposed3d.items() if k in ALLOWED_FLAGS}
        if "model3d" not in relevant:
            raise RuntimeError("No native 3D asset in candidate.")
        if len(matches)==0:
            plan.append({"action":"create","semantic_id":sid,"row":row,
                         "desired":expected,"expected_flags":relevant})
            continue
        old=matches[0]
        acq=old.get("acq") or {}
        if (acq.get("semantic_id")!=sid or
            acq.get("classification")!=CLASSIFICATION or
            acq.get("build_id")!=doc["bundle"] or
            (acq.get("provenance") or {}).get("source")!=doc["source_blend"]):
            raise RuntimeError("Refuse update of unowned/modified Tile: "+sid)
        oldflags=old.get("flags") or {}
        missing=[k for k in relevant if k not in oldflags]
        if missing:raise RuntimeError("Native inspector cannot safely snapshot managed flag(s) "+repr(missing))
        if old.get("runtime_bounds") is None:
            raise RuntimeError("Cannot update unloaded real GLB Tile: "+sid)
        target_acq={"asset_sha256":row["glb_sha256"],"source":doc["source_blend"]}
        if acq.get("provenance") is None:
            raise RuntimeError("Unprovenanced QA Tile: "+sid)
        scalar_delta={k:expected[k] for k in SCALAR
                      if k in expected and not numerically_equal(old.get(k),expected[k])}
        flag_delta={k:v for k,v in relevant.items()
                    if not numerically_equal(oldflags.get(k),v)}
        prov_delta=acq["provenance"]!=target_acq
        backup={"id":old["id"],"semantic_id":sid,
                "scalars":{k:old[k] for k in scalar_delta},
                "flags":{k:oldflags[k] for k in flag_delta},
                "provenance":copy.deepcopy(acq.get("provenance")) if prov_delta else None}
        plan.append({"action":"update" if scalar_delta or flag_delta or prov_delta else "noop",
             "semantic_id":sid,"row":row,"desired":expected,
             "expected_flags":relevant,"old":old,"backup":backup,
             "changes":{"scalars":scalar_delta,"flags":flag_delta,
                        "provenance":target_acq if prov_delta else None}})
    return plan

def numerically_equal(a,b):
    if isinstance(a,bool) or isinstance(b,bool):
        return a is b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):
        return math.isfinite(a) and math.isfinite(b) and abs(a-b)<=1e-7
    return a==b

def update_payload(tileid,scalars,flags,provenance):
    data={"_id":tileid}
    data.update(scalars)
    for name,val in flags.items():
        if name not in ALLOWED_FLAGS:raise RuntimeError("Unexpected mutable flag.")
        data["flags.levels-3d-preview."+name]=val
    if provenance is not None:
        data[METADATA_SCOPE]=provenance
    return data

def stage_log(file,payload):
    file.parent.mkdir(parents=True,exist_ok=True)
    if file.exists():
        raise RuntimeError("Transaction journal exists; inspect prior run before writing.")
    tmp=file.with_suffix(file.suffix+".pending")
    with tmp.open("x",encoding="utf8") as f:
        json.dump(payload,f,indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp,file)

def checkpoint_log(file,payload):
    tmp=file.with_suffix(file.suffix+".pending")
    with tmp.open("w",encoding="utf8") as f:
        json.dump(payload,f,indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp,file)

def check_tiles(plan,scene):
    tiles=scene.get("tiles") or []
    for item in plan:
        match=[t for t in tiles
               if t.get("acq",{}).get("semantic_id")==item["semantic_id"]]
        if len(match)!=1:raise RuntimeError("Expected one managed Tile for "+item["semantic_id"])
        tile=match[0]
        if not tile.get("runtime_bounds"):
            raise RuntimeError("Native model not loaded: "+item["semantic_id"])
        expected=item["desired"]
        for k in SCALAR:
            if k in expected and not numerically_equal(tile.get(k),expected[k]):
                raise RuntimeError("Tile managed scalar mismatch "+item["semantic_id"]+" "+k)
        for k,v in item["expected_flags"].items():
            if not numerically_equal((tile.get("flags") or {}).get(k),v):
                raise RuntimeError("Native Tile flag mismatch "+item["semantic_id"]+" "+k)
        if (tile.get("acq") or {}).get("provenance") != {
                "asset_sha256":item["row"]["glb_sha256"],
                "source":item["source_blend"]}:
            raise RuntimeError("QA provenance mismatch: "+item["semantic_id"])
    return True

def rollback(log,scene_revision):
    # Reverse ONLY successfully recorded first-party owned operations, never
    # unrelated QA or campaign Tiles.
    trace=[]
    for entry in reversed(log["completed"]):
        if entry["action"]=="create":
            op={"op":"delete_semantic_objects",
                "semantic_ids":[entry["semantic_id"]]}
        elif entry["action"]=="update":
            b=entry["backup"]
            op={"op":"embedded_update","document":"Tile",
                "updates":[update_payload(b["id"],b["scalars"],b["flags"],
                                            b["provenance"])]}
        else:
            continue
        response,done=call(QA_SCENE,op,False,scene_revision,80)
        scene_revision=response["after_revision"]
        trace.append({"semantic_id":entry["semantic_id"],"action":entry["action"],
                      "return_revision":scene_revision,"result":done.get("ok")})
    return trace,scene_revision

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bundle-dir",type=pathlib.Path,required=True)
    p.add_argument("--asset-root",type=pathlib.Path,required=True)
    p.add_argument("--journal",type=pathlib.Path,required=True)
    p.add_argument("--apply",action="store_true")
    p.add_argument("--offset-x-px",type=int,default=0)
    p.add_argument("--offset-y-px",type=int,default=0)
    p.add_argument("--qa-inject-failure-after",type=int,default=0,
                   help="Test-only fail after N successful writes, proving rollback.")
    a=p.parse_args()
    if any(abs(v)>10 for v in (a.offset_x_px,a.offset_y_px)):
        raise RuntimeError("QA importer bounded placement adjustment is ±10px.")
    if a.qa_inject_failure_after and not a.apply:
        raise RuntimeError("Fault injection requires apply.")
    if a.qa_inject_failure_after not in (0,1):
        raise RuntimeError("One deliberately bounded fault injection allowed.")
    doc,rows=verify(a.bundle_dir,a.asset_root)
    prior,scene=scene_guard()
    candidates=native_candidates(rows,doc,prior["after_revision"])
    plan=prepare_plan(doc,rows,candidates,scene,a.offset_x_px,a.offset_y_px)
    for item in plan:item["source_blend"]=doc["source_blend"]
    counts={a:sum(it["action"]==a for it in plan) for a in ("create","update","noop")}
    if not a.apply:
        return {"ok":True,"phase":"PREFLIGHT_ONLY","counts":counts,
                "original_revision":prior["after_revision"],
                "scene_changed":False}
    if counts["create"]+counts["update"]==0:
        return {"ok":True,"phase":"IDENTICAL_NOOP",
                "counts":counts,"original_revision":prior["after_revision"],
                "final_revision":prior["after_revision"],"scene_changed":False}
    journal=a.journal.resolve()
    log={"version":"v0.2-update-transaction",
         "source_scene":PROTECTED_SCENE,"qa_scene":QA_SCENE,
         "source_revision":PROTECTED_SHA,
         "before_revision":prior["after_revision"],
         "bundle_sha":doc["source_blend_sha256"],
         "owned_semantics":[x["semantic_id"] for x in plan],
         "status":"IN_PROGRESS","completed":[],"pending":None}
    stage_log(journal,log)
    rev=prior["after_revision"]
    try:
        write_count=0
        for item in plan:
            if item["action"]=="noop":continue
            log["pending"]={"action":item["action"],
                            "semantic_id":item["semantic_id"],
                            "backup":item.get("backup"),
                            "expected_revision":rev}
            checkpoint_log(journal,log)
            if item["action"]=="create":
                row=item["row"]
                document={"document":"Tile","semantic_id":item["semantic_id"],
                     "build_id":doc["bundle"],"classification":CLASSIFICATION,
                     "provenance":{"asset_sha256":row["glb_sha256"],
                                   "source":doc["source_blend"]},
                     "data":item["desired"]}
                op={"op":"apply_semantic_objects","build_id":doc["bundle"],
                    "objects":[document]}
            else:
                c=item["changes"]
                op={"op":"embedded_update","document":"Tile",
                    "updates":[update_payload(item["old"]["id"],c["scalars"],
                                              c["flags"],c["provenance"])]}
            result,done=call(QA_SCENE,op,False,rev,100)
            rev=result["after_revision"]
            if item["action"]=="create":
                ids=[x.get("id") for x in done.get("created") or []]
                if len(ids)!=1 or not ids[0]:
                    raise RuntimeError("Null/ambiguous native Tile create ID.")
            completed={"action":item["action"],"semantic_id":item["semantic_id"],
                       "backup":item.get("backup"),"after_revision":rev}
            log["completed"].append(completed)
            log["pending"]=None
            checkpoint_log(journal,log)
            write_count+=1
            if write_count==a.qa_inject_failure_after:
                raise RuntimeError("INTENTIONAL_QA_INJECTED_FAILURE_AFTER_1")
        end,s=scene_guard()
        check_tiles(plan,s)
        rev=end["after_revision"]
        log["status"]="VERIFIED_APPLIED"
        log["final_revision"]=rev
        checkpoint_log(journal,log)
        return {"ok":True,"phase":"NATIVE_RECONCILED","counts":counts,
           "before_revision":prior["after_revision"],"final_revision":rev,
           "journal":str(journal)}
    except Exception as problem:
        # NEVER make an unbounded retry following an ambiguous command/timeout.
        if log["pending"] is not None:
            log["status"]="STOP_AMBIGUOUS_PENDING_WRITE"
            log["failure"]=str(problem)
            checkpoint_log(journal,log)
            raise RuntimeError("Pending write outcome unknown; NO auto rollback: "+
                               str(problem)) from problem
        try:
            trace,last=rollback(log,rev)
            after,_=scene_guard()
            if after["after_revision"]!=prior["after_revision"]:
                raise RuntimeError("Rollback scene revision mismatch: "+
                                   after["after_revision"])
            log["status"]="ROLLBACK_VERIFIED"
            log["rollback_trace"]=trace
            log["final_revision"]=after["after_revision"]
            log["failure"]=str(problem)
            checkpoint_log(journal,log)
            return {"ok":False,"phase":"ROLLBACK_VERIFIED",
                    "cause":str(problem),"counts":counts,
                    "rollback_ops":len(trace),
                    "restored_revision":after["after_revision"],
                    "journal":str(journal)}
        except Exception as rollback_error:
            log["status"]="STOP_ROLLBACK_UNVERIFIED"
            log["failure"]=str(problem)
            log["rollback_error"]=str(rollback_error)
            checkpoint_log(journal,log)
            raise RuntimeError("Rollback incomplete; STOP: "+str(rollback_error)) from rollback_error

if __name__=="__main__":
    try:print(json.dumps(main(),indent=2))
    except Exception as error:
        print(json.dumps({"ok":False,"error":str(error)}),file=sys.stderr)
        sys.exit(1)
