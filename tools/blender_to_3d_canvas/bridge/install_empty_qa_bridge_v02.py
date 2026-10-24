"""Atomic first-party Foundry bridge patch for the source-guarded empty QA Scene.

Offline candidate syntax checks precede any edit; active bridge source SHA is
pinned. Keeps immutable before-file backups. This does NOT restart/reload the
Foundry client and cannot claim live feature availability until reloaded and
tested. Run on Windows: python install_empty_qa_bridge_v02.py
 --bridge-dir MODULE/scripts --qa-module STAGED/qa-empty-scene.mjs
 --backup-dir VERSIONED_LOCAL_BACKUP [--apply]
"""
from __future__ import annotations
import argparse
import hashlib
import os
import pathlib
import shutil
import subprocess
import tempfile

ORIGINAL_SHA="b25a35aa23c53e361222c53ab0518e7e30f2b17f70df3fef861db3b3151cd631"
IMPORT_MARK='import "./fps-camera-anchor.mjs";'
ADDED='import {manageEmptyQaScene, SOURCE_SCENE_ID as EMPTY_QA_SOURCE_ID} from "./qa-empty-scene.mjs";'
ANCHOR='''  if (type === "manage_vision_qa_scene") {
    return {op:type,ok:true,...(await manageVisionQaScene(scene,op,dryRun))};
  }'''
DISPATCH='''  if (type === "manage_empty_qa_scene") {
    const source=game.scenes?.get(EMPTY_QA_SOURCE_ID);
    if (!source) throw new Error("Protected Area 8 Scene missing.");
    const sourceRevision=(await sceneSnapshot(source)).revision;
    const result=await manageEmptyQaScene(op,dryRun,{
      game,canvas,sourceRevision,
      revisionOf:async doc=>(await sceneSnapshot(doc)).revision
    });
    return {op:type,ok:true,...result};
  }'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def get_patch(before):
    if before.count(IMPORT_MARK)!=1 or before.count(ANCHOR)!=1:
        raise RuntimeError("Vendor/version drift in bridge anchors; refuse.")
    if ADDED in before or DISPATCH in before:
        raise RuntimeError("Already patched; refuse non-idempotent write.")
    return (before.replace(IMPORT_MARK,IMPORT_MARK+"\n"+ADDED,1)
                  .replace(ANCHOR,ANCHOR+"\n"+DISPATCH,1))

def verify_syntax(node,content,module):
    with tempfile.TemporaryDirectory() as folder:
        base=pathlib.Path(folder)
        (base/"qa-empty-scene.mjs").write_bytes(module.read_bytes())
        candidate=base/"acq-foundry-bridge.mjs"
        candidate.write_text(content,encoding="utf8")
        for file in (candidate,base/"qa-empty-scene.mjs"):
            p=subprocess.run([node,"--check",str(file)],capture_output=True,text=True,timeout=15)
            if p.returncode:raise RuntimeError("Node syntax check failed: "+p.stderr[-600:])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bridge-dir",type=pathlib.Path,required=True)
    p.add_argument("--qa-module",type=pathlib.Path,required=True)
    p.add_argument("--backup-dir",type=pathlib.Path,required=True)
    p.add_argument("--apply",action="store_true")
    a=p.parse_args()
    bridge=(a.bridge_dir/"acq-foundry-bridge.js").resolve(strict=True)
    module=a.qa_module.resolve(strict=True)
    dest=(a.bridge_dir/"qa-empty-scene.mjs").resolve()
    backup=a.backup_dir.resolve()
    if dest.exists() or backup.exists() or sha(bridge)!=ORIGINAL_SHA:
        raise RuntimeError("Existing QA module, backup path or bridge SHA mismatch. No write.")
    node=shutil.which("node")
    if not node:raise RuntimeError("Node required for offline parse validation.")
    candidate=get_patch(bridge.read_text(encoding="utf8"))
    verify_syntax(node,candidate,module)
    output={"ok":True,"stage":"OFFLINE_VERIFIED","before":sha(bridge),
            "candidate_sha256":hashlib.sha256(candidate.encode()).hexdigest(),
            "module_sha256":sha(module),"source":str(bridge),
            "new_module":str(dest),"backup_dir":str(backup)}
    if not a.apply:return output
    backup.mkdir(parents=True,exist_ok=False)
    shutil.copy2(bridge,backup/"acq-foundry-bridge.js.before")
    if sha(bridge)!=ORIGINAL_SHA:
        raise RuntimeError("Bridge mutated after backup. STOP.")
    # Safe, versioned first-party patch. Installed module is not edited.
    module_tmp=dest.with_suffix(".mjs.qa-pending")
    bridge_tmp=bridge.with_suffix(".js.qa-pending")
    try:
        module_tmp.write_bytes(module.read_bytes())
        bridge_tmp.write_bytes(candidate.encode("utf8"))
        if sha(module_tmp)!=sha(module):
            raise RuntimeError("Module staging checksum mismatch.")
        os.replace(module_tmp,dest)
        os.replace(bridge_tmp,bridge)
    finally:
        for path in (module_tmp,bridge_tmp):
            if path.exists():path.unlink()
    if sha(bridge)!=output["candidate_sha256"] or sha(dest)!=output["module_sha256"]:
        raise RuntimeError("Installed bridge verification FAILED. Do not reload.")
    output["stage"]="LOCAL_INSTALLED_AWAITING_FOUNDRY_RELOAD"
    output["installed_sha256"]=sha(bridge)
    return output

if __name__=="__main__":
    import json
    try:print(json.dumps(main(),indent=2))
    except Exception as error:
        print(json.dumps({"ok":False,"error":str(error)}))
        raise SystemExit(1)
