"""Pure offline guard tests. No real Blender, Foundry, network, or geometry."""
from __future__ import annotations
import copy
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from reconcile_chunks_v02 import prepare_plan,update_payload,stage_log

class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.doc={"bundle":"test-build","source_blend":"X:/unchanged_fixture.blend"}
        self.rows=[{"chunk_id":"first","semantic_id":"qa:multichunk:test-build:first",
                    "glb_file":"ignored","glb_sha256":"a"*64}]
        self.candidate={"x":1200,"y":1300,"width":150,"height":70,
                        "elevation":0.1,"rotation":0,
                        "flags":{"levels-3d-preview":{"model3d":"modules/qa/chunk.glb",
                                  "collision":True,"sight":True,
                                  "cameraCollision":True,"color":"#ffffff"}}}
        self.existing={"id":"testTile123","x":1200,"y":1300,"width":150,
                       "height":70,"elevation":0.1,"rotation":0,
                       "runtime_bounds":{"center":{"x":1.2,"y":0.1,"z":1.3}},
                       "flags":self.candidate["flags"]["levels-3d-preview"].copy(),
                       "acq":{"semantic_id":self.rows[0]["semantic_id"],
                             "classification":"QA_ONLY_MULTICHUNK_V02",
                             "build_id":"test-build",
                             "provenance":{"asset_sha256":"a"*64,
                                           "source":self.doc["source_blend"]}}}

    def plan(self,items,shift=0):
        return prepare_plan(self.doc,self.rows,[self.candidate],
                            {"tiles":items},shift,0)

    def test_new_create(self):
        p=self.plan([])[0]
        self.assertEqual(p["action"],"create")
        self.assertEqual(p["desired"]["x"],1200)

    def test_existing_identical_noop(self):
        p=self.plan([self.existing])[0]
        self.assertEqual(p["action"],"noop")
        self.assertEqual(p["changes"]["scalars"],{})

    def test_update_snapshots_only_changed_field(self):
        p=self.plan([self.existing],3)[0]
        self.assertEqual(p["action"],"update")
        self.assertEqual(p["changes"]["scalars"],{"x":1203})
        self.assertEqual(p["backup"]["scalars"],{"x":1200})
        self.assertEqual(p["backup"]["flags"],{})

    def test_update_preserves_unmanaged_fields(self):
        p=self.plan([self.existing],3)[0]
        update=update_payload(self.existing["id"],**{
            "scalars":p["changes"]["scalars"],
            "flags":p["changes"]["flags"],
            "provenance":p["changes"]["provenance"]})
        self.assertEqual(update,{"_id":"testTile123","x":1203})

    def test_wrong_classification_rejected(self):
        fake=copy.deepcopy(self.existing)
        fake["acq"]["classification"]="NOT_OUR_ASSET"
        with self.assertRaisesRegex(Exception,"unowned"):
            self.plan([fake])

    def test_ambiguous_duplicates_rejected(self):
        second=copy.deepcopy(self.existing)
        second["id"]="otherTile987"
        with self.assertRaisesRegex(Exception,"Duplicate"):
            self.plan([self.existing,second])

    def test_runtime_missing_rejected(self):
        fake=copy.deepcopy(self.existing)
        fake["runtime_bounds"]=None
        with self.assertRaisesRegex(Exception,"unloaded"):
            self.plan([fake])

    def test_unsnapshotable_new_flag_rejected(self):
        fake=copy.deepcopy(self.existing)
        fake["flags"].pop("collision")
        with self.assertRaisesRegex(Exception,"snapshot"):
            self.plan([fake])

    def test_journal_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/"tx.json"
            stage_log(p,{"status":"START"})
            with self.assertRaisesRegex(Exception,"journal exists"):
                stage_log(p,{"status":"NEXT"})

if __name__=="__main__":
    unittest.main()
