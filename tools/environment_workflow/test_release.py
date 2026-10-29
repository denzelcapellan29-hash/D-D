"""Release-policy tests use mock reports; they are not GLB/native evidence."""
import copy,json,tempfile,unittest
from pathlib import Path
import architecture as engine
import workflow

class ReleasePolicy(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='workflow-policy-test-',dir=Path.cwd());self.root=Path(self.tmp.name).resolve()
        if not self.root.is_relative_to(Path.cwd().resolve()): raise ValueError('Test cleanup must stay within the working directory')
        self.addCleanup(self.tmp.cleanup)
        s=json.loads((Path(__file__).parent/'connected_example.json').read_text());self.a=engine.compile_plan(s)
        self.write('source.json',s);self.write('export/assembly.json',self.a)
        self.write('recipe.json',{'code':{n:workflow.sha(Path(workflow.__file__).parent/n)for n in workflow.CODE}})
        self.write('export/export_qa.json',{'ok':True,'families':[{'ok':True}]})
        (self.root/'export/mock.glb').write_bytes(b'NOT A REAL GLB: POLICY TEST ONLY')
        asset_hash=workflow.sha(self.root/'export/mock.glb')
        self.manifest={'spec_sha256':engine.digest(s),'generator_sha256':self.a['generator_sha256'],'adapter_sha256':workflow.sha(Path(workflow.__file__).parent/'export_blender.py'),'parts':[{**p,'asset':'mock.glb','asset_sha256':asset_hash}for p in self.a['parts']],'families':[{'file':'mock.glb','sha256':asset_hash}]}
        self.write('export/manifest.json',self.manifest)
    def write(self,path,value):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value))
    def test_unreviewed_never_ready(self):
        r=workflow.audit(self.root);self.assertFalse(r['ready_for_play']);self.assertEqual(r['gates']['NATIVE'],'UNVERIFIED')
    def test_stale_geometry_file_detected(self):
        (self.root/'export/mock.glb').write_bytes(b'changed');self.assertTrue(workflow.audit(self.root)['failures'])
    def test_placement_bounds_mismatch_detected(self):
        self.manifest['parts'][0]['bounds']=copy.deepcopy(self.manifest['parts'][0]['bounds']);self.manifest['parts'][0]['bounds'][0][0]+=.01;self.write('export/manifest.json',self.manifest);self.assertTrue(workflow.audit(self.root)['failures'])
    def test_stale_attestation_rejected(self):
        self.write('evidence/reviews.json',{'ART':{'status':'PASS','bundle_sha256':'old','reviewer':'tester','basis':'mock','artifacts':[{'path':'source.json','sha256':workflow.sha(self.root/'source.json')}]}})
        self.assertEqual(workflow.audit(self.root)['gates']['ART'],'UNVERIFIED')
    def test_native_inventory_only_insufficient(self):
        f=engine.digest(workflow.inventory(self.root));self.write('evidence/reviews.json',{'NATIVE':{'status':'PASS','bundle_sha256':f,'reviewer':'tester','basis':'inventory only','artifacts':[{'path':'source.json','sha256':workflow.sha(self.root/'source.json')}],'features_verified':[v['id']for v in self.a['features']]}})
        self.assertEqual(workflow.audit(self.root)['gates']['NATIVE'],'UNVERIFIED')
    def test_existing_revision_never_overwritten(self):
        with self.assertRaises(ValueError):workflow.build(self.root/'source.json',self.root,'not-invoked')

if __name__=='__main__':unittest.main()
