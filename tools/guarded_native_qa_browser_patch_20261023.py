#!/usr/bin/env python3
"""Guarded first-party browser QA fixes ONLY; dry-run default, one rollback.

Updates ONLY acq-foundry-bridge/scripts/acq-foundry-bridge.js.
No 3D Canvas vendor edits, no D&D5e/game settings, no Scene writes.
Native first-party GM browser needs an independently guarded reload afterwards.
"""
from __future__ import annotations
import argparse,datetime as dt,hashlib,json,os,pathlib,subprocess,urllib.request

OLD_SHA="a0085c1f437c5da57feb5bd9e8554803f80226ca5ff7d6cf341bb689745bf443"
NEW_SHA="1d36a6e9aed966dec64e54811a8909317cd6b6be2b9fd906451f3ee4cd8c29ba"
SOURCE_SCENE="NUEDEFAULTSCENE0"
SOURCE_SHA="e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f"

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def locations():
    home=pathlib.Path.home()
    return (
      home/"AppData/Local/FoundryVTT/Data/modules/acq-foundry-bridge/scripts/acq-foundry-bridge.js",
      home/"Acq3DDeployAgent/staging/native-qa-20261023-acq-foundry-bridge.js",
      home/"Acq3DDeployAgent/backups",
      pathlib.Path(r"G:\My Drive\D&D\Foundry Bridge\state\current_scene.json")
    )

def preflight():
    target,candidate,backups,snapshot=locations()
    if target.name!="acq-foundry-bridge.js" or target.parent.name!="scripts":
        raise RuntimeError("STOP: unexpected vendor/target path")
    if not backups.is_dir() or not candidate.is_file():raise RuntimeError("STOP: backup/staging absent")
    old=target.read_bytes();new=candidate.read_bytes()
    if sha(old)!=OLD_SHA or sha(new)!=NEW_SHA:raise RuntimeError("STOP: source hash mismatch")
    ck=subprocess.run(["node","--check",str(candidate)],capture_output=True,text=True,timeout=10)
    if ck.returncode:raise RuntimeError("STOP: candidate syntax invalid")
    scene=json.loads(snapshot.read_text(encoding="utf8"))
    if scene.get("scene_id")!=SOURCE_SCENE or scene.get("revision")!=SOURCE_SHA:
        raise RuntimeError("STOP: accepted source Scene is not baseline")
    with urllib.request.urlopen("http://127.0.0.1:18747/health",timeout=3) as r:
        health=json.loads(r.read())
    if not health.get("ok"):raise RuntimeError("STOP: Bridge agent unhealthy")
    status=health.get("status",{})
    if any(status.get(k) for k in ("queued","rpc_queued","inflight")):
        raise RuntimeError("STOP: Bridge command queue nonempty")
    if not status.get("browser_poll",{}).get("recent_within_10s"):
        raise RuntimeError("STOP: native GM browser not polling recently")
    return dict(target=target,old=old,new=new,backups=backups)

def replace_checked(target: pathlib.Path,data: bytes,pin: str):
    tmp=target.with_suffix(".acq-qa-stage.tmp")
    if tmp.exists():raise RuntimeError("STOP: stale first-party temp file")
    try:
        tmp.write_bytes(data)
        if sha(tmp.read_bytes())!=pin:raise RuntimeError("STOP: temp checksum mismatch")
        os.replace(tmp,target)
    finally:tmp.unlink(missing_ok=True)

def verify_served():
    url="http://127.0.0.1:30000/modules/acq-foundry-bridge/scripts/acq-foundry-bridge.js"
    req=urllib.request.Request(url,headers={"Cache-Control":"no-cache"})
    with urllib.request.urlopen(req,timeout=6) as r:
        if r.status!=200:return False
        return sha(r.read())==NEW_SHA

def deploy(apply=False,allow_deploy=False):
    before=preflight()
    if not apply:return {"status":"DRY_RUN_PASS","installed_sha":OLD_SHA,"candidate_sha":NEW_SHA}
    if not allow_deploy:raise PermissionError("Explicit --allow-deploy required")
    checkpoint=before["backups"]/("qa-native-surface-and-gamecamera-"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    checkpoint.mkdir(mode=0o700,exist_ok=False)
    old=before["old"];target=before["target"]
    (checkpoint/"acq-foundry-bridge.js.before").write_bytes(old)
    (checkpoint/"manifest.json").write_text(json.dumps({"old_sha":OLD_SHA,"new_sha":NEW_SHA,"source_scene":SOURCE_SCENE,"source_revision":SOURCE_SHA},indent=2),encoding="utf8")
    if sha((checkpoint/"acq-foundry-bridge.js.before").read_bytes())!=OLD_SHA:
        raise RuntimeError("STOP: backup unreadable")
    changed=False
    try:
        replace_checked(target,before["new"],NEW_SHA)
        changed=True
        if sha(target.read_bytes())!=NEW_SHA or not verify_served():
            raise RuntimeError("Installed/HTTP-served browser JS did not match approved candidate")
        return {"status":"INSTALLED_AND_HTTP_VERIFIED","backup":str(checkpoint),"sha":NEW_SHA,"browser_reload_required":True,"scene_untouched":True}
    except Exception as failure:
        if not changed:raise
        try:
            replace_checked(target,old,OLD_SHA)
            if sha(target.read_bytes())!=OLD_SHA:raise RuntimeError("Rollback SHA incorrect")
            raise RuntimeError(f"QA JS upgrade failed; original file restored and checksum verified: {failure}")
        except Exception as rollback:
            raise RuntimeError(f"STOP: deployment failure {failure}, rollback outcome {rollback}, checkpoint {checkpoint}") from rollback

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--apply",action="store_true")
    p.add_argument("--allow-deploy",action="store_true")
    x=p.parse_args()
    print(json.dumps(deploy(x.apply,x.allow_deploy),indent=2))
if __name__=="__main__":main()
