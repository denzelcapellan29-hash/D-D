"""Source-only native-grid stair clearance sweep for current Foundry 3D Canvas GLBs.

Uses the separately pinned v06 GLB triangle parser, never imports to a Blender
scene, never edits the source, and never claims TokenLayer/native passage.
Source geometry is in glTF Y-up coordinates. World scaling is measured from
the *same* native Tile's x/y/z size, not assumed from a previous QA fixture.
"""
import hashlib, json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from foundry_stair_glb_ray_gate_v06 import load_triangles

def sweep(path, expected_sha, native_size, lanes, start_positions, eye_clearances_m,
          native_step_m=.1, outside_lanes=()):
    """Sample support difference and fixed-old-height horizontal BVH intersections.

    This is a collision *risk* gate: true native TokenLayer, camera-relative
    movement, collision wrappers, and combined floor materials are not executed.
    """
    verts,faces,sha,parts=load_triangles(path,expected_sha=expected_sha)
    mins=[min(v[i] for v in verts) for i in range(3)]
    maxs=[max(v[i] for v in verts) for i in range(3)]
    spans=[maxs[i]-mins[i] for i in range(3)]
    sizes=[float(native_size[k]) for k in ('x','y','z')]
    if min(spans)<=0 or min(sizes)<=0 or native_step_m<=0: raise ValueError('invalid bounds')
    scales=[sizes[i]/spans[i] for i in range(3)]
    if max(scales)-min(scales)>max(scales)*0.002:
        raise ValueError('nonuniform/asymmetric runtime scale; cannot use local-axis approximation')
    scale=sum(scales)/3
    dist=native_step_m/scale
    bvh=BVHTree.FromPolygons([Vector(v) for v in verts],faces,all_triangles=True)
    top=maxs[1]+max(1,spans[1])
    def support(x,z):
        hit,normal,tri,d=bvh.ray_cast(Vector((x,top,z)),Vector((0,-1,0)),spans[1]+max(1,spans[1])*2)
        return None if hit is None else float(hit.y)
    lanes_out=[]
    for x in [*lanes,*outside_lanes]:
        entries=[]
        for z in start_positions:
            y0=support(x,z)
            y1=support(x,z+dist)
            if y0 is None or y1 is None: continue
            rays=[]
            for h in eye_clearances_m:
                hit,normal,tri,d=bvh.ray_cast(
                    Vector((x,y0+float(h)/scale,z)),Vector((0,0,1)),dist-1e-5)
                rays.append({'eye_m':float(h),'blocked':hit is not None,
                             'source_hit_z':round(float(hit.z),6) if hit else None})
            entries.append({'source_start_z':z,'source_end_z':round(z+dist,6),
                'support_start_y':round(y0,6),'support_end_y':round(y1,6),
                'support_rise_native_m':round((y1-y0)*scale,6),'rays':rays})
        lanes_out.append({'source_x':x,'control_outside':x in outside_lanes,'entries':entries})
    return {'source_sha256':sha,'source_bytes':Path(path).stat().st_size,
       'part_count':len(parts),'triangle_count':len(faces),'native_bounds_m':native_size,
       'uniform_native_scale':round(scale,10),'source_units_per_native_grid_step':round(dist,8),
       'lanes':lanes_out,'native_runtime_certified':False,
       'note':'Offline source BVH only; no moved token, scene write or acceptance.'}

def a01_v016_regression(path):
    """Pinned real Manor v016 *input artifact* test; not Manor scene acceptance."""
    q=sweep(path,'d8ab55e22488c69d64b100fd2ada832786669709321facd483702baad93769e6',
        {'x':.1,'y':.2,'z':.5},[3.3,3.8,4.25],[-3.0],
        [.02,.03,.04,.06,.08,.1,.12],outside_lanes=[4.9])
    regular=q['lanes'][:3]
    checks={
        'sha_pinned':q['source_sha256']=='d8ab55e22488c69d64b100fd2ada832786669709321facd483702baad93769e6',
        'three_supported_lanes':all(len(l['entries'])==1 for l in regular),
        'native_rise_107mm':all(.106 < l['entries'][0]['support_rise_native_m'] < .109 for l in regular),
        'fixed_100mm_horizontal_hit':all(
            next(r for r in l['entries'][0]['rays'] if r['eye_m']==.1)['blocked'] for l in regular),
        'fixed_120mm_horizontal_clear':all(
            not next(r for r in l['entries'][0]['rays'] if r['eye_m']==.12)['blocked'] for l in regular),
        'outside_lane_support_absent':not q['lanes'][3]['entries'],
    }
    return {'pass':all(checks.values()),'checks':checks,'sample':q,
            'scope':'Current as-built A01 v016 stair source only; no native passage claim.'}

if __name__=='__main__' and '--' in __import__('sys').argv:
    import sys
    from argparse import ArgumentParser
    parser=ArgumentParser()
    parser.add_argument('--asset',required=True)
    parser.add_argument('--a01-v016',action='store_true')
    arg=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not arg.a01_v016:parser.error('select a known fixture, or import sweep() for a new pinned candidate')
    out=a01_v016_regression(arg.asset)
    print(json.dumps(out,indent=2,sort_keys=True))
    if not out['pass']:raise SystemExit(3)
