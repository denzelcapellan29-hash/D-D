"""Run with Blender Python or CPython + NumPy. No geometry is authored."""
import unittest
import numpy as np
from area8_rigid_connector_fit_3d import fit_rigid_3d

class ConnectorFitTests(unittest.TestCase):
    def setUp(self):
        self.a=np.array([[0.,0,0],[1,0,0],[0,2,0],[0,0,3],[1,2,3]])
        theta=.4; c,s=np.cos(theta),np.sin(theta)
        self.rotation=np.array([[c,-s,0],[s,c,0],[0,0,1]])
        self.b=self.a@self.rotation.T+[3,-2,4]
    def test_rigid(self):
        got=fit_rigid_3d(self.a,self.b)
        self.assertLess(got["max_residual"],1e-9)
        self.assertAlmostEqual(got["determinant"],1.)
        self.assertTrue(np.allclose(got["translation"],[3,-2,4]))
    def test_reflection_guard(self):
        mirrored=self.a*np.array([-1,1,1])
        got=fit_rigid_3d(self.a,mirrored)
        self.assertGreater(got["max_residual"],.01)
        self.assertGreater(got["determinant"],0)
    def test_scale_rejection(self):
        with self.assertRaises(ValueError):
            fit_rigid_3d(self.a,self.b*1.3,max_scale=1.1,allow_scale=True)
    def test_degenerate_rejection(self):
        with self.assertRaises(ValueError):
            fit_rigid_3d([[0,0,0],[1,0,0],[2,0,0]],[[0,0,0],[1,0,0],[2,0,0]])
if __name__=="__main__":unittest.main()
