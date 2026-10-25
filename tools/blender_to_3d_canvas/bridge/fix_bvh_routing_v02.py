"""First-party bridge hotfix: route read-only BVH QA via accepted active Scene envelope.

The bridge polls commands only for the ACTIVE original Scene; the GM may VIEW
an inactive QA Scene, but the command envelope MUST target the active Scene.
Resolve explicitly tagged QA id from op.qa_scene_id before delegating to
inspectEmptyQaNativePlayability, which enforces full GM/Scene/provenance guards.

Exact installed checksum, immutable backup, JS syntax check, atomic write.
No Foundry Scene, vendor module, global setting or asset writes.
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

BEFORE_SHA="75746a7de10b0721bba60f4749960390b06da40286ce84df1735fec841ac57d0"
OLD='''    const result=await inspectEmptyQaNativePlayability(scene,{
      game,canvas,sourceRevision,l3d:levels3d(),THREE:await getThreeModule()
    });'''
NEW='''    // The command envelope is pinned to the active accepted Scene. Native GM
    // viewing an inactive QA Scene does NOT activate it for players.
    const qa=game.scenes?.get(String(op.qa_scene_id ?? ""));
    if (!qa || qa.id===source.id)
      throw new Error("Explicit non-source QA Scene ID is required.");
    const result=await inspectEmptyQaNativePlayability(qa,{
      game,canvas,sourceRevision,l3d:levels3d(),THREE:await getThreeModule()
    });'''

def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bridge",required=True,type=pathlib.Path)
    p.add_argument("--backup-dir",required=True,type=pathlib.Path)
    p.add_argument("--apply",action="store_true")
    a=p.parse_args()
    bridge=a.bridge.resolve(strict=True);backup=a.backup_dir.resolve()
    if backup.exists():raise RuntimeError("Immutable backup already exists; STOP.")
    original=bridge.read_bytes()
    if sha(original)!=BEFORE_SHA:raise RuntimeError("First-party bridge SHA drift; STOP.")
    text=original.decode("utf8")
    if text.count(OLD)!=1:raise RuntimeError("BVH dispatcher exact-match anchor missing.")
    candidate=text.replace(OLD,NEW,1).encode("utf8")
    node=shutil.which("node")
    if not node:raise RuntimeError("Node required for syntax verification.")
    with tempfile.TemporaryDirectory() as td:
        tmp=pathlib.Path(td)/"acq-foundry-bridge.mjs"
        tmp.write_bytes(candidate)
        r=subprocess.run([node,"--check",str(tmp)],capture_output=True,text=True,timeout=20)
        if r.returncode:raise RuntimeError("Native JS syntax failed: "+r.stderr[-500:])
    expected=sha(candidate)
    out={"ok":True,"phase":"OFFLINE_PRECHECK",
         "source_sha":BEFORE_SHA,"target_sha":expected,
         "scene_writes":False,"vendor_edits":False}
    if not a.apply:return out
    backup.mkdir(parents=True,exist_ok=False)
    shutil.copy2(bridge,backup/"acq-foundry-bridge.js.before")
    if sha(bridge.read_bytes())!=BEFORE_SHA:raise RuntimeError("Source drifted after backup; STOP.")
    temp=bridge.with_suffix(".js.routing-stage")
    try:
        temp.write_bytes(candidate)
        if sha(temp.read_bytes())!=expected:raise RuntimeError("Staged candidate SHA mismatch.")
        os.replace(temp,bridge)
    finally:
        if temp.exists():temp.unlink()
    if sha(bridge.read_bytes())!=expected:raise RuntimeError("Installed SHA check failed.")
    return {**out,"phase":"INSTALLED_AWAITING_GM_CLIENT_RELOAD"}

if __name__=="__main__":
    try:print(json.dumps(main(),indent=2))
    except Exception as e:
        print(json.dumps({"ok":False,"error":str(e)}))
        raise SystemExit(1)
