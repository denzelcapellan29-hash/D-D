"""Offline deterministic tests for fail-closed native Tile recovery classification."""
import copy
import pathlib
import sys
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from recover_chunks_v02 import entry_state,assert_exclusive_inventory

class UnknownRpcRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.source="X:/source.blend"
        self.sid="qa:multichunk:bundle:first"
        self.old={"id":"oldTile","x":40,"y":30,"width":100,"height":120,
                  "elevation":0.1,"rotation":0,"hidden":False,
                  "flags":{"model3d":"old.glb","color":"#ffffff","collision":True},
                  "acq":{"semantic_id":self.sid,"classification":"QA_ONLY_MULTICHUNK_V02",
                         "build_id":"bundle","provenance":{"source":self.source,"asset_sha256":"a"}}}
        self.update={
          "action":"update","semantic_id":self.sid,
          "backup":{"id":"oldTile","semantic_id":self.sid,
                    "scalars":{"x":40},"flags":{"model3d":"old.glb"},
                    "provenance":None},
          "desired_managed":{"scalars":{"x":43},"flags":{"model3d":"new.glb"},
                 "provenance":{"source":self.source,"asset_sha256":"a"},
                 "build_id":"bundle","classification":"QA_ONLY_MULTICHUNK_V02"}}
        self.create={
          "action":"create","semantic_id":"qa:multichunk:bundle:new",
          "backup":None,
          "desired_managed":{"scalars":{"x":99,"y":120},
                             "flags":{"model3d":"new.glb"},
                             "provenance":{"source":self.source,"asset_sha256":"a"},
                             "build_id":"bundle","classification":"QA_ONLY_MULTICHUNK_V02"}}
        self.before={"id":"orig","x":4,"y":5,"width":100,"height":100,
                     "elevation":0,"rotation":0,"hidden":False,
                     "flags":{"model3d":"ground.glb","collision":True},
                     "acq":{"semantic_id":"other","build_id":"other","classification":"old"}}
        self.log={"owned_semantics":[self.sid,self.create["semantic_id"]],
                  "completed":[],"pending":self.create,
                  "baseline_inventory":{"tiles":[self.old,self.before],
                                        "tile_count":2,"light_count":2,"region_count":3}}
    def test_unknown_create_not_applied(self):
        self.assertEqual(entry_state(self.create,None,None),"BEFORE")
    def test_unknown_create_applied(self):
        tile={"id":"created","x":99,"y":120,"flags":{"model3d":"new.glb"},
              "runtime_bounds":{"size":{"x":1}},
              "acq":{"semantic_id":self.create["semantic_id"],
                     "build_id":"bundle","classification":"QA_ONLY_MULTICHUNK_V02",
                     "provenance":{"source":self.source,"asset_sha256":"a"}}}
        self.assertEqual(entry_state(self.create,tile,None),"APPLIED")
    def test_unknown_create_wrong_provenance_rejected(self):
        tile={"id":"foreign","x":99,"y":120,"flags":{"model3d":"new.glb"},
              "runtime_bounds":{"size":{"x":1}},
              "acq":{"semantic_id":self.create["semantic_id"],
                     "build_id":"bundle","classification":"QA_ONLY_MULTICHUNK_V02",
                     "provenance":{"source":"OTHER","asset_sha256":"a"}}}
        with self.assertRaisesRegex(Exception,"Untrusted"):
            entry_state(self.create,tile,None)
    def test_update_not_applied(self):
        self.assertEqual(entry_state(self.update,self.old,self.old),"BEFORE")
    def test_update_applied(self):
        tile=copy.deepcopy(self.old);tile["x"]=43;tile["flags"]["model3d"]="new.glb"
        self.assertEqual(entry_state(self.update,tile,self.old),"APPLIED")
    def test_update_partial_rejected(self):
        tile=copy.deepcopy(self.old);tile["x"]=43
        with self.assertRaisesRegex(Exception,"Partial"):
            entry_state(self.update,tile,self.old)
    def test_unrelated_tile_change_rejected(self):
        bad=copy.deepcopy(self.before);bad["y"]=12
        scene={"tiles":[copy.deepcopy(self.old),bad],"tile_count":2,
               "light_count":2,"region_count":3}
        with self.assertRaisesRegex(Exception,"Unrelated"):
            assert_exclusive_inventory(self.log,scene)
    def test_foreign_created_tile_rejected(self):
        extra=copy.deepcopy(self.before);extra["id"]="foreignTile"
        scene={"tiles":[copy.deepcopy(self.old),copy.deepcopy(self.before),extra],
               "tile_count":3,"light_count":2,"region_count":3}
        with self.assertRaisesRegex(Exception,"Foreign Tile"):
            assert_exclusive_inventory(self.log,scene)
    def test_other_document_counts_rejected(self):
        scene={"tiles":[copy.deepcopy(self.old),copy.deepcopy(self.before)],
               "tile_count":2,"light_count":3,"region_count":3}
        with self.assertRaisesRegex(Exception,"Non-Tile"):
            assert_exclusive_inventory(self.log,scene)

if __name__=="__main__":unittest.main()
