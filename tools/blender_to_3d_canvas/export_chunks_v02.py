"""Read-only Blender -> native 3D Canvas v0.2 multi-chunk GLB export.

Use Blender -b SOURCE.blend --python export_chunks_v02.py -- --output NEW_FOLDER
 --bundle QA_ID --px-per-meter 75 --origin-x 1920 --origin-y 960
 --grid-size 100 --grid-distance 1

This runs in a disposable background Blender process. It creates NO geometry,
does not save or alter its source .blend, and refuses to flatten moving parts
into the static architecture. Each visible source mesh belongs to exactly one
GLB chunk through acq_chunk; absent tags yield one chunk per source object.
Source objects are never remeshed, and their world matrices are preserved.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import pathlib
import sys
from datetime import datetime, timezone
import bpy
from mathutils import Matrix, Vector

SCHEMA = "acq.blender-3dcanvas.multichunk.v0.2"
BLOCKED_GEOMETRY = {"CURVE","SURFACE","FONT","META","CURVES","POINTCLOUD","VOLUME"}
DOOR_FIELDS = ("isDoor","doorId","ds","doorStyle","doorAnimateAngle",
               "doorType","doorState","slidePercent")
# Explicit author role contract. No inference from names, dimensions, or all-true
# legacy flags: silence is an error for a new native import.
ALLOWED_ACQ_ROLES = {
    "walkable_floor", "stair", "opaque_wall", "roof",
    "door_leaf", "solid_prop", "decorative_prop", "foliage",
}


def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def parse():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    p.add_argument("--bundle",required=True)
    p.add_argument("--px-per-meter",type=float,required=True)
    p.add_argument("--origin-x",type=float,required=True)
    p.add_argument("--origin-y",type=float,required=True)
    p.add_argument("--grid-size",type=float,default=100.0)
    p.add_argument("--grid-distance",type=float,default=1.0)
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    return p.parse_args(argv)

def matrix_flat(mat):
    return [float(mat[row][col]) for row in range(4) for col in range(4)]

def bounds(objects):
    # Object.bound_box corners exaggerate world-axis extents of irregular
    # geometry after rotation. Native Three.Box3 measures actual mesh
    # vertices. Match that measurement using Blender's genuine source
    # vertices and exact evaluated world matrices; no mesh is modified.
    import numpy as np
    result_min=np.array([float("inf")]*3,dtype=np.float64)
    result_max=np.array([-float("inf")]*3,dtype=np.float64)
    for ob in objects:
        if any(mod.show_render for mod in ob.modifiers):
            raise RuntimeError("Unbaked evaluated modifiers need explicit source QA: "+ob.name)
        count=len(ob.data.vertices)
        if not count:
            raise RuntimeError("Empty source mesh: "+ob.name)
        flat=np.empty(count*3,dtype=np.float32)
        ob.data.vertices.foreach_get("co",flat)
        arr=flat.reshape((count,3)).astype(np.float64,copy=False)
        matrix=np.array([[float(ob.matrix_world[i][j]) for j in range(4)]
                         for i in range(3)],dtype=np.float64)
        world=arr @ matrix[:,:3].T + matrix[:,3]
        if not np.isfinite(world).all():
            raise RuntimeError("Non-finite source geometry: "+ob.name)
        result_min=np.minimum(result_min,np.min(world,axis=0))
        result_max=np.maximum(result_max,np.max(world,axis=0))
    return result_min.tolist(),result_max.tolist()

def main():
    a=parse()
    vals=[a.px_per_meter,a.grid_size,a.grid_distance,a.origin_x,a.origin_y]
    if not all(math.isfinite(t) for t in vals) or any(v<=0 for v in vals[:3]):
        raise ValueError("Finite positive scale and finite origin required.")
    if not a.bundle.isascii() or not a.bundle.replace("-","").replace("_","").isalnum():
        raise ValueError("Bundle identifier must be ASCII alphanumeric, - or _.")
    src=pathlib.Path(bpy.data.filepath).resolve()
    if not src.is_file() or not bpy.data.is_saved or bpy.data.is_dirty:
        raise RuntimeError("Require a clean, saved source opened in background Blender.")
    dst=pathlib.Path(a.output).resolve()
    if src==dst or src in dst.parents or dst==src.parent:
        raise RuntimeError("Isolated output folder required; never write into source.")
    if dst.exists() and any(dst.iterdir()):
        raise RuntimeError("Output must be an unused, empty versioned folder.")
    visible=[ob for ob in bpy.context.scene.objects
             if not ob.hide_render and not ob.hide_viewport]
    bad=[ob.name for ob in visible if ob.type in BLOCKED_GEOMETRY]
    if bad:
        raise RuntimeError("Visible unsupported geometry cannot be silently omitted: "+repr(bad[:10]))
    meshes=sorted((ob for ob in visible if ob.type=="MESH"),key=lambda ob:ob.name)
    if not meshes:
        raise RuntimeError("No visible source meshes.")
    groups={}
    ids=set()
    for ob in meshes:
        if not ob.data or len(ob.data.vertices)<3:
            raise RuntimeError("Empty mesh: "+ob.name)
        cid=str(ob.get("acq_chunk",ob.name)).strip()
        if not cid or not cid.isascii() or len(cid)>70 or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for ch in cid):
            raise RuntimeError("Unsafe source chunk ID: "+repr(cid))
        mode="interactive" if (ob.get("acq_interactive") or ob.get("isDoor") or ob.get("doorType")) else "static"
        door=bool(ob.get("isDoor") or ob.get("doorType"))
        role=str(ob.get("acq_role","")).strip()
        if role not in ALLOWED_ACQ_ROLES:
            raise RuntimeError("Explicit acq_role required for native-safe export: "+ob.name)
        if door != (role=="door_leaf"):
            raise RuntimeError("Door tagging and acq_role=door_leaf must agree: "+ob.name)
        if door and not ob.get("doorId"):
            raise RuntimeError("Native door requires an explicit source doorId: "+ob.name)
        if door and int(ob.get("doorStyle",0)) not in (0,1,2):
            raise RuntimeError("Unsupported 3D Canvas native door style: "+ob.name)
        if any(ob.get(f) is not None for f in DOOR_FIELDS) and not door:
            raise RuntimeError("Door fields on a non-door mesh: "+ob.name)
        if mode=="interactive" and not door and not ob.get("acq_interactive_kind"):
            raise RuntimeError("Interactive part requires acq_interactive_kind metadata.")
        groups.setdefault(cid,[]).append((ob,mode,door))
    if len(groups)>64:
        raise RuntimeError("QA v0.2 guard: at most 64 chunks in one export.")
    for cid,items in groups.items():
        active=[(ob,door) for ob,mode,door in items if mode=="interactive"]
        if not active:
            continue
        # Interactive GLBs can be a native multi-mesh door assembly:
        # door slab, frame and handle. All parts must explicitly opt into
        # one rigid QA group; missing tags must fail rather than silently
        # inventing a joint or treating the entire room as a door.
        if len(items)>1 and not all(ob.get("acq_rigid_assembly") for ob,_,_ in items):
            raise RuntimeError("Multi-mesh interactive assembly needs acq_rigid_assembly on every part: "+cid)
        door_ids={str(ob.get("doorId")) for ob,_,door in items if door}
        if len(door_ids)>1:
            raise RuntimeError("Conflicting native door IDs in assembly: "+cid)
        if any(ob.get("acq_interactive") and not door and not ob.get("acq_interactive_kind")
               for ob,_,door in items):
            raise RuntimeError("Untagged non-door interactive component: "+cid)
    dlo,dhi=bounds(meshes)
    dst.mkdir(parents=True,exist_ok=True)
    manifest={"schema":SCHEMA,"status":"SAVED_EXPORT_NOT_RUNTIME_ACCEPTED",
      "source_blend":str(src),"source_blend_bytes":src.stat().st_size,
      "source_blend_sha256":digest(src),"bundle":a.bundle,
      "created_utc":datetime.now(timezone.utc).isoformat(),
      "foundry":{"scene_origin_px":[a.origin_x,a.origin_y],
         "pixels_per_blender_meter":a.px_per_meter,
         "scene_grid_size_px":a.grid_size,"scene_grid_distance":a.grid_distance,
         "native_3d_tile_scale":a.px_per_meter/a.grid_size,
         "coordinate_rule":"Blender +X=>Foundry +x; Blender +Y=>Foundry -y; Blender +Z=>Foundry elevation",
         "runtime_tile_xy_are_centers":True},
      "source_global_bounds_m":{"min":dlo,"max":dhi},
      "limits":{"max_chunks":64,"interactive_explicit_only":True},
      "chunks":[]}
    for idx,(cid,items) in enumerate(sorted(groups.items())):
        objs=[entry[0] for entry in items]
        lo,hi=bounds(objs)
        cx,cy=(lo[0]+hi[0])/2,(lo[1]+hi[1])/2
        filename=f"{a.bundle}-{idx:03d}-{cid}.glb"
        glb=dst/filename
        original=[(ob,ob.parent,ob.matrix_world.copy(),ob.select_get()) for ob in objs]
        selected=list(bpy.context.selected_objects)
        try:
            for ob in selected:
                ob.select_set(False)
            shift=Matrix.Translation((-cx,-cy,-lo[2]))
            for ob,parent,world,was_selected in original:
                # Parent links can cause a glTF exporter to alter exported
                # transforms when parents are omitted. Detach only in this
                # in-memory disposable process, then restore matrices.
                ob.parent=None
                ob.matrix_world=shift @ world
                ob.select_set(True)
            bpy.context.view_layer.objects.active=objs[0]
            bpy.context.view_layer.update()
            bpy.ops.export_scene.gltf(
                filepath=str(glb),export_format="GLB",use_selection=True,
                export_extras=True,export_yup=True,export_apply=False,
                export_materials="EXPORT",export_image_format="AUTO",
                export_cameras=False,export_lights=False)
        finally:
            for ob,parent,world,was_selected in original:
                ob.select_set(False)
                ob.parent=parent
                ob.matrix_world=world
            for ob in selected:
                ob.select_set(True)
            bpy.context.view_layer.update()
        if not glb.exists() or glb.stat().st_size<1024:
            raise RuntimeError("Empty GLB for "+cid)
        mode="interactive" if any(v=="interactive" for _,v,_ in items) else "static"
        door=any(v for _,_,v in items)
        source_objects=[]
        for ob,_,_ in items:
            source_objects.append({
              "name":ob.name,"mesh_datablock":ob.data.name,
              "source_parent":ob.parent.name if ob.parent else None,
              "source_matrix_world_rowmajor":matrix_flat(ob.matrix_world),
              "source_asset":ob.get("asset_source",ob.get("source_glb")),
              "vertices":len(ob.data.vertices),"faces":len(ob.data.polygons),
              "materials":[m.name for m in ob.data.materials if m],
              "acq_role":str(ob.get("acq_role")),
              "collision":ob.get("collision"),"sight":ob.get("sight"),
              "camera_collision":ob.get("cameraCollision"),
              "native_door_extras":{k:ob.get(k) for k in DOOR_FIELDS if ob.get(k) is not None},
              "interactive_kind":ob.get("acq_interactive_kind"),
            })
        elevation=lo[2]*a.px_per_meter*a.grid_distance/a.grid_size
        chunk={
          "chunk_id":cid,"kind":mode,"interactive_door":door,
          "rigid_assembly":bool(mode=="interactive" and len(items)>1),
          "asset":{"filename":filename,"sha256":digest(glb),"bytes":glb.stat().st_size,"format":"GLB"},
          "source_bounds_m":{"min":lo,"max":hi},
          "tile_center_xy_px":[a.origin_x+cx*a.px_per_meter,
                               a.origin_y-cy*a.px_per_meter],
          "tile_elevation_scene_units":elevation,
          "native_3d_tile_scale":a.px_per_meter/a.grid_size,
          "expected_tile_footprint_px":[(hi[0]-lo[0])*a.px_per_meter,
                                        (hi[1]-lo[1])*a.px_per_meter],
          "expected_tile_depth_px":(hi[2]-lo[2])*a.px_per_meter,
          "source_objects":source_objects,
          "runtime_visual_verified":False,"runtime_collision_verified":False,
          "runtime_camera_verified":False}
        manifest["chunks"].append(chunk)
    outfile=dst/"manifest.json"
    outfile.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf8")
    print("ACQ_MULTI_EXPORT_RESULT="+json.dumps({
      "ok":True,"schema":SCHEMA,"manifest":str(outfile),
      "chunks":len(manifest["chunks"]),
      "bytes":sum(c["asset"]["bytes"] for c in manifest["chunks"]),
      "interactive":sum(c["kind"]=="interactive" for c in manifest["chunks"])}))

if __name__=="__main__":
    main()
