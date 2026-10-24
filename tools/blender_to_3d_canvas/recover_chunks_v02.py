"""Fail-closed recovery of a v0.2 importer journal after unknown RPC acknowledgment.

Only for the original inactive GM-owned QA clone, with pinned source hash.
It inspects the current native Foundry documents BEFORE deciding whether an
unacknowledged Tile create/update executed. No blind replay of the write.
Journal remains locally durable and records each recovery step.
"""
from __future__ import annotations
import argparse
import copy
import json
import pathlib
import sys

from reconcile_chunks_v02 import (scene_guard, checkpoint_log, update_payload,
        numerically_equal, SCALAR, CLASSIFICATION, QA_SCENE, PROTECTED_SCENE,
        PROTECTED_SHA, call)

STATES={"STOP_AMBIGUOUS_PENDING_WRITE","RECOVERY_IN_PROGRESS",
        "STOP_RECOVERY_UNVERIFIED"}
FIELDS=("id","x","y","width","height","elevation","rotation","hidden","flags","acq")

def compact(t):
    return {k:copy.deepcopy(t.get(k)) for k in FIELDS}

def same(a,b):
    if isinstance(a,dict) and isinstance(b,dict):
        return (a.keys()==b.keys() and
                all(same(a[k],b[k]) for k in a.keys()))
    if isinstance(a,list) and isinstance(b,list):
        return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return numerically_equal(a,b)

def getmatch(tiles,entry):
    found=[t for t in tiles if (t.get("acq") or {}).get("semantic_id")==entry["semantic_id"]]
    if len(found)>1:raise RuntimeError("Duplicate semantic ID; refuse recovery.")
    return found[0] if found else None

def entry_state(entry,current,baseline):
    """BEFORE/APPLIED; otherwise raise instead of guessing partial updates."""
    action=entry["action"]
    wanted=entry["desired_managed"]
    if action=="create":
        if current is None:return "BEFORE"
        acq=current.get("acq") or {}
        if (acq.get("classification")!=CLASSIFICATION or
            acq.get("build_id")!=wanted["build_id"] or
            acq.get("provenance")!=wanted["provenance"]):
            raise RuntimeError("Untrusted created Tile ownership/provenance.")
        if any(not same(current.get(k),v) for k,v in wanted["scalars"].items()):
            raise RuntimeError("Created Tile dimensions/placement unexpected.")
        if any(not same((current.get("flags") or {}).get(k),v)
               for k,v in wanted["flags"].items()):
            raise RuntimeError("Created Tile native flags unexpected.")
        if not current.get("runtime_bounds"):
            raise RuntimeError("Created Tile runtime model has not loaded.")
        return "APPLIED"
    if action!="update" or not entry.get("backup"):
        raise RuntimeError("Unknown journal action/snapshot.")
    if current is None or baseline is None:
        raise RuntimeError("Missing pre-existing Tile during update recovery.")
    if current["id"]!=entry["backup"]["id"] or current["id"]!=baseline["id"]:
        raise RuntimeError("Tile ID drifted during recovery.")
    backup=entry["backup"]
    tests=[]
    for k,b in backup["scalars"].items():
        tests.append((same(current.get(k),b),
                      same(current.get(k),wanted["scalars"][k])))
    for k,b in backup["flags"].items():
        tests.append((same((current.get("flags") or {}).get(k),b),
                      same((current.get("flags") or {}).get(k),wanted["flags"][k])))
    if backup["provenance"] is not None:
        tests.append((same((current.get("acq") or {}).get("provenance"),backup["provenance"]),
                      same((current.get("acq") or {}).get("provenance"),wanted["provenance"])))
    if not tests:raise RuntimeError("No recorded changed managed fields.")
    if all(a for a,_ in tests):return "BEFORE"
    if all(b for _,b in tests):return "APPLIED"
    raise RuntimeError("Partial or externally changed Tile update; cannot classify safely.")

def assert_exclusive_inventory(log,scene):
    base=log["baseline_inventory"]
    if any(scene.get(key)!=base.get(key) for key in ("light_count","region_count")):
        raise RuntimeError("Non-Tile scene document counts changed.")
    old={t["id"]:t for t in base["tiles"]}
    current={t["id"]:t for t in scene["tiles"]}
    if len(old)!=len(base["tiles"]) or len(current)!=len(scene["tiles"]):
        raise RuntimeError("Duplicate Tile document IDs.")
    allowed=set(log["owned_semantics"])
    owned_current=[t for t in scene["tiles"]
                   if (t.get("acq") or {}).get("semantic_id") in allowed]
    new_ids=set(current)-set(old)
    if any(current[i] not in owned_current for i in new_ids):
        raise RuntimeError("Foreign Tile created since pre-write snapshot.")
    if any(i not in current for i in old):
        raise RuntimeError("Source QA Tile deleted since pre-write snapshot.")
    for i,original in old.items():
        now=current[i]
        sid=(original.get("acq") or {}).get("semantic_id")
        if sid not in allowed and not same(compact(now),compact(original)):
            raise RuntimeError("Unrelated QA Tile changed during pending RPC.")
        if sid in allowed:
            if original.get("hidden")!=now.get("hidden"):
                raise RuntimeError("Owned Tile visibility changed unexpectedly.")
            if (original.get("acq") or {}).get("classification")!=(now.get("acq") or {}).get("classification"):
                raise RuntimeError("Owned Tile classification changed unexpectedly.")
            if (original.get("acq") or {}).get("build_id")!=(now.get("acq") or {}).get("build_id"):
                raise RuntimeError("Owned Tile build ID changed unexpectedly.")
            # Only fields explicitly touched in the journal may differ.
            entries=[e for e in log["completed"]+[log["pending"]]
                     if e is not None and e["semantic_id"]==sid]
            keys=set()
            for e in entries:
                if e["action"]=="update":
                    b=e["backup"]
                    keys.update(b["scalars"])
            for key in ("x","y","width","height","elevation","rotation"):
                if key not in keys and not same(original.get(key),now.get(key)):
                    raise RuntimeError("Unmanaged source placement changed.")
            changed_flags=set()
            for e in entries:
                if e["action"]=="update":changed_flags.update(e["backup"]["flags"])
            a=original.get("flags") or {}
            b=now.get("flags") or {}
            if any(not same(a.get(k),b.get(k))
                   for k in set(a)|set(b) if k not in changed_flags):
                raise RuntimeError("Unmanaged native Tile flag changed.")
    return True

def assess(log,scene):
    assert_exclusive_inventory(log,scene)
    originals={((t.get("acq") or {}).get("semantic_id")):t
               for t in log["baseline_inventory"]["tiles"]}
    entries=list(log["completed"])
    if log.get("pending") is not None:entries.append(log["pending"])
    seen=set()
    status=[]
    for entry in entries:
        sid=entry["semantic_id"]
        if sid in seen:raise RuntimeError("Multiple journal operations for same Tile.")
        seen.add(sid)
        live=getmatch(scene["tiles"],entry)
        state=entry_state(entry,live,originals.get(sid))
        status.append({"entry":entry,"state":state})
    return status

def recover(journal,dry_run=False):
    path=pathlib.Path(journal).resolve(strict=True)
    log=json.loads(path.read_text(encoding="utf8"))
    if (log.get("version")!="v0.2-update-transaction" or
        log.get("status") not in STATES or
        log.get("source_scene")!=PROTECTED_SCENE or
        log.get("qa_scene")!=QA_SCENE or
        log.get("source_revision")!=PROTECTED_SHA or
        not log.get("baseline_inventory") or
        not log.get("pending")):
        raise RuntimeError("Unknown, completed or non-recoverable journal; refuse.")
    before,scene=scene_guard()
    states=assess(log,scene)
    plans=[{"semantic_id":q["entry"]["semantic_id"],
            "action":q["entry"]["action"],"state":q["state"]} for q in states]
    if dry_run:return {"ok":True,"phase":"RECOVERY_ASSESSMENT_ONLY",
                       "before_revision":before["after_revision"],"observed":plans}
    rev=before["after_revision"]
    log["status"]="RECOVERY_IN_PROGRESS"
    log["recovery_plan"]=plans
    checkpoint_log(path,log)
    try:
        actions=0
        for item in reversed(states):
            entry=item["entry"]
            # Reinspect on each iteration to allow safe, crash-resumable recovery.
            current,scene=scene_guard()
            assert_exclusive_inventory(log,scene)
            originals={((t.get("acq") or {}).get("semantic_id")):t
                       for t in log["baseline_inventory"]["tiles"]}
            state=entry_state(entry,getmatch(scene["tiles"],entry),
                              originals.get(entry["semantic_id"]))
            if state=="BEFORE":continue
            if entry["action"]=="create":
                op={"op":"delete_semantic_objects",
                    "semantic_ids":[entry["semantic_id"]]}
            else:
                b=entry["backup"]
                op={"op":"embedded_update","document":"Tile",
                    "updates":[update_payload(b["id"],b["scalars"],
                                              b["flags"],b["provenance"])]}
            log["recovery_pending"]=entry["semantic_id"]
            checkpoint_log(path,log)
            r,done=call(QA_SCENE,op,False,current["after_revision"],90)
            log.setdefault("recovery_steps",[]).append({
                "semantic_id":entry["semantic_id"],"action":entry["action"],
                "revision":r["after_revision"]})
            log["recovery_pending"]=None
            checkpoint_log(path,log)
            actions+=1
        end,scene=scene_guard()
        baseline=log["baseline_inventory"]
        if (end["after_revision"]!=log["before_revision"] or
            not all(same(compact(a),compact(b))
                    for a,b in zip(sorted(scene["tiles"],key=lambda x:x["id"]),
                                   sorted(baseline["tiles"],key=lambda x:x["id"])))):
            raise RuntimeError("Recovery did not restore exact QA baseline.")
        log["status"]="RECOVERY_VERIFIED"
        log["final_revision"]=end["after_revision"]
        checkpoint_log(path,log)
        return {"ok":True,"phase":"RECOVERY_VERIFIED",
                "reversed_native_writes":actions,
                "restored_revision":end["after_revision"],
                "observed_before":plans,"journal":str(path)}
    except Exception as e:
        log["status"]="STOP_RECOVERY_UNVERIFIED"
        log["recovery_error"]=str(e)
        checkpoint_log(path,log)
        raise

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--journal",required=True,type=pathlib.Path)
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args()
    try:print(json.dumps(recover(args.journal,not args.apply),indent=2))
    except Exception as e:
        print(json.dumps({"ok":False,"error":str(e)}),file=sys.stderr)
        sys.exit(1)
