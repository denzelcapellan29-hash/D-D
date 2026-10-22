"""Deterministic, reversible Blender GLB -> native 3D Canvas Tile importer.

This runs beside Foundry on the GM computer. It uses *existing* Acq first-party
bridge operations, not a private 3D engine. Intended workflow:
1. export_bundle.py creates GLB + placement manifest from saved Blender .blend;
2. manifest and GLB are staged under local first-party bridge assets;
3. with a disposable GM-only Scene already viewed in 3D Canvas, run this
   helper in --dry-run (default), then --apply once QA preflight is clean.

No dependency on Foundry browser devtools or vendor module modifications.
The source / active campaign Scene is always refused. An idempotent semantic
ID allows retries and updates without duplicate Tile accumulation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import pathlib
import sys
import urllib.error
import urllib.request
import uuid


BRIDGE_URL = "http://127.0.0.1:18747/rpc"
FORBIDDEN_SCENES = frozenset({"NUEDEFAULTSCENE0"})
SCHEMA = "acq.blender-3dcanvas.bundle.v0.1"
ASSET_PREFIX = "modules/acq-foundry-bridge/assets/blender_bundles/"


def digest(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while chunk := f.read(8 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def command(scene_id: str, op: dict, *, dry_run: bool,
            expected_revision: str | None = None, timeout: int = 70) -> tuple[dict,dict]:
    data = {
        "protocol_version":1,
        "command_id":"mcp-"+str(uuid.uuid4()),
        "scene_id":scene_id,
        "dry_run":dry_run,
        "_timeout_seconds":float(timeout),
        "operations":[op]
    }
    if expected_revision:
        data["expected_revision"] = expected_revision
    req = urllib.request.Request(
        BRIDGE_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type":"application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout+5) as resp:
            doc = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as ex:
        raise RuntimeError(
            f"Native Acq GM bridge HTTP {ex.code}: " +
            ex.read(1200).decode("utf-8","replace")
        ) from ex
    item = (doc.get("operations") or [{}])[0]
    if not doc.get("ok") or not item.get("ok"):
        raise RuntimeError("Native GM operation failed: " + str(item.get("error"))[:600])
    return doc,item


def prepare(bundle: pathlib.Path, module_assets_root: pathlib.Path) -> tuple[dict,pathlib.Path,str]:
    folder = bundle.resolve(strict=True)
    root = module_assets_root.resolve(strict=True)
    if not folder.is_relative_to(root):
        raise ValueError("Bundle must be staged inside the authorized first-party module asset root.")
    manifest = json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA:
        raise ValueError("Unsupported or missing bundle manifest schema.")
    relative = folder.relative_to(root)
    if any(part in ("..",".") for part in relative.parts):
        raise ValueError("Unsafe staging directory.")
    glbname = manifest["asset"]["filename"]
    if pathlib.PurePath(glbname).name != glbname or not glbname.endswith(".glb"):
        raise ValueError("Unsafe or missing GLB filename.")
    glb = folder/glbname
    if not glb.is_file():
        raise FileNotFoundError(glb)
    if glb.stat().st_size != manifest["asset"]["bytes"]:
        raise RuntimeError("GLB file size changed since Blender export.")
    if digest(glb) != manifest["asset"]["sha256"]:
        raise RuntimeError("GLB provenance SHA256 differs; refusing to import.")
    foundry_path = ASSET_PREFIX+relative.as_posix()+"/"+glbname
    for f in ["pixels_per_blender_meter","scene_grid_size_px","native_3d_tile_scale"]:
        key = "native_3d_tile_scale" if f=="native_3d_tile_scale" else f
        val = float(manifest["foundry"][key])
        if not math.isfinite(val) or val<=0:
            raise ValueError("Invalid Blender-to-Foundry scale: "+f)
    return manifest,glb,foundry_path


def validate_geometry(preview: dict, manifest: dict, tol_pixels: float = 1.05) -> dict:
    candidate = preview.get("candidate") or {}
    bounds = preview.get("model_bounds") or {}
    expected = manifest["qa"]["expected_tile_footprint_px"]
    w,h = candidate.get("width"),candidate.get("height")
    if not isinstance(w,int) or not isinstance(h,int):
        raise RuntimeError("3D Canvas native preview omitted Tile dimensions.")
    residual=[abs(w-expected[0]),abs(h-expected[1])]
    if max(residual)>tol_pixels:
        raise RuntimeError(f"Native dimensions do not agree with Blender (pixels): {residual}")
    depth = candidate.get("flags",{}).get("levels-3d-preview",{}).get("depth")
    expected_depth=(manifest["source_bounds_blender_m"]["max"][2]-
                    manifest["source_bounds_blender_m"]["min"][2]) * manifest["foundry"]["pixels_per_blender_meter"]
    if not isinstance(depth,(float,int)) or abs(depth-expected_depth) > 0.2:
        raise RuntimeError("Native depth does not match original Blender geometry.")
    return {"width_px":w,"height_px":h,"depth_px":depth,
            "expected_width_px":expected[0],"expected_height_px":expected[1],
            "expected_depth_px":expected_depth,"footprint_residual_px":residual}


def qa_native_tile(scene_id: str, semantic_id: str, center: tuple[float,float],
                   expected_dimensions: tuple[int,int,float]) -> dict:
    # Live inspector's runtime_bounds are in 3D Canvas world coordinates,
    # where 1000 Foundry scene pixels = 1 native Three world unit for this world.
    # Compare the observed center to the actual Tile document x/y; this is
    # intentionally derived from live results, not from the preview's old
    # x-w/2 heuristic.
    snap,item=command(scene_id,{"op":"inspect_3d_scene"},dry_run=True,timeout=50)
    tiles=item.get("tiles") or []
    found=[x for x in tiles if x.get("acq",{}).get("semantic_id")==semantic_id]
    if len(found)!=1:
        raise RuntimeError(f"Expected exactly one imported Tile, got {len(found)}")
    tile=found[0]
    box=tile.get("runtime_bounds")
    if not box:
        raise RuntimeError("Native Three world bounds for imported Tile unavailable.")
    expected_x,expected_y=center
    errors={
        "center_x_pixels":abs(box["center"]["x"]*1000-expected_x),
        "center_y_pixels":abs(box["center"]["z"]*1000-expected_y),
        "width_pixels":abs(box["size"]["x"]*1000-expected_dimensions[0]),
        "height_pixels":abs(box["size"]["z"]*1000-expected_dimensions[1]),
        "depth_pixels":abs(box["size"]["y"]*1000-expected_dimensions[2]),
    }
    if max(errors.values()) > 1.1:
        raise RuntimeError(f"Native Tile bounds parity gate failed: {errors}")
    return {"tile_id":tile["id"],"observed_center_3d":box["center"],
            "observed_size_3d":box["size"],"max_error_px":max(errors.values()),
            "errors_px":errors,"scene_revision":snap.get("after_revision")}


def cli():
    p = argparse.ArgumentParser()
    p.add_argument("--bundle-dir",type=pathlib.Path,required=True)
    p.add_argument("--module-asset-root",type=pathlib.Path,required=True)
    p.add_argument("--scene-id",required=True)
    p.add_argument("--build-id",required=True)
    p.add_argument("--semantic-id",default=None,
                   help="QA-only stable semantic ID for updating an existing import.")
    p.add_argument("--offset-x-px",type=float,default=0)
    p.add_argument("--offset-y-px",type=float,default=0)
    p.add_argument("--apply",action="store_true")
    return p.parse_args()


def main():
    a=cli()
    if a.scene_id in FORBIDDEN_SCENES:
        raise RuntimeError("Refusing to import to an approved active campaign scene.")
    if not a.scene_id.isalnum() or len(a.scene_id)>32:
        raise ValueError("Invalid Foundry scene id")
    if not a.build_id.replace("-","").replace("_","").isalnum():
        raise ValueError("Invalid build ID")
    manifest, glb, url=prepare(a.bundle_dir,a.module_asset_root)
    center=manifest["foundry"]["tile_center_xy_px"]
    cx=center[0]+a.offset_x_px
    cy=center[1]+a.offset_y_px
    if not all(math.isfinite(x) and abs(x)<100000 for x in (cx,cy)):
        raise RuntimeError("Import target outside safe coordinates.")
    # The first release is intentionally bound to the independent,
    # previously validated inactive Scene clone. DO NOT broaden this
    # restriction merely by supplying an arbitrary scene id.
    # The former QA ownership inspection command can block when the GM is
    # already viewing the clone; source proof and nonactivation were
    # independently verified when this fixture was created.
    if a.scene_id != "sW4aXZgKXj1cH0US":
        raise RuntimeError("Only the verified inactive Area8 QA clone is allowed in v0.1.")
    observed_scene,scene=command(a.scene_id,{"op":"inspect_3d_scene"},dry_run=True,timeout=55)
    if observed_scene.get("scene_id") != a.scene_id:
        raise RuntimeError("Native GM is not viewing the exact intended QA Scene.")
    if not scene.get("levels3d_active"):
        raise RuntimeError("Native 3D Canvas renderer must be active on viewed QA Scene.")
    revision=observed_scene.get("after_revision")
    preview_op={"op":"preview_native_asset_tile","foundry_path":url,
                "x":cx,"y":cy,"scale":manifest["foundry"]["native_3d_tile_scale"],
                "elevation":0,"origin":"center","rotation":0,
                "collision":True,"sight":True,"camera_collision":True}
    _,preview=command(a.scene_id,preview_op,dry_run=True,timeout=75)
    validation=validate_geometry(preview,manifest)
    candidate=copy.deepcopy(preview["candidate"])
    # Native Three.js Tile x/y are *centers*, verified numerically on
    # Area8 fixture. Earlier preview adapter wrongly subtracts w/2,h/2.
    candidate["x"]=round(cx)
    candidate["y"]=round(cy)
    sid=a.semantic_id or "blender-bundle:"+a.build_id
    if not (sid.startswith("blender-bundle:") or sid.startswith("qa:blender-import:")) or len(sid)>130:
        raise ValueError("Only scoped Blender QA import semantic IDs are allowed.")
    create={
        "op":"apply_semantic_objects","build_id":a.build_id,
        "objects":[{"document":"Tile","semantic_id":sid,"build_id":a.build_id,
                    "classification":"QA_ONLY_BLENDER_BUNDLE",
                    "provenance":{"asset_sha256":manifest["asset"]["sha256"],
                                  "source":manifest["source_blend"]},
                    "data":candidate}]
    }
    if not a.apply:
        _,dry=command(a.scene_id,create,dry_run=True,
                      expected_revision=revision,timeout=52)
        return {
            "ok":True,"status":"PREFLIGHT_ONLY","asset_path":url,
            "scene_id":a.scene_id,"semantic_id":sid,
            "Blender_to_native_validation":validation,
            "candidate":candidate,"idempotent_dry_run":dry,
            "saved_scene_unchanged":True
        }
    wrote=False
    try:
        _,changed=command(a.scene_id,create,dry_run=False,
                          expected_revision=revision,timeout=70)
        wrote=True
        parity=qa_native_tile(a.scene_id,sid,(candidate["x"],candidate["y"]),
                (validation["width_px"],validation["height_px"],validation["depth_px"]))
        return {
            "ok":True,"status":"IMPORTED_AND_GEOMETRY_QA_PASSED",
            "asset_path":url,"scene_id":a.scene_id,"semantic_id":sid,
            "native_tile":parity,
            "source_glb_sha256":manifest["asset"]["sha256"],
            "saved_scene_unchanged":False
        }
    except Exception as e:
        # Best-effort bounded rollback restricted to our semantic import ID.
        # Do not conceal rollback failures; never touch other Scene documents.
        if wrote:
            try:
                command(a.scene_id,{"op":"delete_semantic_objects",
                                   "semantic_ids":[sid]},dry_run=False,timeout=45)
            except Exception as undo:
                raise RuntimeError(
                    f"Import failed ({e}); rollback also failed ({undo})"
                ) from undo
        raise


if __name__=="__main__":
    try:
        print(json.dumps(main(),indent=2))
    except Exception as err:
        print(json.dumps({"ok":False,"error":str(err)}),file=sys.stderr)
        sys.exit(1)
