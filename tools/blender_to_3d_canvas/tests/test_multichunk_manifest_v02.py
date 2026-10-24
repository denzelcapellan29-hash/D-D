"""No-art, metadata-only negative tests for v0.2 bundle validation.

The GLB fixtures contain a JSON mesh declaration but NO position/vertex
buffers and therefore cannot render visible geometry. Tests never call
Foundry, write project Scenes, use vendor assets, or charge Meshy credits.
"""
import copy
import hashlib
import json
import pathlib
import struct
import sys
import tempfile
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from import_chunks_v02 import verify

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def fake_glb(p):
    # GLB2 metadata only: no vertices, triangles, buffers or renderable mesh.
    body=json.dumps({"asset":{"version":"2.0"},
                     "nodes":[{"name":"Unit test metadata"}],
                     "meshes":[{"name":"No renderable primitive"}],
                     "materials":[]}).encode()
    body+=b" "*((-len(body))%4)
    p.write_bytes(struct.pack("<4sIII4s",b"glTF",2,20+len(body),
                              len(body),b"JSON")+body)

def identity():
    return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]

class ManifestV02UnitTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=pathlib.Path(self.tmp.name)
        self.source=self.root/"qa-fixture.blend"
        self.source.write_bytes(b"Metadata-only dummy source, not Blender geometry")
        self.bundle=self.root/"bundle"
        self.bundle.mkdir()
        chunks=[]
        for cid in ("static","interactive"):
            p=self.bundle/(cid+".glb")
            fake_glb(p)
            obj={"name":"Mock "+cid,"source_parent":None,
                 "source_matrix_world_rowmajor":identity(),
                 "native_door_extras":{"doorId":"qa"} if cid=="interactive" else {}}
            chunks.append({"chunk_id":cid,
                "kind":cid if cid=="static" else "interactive",
                "interactive_door":cid=="interactive",
                "rigid_assembly":False,
                "asset":{"filename":p.name,"sha256":sha(p),"bytes":p.stat().st_size},
                "source_bounds_m":{"min":[0,0,0],"max":[1,1,1]},
                "tile_center_xy_px":[1920,960],
                "tile_elevation_scene_units":0,
                "expected_tile_footprint_px":[75,75],
                "expected_tile_depth_px":75,
                "source_objects":[obj]})
        self.doc={"schema":"acq.blender-3dcanvas.multichunk.v0.2",
          "bundle":"unit-test","source_blend":str(self.source),
          "source_blend_sha256":sha(self.source),
          "source_blend_bytes":self.source.stat().st_size,
          "foundry":{"pixels_per_blender_meter":75,"scene_grid_size_px":100,
                     "scene_grid_distance":1,"native_3d_tile_scale":0.75},
          "chunks":chunks}
        self.flush()

    def tearDown(self):
        self.tmp.cleanup()

    def flush(self):
        (self.bundle/"manifest.json").write_text(json.dumps(self.doc))

    def assert_rejected(self,expected):
        self.flush()
        with self.assertRaisesRegex(Exception,expected):
            verify(self.bundle)

    def test_positive_metadata(self):
        doc,rows=verify(self.bundle)
        self.assertEqual(len(rows),2)
        self.assertEqual([r["chunk_id"] for r in rows],["static","interactive"])

    def test_duplicate_chunk_id(self):
        self.doc["chunks"][1]["chunk_id"]="static"
        self.assert_rejected("duplicate chunk")

    def test_corrupted_glb_hash(self):
        self.doc["chunks"][0]["asset"]["sha256"]="0"*64
        self.assert_rejected("hash/length mismatch")

    def test_changed_source_blend(self):
        self.doc["source_blend_sha256"]="0"*64
        self.assert_rejected("Source .blend changed")

    def test_incorrect_elevation(self):
        self.doc["chunks"][0]["tile_elevation_scene_units"]=12.5
        self.assert_rejected("Elevation anchor")

    def test_path_traversal(self):
        self.doc["chunks"][0]["asset"]["filename"]="../escape.glb"
        self.assert_rejected("Unsafe GLB filename")

    def test_wrong_world_matrix(self):
        self.doc["chunks"][0]["source_objects"][0]["source_matrix_world_rowmajor"]=[1]*15
        self.assert_rejected("Invalid authored world transform")

    def test_non_rigid_multi_mesh_interactive(self):
        obj=copy.deepcopy(self.doc["chunks"][1]["source_objects"][0])
        self.doc["chunks"][1]["source_objects"].append(obj)
        self.assert_rejected("explicit rigid_assembly")

    def test_scale_mismatch(self):
        self.doc["foundry"]["native_3d_tile_scale"]=7.5
        self.assert_rejected("Inconsistent Foundry native scale")

if __name__=="__main__":
    unittest.main()
