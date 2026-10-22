"""One-command orchestration: saved Blender .blend -> GLB/manifest -> 3D Canvas.

Runs on the Foundry GM machine. Does NOT require the DM to build in Foundry,
paste JavaScript or manually place Tiles.

First release is deliberately restricted to the verified inactive Area8 QA
clone. Full-room scale and generic scene lifecycle are separate QA gates.
The game server must already be running with the first-party Acq bridge;
the GM client must be viewing this QA Scene with 3D Canvas renderer ready
(or the caller can manage that view through existing Acq tools).

Syntax:
  python run_pipeline.py --blend SOURCE.blend \
    --bundle area8-rim-new --px-per-meter 75 --origin-x 1920 --origin-y 960 \
    --scene-id sW4aXZgKXj1cH0US --build-id test-area8
    [--apply]

Default is preflight only. --apply creates/updates exactly one identified QA
Tile after native geometry verification. Never writes to approved scene.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys


def execute(cmd: list[str], label: str, max_seconds: int) -> dict:
    print("STAGE " + label, file=sys.stderr, flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=max_seconds)
    if r.returncode:
        raise RuntimeError(
            f"{label} failed (exit {r.returncode}): " + r.stderr[-1800:] +
            " output=" + r.stdout[-500:]
        )
    if label == "Blender export":
        token = "ACQ_EXPORT_RESULT="
        found = [ln[len(token):] for ln in r.stdout.splitlines()
                 if ln.startswith(token)]
        if len(found) != 1:
            raise RuntimeError("Blender did not return a single verified export report.")
        return json.loads(found[0])
    return json.loads(r.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", type=pathlib.Path, required=True)
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--build-id", required=True)
    parser.add_argument("--px-per-meter", type=float, required=True)
    parser.add_argument("--origin-x", type=float, required=True)
    parser.add_argument("--origin-y", type=float, required=True)
    parser.add_argument("--grid-size", type=float, default=100)
    parser.add_argument("--offset-x-px", type=float, default=0)
    parser.add_argument("--offset-y-px", type=float, default=0)
    parser.add_argument("--semantic-id", default=None)
    parser.add_argument("--blender-bin", type=pathlib.Path, required=True)
    parser.add_argument("--module-asset-root", type=pathlib.Path, required=True)
    parser.add_argument("--reuse-existing-export", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.scene_id != "sW4aXZgKXj1cH0US":
        raise RuntimeError("v0.1 importer is restricted to the verified inactive Area8 QA clone.")
    if not args.blend.is_file() or args.blend.suffix.lower() != ".blend":
        raise RuntimeError("Require an existing saved .blend file.")
    folder = args.module_asset_root / args.bundle
    if args.reuse_existing_export:
        if not (folder/"manifest.json").is_file():
            raise RuntimeError("Cannot reuse missing versioned GLB bundle.")
        manifest=json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
        if pathlib.Path(manifest["source_blend"]).resolve()!=args.blend.resolve():
            raise RuntimeError("Existing bundle is not derived from the requested .blend.")
        export = {"ok":True,"reused":True,"manifest":str(folder/"manifest.json")}
    else:
        if folder.exists():
            raise RuntimeError("A new bundle must use a new unused output directory.")
        if not args.blender_bin.is_file():
            raise RuntimeError("Blender executable missing.")
        cmd = [
            str(args.blender_bin),"-b",str(args.blend),"-t","2",
            "--python",str(pathlib.Path(__file__).with_name("export_bundle.py")),
            "--","--output",str(folder),"--bundle",args.bundle,
            "--px-per-meter",str(args.px_per_meter),
            "--origin-x",str(args.origin_x),
            "--origin-y",str(args.origin_y),
            "--grid-size",str(args.grid_size)
        ]
        export=execute(cmd,"Blender export",max_seconds=330)
    importer=[
        sys.executable,str(pathlib.Path(__file__).with_name("import_bundle.py")),
        "--bundle-dir",str(folder),
        "--module-asset-root",str(args.module_asset_root),
        "--scene-id",args.scene_id,
        "--build-id",args.build_id,
        "--offset-x-px",str(args.offset_x_px),
        "--offset-y-px",str(args.offset_y_px)
    ]
    if args.semantic_id: importer += ["--semantic-id",args.semantic_id]
    preflight=execute(importer,"3D Canvas model/geometry preflight",max_seconds=160)
    if preflight.get("status") != "PREFLIGHT_ONLY":
        raise RuntimeError("Importer preview did not certify GLB")
    report={"ok":True,"export":export,"preflight":preflight}
    if args.apply:
        applied=execute(importer+["--apply"],"3D Canvas idempotent import",max_seconds=160)
        if applied.get("status")!="IMPORTED_AND_GEOMETRY_QA_PASSED":
            raise RuntimeError("Native Tile import is not verified.")
        report["import"]=applied
    else:
        report["status"]="PREFLIGHT_ONLY"
    return report


if __name__=="__main__":
    try:
        print(json.dumps(main(),indent=2))
    except Exception as exc:
        print(json.dumps({"ok":False,"error":str(exc)}),file=sys.stderr)
        sys.exit(1)
