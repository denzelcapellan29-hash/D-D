"""Blender-first 3D Canvas export bundle.

Run ONLY in a separate background Blender process on a verified, saved .blend.
This code never creates visible meshes and never saves/mutates the source .blend.
Outputs a centered, Y-up GLB of source meshes plus a deterministic spatial
manifest for native Foundry 3D Canvas placement.

Usage:
  blender -b Area8_Asset.blend -t 2 --python export_bundle.py -- \
    --output /path/to/staged --bundle area8-smoke \
    --px-per-meter 75 --origin-x 1920 --origin-y 960 --grid-size 100

This first release exports visible static MESH objects only; nonmesh curves,
unsupported shader nodes, particle effects, animations, lights, door dynamics
and cameras are separately reported and NOT silently declared imported.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import sys
from datetime import datetime, timezone

import bpy
from mathutils import Matrix, Vector


def sha256_file(p: pathlib.Path) -> str:
    dig = hashlib.sha256()
    with p.open("rb") as fd:
        while blob := fd.read(8 * 1024 * 1024):
            dig.update(blob)
    return dig.hexdigest()


def parse():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    p.add_argument("--bundle", required=True)
    p.add_argument("--px-per-meter", type=float, required=True)
    p.add_argument("--origin-x", type=float, required=True)
    p.add_argument("--origin-y", type=float, required=True)
    p.add_argument("--grid-size", type=float, default=100)
    p.add_argument("--limit", type=int, default=0,
                   help="QA only: mesh count limit. 0 exports all.")
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return p.parse_args(args)


def bounds_object(obj):
    return [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]


def ensure_finite(items):
    if not all(math.isfinite(x) for x in items):
        raise RuntimeError("Scene contains non-finite transformed bounds.")


def main():
    args = parse()
    for label in ("px_per_meter", "grid_size"):
        if not math.isfinite(getattr(args, label)) or getattr(args, label) <= 0:
            raise ValueError(label + " must be a positive finite quantity.")
    if any(not math.isfinite(getattr(args, t)) for t in ("origin_x", "origin_y")):
        raise ValueError("Origin must be finite.")
    source = pathlib.Path(bpy.data.filepath).resolve()
    if not source.is_file() or not bpy.data.is_saved:
        raise RuntimeError("Require a real saved Blender source file, opened read-only in background.")
    if bpy.data.is_dirty:
        raise RuntimeError("Refusing to export a dirty Blender source.")
    output = pathlib.Path(args.output).resolve()
    if output == source.parent or source in output.parents:
        raise RuntimeError("Export must go into an isolated staging directory.")
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("The export folder is not empty; require an immutable new bundle.")
    output.mkdir(parents=True, exist_ok=True)
    if not args.bundle.replace("-", "").replace("_", "").isalnum():
        raise ValueError("Bundle ID supports only ASCII letters, digits, - and _.")
    visible = sorted(
        (o for o in bpy.context.scene.objects
         if o.type == "MESH" and not o.hide_render and not o.hide_viewport),
        key=lambda o: o.name,
    )
    if args.limit:
        if args.limit < 1:
            raise ValueError("Limit must be positive.")
        visible = visible[:args.limit]
    if not visible:
        raise RuntimeError("No visible source MESH objects to export.")
    other_geometry = [o.name for o in bpy.context.scene.objects
        if o.type in ("CURVE","SURFACE","FONT","META","CURVES","POINTCLOUD","VOLUME")
        and not o.hide_render]
    if other_geometry:
        raise RuntimeError("Visible non-MESH geometry would be silently omitted: "
                           + repr(other_geometry[:12]))
    depsgraph = bpy.context.evaluated_depsgraph_get()
    coords = []
    source_meshes = []
    interactive = []
    for obj in visible:
        if obj.data is None or len(obj.data.vertices) == 0:
            raise RuntimeError("Source mesh has no vertices: " + obj.name)
        coords.extend(bounds_object(obj))
        source_meshes.append({
            "name": obj.name,
            "data": obj.data.name,
            "source_vertex_count": len(obj.data.vertices),
            "source_face_count": len(obj.data.polygons),
            "source_asset": obj.get("asset_source", obj.get("source_glb")),
            "collision": obj.get("collision"),
            "sight": obj.get("sight"),
            "door_id": obj.get("doorId"),
            "interactive": bool(obj.get("acq_interactive") or obj.get("isDoor")),
        })
        if source_meshes[-1]["interactive"]:
            interactive.append(obj.name)
    if interactive:
        raise RuntimeError("Do not bake dynamic or door geometry into a static world chunk: "
                           + repr(interactive[:12]) + ". Export as separately interactive parts.")
    xs = [v.x for v in coords]
    ys = [v.y for v in coords]
    zs = [v.z for v in coords]
    ensure_finite(xs + ys + zs)
    minx,maxx,miny,maxy,minz,maxz=min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
    centerx,centery=(minx+maxx)/2,(miny+maxy)/2
    glb = output / (args.bundle + ".glb")
    # Only non-destructive object/world transforms in this *background* file
    # and never saves the source .blend. Zero horizontal GLB origin and floor Y.
    delta=Matrix.Translation(Vector((-centerx,-centery,-minz)))
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    prior={obj.name:obj.matrix_world.copy() for obj in visible}
    try:
        for obj in visible:
            obj.matrix_world = delta @ prior[obj.name]
            obj.select_set(True)
        bpy.context.view_layer.objects.active=visible[0]
        bpy.ops.export_scene.gltf(
            filepath=str(glb), export_format="GLB", use_selection=True,
            export_extras=True, export_yup=True, export_apply=False,
            export_materials="EXPORT", export_image_format="AUTO",
            export_cameras=False, export_lights=False,
        )
    finally:
        for obj in visible:
            obj.matrix_world = prior[obj.name]
            obj.select_set(False)
    if not glb.is_file() or glb.stat().st_size < 1024:
        raise RuntimeError("GLB export failed or produced no meaningful geometry.")
    # Source Blender X maps to Foundry X. Source Blender Y maps to
    # decreasing Foundry Y; Y-up GLTF maps Blender Z to model Y.
    xcenter=args.origin_x+centerx*args.px_per_meter
    ycenter=args.origin_y-centery*args.px_per_meter
    scale=args.px_per_meter/args.grid_size
    unsupported={
        "nonmesh_visible_object_names": [
            o.name for o in bpy.context.scene.objects
            if o.type not in ("MESH","CAMERA","LIGHT","EMPTY")
            and not o.hide_render
        ],
        "lights": [o.name for o in bpy.context.scene.objects if o.type=="LIGHT"],
        "cameras": [o.name for o in bpy.context.scene.objects if o.type=="CAMERA"],
        "interactive_mesh_names_require_native_overlay":interactive,
        "animations_exported": False,
        "blender_shader_node_equivalence_verified": False,
        "runtime_collisions_verified": False,
    }
    manifest={
        "schema":"acq.blender-3dcanvas.bundle.v0.1",
        "status":"SAVED_EXPORT_NOT_RUNTIME_ACCEPTED",
        "created_utc":datetime.now(timezone.utc).isoformat(),
        "source_blend":str(source),
        "source_blend_size_bytes":source.stat().st_size,
        "source_mesh_count":len(visible),
        "source_bounds_blender_m":{
            "min":[minx,miny,minz], "max":[maxx,maxy,maxz],
            "pivot_center_xy_floor_z":[centerx,centery,minz]
        },
        "asset":{
            "filename":glb.name,"sha256":sha256_file(glb),
            "bytes":glb.stat().st_size,
            "format":"GLB","export_y_up":True,
            "embedded_materials":True,
            "model_is_centered_xy_and_floor_zero":True,
            "foundry_path":None
        },
        "foundry":{
            "scene_origin_px":[args.origin_x,args.origin_y],
            "pixels_per_blender_meter":args.px_per_meter,
            "scene_grid_size_px":args.grid_size,
            "native_3d_tile_scale":scale,
            "tile_center_xy_px":[xcenter,ycenter],
            "tile_elevation_scene_units":0,
            "source_anchor_floor_z_blender_m":minz,
            "tile_rotation_degrees":0,
            "tile_flags":{
                "collision":True,"sight":True,
                "cameraCollision":True,
                "autoCenter":True,
                "autoGround":True,
            }
        },
        "mesh_provenance":source_meshes,
        "omissions_and_unverified":unsupported,
        "qa":{
            "world_bounds_source_m":[maxx-minx,maxy-miny,maxz-minz],
            "expected_tile_footprint_px":[
                (maxx-minx)*args.px_per_meter,
                (maxy-miny)*args.px_per_meter
            ],
            "measured_native_model_bounds":None,
            "actual_runtime_visual_parity":False,
        },
    }
    out=output/"manifest.json"
    out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print("ACQ_EXPORT_RESULT="+json.dumps({
        "ok":True,"manifest":str(out),"glb":str(glb),
        "mesh_count":len(visible),"glb_bytes":glb.stat().st_size,
        "static_interactives_require_overlay":len(interactive)
    }))


if __name__ == "__main__":
    main()
