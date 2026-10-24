"""Prepare or install ONLY the first-party guarded BVH QA inspector.

Original first-party bridge must match the exact known installed SHA;
no third-party 3D Canvas files or global game settings touched.
Offline dry run validates anchors, JS syntax and source checksums.
--apply creates immutable bridge backup then writes guarded import/dispatch.
A verified GM reload is still required; do not claim the op available until
the browser actually responds. Reconnect using the user's credentials in UI.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import tempfile

INSTALLED_SHA="6147f04f0c8896fee9e91ac074b6a7e794f77bd36a56a86a2e550ee22ed5a158"
ANCHOR='''  if (type === "manage_empty_qa_scene") {
    const source=game.scenes?.get(EMPTY_QA_SOURCE_ID);
    if (!source) throw new Error("Protected Area 8 Scene missing.");
    const sourceRevision=(await sceneSnapshot(source)).revision;
    const result=await manageEmptyQaScene(op,dryRun,{
      game,canvas,sourceRevision,
      revisionOf:async doc=>(await sceneSnapshot(doc)).revision
    });
    return {op:type,ok:true,...result};
  }'''
IMPORT_LINE='import {inspectEmptyQaNativePlayability} from "./qa-empty-native-playability.mjs";'
INSERT='''  if (type === "inspect_empty_qa_native_playability") {
    const source=game.scenes?.get(EMPTY_QA_SOURCE_ID);
    if (!source) throw new Error("Protected Area 8 Scene missing.");
    const sourceRevision=(await sceneSnapshot(source)).revision;
    const result=await inspectEmptyQaNativePlayability(scene,{
      game,canvas,sourceRevision,l3d:levels3d(),THREE:await getThreeModule()
    });
    return {op:type,ok:true,...result};
  }'''

def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def transform(before):
    if before.count(ANCHOR)!=1:
        raise RuntimeError("QA Scene dispatch anchor drift; stop.")
    if IMPORT_LINE in before or INSERT in before:
        raise RuntimeError("BVH probe already installed; refuse duplicate.")
    hook='import {manageEmptyQaScene, SOURCE_SCENE_ID as EMPTY_QA_SOURCE_ID} from "./qa-empty-scene.mjs";'
    if before.count(hook)!=1:raise RuntimeError("Empty QA Scene import is not exactly once.")
    return before.replace(hook,hook+"\n"+IMPORT_LINE,1).replace(ANCHOR,ANCHOR+"\n"+INSERT,1)

def parse_check(node,payload,module):
    with tempfile.TemporaryDirectory() as tmp:
        folder=pathlib.Path(tmp)
        target=folder/"acq-foundry-bridge.mjs"
        imported=folder/"qa-empty-native-playability.mjs"
        target.write_bytes(payload.encode("utf8"))
        imported.write_bytes(module.read_bytes())
        for p in (target,imported):
            r=subprocess.run([node,"--check",str(p)],capture_output=True,text=True,timeout=20)
            if r.returncode:
                raise RuntimeError("Node syntax check failed: "+r.stderr[-1100:])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--bridge-dir",required=True,type=pathlib.Path)
    parser.add_argument("--probe-file",required=True,type=pathlib.Path)
    parser.add_argument("--backup-dir",required=True,type=pathlib.Path)
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args()
    bridge=(args.bridge_dir/"acq-foundry-bridge.js").resolve(strict=True)
    probe=args.probe_file.resolve(strict=True)
    destination=args.bridge_dir/"qa-empty-native-playability.mjs"
    backup=args.backup_dir.resolve()
    if file_sha(bridge)!=INSTALLED_SHA:
        raise RuntimeError("First-party bridge SHA changed, refuse plugin install.")
    if destination.exists() or backup.exists():
        raise RuntimeError("Probe file or backup already exists; refuse overwrite.")
    node=shutil.which("node")
    if not node:raise RuntimeError("Node.js syntax validation unavailable.")
    output=transform(bridge.read_text(encoding="utf8"))
    parse_check(node,output,probe)
    expected=hashlib.sha256(output.encode("utf8")).hexdigest()
    reply={"ok":True,"phase":"OFFLINE_PRECHECK",
           "before_sha":INSTALLED_SHA,"candidate_sha":expected,
           "probe_sha":file_sha(probe),"no_scene_writes":True}
    if not args.apply:return reply
    backup.mkdir(parents=True,exist_ok=False)
    shutil.copy2(bridge,backup/"acq-foundry-bridge.js.before")
    if file_sha(bridge)!=INSTALLED_SHA:
        raise RuntimeError("Bridge changed after backup; STOP.")
    temp_code=bridge.with_suffix(".js.bvh-stage")
    temp_probe=destination.with_suffix(".mjs.bvh-stage")
    try:
        temp_code.write_bytes(output.encode("utf8"))
        temp_probe.write_bytes(probe.read_bytes())
        if file_sha(temp_code)!=expected or file_sha(temp_probe)!=file_sha(probe):
            raise RuntimeError("Staged hashes mismatch.")
        # Write module first; if second replace fails, original JS remains
        # operational but a dormant imported module may remain.
        os.replace(temp_probe,destination)
        os.replace(temp_code,bridge)
    finally:
        for p in (temp_code,temp_probe):
            if p.exists():p.unlink()
    if file_sha(bridge)!=expected or file_sha(destination)!=file_sha(probe):
        raise RuntimeError("Installed first-party probe failed checksum verification; DO NOT RELOAD.")
    reply["phase"]="INSTALLED_AWAITING_AUTHENTICATED_GM_RELOAD"
    return reply

if __name__=="__main__":
    try:print(json.dumps(main(),indent=2))
    except Exception as e:
        print(json.dumps({"ok":False,"error":str(e)}))
        raise SystemExit(1)
