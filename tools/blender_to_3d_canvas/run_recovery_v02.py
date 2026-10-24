"""Single-command safe recovery for the pinned GM-only native importer QA clone.

Example:
  python run_recovery_v02.py --journal EXISTING.json [--apply]

No source Blender export, vendor edits, or campaign Scene writes. This
wrapper restores the original GM view even when recovery fails, and never
pulls players to the QA clone. It doesn't certify arbitrary production
Scene recovery.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import subprocess
import sys
from import_chunks_v02 import call, QA_SCENE, PROTECTED_SCENE, PROTECTED_SHA

def execute(journal,apply):
    path=pathlib.Path(journal).resolve(strict=True)
    record=json.loads(path.read_text(encoding="utf8"))
    if (record.get("version")!="v0.2-update-transaction"
        or record.get("source_scene")!=PROTECTED_SCENE
        or record.get("qa_scene")!=QA_SCENE
        or record.get("source_revision")!=PROTECTED_SHA
        or record.get("status") not in (
            "STOP_AMBIGUOUS_PENDING_WRITE","RECOVERY_IN_PROGRESS",
            "STOP_RECOVERY_UNVERIFIED")):
        raise RuntimeError("Untrusted or already completed recovery journal.")
    initial,_=call(PROTECTED_SCENE,{"op":"inspect_3d_scene"},True,timeout=70)
    if initial.get("after_revision")!=PROTECTED_SHA:
        raise RuntimeError("Accepted source Scene revision drift.")
    switched=False
    failure=None
    result=None
    returned=False
    try:
        _,view=call(PROTECTED_SCENE,{"op":"manage_vision_qa_scene",
                "action":"view","qa_scene_id":QA_SCENE},False,timeout=75)
        if view.get("now_viewed")!=QA_SCENE or view.get("players_pulled"):
            raise RuntimeError("GM-only QA view guard failed.")
        switched=True
        _,renderer=call(QA_SCENE,{"op":"capture_3d_view","format":"webp",
                 "quality":0.3,"restore_camera":True},False,timeout=105)
        if not renderer.get("image_base64"):
            raise RuntimeError("Native 3D Canvas did not render.")
        args=[sys.executable,
              str(pathlib.Path(__file__).with_name("recover_chunks_v02.py")),
              "--journal",str(path)]
        if apply:args.append("--apply")
        proc=subprocess.run(args,capture_output=True,text=True,timeout=350)
        if proc.returncode:
            raise RuntimeError("Recovery refused: "+proc.stderr[-1700:])
        result=json.loads(proc.stdout)
        if not result.get("ok"):
            raise RuntimeError("Recovery did not certify its final status.")
    except Exception as e:
        failure=e
    finally:
        if switched:
            try:
                _,viewback=call(QA_SCENE,{"op":"manage_vision_qa_scene",
                    "action":"restore_view"},False,timeout=75)
                if viewback.get("now_viewed")!=PROTECTED_SCENE or viewback.get("players_pulled"):
                    raise RuntimeError("GM view not safely returned.")
                final,_=call(PROTECTED_SCENE,{"op":"inspect_3d_scene"},True,timeout=75)
                if final.get("after_revision")!=PROTECTED_SHA:
                    raise RuntimeError("Protected source Scene mutated.")
                returned=True
            except Exception as e:
                raise RuntimeError("STOP: GM-view restore UNVERIFIED: "+
                                   str(e)+"; earlier error: "+str(failure)) from e
    if failure is not None:raise failure
    return {"ok":True,"stage":result["phase"],
            "recovery":result,"gm_view_restored":returned,
            "source_scene_unchanged":True,"production_acceptance":False}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--journal",required=True,type=pathlib.Path)
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args()
    try:print(json.dumps(execute(args.journal,args.apply),indent=2))
    except Exception as e:
        print(json.dumps({"ok":False,"error":str(e)}),file=sys.stderr)
        sys.exit(1)
