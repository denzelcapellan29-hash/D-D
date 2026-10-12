"""Geometry-free 2D connector fit for imported GLB interface metadata.
Transform proposal only. Does not modify or certify source mesh contact.
"""
import math

def fit_xy(src, dst):
    if len(src)!=len(dst) or len(src)<3: raise ValueError("3+ matched connector samples required")
    ax=sum(p[0] for p in src)/len(src); ay=sum(p[1] for p in src)/len(src)
    bx=sum(p[0] for p in dst)/len(dst); by=sum(p[1] for p in dst)/len(dst)
    dot=cross=0.0
    for a,b in zip(src,dst):
        x,y=a[0]-ax,a[1]-ay; u,v=b[0]-bx,b[1]-by
        dot+=x*u+y*v; cross+=x*v-y*u
    angle=math.atan2(cross,dot)
    c,s=math.cos(angle),math.sin(angle)
    tx=bx-(ax*c-ay*s); ty=by-(ax*s+ay*c)
    errors=[math.hypot(p[0]*c-p[1]*s+tx-q[0],p[0]*s+p[1]*c+ty-q[1]) for p,q in zip(src,dst)]
    return {"angle_rad":angle,"translation_xy":[tx,ty],"max_error_m":max(errors),"status":"PROPOSAL_NOT_PHYSICAL_CONTACT"}
