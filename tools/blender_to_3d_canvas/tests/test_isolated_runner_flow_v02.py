"""Offline isolated QA runner control-plane regression tests.

Uses mocked first-party RPC replies; NEVER connects to Foundry, edits Scenes,
or calls Blender. Run with: python -m unittest discover -s tests -p 'test_isolated_runner_flow_v02.py'
"""
import pathlib
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
import run_isolated_qa_v02 as qa

SOURCE=qa.PROTECTED_SCENE
SHA=qa.PROTECTED_SHA
QA="test-owned-inactive-scene"
BASELINE="test-initial-empty-revision"
LOADED="test-seven-loaded-revision"

def state(view=SOURCE, owned=True):
    return {"qa_scene_id":QA,"qa_owned":owned,"qa_exists":True,
            "qa_empty":True,"source_revision":SHA,
            "foundry_active_scene_id":SOURCE,
            "gm_viewed_scene_id":view,"players_pulled":False,
            "qa_revision":BASELINE,
            "qa_counts":{k:0 for k in qa.REQUIRED_COUNTS}}

def args():
    return SimpleNamespace(bundle_dir=pathlib.Path("inert"),
                           asset_root=pathlib.Path("inert-root"),
                           live=True,retain_import=False,restore_view_only=False)

def manifest():
    return {"bundle":"qa-twolevel-library-v02",
            "source_blend":"X:/readonly-source.blend",
            "source_blend_sha256":"a"*64}

def chunks():
    return [{"chunk_id":key,
             "semantic_id":"qa:multichunk:qa-twolevel-library-v02:"+key,
             "glb_sha256":"b"*64}
            for key in sorted(qa.REQUIRED_CHUNKS)]

class IsolatedRunnerTests(unittest.TestCase):
    def test_restore_view_only_from_owned_scene(self):
        calls=[]
        def rpc(scene, op, dry, *extra, **kw):
            calls.append((scene,op["action"]))
            if op["action"]=="inspect":
                return ({"after_revision":SHA},
                        state(QA if len(calls)==1 else SOURCE))
            self.assertEqual((scene,op["action"]),(QA,"restore_view"))
            return ({"after_revision":SHA},
                    {"now_viewed":SOURCE,"players_pulled":False})
        with patch.object(qa,"call",side_effect=rpc):
            result=qa.restore_gm_if_needed()
        self.assertEqual(result["stage"],"GM_ORIGINAL_VIEW_RESTORED")
        self.assertEqual([x[1] for x in calls],["inspect","restore_view","inspect"])

    def test_already_viewing_source_is_no_write(self):
        with patch.object(qa,"call",return_value=({"after_revision":SHA},state())) as rpc:
            result=qa.restore_gm_if_needed()
        self.assertEqual(result["stage"],"ALREADY_VIEWING_ORIGINAL")
        self.assertEqual(rpc.call_count,1)

    def test_foreign_view_never_restored(self):
        with patch.object(qa,"call",return_value=({"after_revision":SHA},state("other-scene"))):
            with self.assertRaisesRegex(RuntimeError,"unrelated Scene"):
                qa.restore_gm_if_needed()

    def test_wrong_source_revision_blocks_view_recovery(self):
        invalid=state(QA);invalid["source_revision"]="different"
        with patch.object(qa,"call",return_value=({"after_revision":SHA},invalid)):
            with self.assertRaisesRegex(RuntimeError,"exact owned"):
                qa.restore_gm_if_needed()

    def test_complete_seven_tile_import_and_exact_cleanup(self):
        def rpc(scene,op,*pos,**kw):
            if op["op"]=="capture_3d_view":
                return ({"after_revision":LOADED},{"image_base64":"nonempty-capture"})
            if op["op"]=="inspect_3d_scene":
                return ({"after_revision":BASELINE},{"tile_count":0})
            if op["op"]=="manage_empty_qa_scene" and op["action"]=="view":
                return ({"after_revision":SHA},{"now_viewed":QA,"players_pulled":False})
            raise AssertionError("Unanticipated mock RPC "+str(op))
        rows=chunks()
        with patch.object(qa,"verify",return_value=(manifest(),rows)), \
             patch.object(qa,"provision",return_value=(QA,False)), \
             patch.object(qa,"owned_inspect",side_effect=[state(),state()]), \
             patch.object(qa,"call",side_effect=rpc), \
             patch.object(qa,"import_once",return_value=(LOADED,[{} for _ in rows])) as importer, \
             patch.object(qa,"cleanup",return_value=BASELINE) as cleaner, \
             patch.object(qa,"view_original",return_value={"now_viewed":SOURCE}) as restore:
            result=qa.execute(args())
        self.assertTrue(result["empty_revision_restored"])
        self.assertTrue(result["gm_view_restored"])
        self.assertEqual(result["chunks"],7)
        self.assertEqual(importer.call_count,1)
        self.assertEqual(cleaner.call_count,1)
        self.assertEqual(restore.call_count,1)

    def test_cleanup_checksum_drift_is_error_but_view_restored(self):
        def rpc(scene,op,*pos,**kw):
            if op["op"]=="capture_3d_view":
                return ({"after_revision":LOADED},{"image_base64":"nonempty"})
            if op["op"]=="inspect_3d_scene":
                return ({"after_revision":BASELINE},{"tile_count":0})
            if op["action"]=="view":
                return ({"after_revision":SHA},{"now_viewed":QA,"players_pulled":False})
            raise AssertionError(str(op))
        rows=chunks()
        with patch.object(qa,"verify",return_value=(manifest(),rows)), \
             patch.object(qa,"provision",return_value=(QA,False)), \
             patch.object(qa,"owned_inspect",return_value=state()), \
             patch.object(qa,"call",side_effect=rpc), \
             patch.object(qa,"import_once",return_value=(LOADED,[{} for _ in rows])), \
             patch.object(qa,"cleanup",return_value="WRONG_BASELINE"), \
             patch.object(qa,"view_original",return_value={"now_viewed":SOURCE}) as restore:
            with self.assertRaisesRegex(RuntimeError,"exact baseline"):
                qa.execute(args())
        restore.assert_called_once()

    def test_failure_before_creation_restores_view(self):
        def rpc(scene,op,*pos,**kw):
            if op["op"]=="capture_3d_view":
                raise RuntimeError("renderer unavailable")
            if op["action"]=="view":
                return ({"after_revision":SHA},{"now_viewed":QA,"players_pulled":False})
            raise AssertionError(str(op))
        with patch.object(qa,"verify",return_value=(manifest(),chunks())), \
             patch.object(qa,"provision",return_value=(QA,False)), \
             patch.object(qa,"owned_inspect",return_value=state()), \
             patch.object(qa,"call",side_effect=rpc), \
             patch.object(qa,"import_once") as imp, \
             patch.object(qa,"view_original") as restore:
            with self.assertRaisesRegex(RuntimeError,"renderer unavailable"):
                qa.execute(args())
        imp.assert_not_called()
        restore.assert_called_once()

    def test_foreign_preexisting_tile_never_imported_over(self):
        altered=state();altered["qa_empty"]=False
        with patch.object(qa,"verify",return_value=(manifest(),chunks())), \
             patch.object(qa,"provision",return_value=(QA,False)), \
             patch.object(qa,"owned_inspect",return_value=altered), \
             patch.object(qa,"call") as rpc:
            with self.assertRaisesRegex(RuntimeError,"totally empty"):
                qa.execute(args())
        rpc.assert_not_called()

if __name__=="__main__":
    unittest.main()
