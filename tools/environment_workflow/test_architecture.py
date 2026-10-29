import copy,json,tempfile,unittest
from pathlib import Path
import architecture as engine

class AssemblyRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=json.loads((Path(__file__).parent/'connected_example.json').read_text());cls.assembly=engine.compile_plan(cls.spec)
    def test_whole_connected_fixture(self):
        r=engine.check_assembly(self.spec,self.assembly);self.assertTrue(r['ok'],r['failures'][:3]);self.assertGreater(r['counts']['wall'],1000)
    def test_repeatable(self):self.assertEqual(self.assembly,engine.compile_plan(self.spec))
    def test_full_floor_is_shared_standard_size(self):
        full=[p for p in self.assembly['parts']if p['role']=='floor'and abs(p['bounds'][1][0]-p['bounds'][0][0]-1.524)<1e-6 and abs(p['bounds'][1][1]-p['bounds'][0][1]-1.524)<1e-6];self.assertGreater(len(full),10);self.assertEqual(len({p['family']for p in full}),1)
    def mutate(self,predicate):
        a=copy.deepcopy(self.assembly);a['parts']=[p for p in a['parts']if not predicate(p)];return a
    def test_missing_floor_detected(self):
        r=engine.check_assembly(self.spec,self.mutate(lambda p:p['area']=='lower'and p['role']=='floor'));self.assertFalse(r['ok']);self.assertTrue(any(f['kind']=='floor'for f in r['failures']))
    def test_upper_enclosure_return_detected(self):
        a=self.mutate(lambda p:p['role']=='wall'and p['area']=='flight'and p['bounds'][1][0]<=6.401 and p['bounds'][0][2]>3)
        r=engine.check_assembly(self.spec,a);self.assertFalse(r['ok']);self.assertTrue(any(f['kind']=='wall'for f in r['failures']))
    def test_missing_tread_detected(self):
        a=self.mutate(lambda p:p['area']=='flight'and 'step3'in p['id']);r=engine.check_assembly(self.spec,a);self.assertFalse(r['ok']);self.assertTrue(any(f['kind']=='floor'for f in r['failures']))
    def test_obstructed_portal_detected(self):
        a=copy.deepcopy(self.assembly);a['parts'].append({'id':'deliberate.obstruction','area':'flight','role':'wall','bounds':[[6.1,2.44,0],[6.4,3.65,2.4]],'family':'negative'});r=engine.check_assembly(self.spec,a);self.assertFalse(r['ok']);self.assertTrue(any(f['kind']=='portal_clearance'for f in r['failures']))
    def test_body_can_fail_when_center_ray_is_clear(self):
        a=copy.deepcopy(self.assembly);a['parts'].append({'id':'deliberate.body-edge-obstruction','area':'lower','role':'wall','bounds':[[2,3.2,0],[2.3,3.3,2.5]],'family':'negative'});self.assertFalse(engine.check_assembly(self.spec,a)['ok'])
    def test_feature_inventory_loss_detected(self):
        a=copy.deepcopy(self.assembly);a['features']=[];self.assertFalse(engine.check_assembly(self.spec,a)['ok'])
    def test_stale_spec_detected(self):
        s=copy.deepcopy(self.spec);s['spaces'][0]['ceiling']+=.2;self.assertFalse(engine.check_assembly(s,self.assembly)['ok'])
    def test_body_size_contract(self):
        s=copy.deepcopy(self.spec);s['body_radius_m']=.8
        with self.assertRaises(ValueError):engine.compile_plan(s)
    def test_negative_body_radius(self):
        s=copy.deepcopy(self.spec);s['body_radius_m']=-.25
        with self.assertRaises(ValueError):engine.compile_plan(s)
    def test_disconnected_portal_rejected(self):
        s=copy.deepcopy(self.spec);s['portals'][0]['opening'][0][0]+=20;s['portals'][0]['opening'][1][0]+=20
        with self.assertRaises(ValueError):engine.compile_plan(s)
    def test_outward_box_normals(self):
        ts=engine.triangles([[0,0,0],[1,1,1]])
        def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
        self.assertAlmostEqual(sum(det(*t)/6 for t in ts),1)
    def test_missing_closed_leaves_detected(self):
        r=engine.check_assembly(self.spec,self.mutate(lambda p:p['role']=='door'));self.assertFalse(r['ok']);self.assertTrue(any(f['kind']=='door_inventory'for f in r['failures']))
    def test_floor_role_cannot_hide_obstruction(self):
        a=copy.deepcopy(self.assembly);a['parts'].append({'id':'false-floor','area':'lower','role':'floor','bounds':[[2,2.9,0],[2.3,3.2,2.5]],'family':'negative'});self.assertFalse(engine.check_assembly(self.spec,a)['ok'])
    def test_thin_edge_gap_detected_continuously(self):
        a=copy.deepcopy(self.assembly)
        for p in a['parts']:
            if p['area']=='lower'and p['role']=='floor':p['bounds'][0][1]=max(p['bounds'][0][1],.12)
        a['parts']=[p for p in a['parts']if engine.valid(p['bounds'])]
        r=engine.check_assembly(self.spec,a);self.assertFalse(r['ok']);self.assertTrue(any(f['kind']=='continuous_surface'for f in r['failures']))
    def test_subtraction_volume(self):
        def volume(b):return math.prod(b[1][k]-b[0][k]for k in range(3))
        import math
        a=[[0,0,0],[3,3,3]];cut=[[1,1,1],[2,2,2]];out=engine.subtract(a,cut);self.assertAlmostEqual(sum(volume(v)for v in out),26)
    def test_pit_walls_missing(self):
        a=self.mutate(lambda p:'.pit0.'in p['id']);self.assertFalse(engine.check_assembly(self.spec,a)['ok'])
    def test_paper_thin_wall(self):
        a=copy.deepcopy(self.assembly)
        for p in a['parts']:
            if p['role']=='wall'and p['bounds'][1][0]<=0:p['bounds'][0][0]=p['bounds'][1][0]-.003
        self.assertFalse(engine.check_assembly(self.spec,a)['ok'])

if __name__=='__main__':unittest.main()
