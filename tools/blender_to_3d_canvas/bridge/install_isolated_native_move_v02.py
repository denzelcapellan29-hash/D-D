"""Guarded first-party QA native TokenLayer.moveMany test on isolated seven-GLB Scene.

Only changes Acq first-party JS, with immutable backup and exact source SHA.
Does NOT patch native 3D Canvas or gameplay rules, and does not change Scenes.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,shutil,subprocess,tempfile,os
BEFORE="3086f20da4bdf2ae0ec3558d696014d19518e970db4abada7dc08efb82ef8e7e"
OLD_IMPORT='import {manageEmptyQaScene, SOURCE_SCENE_ID as EMPTY_QA_SOURCE_ID} from "./qa-empty-scene.mjs";'
NEW_IMPORT='import {manageEmptyQaScene, isOwnedEmptyQaScene, SOURCE_SCENE_ID as EMPTY_QA_SOURCE_ID, SOURCE_SHA as EMPTY_QA_SOURCE_SHA} from "./qa-empty-scene.mjs";'
OLD='''  if (!isAcqVisionClone(scene) || scene.active) throw new Error("Native movement exercise requires an inactive GM-only QA clone.");'''
NEW='''  let isolatedFixture = false;
  if (!isAcqVisionClone(scene) && isOwnedEmptyQaScene(scene)) {
    const original = game.scenes?.get(EMPTY_QA_SOURCE_ID);
    const correctOriginal = original?.active === true &&
      game.scenes?.active?.id === EMPTY_QA_SOURCE_ID &&
      (await sceneSnapshot(original))?.revision === EMPTY_QA_SOURCE_SHA;
    const seven = new Set([
      "lower_back_wall", "lower_floor", "lower_side_wall",
      "stair_connector", "upper_doorway", "upper_floor", "upper_interactive_door"
    ]);
    const tiles = Array.from(scene.tiles?.contents ?? []);
    const token = scene.tokens?.get(op.token_id);
    const exactLibrary = tiles.length === seven.size &&
      tiles.every(t => {
        const acq = t.flags?.acq ?? {};
        const prefix = "qa:multichunk:qa-twolevel-library-v02:";
        const sid = String(acq.semantic_id ?? "");
        const part = sid.startsWith(prefix) ? sid.slice(prefix.length) : "";
        if (!seven.has(part) || acq.classification !== "QA_ONLY_MULTICHUNK_V02" ||
            acq.build_id !== "qa-twolevel-library-v02") return false;
        seven.delete(part);
        return true;
      }) && seven.size === 0;
    isolatedFixture = Boolean(correctOriginal && !scene.active &&
      canvas?.scene?.id === scene.id && exactLibrary &&
      scene.tokens?.size === 1 && token?.name === "QA ONLY — Two-Level Stair Walker" &&
      token?.actorId === "0RE9y8365cStS6x4" &&
      token?.flags?.acq?.semantic_id === "qa:token:isolated-stair-walker-v01" &&
      token?.flags?.acq?.classification === "QA_ONLY_TEMP_TOKEN");
  }
  if (!(isAcqVisionClone(scene) || isolatedFixture) || scene.active) {
    throw new Error("Native movement requires the original approved QA clone or exact source-owned isolated seven-part QA fixture.");
  }'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--bridge",required=True,type=pathlib.Path)
 p.add_argument("--backup-dir",required=True,type=pathlib.Path)
 p.add_argument("--apply",action="store_true")
 a=p.parse_args()
 bridge=a.bridge.resolve(strict=True); backup=a.backup_dir.resolve()
 if backup.exists() or sha(bridge)!=BEFORE:raise RuntimeError("Unknown bridge SHA or backup collision; STOP")
 before=bridge.read_text(encoding="utf8")
 if before.count(OLD_IMPORT)!=1 or before.count(OLD)!=1:
  raise RuntimeError("Isolated movement patch anchors drifted.")
 candidate=before.replace(OLD_IMPORT,NEW_IMPORT,1).replace(OLD,NEW,1).encode("utf8")
 with tempfile.TemporaryDirectory() as d:
  tmp=pathlib.Path(d)/"acq-bridge.mjs";tmp.write_bytes(candidate)
  q=subprocess.run([shutil.which("node"),"--check",str(tmp)],capture_output=True,text=True,timeout=20)
  if q.returncode:raise RuntimeError("JS syntax failed "+q.stderr[-700:])
 output={"ok":True,"phase":"OFFLINE_PRECHECK","source_sha":BEFORE,
         "candidate_sha":hashlib.sha256(candidate).hexdigest(),"vendor_edits":False,
         "world_edits":False}
 if not a.apply:return output
 backup.mkdir(parents=True,exist_ok=False)
 shutil.copy2(bridge,backup/"acq-foundry-bridge.js.before")
 if sha(bridge)!=BEFORE:raise RuntimeError("Bridge drift after immutable backup.")
 stage=bridge.with_suffix(".js.isolated-move-stage")
 try:
  stage.write_bytes(candidate)
  if sha(stage)!=output["candidate_sha"]:raise RuntimeError("Staged checksum failed.")
  os.replace(stage,bridge)
 finally:
  if stage.exists():stage.unlink()
 if sha(bridge)!=output["candidate_sha"]:raise RuntimeError("Installed checksum mismatch.")
 output["phase"]="INSTALLED_AWAITING_GM_CLIENT_RELOAD"
 return output
if __name__=="__main__":
 try:print(json.dumps(main(),indent=2))
 except Exception as e:
  print(json.dumps({"ok":False,"error":str(e)}))
  raise SystemExit(1)
