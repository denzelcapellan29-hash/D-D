"""Unit tests of native internal GLB door state and role flags; no RPC or Scene writes."""
import copy
import pathlib
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from import_chunks_v02 import native_candidates, semantic_flags

def source(role, interactive=False, style=1):
    extras={"isDoor": True, "doorId":"qa-hinge", "doorStyle":style, "doorState":0} if interactive else {}
    ob={"name":"Leaf" if interactive else "Floor","acq_role":role,
        "native_door_extras":extras}
    return {"chunk_id":"leaf" if interactive else "floor",
            "interactive_door":interactive,
            "source_objects":[ob]}

def run_case(interactive, style=1):
    item=source("door_leaf" if interactive else "walkable_floor",interactive,style)
    _,flags=semantic_flags(item)
    row={"chunk_id":item["chunk_id"],"interactive_door":interactive,
         "semantic_flags":flags,"foundry_path":"modules/test/qa-fixture.glb",
         "tile_center_xy_px":[1920,960],"tile_elevation":0,
         "expected_dimensions_px":[100,80,25]}
    candidate={"x":1,"y":1,"width":100,"height":80,"elevation":0,
        "flags":{"levels-3d-preview":{"depth":25,
             "collision":flags[0],"sight":flags[1],"cameraCollision":flags[2]}}}
    with patch("import_chunks_v02.call",return_value=({},{"candidate":candidate})) as mock:
        got=native_candidates([row],{"foundry":{"native_3d_tile_scale":1},"chunks":[item]},"revision")
    return got[0],mock.call_args_list

class EmbeddedModelDoorV02(unittest.TestCase):
    def test_hinged_door_uses_modelDoors_not_whole_tile(self):
        c,_=run_case(True)
        f=c["flags"]["levels-3d-preview"]
        self.assertEqual(f["modelDoors"],{"qa-hinge":{"ds":0}})
        self.assertEqual(f["fillType"],"fit")
        self.assertTrue(f["collision"])
        self.assertTrue(f["sight"])
        for name in ("doorType","doorState","doorStyle"):
            self.assertNotIn(name,f)

    def test_floor_intent_passes_to_native_preview(self):
        c,calls=run_case(False)
        f=c["flags"]["levels-3d-preview"]
        self.assertEqual((f["collision"],f["sight"],f["cameraCollision"]),(True,False,False))
        op=calls[0].args[1]
        self.assertEqual((op["collision"],op["sight"],op["camera_collision"]),(True,False,False))
        self.assertNotIn("modelDoors",f)

    def test_non_hinged_model_door_rejected(self):
        with self.assertRaisesRegex(RuntimeError,"hinged"):
            run_case(True,style=0)

if __name__=="__main__":
    unittest.main()
