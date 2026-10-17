// Area 8 verified first-person 3D Canvas camera follow patch, v2.7.20.
// Reapply only after a 3D Canvas upgrade if required. No mesh or map modifications.
// Requires Node.js on Windows. Guards vendor source and writes an immutable backup.
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import {spawnSync} from "node:child_process";
const main = path.join(process.env.LOCALAPPDATA ?? path.join(os.homedir(),"AppData","Local"),"FoundryVTT","Data","modules","levels-3d-preview","scripts","main.js");
const original = fs.readFileSync(main,"utf8");
const marker = "// Acq v2.7.20: preserve first-person look bearing";
if (original.includes(marker)) { console.log("Already installed; unchanged:",main); process.exit(0); }
const setter = "                        this.camera.position.set(pos.x, pos.y, pos.z);";
const toggle = "        this.firstPersonMode = !this.firstPersonMode;";
if (original.split(setter).length !== 2 || original.split(toggle).length !== 2)
  throw new Error("Unexpected upstream 3D Canvas source; no edit applied.");
const patch = [
"                        // Acq v2.7.20: preserve first-person look bearing while following controlled token.",
"                        const forward = this.camera.getWorldDirection(new THREE.Vector3());",
"                        const desiredY = this._acqLastHead ? this._acqLastHead.y + (pos.y - this._acqLastHead.y) * 0.35 : pos.y;",
"                        this.camera.position.set(pos.x, desiredY, pos.z);",
"                        this.controls.target.copy(this.camera.position).addScaledVector(forward, 1.5);",
"                        this._acqLastHead = {x:pos.x,y:desiredY,z:pos.z};"
].join("\n");
const updated = original.replace(setter,patch).replace(toggle,toggle+"\n        this._acqLastHead = null;");
const scratch = path.join(os.tmpdir(),"acq-3d-canvas-camera-source-check.mjs");
fs.writeFileSync(scratch,updated);
const check = spawnSync(process.execPath,["--check",scratch],{encoding:"utf8"});
if (check.status !== 0) throw new Error("Syntax check failed: "+check.stderr);
const backup = main+".acq-pristine-"+new Date().toISOString().replace(/[.:]/g,"-")+".bak";
fs.copyFileSync(main,backup,fs.constants.COPYFILE_EXCL);
const temp = main+".acq-pending";
fs.writeFileSync(temp,updated,"utf8");
fs.renameSync(temp,main);
console.log("Installed. Immutable backup:",backup,"; reload Foundry, enter 3D first person, test headings after X/Z/elevation moves.");
