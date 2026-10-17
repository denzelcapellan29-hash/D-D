// Acquisitions Incorporated / Area 8 native first-person mouse-look v2.7.23.
// Guarded installer for the tested Levels 3D Preview 9.0.35 scripts.
// Leave Game Camera disabled in native first-person mode.
// No geometry, scene documents, or actor settings are modified.
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import {spawnSync} from "node:child_process";

const scripts = path.join(process.env.LOCALAPPDATA ?? path.join(os.homedir(),"AppData","Local"),
  "FoundryVTT","Data","modules","levels-3d-preview","scripts");
const mainPath = path.join(scripts,"main.js");
const cameraPath = path.join(scripts,"handlers","GameCamera.js");
const main = fs.readFileSync(mainPath,"utf8");
const camera = fs.readFileSync(cameraPath,"utf8");
const marker = "// Acq FPS look v2.7.22";
if (main.includes(marker) && camera.includes("Leave FPS mouse-look pivot to OrbitControls.")) {
  console.log("Area 8 right-drag FPS look patch already installed. No changes.");
  process.exit(0);
}
if (main.includes(marker) || camera.includes("Leave FPS mouse-look pivot to OrbitControls.")) {
  throw new Error("Only one script contains the patch: do not apply a partial overwrite.");
}
if (!main.includes("Acq v2.7.21: translate camera and OrbitControls target together.")) {
  throw new Error("The already-verified v2.7.21 first-person follow anchor is missing.");
}
function replaceOne(src,needle,replacement,label) {
  if (src.split(needle).length !== 2) throw new Error("Unexpected vendor source at "+label);
  return src.replace(needle,replacement);
}
const anchor = `        this.firstPersonMode = !this.firstPersonMode;
        this._acqLastHead = null;
        this.camera.near = this.firstPersonMode ? 0.05 : 0.01;
        if (this.GameCamera.enabled && this.firstPersonMode) this.GameCamera.toggle();`;
const revised = `        this.firstPersonMode = !this.firstPersonMode;
        this._acqLastHead = null;
        this.camera.near = this.firstPersonMode ? 0.05 : 0.01;
        if (this.GameCamera.enabled && this.firstPersonMode) this.GameCamera.toggle();
        // Acq FPS look v2.7.22: right drag rotates rather than pans the pivot.
        if (this.firstPersonMode) {
            this._acqFpsOriginalControls = {
                right: this.controls.mouseButtons.RIGHT,
                minPolar: this.controls.minPolarAngle,
                maxPolar: this.controls.maxPolarAngle,
                minAzimuth: this.controls.minAzimuthAngle,
                maxAzimuth: this.controls.maxAzimuthAngle
            };
            this.controls.mouseButtons.RIGHT = THREE.MOUSE.ROTATE;
            this.controls.minPolarAngle = 0.08;
            this.controls.maxPolarAngle = Math.PI - 0.08;
            this.controls.minAzimuthAngle = -Infinity;
            this.controls.maxAzimuthAngle = Infinity;
            const forward = this.camera.getWorldDirection(new THREE.Vector3());
            forward.y = 0;
            if (forward.lengthSq() < 0.01) forward.set(0, 0, 1);
            forward.normalize();
            this.controls.target.copy(this.camera.position).addScaledVector(forward, 1.5);
            this.controls.update();
        } else if (this._acqFpsOriginalControls) {
            const previous = this._acqFpsOriginalControls;
            this.controls.mouseButtons.RIGHT = previous.right;
            this.controls.minPolarAngle = previous.minPolar;
            this.controls.maxPolarAngle = previous.maxPolar;
            this.controls.minAzimuthAngle = previous.minAzimuth;
            this.controls.maxAzimuthAngle = previous.maxAzimuth;
            delete this._acqFpsOriginalControls;
        }`;
let newMain = replaceOne(main,anchor,revised,"toggleFirstPerson");
newMain = replaceOne(newMain,"    _onCameraChange() {",
  "    _onCameraChange() {\n        if (this.firstPersonMode) return; // FPS pitch not ground-locked.",
  "_onCameraChange");
const newCamera = replaceOne(camera,"    onChangeFreeCamera() {",
  "    onChangeFreeCamera() {\n        if (this._parent.firstPersonMode) return; // Leave FPS mouse-look pivot to OrbitControls.",
  "GameCamera.onChangeFreeCamera");
for (const [name,contents] of [["main",newMain],["GameCamera",newCamera]]) {
  const checked = path.join(os.tmpdir(),"acq-fps-"+name+"-check.mjs");
  fs.writeFileSync(checked,contents,"utf8");
  const res = spawnSync(process.execPath,["--check",checked],{encoding:"utf8"});
  if (res.status !== 0) throw new Error("JavaScript syntax check FAILED for "+name+": "+res.stderr);
}
const stamp = new Date().toISOString().replace(/[.:]/g,"-");
const pairs = [[mainPath,newMain],[cameraPath,newCamera]];
const backups = [];
for (const [filename] of pairs) {
  const backup = filename+".acq-pristine-pre-look-"+stamp+".bak";
  fs.copyFileSync(filename,backup,fs.constants.COPYFILE_EXCL);
  backups.push([filename,backup]);
}
try {
  for (const [filename,contents] of pairs) {
    const temp = filename+".acq-stage";
    fs.writeFileSync(temp,contents,"utf8");
    fs.renameSync(temp,filename);
  }
} catch (e) {
  for (const [filename,backup] of backups) fs.copyFileSync(backup,filename);
  throw e;
}
console.log("FPS right-drag ROTATE + free pitch + live camera-follow installed.");
console.log("Backups:",backups);
console.log("Restart/reload 3D Canvas and verify client drag UP, drag DOWN, then token movement.");
