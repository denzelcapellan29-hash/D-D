"""Source-preserving GLB2 primitive normalizer for native 3D Canvas v9 doors.

No Blender dependency. For tagged doors with multiple material primitives, keep
the tagged leaf a real glTF Mesh and move other primitives into child meshes.
Never change binary mesh data, original source objects, or PBR materials.
"""
import json
import pathlib

def normalize_native_model_door_glb(glb_path):
    """Keep vendor door extras on a real Mesh, not a multi-primitive Group.

    Blender emits multi-material mesh primitives inside a single glTF mesh.
    THREE.GLTFLoader makes a Group for multiple primitives, but native 3D
    Canvas 9.0.36 setUpDoors only registers child.isMesh with userData.isDoor.
    Move secondary primitives into child meshes with *identity transforms*,
    keeping their PBR materials and binary geometry absolutely unchanged.
    Mutates only the newly exported temporary GLB; never the source .blend.
    """
    import copy
    import struct
    import os
    path=pathlib.Path(glb_path)
    raw=path.read_bytes()
    if len(raw)<28 or raw[:4]!=b"glTF":
        raise RuntimeError("Native door GLB2 missing header")
    magic,version,total=struct.unpack_from("<4sII",raw,0)
    if version!=2 or total!=len(raw):
        raise RuntimeError("Native door GLB2 header invalid")
    chunks=[];offset=12
    while offset<len(raw):
        if offset+8>len(raw):
            raise RuntimeError("Truncated native door GLB chunk")
        length,kind=struct.unpack_from("<II",raw,offset)
        offset+=8
        if offset+length>len(raw):
            raise RuntimeError("Native door GLB chunk overruns file")
        chunks.append((kind,raw[offset:offset+length]))
        offset+=length
    if len(chunks)!=2 or chunks[0][0]!=0x4e4f534a or chunks[1][0]!=0x004e4942:
        raise RuntimeError("Native door requires a standard GLB JSON + BIN")
    gltf=json.loads(chunks[0][1].decode("utf8"))
    meshes=gltf.get("meshes") or []
    nodes=gltf.get("nodes") or []
    door_nodes=[(n,node) for n,node in enumerate(nodes)
                if node.get("extras",{}).get("isDoor")]
    if len(door_nodes)!=1:
        raise RuntimeError("One tagged Mesh leaf is required for native modelDoors")
    node_index,node=door_nodes[0]
    mi=node.get("mesh")
    if not isinstance(mi,int) or mi<0 or mi>=len(meshes) or node.get("skin") is not None:
        raise RuntimeError("Native door tag must belong to an unskinned mesh node")
    primitives=meshes[mi].get("primitives") or []
    if not primitives:
        raise RuntimeError("Tagged door mesh contains no primitives")
    if len(primitives)==1:
        return {"normalized":False,"door_node":node_index,"primitives":1}
    if gltf.get("animations") or meshes[mi].get("weights"):
        raise RuntimeError("Animated/morphed native door requires an explicit QA review")
    source_primitives=copy.deepcopy(primitives)
    meshes[mi]["primitives"]=[source_primitives[0]]
    children=list(node.get("children") or [])
    for ordinal,primitive in enumerate(source_primitives[1:],start=1):
        new_mesh=copy.deepcopy(meshes[mi])
        new_mesh["name"]=str(meshes[mi].get("name") or "Door")+"_attached_material_"+str(ordinal)
        new_mesh["primitives"]=[primitive]
        new_mesh_index=len(meshes)
        meshes.append(new_mesh)
        new_node_index=len(nodes)
        nodes.append({
            "name":"DoorAttachedMaterial_"+str(ordinal),
            "mesh":new_mesh_index,
            "extras":{
                "acq_role":"door_leaf",
                "acq_door_attachment":True,
                "acq_native_split_existing_primitive":True
            }
        })
        children.append(new_node_index)
    node["children"]=children
    # Verify primitive payload is only reparented, never changed.
    recovered=[meshes[mi]["primitives"][0]]
    recovered.extend(meshes[nodes[n]["mesh"]]["primitives"][0]
                     for n in children if nodes[n].get("extras",{}).get("acq_native_split_existing_primitive"))
    if recovered!=source_primitives:
        raise RuntimeError("Native door material primitive preservation failed")
    json_bytes=json.dumps(gltf,ensure_ascii=False,separators=(",",":")).encode("utf8")
    json_bytes+=b" "*((-len(json_bytes))%4)
    binary=chunks[1][1]
    new_total=12+8+len(json_bytes)+8+len(binary)
    revised=(b"glTF"+struct.pack("<II",2,new_total)
             +struct.pack("<II",len(json_bytes),0x4e4f534a)+json_bytes
             +struct.pack("<II",len(binary),0x004e4942)+binary)
    if revised[-len(binary):]!=binary:
        raise RuntimeError("Native door GLB binary buffer was modified")
    temp=path.with_suffix(".glb.nativepart")
    if temp.exists():
        raise RuntimeError("Temporary native door GLB already exists")
    temp.write_bytes(revised)
    if len(temp.read_bytes())!=new_total:
        raise RuntimeError("Native door GLB rewrite length mismatch")
    os.replace(str(temp),str(path))
    return {"normalized":True,"door_node":node_index,
            "primitives":len(source_primitives),"child_nodes_added":len(source_primitives)-1}


