"""Offline regression of source-preserving GLB multi-primitive native-door split."""
import ast
import json
import pathlib
import struct
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]

def load_normalizer():
    source=(ROOT/"export_chunks_v02.py").read_text(encoding="utf8")
    parsed=ast.parse(source)
    fn=[n for n in parsed.body if isinstance(n,ast.FunctionDef)
        and n.name=="normalize_native_model_door_glb"]
    if len(fn)!=1:
        raise AssertionError("Native door GLB normalizer must exist exactly once")
    compiled=compile(ast.Module(body=fn,type_ignores=[]),
                     str(ROOT/"export_chunks_v02.py"),"exec")
    space={"pathlib":pathlib,"json":json}
    exec(compiled,space)
    return space["normalize_native_model_door_glb"]

NORMALIZE=load_normalizer()

def encode(gltf,binary=b"\x01\x02\x03\x04"):
    data=json.dumps(gltf,separators=(",",":")).encode()
    data+=b" "*((-len(data))%4)
    assert len(binary)%4==0
    return (b"glTF"+struct.pack("<II",2,12+8+len(data)+8+len(binary))+
            struct.pack("<II",len(data),0x4e4f534a)+data+
            struct.pack("<II",len(binary),0x004e4942)+binary)

def decode(raw):
    assert struct.unpack_from("<4sII",raw,0)==(b"glTF",2,len(raw))
    n=struct.unpack_from("<I",raw,12)[0]
    gltf=json.loads(raw[20:20+n])
    off=20+n
    bin_length,bin_type=struct.unpack_from("<II",raw,off)
    assert bin_type==0x004e4942
    return gltf,raw[off+8:off+8+bin_length]

def fixture(primitives=2, tagged=True, animations=False):
    door_primitive=[
        {"attributes":{"POSITION":0},"indices":0,"material":0},
        {"attributes":{"POSITION":1},"indices":1,"material":1},
    ][:primitives]
    d={"asset":{"version":"2.0"},
       "meshes":[
          {"name":"DoorPanel","primitives":door_primitive},
          {"name":"Handle","primitives":[{"attributes":{"POSITION":2},"indices":2,"material":2}]}
       ],
       "nodes":[
          {"name":"DoorHandle","mesh":1},
          {"name":"Door","mesh":0,"children":[0],
           "extras":{"isDoor":True,"doorId":"qa-hinge","doorStyle":1} if tagged else {}}
       ],
       "scenes":[{"nodes":[1]}],"scene":0,"materials":[{"name":"wood"},{"name":"metal"},{"name":"handle"}],
       "buffers":[{"byteLength":4}]}
    if animations:d["animations"]=[{"name":"not-approved"}]
    return d

class NativeDoorPrimitiveNormalization(unittest.TestCase):
    def with_glb(self,fixture_doc):
        d=tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        p=pathlib.Path(d.name)/"door.glb"
        p.write_bytes(encode(fixture_doc))
        return p

    def test_preserves_all_primitives_and_binary_under_tagged_mesh(self):
        src=fixture(2)
        path=self.with_glb(src)
        report=NORMALIZE(path)
        self.assertEqual(report["primitives"],2)
        self.assertTrue(report["normalized"])
        gltf,binary=decode(path.read_bytes())
        self.assertEqual(binary,b"\x01\x02\x03\x04")
        door=gltf["nodes"][1]
        self.assertEqual(door["mesh"],0)
        self.assertEqual(door["extras"]["isDoor"],True)
        self.assertEqual(door["children"],[0,2])
        self.assertEqual(len(gltf["meshes"][0]["primitives"]),1)
        self.assertEqual(gltf["meshes"][0]["primitives"][0],src["meshes"][0]["primitives"][0])
        child=gltf["nodes"][2]
        self.assertNotIn("isDoor",child["extras"])
        self.assertEqual(gltf["meshes"][child["mesh"]]["primitives"],[src["meshes"][0]["primitives"][1]])
        self.assertEqual(gltf["materials"],src["materials"])

    def test_single_primitive_does_not_rewrite_glb(self):
        path=self.with_glb(fixture(1))
        before=path.read_bytes()
        self.assertFalse(NORMALIZE(path)["normalized"])
        self.assertEqual(path.read_bytes(),before)

    def test_second_normalization_is_idempotent(self):
        path=self.with_glb(fixture(2))
        NORMALIZE(path)
        once=path.read_bytes()
        self.assertFalse(NORMALIZE(path)["normalized"])
        self.assertEqual(once,path.read_bytes())

    def test_untagged_door_rejected(self):
        path=self.with_glb(fixture(2,tagged=False))
        with self.assertRaisesRegex(RuntimeError,"tagged"):
            NORMALIZE(path)

    def test_animated_split_rejected(self):
        path=self.with_glb(fixture(2,animations=True))
        with self.assertRaisesRegex(RuntimeError,"Animated"):
            NORMALIZE(path)

    def test_duplicate_door_nodes_rejected(self):
        d=fixture(2)
        d["nodes"].append({"name":"DoorSecond","mesh":0,"extras":{"isDoor":True,"doorId":"another"}})
        path=self.with_glb(d)
        with self.assertRaisesRegex(RuntimeError,"One tagged"):
            NORMALIZE(path)

if __name__=="__main__":
    unittest.main()
