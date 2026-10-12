"""Area 8 geometry-free 3D rigid connector fit. No Blender mesh creation/editing.
All points must be verified corresponding connector samples in identical calibrated units.
A transform proposal is NOT certified physical contact or a production room solver.
"""
import numpy as np

def fit_rigid_3d(source_points, target_points, max_scale=1.0, allow_scale=False):
    a=np.asarray(source_points,dtype=float); b=np.asarray(target_points,dtype=float)
    if a.shape!=b.shape or a.ndim!=2 or a.shape[1]!=3 or len(a)<3:
        raise ValueError("Need >=3 corresponding 3D connector points")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("Nonfinite connector coordinate")
    ac=a.mean(axis=0); bc=b.mean(axis=0); x=a-ac; y=b-bc
    if np.linalg.matrix_rank(x,tol=1e-9)<2 or np.linalg.matrix_rank(y,tol=1e-9)<2:
        raise ValueError("Degenerate matched connector points")
    u,s,vt=np.linalg.svd(x.T@y)
    d=np.linalg.det(u@vt)
    correction=np.diag([1.,1.,1. if d>0 else -1.])
    R=u@correction@vt
    scale=1.
    if allow_scale:
        scale=float(np.trace(np.diag(s)@correction)/np.sum(x*x))
        if not 1/max_scale<=scale<=max_scale:
            raise ValueError("Scale exceeds explicit approved bound")
    translation=bc-scale*(ac@R)
    residual=np.linalg.norm(scale*(a@R)+translation-b,axis=1)
    return dict(rotation_row_major=R.tolist(),scale=scale,translation=translation.tolist(),
                median_residual=float(np.median(residual)),max_residual=float(np.max(residual)),
                determinant=float(np.linalg.det(R)),status="TRANSFORM_PROPOSAL_NOT_CONTACT_QA")
