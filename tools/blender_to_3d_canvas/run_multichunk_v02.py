"""Single-command source-preserving multi-chunk Blender -> 3D Canvas pipeline.

Use native Python, not the Blender UI process. First-pass export requires
a saved .blend and a NEW bundle directory under the first-party module assets.
--reuse-staged checks existing GLB source SHA and avoids redundant exports.
--native-preview requires the GM to have opened the inactive QA clone and
enabled native 3D Canvas. --apply requires --native-preview; no source Scene
or installed 3D Canvas vendor source is changed.

Example:
 python run_multichunk_v02.py --blend SOURCE.blend \
  --blender-bin blender.exe --asset-root MODULE/assets/blender_bundles \
  --bundle QA-20261023 --px-per-meter 75 --origin-x 1920 --origin-y 960 \
  --native-preview [--apply]
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import pathlib
import subprocess
import sys
from import_chunks_v02 import verify, QA_SCENE

def file_hash(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda:f.read(1<<20),b""):
            h.update(ch)
    return h.hexdigest()

def run(cmd,phase,limit):
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=limit)
    if p.returncode:
        raise RuntimeError(phase+" failed (exit "+str(p.returncode)+"): "+
                           p.stderr[-1500:]+p.stdout[-900:])
    return p.stdout

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--blend",type=pathlib.Path,required=True)
    p.add_argument("--blender-bin",type=pathlib.Path,required=True)
    p.add_argument("--asset-root",type=pathlib.Path,required=True)
    p.add_argument("--bundle",required=True)
    p.add_argument("--px-per-meter",type=float,required=True)
    p.add_argument("--origin-x",type=float,required=True)
    p.add_argument("--origin-y",type=float,required=True)
    p.add_argument("--grid-size",type=float,default=100)
    p.add_argument("--grid-distance",type=float,default=1)
    p.add_argument("--reuse-staged",action="store_true")
    p.add_argument("--native-preview",action="store_true")
    p.add_argument("--apply",action="store_true")
    a=p.parse_args()
    if a.apply and not a.native_preview:
        raise RuntimeError("Cannot apply without native preflight.")
    if not a.blend.is_file() or a.blend.suffix.lower()!=".blend":
        raise RuntimeError("Saved .blend source required.")
    if not a.asset_root.is_dir():
        raise RuntimeError("Verified first-party asset root required.")
    if not a.bundle.isascii() or not a.bundle.replace("-","").replace("_","").isalnum():
        raise RuntimeError("Unsafe bundle ID.")
    for val in (a.px_per_meter,a.grid_size,a.grid_distance,a.origin_x,a.origin_y):
        if not math.isfinite(val):
            raise RuntimeError("Non-finite scale/origin.")
    if min(a.px_per_meter,a.grid_size,a.grid_distance)<=0:
        raise RuntimeError("Non-positive scale.")
    folder=a.asset_root/a.bundle
    before=file_hash(a.blend)
    if a.reuse_staged:
        if not (folder/"manifest.json").exists():
            raise RuntimeError("Cannot reuse missing manifest.")
    else:
        if folder.exists():
            raise RuntimeError("Never overwrite a staged GLB bundle.")
        if not a.blender_bin.is_file():
            raise RuntimeError("Blender executable missing.")
        args=[
            str(a.blender_bin),"-b",str(a.blend),"-t","2",
            "--python",str(pathlib.Path(__file__).with_name("export_chunks_v02.py")),
            "--","--output",str(folder),"--bundle",a.bundle,
            "--px-per-meter",str(a.px_per_meter),
            "--origin-x",str(a.origin_x),"--origin-y",str(a.origin_y),
            "--grid-size",str(a.grid_size),"--grid-distance",str(a.grid_distance)
        ]
        output=run(args,"Immutable background Blender source export",480)
        matched=[ln for ln in output.splitlines()
                 if ln.startswith("ACQ_MULTI_EXPORT_RESULT=")]
        if len(matched)!=1 or not json.loads(matched[0].split("=",1)[1]).get("ok"):
            raise RuntimeError("Missing verified export summary.")
    doc,rows=verify(folder,a.asset_root)
    if pathlib.Path(doc["source_blend"]).resolve()!=a.blend.resolve() or doc["source_blend_sha256"]!=before:
        raise RuntimeError("Bundle originated from another .blend source/revision.")
    if file_hash(a.blend)!=before:
        raise RuntimeError("Source Blender changed during workflow.")
    importer=[
        sys.executable,str(pathlib.Path(__file__).with_name("import_chunks_v02.py")),
        "--bundle-dir",str(folder),"--asset-root",str(a.asset_root)
    ]
    if a.native_preview:importer.append("--native-preview")
    if a.apply:importer.append("--apply")
    output=run(importer,"Guarded native multi-chunk QA",720)
    report=json.loads(output)
    if not report.get("ok"):
        raise RuntimeError("Native stage did not report successful validation.")
    if file_hash(a.blend)!=before:
        raise RuntimeError("Source Blender changed after importer stage.")
    return {"ok":True,"source_untouched_sha256":before,"stage":report["stage"],
      "qa_scene_id":QA_SCENE if a.native_preview else None,
      "chunks":len(rows),"bundle":str(folder),
      "native_tile_ids":report.get("native_tile_ids"),
      "production_acceptance":False,"source_scene_writes":False}

if __name__=="__main__":
    try:print(json.dumps(main(),indent=2))
    except Exception as e:
        print(json.dumps({"ok":False,"error":str(e)}),file=sys.stderr)
        sys.exit(1)
