#!/usr/bin/env python3
"""Guarded first-party bridge long-poll deployment. Dry-run by default.

Do not touch 3D Canvas/Premium, Blender, Foundry world settings, or scene data.
Uses exact code SHA pins, checked source Scene, immutable backup, single rollback.
After install the GM client must reload its own first-party bridge script.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile

from guarded_bridge_agent_heartbeat_upgrade_20261023 import (
    health, processes_and_listener, stop_specific_worker, spawn_agent,
)
from patch_bridge_longpoll_20261023 import patch_agent, patch_browser

JS_OLD = "82cf6f20b10825ca09578d6103ede742174423b8db23956994ad4cd5fae189f1"
JS_NEW = "a0085c1f437c5da57feb5bd9e8554803f80226ca5ff7d6cf341bb689745bf443"
AGENT_OLD = "93edf24c0bcc60f3a3a63fe611b83303fec024fff4f5289194203b23184f49d2"
AGENT_NEW = "a44aeb6ba646b3d99532ab2816fc8007d47101243c0c4fdf3063e9d94f96c2ec"
SCENE_REV = "e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f"

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def target_paths() -> tuple[Path, Path, Path]:
    home=Path.home()
    return (
        home/"Downloads"/"Acq_Foundry_3D_MCP"/"agent"/"acq_bridge_agent.py",
        home/"AppData"/"Local"/"FoundryVTT"/"Data"/"modules"/"acq-foundry-bridge"/"scripts"/"acq-foundry-bridge.js",
        home/"Acq3DDeployAgent"/"backups",
    )

def preflight():
    agent,js,backups=target_paths()
    if agent.name!="acq_bridge_agent.py" or js.name!="acq-foundry-bridge.js":
        raise RuntimeError("Unexpected target")
    olda=agent.read_bytes()
    oldj=js.read_bytes()
    if (sha(olda),sha(oldj)) != (AGENT_OLD,JS_OLD):
        raise RuntimeError("STOP: installed bridge source differs from reviewed pinned baseline")
    newa=patch_agent(olda.decode("utf8")).encode("utf8")
    newj=patch_browser(oldj.decode("utf8")).encode("utf8")
    if (sha(newa),sha(newj)) != (AGENT_NEW,JS_NEW):
        raise RuntimeError("STOP: candidate source SHA differs from reviewed pinned candidate")
    if not backups.is_dir():
        raise RuntimeError("STOP: backup root missing")
    import subprocess
    with tempfile.TemporaryDirectory(prefix="acq_longpoll_node_") as temp:
        p=Path(temp)/"candidate_browser.js"
        p.write_bytes(newj)
        chk=subprocess.run(["node","--check",str(p)],text=True,capture_output=True,timeout=12)
        if chk.returncode:
            raise RuntimeError("STOP: Node JS parse failed: "+chk.stderr[:250])
    s=health()["status"]
    if any(s.get(k) for k in ("queued","rpc_queued","inflight")):
        raise RuntimeError("STOP: agent RPC queue is not empty")
    processes,listeners=processes_and_listener()
    if len(set(listeners))!=1:
        raise RuntimeError("STOP: ambiguous Bridge TCP listener")
    worker_id=int(listeners[0])
    if len([p for p in processes if int(p["pid"])==worker_id])!=1:
        raise RuntimeError("STOP: listener owner is not the pinned first-party agent worker")
    transport=Path(r"G:\My Drive\D&D\Foundry Bridge")
    current=json.loads((transport/"state"/"current_scene.json").read_text(encoding="utf8"))
    if current.get("revision")!=SCENE_REV or current.get("scene_id")!="NUEDEFAULTSCENE0":
        raise RuntimeError("STOP: accepted Scene revision changed")
    return {"ok":True,"status":"PREFLIGHT_PASS","worker_pid":worker_id,
            "agent_old_sha":AGENT_OLD,"agent_new_sha":AGENT_NEW,
            "browser_old_sha":JS_OLD,"browser_new_sha":JS_NEW,
            "source_scene_sha":SCENE_REV,"candidate_agent":newa,
            "candidate_browser":newj,"old_agent":olda,"old_browser":oldj,
            "transport":str(transport)}

def replace_checked(path:Path,data:bytes,expected_sha:str):
    tmp=path.with_suffix(path.suffix+".acqstage")
    try:
        tmp.write_bytes(data)
        if sha(tmp.read_bytes())!=expected_sha:
            raise RuntimeError("Staged checksum mismatch for "+path.name)
        os.replace(tmp,path)
    finally:
        tmp.unlink(missing_ok=True)

def deploy(*,apply:bool,allow_deploy:bool):
    info=preflight()
    if not apply:
        return {k:v for k,v in info.items() if not k.startswith(("candidate_","old_")) and k!="transport"}
    if not allow_deploy:
        raise PermissionError("Explicit --allow-deploy required for first-party file writes")
    agent,js,backup_root=target_paths()
    checkpoint=backup_root/("longpoll-bridge-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    checkpoint.mkdir(exist_ok=False,mode=0o700)
    (checkpoint/"acq_bridge_agent.py.before").write_bytes(info["old_agent"])
    (checkpoint/"acq-foundry-bridge.js.before").write_bytes(info["old_browser"])
    if sha((checkpoint/"acq_bridge_agent.py.before").read_bytes())!=AGENT_OLD or sha((checkpoint/"acq-foundry-bridge.js.before").read_bytes())!=JS_OLD:
        raise RuntimeError("STOP: immutable backup checksum error")
    (checkpoint/"manifest.json").write_text(json.dumps({
        "old_agent_sha":AGENT_OLD,"old_js_sha":JS_OLD,"new_agent_sha":AGENT_NEW,
        "new_js_sha":JS_NEW,"source_scene_revision":SCENE_REV,
        "status":"CHECKPOINTED_BEFORE_DEPLOYMENT",
    },indent=2),encoding="utf8")
    halted=False
    started=None
    try:
        stop_specific_worker(info["worker_pid"])
        halted=True
        replace_checked(agent,info["candidate_agent"],AGENT_NEW)
        replace_checked(js,info["candidate_browser"],JS_NEW)
        new=spawn_agent(agent,info["transport"],checkpoint,"new-longpoll-agent")
        started=new.pid
        import time
        deadline=time.monotonic()+8.0
        observed=None
        while time.monotonic()<deadline:
            try:
                status=health(1)["status"]
                if "active_browser_longpoll_requests" in status:
                    observed=status
                    break
            except Exception:
                pass
            time.sleep(0.25)
        if observed is None:
            raise RuntimeError("New agent did not return long-poll health schema")
        if sha(agent.read_bytes())!=AGENT_NEW or sha(js.read_bytes())!=JS_NEW:
            raise RuntimeError("New source changed after staging")
        scene=json.loads((Path(info["transport"])/"state"/"current_scene.json").read_text(encoding="utf8"))
        if scene.get("revision")!=SCENE_REV:
            raise RuntimeError("Protected Scene state differs")
        return {"ok":True,"status":"FILES_INSTALLED_AGENT_HTTP_PASS_CLIENT_RELOAD_REQUIRED",
                "checkpoint":checkpoint.name,"agent_pid":started,"source_scene_revision":SCENE_REV,
                "active_browser_longpoll_requests":observed["active_browser_longpoll_requests"],
                "browser_js_currently_running":"UNKNOWN_UNTIL_GM_RELOAD"}
    except Exception as e:
        if not halted:
            raise
        # Exactly one rollback, never silent retries.
        errors=[]
        try:
            procs, listeners=processes_and_listener()
            if listeners:
                if len(set(listeners))==1 and started and int(listeners[0])==started:
                    stop_specific_worker(started)
                else:
                    raise RuntimeError("Unrecognized listener owner; unsafe to stop it")
            replace_checked(agent,info["old_agent"],AGENT_OLD)
            replace_checked(js,info["old_browser"],JS_OLD)
            restore=spawn_agent(agent,info["transport"],checkpoint,"restored-old-agent")
            import time
            for i in range(25):
                try:
                    if health(0.6).get("ok"):break
                except Exception:
                    time.sleep(0.2)
            else: raise RuntimeError("Old Bridge agent health did not recover")
            raise RuntimeError(f"Upgrade failed, old source restored and health verified; restore pid {restore.pid}; failure: {e}")
        except Exception as rollback_error:
            raise RuntimeError(f"STOP: deploy failed: {e}; one rollback outcome: {rollback_error}; checkpoint {checkpoint}") from rollback_error

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply",action="store_true")
    parser.add_argument("--allow-deploy",action="store_true")
    args=parser.parse_args()
    print(json.dumps(deploy(apply=args.apply,allow_deploy=args.allow_deploy),indent=2))

if __name__=="__main__":
    main()
