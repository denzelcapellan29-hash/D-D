"""Native 3D Canvas 9 door: Blender multi-material leaves must load as Mesh.

Isolated standard-library tests: never open Blender or write a Foundry Scene.
"""
import copy
import json
import pathlib
import struct
import sys
import tempfile
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from native_door_glb_v02 import normalize_native_model_door_glb

BIN=bytes(range(24))
PRIMS=[
    {"attributes":{"POSITION":0,"NORMAL":1},"indices":2,"material":0,"mode":4},
    {"attributes":{"POSITION":3,"NORMAL":4},"indices":5,"material":1,"mode":4},
]

def make_glb(file, nprimitives=2, door_extras=None, mesh_node=True, animated=False):
    extras=copy.deepcopy(door_extras if door_extras is not None else
                         {"isDoor":True,"doorId":"qa-ramp-v01-upper-door","doorStyle":1})
    leaf={"name":"Door","mesh":1,"children":[0],"extras":extras}
    if not mesh_node:leaf.pop("mesh")
    doc={
        "asset":{"version":"2.0","generator":"v02 QA fixture"},
        "scene":0,"scenes":[{"nodes":[1]}],
        "nodes":[{"name":"DoorHandle","mesh":0},{"name":"Door","children":[0],"extras":extras}],
        "meshes":[{"name":"Handle","primitives":[{"attributes":{"POSITION":6},"material":2}]},
                  {"name":"TwoMaterialLeaf","primitives":copy.deepcopy(PRIMS[:nprimitives])}],
        "materials":[{"name":"TimberPBR"},{"name":"IronPBR"},{"name":"BrassHandle"}],
        "buffers":[{"byteLength":len(BIN)}]
    }
    if mesh_node:doc["nodes"][1]["mesh"]=1
    if animated:doc["animations"]=[{"channels":[],"samplers":[]}]
    write_glb(file,doc)
    return doc

def write_glb(path, doc, blob=BIN):
    raw=json.dumps(doc,separators=(",",":")).encode()
    raw+=b" "*((-len(raw))%4)
    total=12+8+len(raw)+8+len(blob)
    path.write_bytes(b"glTF"+struct.pack("<II",2,total)
                     +struct.pack("<II",len(raw),0x4e4f534a)+raw
                     +struct.pack("<II",len(blob),0x004e4942)+blob)

def read_glb(path):
    b=path.read_bytes()
    sz=struct.unpack_from("<I",b,12)[0]
    return json.loads(b[20:20+sz]),b[-len(BIN):]

class NativeDoorGLBTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="acq_native_door_test_")
        self.addCleanup(self.temp.cleanup)
        self.file=pathlib.Path(self.temp.name)/"qa-door.glb"

    def test_two_material_leaf_is_single_tagged_mesh_plus_secondary_child(self):
        original=make_glb(self.file)
        before_binary=self.file.read_bytes()[-len(BIN):]
        r=normalize_native_model_door_glb(self.file)
        doc,after_binary=read_glb(self.file)
        self.assertTrue(r["normalized"])
        self.assertEqual(r["child_nodes_added"],1)
        self.assertEqual(after_binary,before_binary)
        leaf=doc["nodes"][1]
        self.assertTrue(leaf["extras"]["isDoor"])
        self.assertEqual(leaf["extras"]["doorId"],"qa-ramp-v01-upper-door")
        self.assertEqual(leaf["children"][0],0)  # actual DoorHandle preserved
        self.assertEqual(len(leaf["children"]),2)
        self.assertEqual(doc["meshes"][1]["primitives"],[PRIMS[0]])
        child=doc["nodes"][leaf["children"][1]]
        self.assertEqual(doc["meshes"][child["mesh"]]["primitives"],[PRIMS[1]])
        self.assertTrue(child["extras"]["acq_door_attachment"])
        self.assertNotIn("isDoor",child["extras"])
        self.assertEqual(doc["materials"],original["materials"])

    def test_already_single_primitive_is_byte_identical(self):
        make_glb(self.file,nprimitives=1)
        orig=self.file.read_bytes()
        r=normalize_native_model_door_glb(self.file)
        self.assertFalse(r["normalized"])
        self.assertEqual(orig,self.file.read_bytes())

    def test_three_material_leaf_retains_all_material_primitives(self):
        extra={"attributes":{"POSITION":8},"indices":9,"material":2}
        orig=make_glb(self.file)
        orig["meshes"][1]["primitives"].append(extra)
        write_glb(self.file,orig)
        result=normalize_native_model_door_glb(self.file)
        doc,binary=read_glb(self.file)
        self.assertEqual(result["child_nodes_added"],2)
        self.assertEqual(len(doc["nodes"][1]["children"]),3)
        self.assertEqual(binary,BIN)
        self.assertEqual([doc["meshes"][1]["primitives"][0]]+
            [doc["meshes"][doc["nodes"][n]["mesh"]]["primitives"][0] for n in doc["nodes"][1]["children"][1:]],
            orig["meshes"][1]["primitives"])

    def test_reject_missing_mesh_for_tagged_door(self):
        make_glb(self.file,mesh_node=False)
        with self.assertRaisesRegex(RuntimeError,"mesh"):
            normalize_native_model_door_glb(self.file)

    def test_reject_animation_without_mutation(self):
        make_glb(self.file,animated=True)
        old=self.file.read_bytes()
        with self.assertRaisesRegex(RuntimeError,"Animated"):
            normalize_native_model_door_glb(self.file)
        self.assertEqual(old,self.file.read_bytes())

    def test_reject_missing_door_tag(self):
        make_glb(self.file,door_extras={"acq_role":"door_leaf"})
        with self.assertRaisesRegex(RuntimeError,"One tagged Mesh"):
            normalize_native_model_door_glb(self.file)

    def test_reject_bad_binary_header(self):
        self.file.write_bytes(b"not a GLB")
        with self.assertRaisesRegex(RuntimeError,"header"):
            normalize_native_model_door_glb(self.file)

    def test_reject_preexisting_temporary_output(self):
        make_glb(self.file)
        self.file.with_suffix(".glb.nativepart").write_bytes(b"collision")
        before=self.file.read_bytes()
        with self.assertRaisesRegex(RuntimeError,"already exists"):
            normalize_native_model_door_glb(self.file)
        self.assertEqual(before,self.file.read_bytes())

if __name__=="__main__":
    unittest.main()
