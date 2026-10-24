"""Backup-first patch for bounded native BVH QA, first-party code ONLY.

Preconditions: pinned checked installed bridge and original native-QA module.
Patch lets operation pass inventory/one-ray args. Replace module with
bounded version after backing up both current exact source files.
"""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,tempfile
BEFORE_BRIDGE="7e8408e4ae4b93d9f41fa9e9a1bd30c624bfbc10f3e3e1a7bc791454c6bbf115"
BEFORE_MODULE="35d3a449e3ef0bb8e36d19a290d2ee083d194170332dc5816a4dea26ad462aef"
NEXT_MODULE="448a46ac65aed1020739155c2512743d374793cc1f01faff32c2d521204d84b3"
OLD='''    const result=await inspectEmptyQaNativePlayability(qa,{
      game,canvas,sourceRevision,l3d:levels3d(),THREE:await getThreeModule()
    });'''
NEW='''    const result=await inspectEmptyQaNativePlayability(qa,{
      game,canvas,sourceRevision,l3d:levels3d(),THREE:await getThreeModule()
    },{
      mode:op.mode,probe_name:op.probe_name,collision_type:op.collision_type
    });'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--bridge-dir",type=pathlib.Path,required=True)
 p.add_argument("--bounded-module",type=pathlib.Path,required=True)
 p.add_argument("--backup-dir",type=pathlib.Path,required=True)
 p.add_argument("--apply",action="store_true")
 a=p.parse_args()
 bridge=(a.bridge_dir/"acq-foundry-bridge.js").resolve(strict=True)
 mod=(a.bridge_dir/"qa-empty-native-playability.mjs").resolve(strict=True)
 new=a.bounded_module.resolve(strict=True)
 backup=a.backup_dir.resolve()
 if backup.exists():raise RuntimeError("Existing backup path; refuse overwrite.")
 if (sha(bridge),sha(mod),sha(new))!=(BEFORE_BRIDGE,BEFORE_MODULE,NEXT_MODULE):
  raise RuntimeError("Installed or candidate source hash drift; STOP.")
 original=bridge.read_text(encoding="utf8")
 if original.count(OLD)!=1:raise RuntimeError("Expected exact dispatch anchor not found.")
 candidate=original.replace(OLD,NEW,1).encode("utf8")
 node=shutil.which("node")
 if not node:raise RuntimeError("Node unavailable.")
 with tempfile.TemporaryDirectory() as td:
  pb=pathlib.Path(td)/"bridge.mjs";pb.write_bytes(candidate)
  for f in (pb,new):
   q=subprocess.run([node,"--check",str(f)],capture_output=True,text=True,timeout=22)
   if q.returncode:raise RuntimeError("JS syntax fail "+q.stderr[-500:])
 expected=hashlib.sha256(candidate).hexdigest()
 result={"ok":True,"phase":"OFFLINE_PRECHECK","new_bridge_sha":expected,
         "new_module_sha":NEXT_MODULE,"vendor_edits":False,"scene_writes":False}
 if not a.apply:return result
 backup.mkdir(parents=True,exist_ok=False)
 shutil.copy2(bridge,backup/"acq-foundry-bridge.js.before")
 shutil.copy2(mod,backup/"qa-empty-native-playability.mjs.before")
 if sha(bridge)!=BEFORE_BRIDGE or sha(mod)!=BEFORE_MODULE:
  raise RuntimeError("Source drift after backup.")
 tmpb=bridge.with_suffix(".js.bounded-stage")
 tmpm=mod.with_suffix(".mjs.bounded-stage")
 try:
  tmpb.write_bytes(candidate);tmpm.write_bytes(new.read_bytes())
  if sha(tmpb)!=expected or sha(tmpm)!=NEXT_MODULE:
   raise RuntimeError("Staged bytes failed checksums.")
  os.replace(tmpm,mod)
  os.replace(tmpb,bridge)
 finally:
  for f in (tmpb,tmpm):
   if f.exists():f.unlink()
 if sha(bridge)!=expected or sha(mod)!=NEXT_MODULE:
  raise RuntimeError("Post-install SHA mismatch; don't reload.")
 result["phase"]="INSTALLED_AWAITING_GM_CLIENT_RELOAD"
 return result
if __name__=="__main__":
 try:print(json.dumps(main(),indent=2))
 except Exception as exc:
  print(json.dumps({"ok":False,"error":str(exc)}))
  raise SystemExit(1)
