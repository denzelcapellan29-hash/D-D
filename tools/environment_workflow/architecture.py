"""Deterministic rectilinear architecture reference; no application or network writes.

Coordinates are metres, never a forced voxel/grid trace. Closed structural boxes
are an exact intermediate solid representation, not arbitrary mesh AABBs.
Native gameplay, art and source interpretation remain separate acceptance gates.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path

EPS = 1e-7
FACES = [(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]

def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def box(lo, hi):
    return [list(map(float,lo)), list(map(float,hi))]

def valid(b):
    return len(b)==2 and all(len(p)==3 for p in b) and all(math.isfinite(x) for p in b for x in p) and all(b[1][k]-b[0][k]>EPS for k in range(3))

def subtract(b, cut):
    """Exact difference of two axis-aligned closed boxes, with disjoint interiors."""
    lo=[max(b[0][k],cut[0][k]) for k in range(3)]
    hi=[min(b[1][k],cut[1][k]) for k in range(3)]
    if any(hi[k]-lo[k]<=EPS for k in range(3)): return [b]
    out=[]; core=[b[0][:],b[1][:]]
    for k in range(3):
        if lo[k]>core[0][k]+EPS:
            q=[core[0][:],core[1][:]];q[1][k]=lo[k];out.append(q);core[0][k]=lo[k]
        if hi[k]<core[1][k]-EPS:
            q=[core[0][:],core[1][:]];q[0][k]=hi[k];out.append(q);core[1][k]=hi[k]
    return out

def vertices(b):
    return [[b[(i>>2)&1][0],b[(i>>1)&1][1],b[i&1][2]] for i in range(8)]

def triangles(b):
    v=vertices(b)
    return [[v[f[0]],v[f[i]],v[f[i+1]]] for f in FACES for i in [1,2]]

def ray_triangle(o,d,tri):
    def sub(a,b):return [a[k]-b[k]for k in range(3)]
    def dot(a,b):return sum(a[k]*b[k]for k in range(3))
    def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    e1=sub(tri[1],tri[0]);e2=sub(tri[2],tri[0]);h=cross(d,e2);a=dot(e1,h)
    if abs(a)<1e-11:return None
    s=sub(o,tri[0]);u=dot(s,h)/a
    if not -EPS<=u<=1+EPS:return None
    q=cross(s,e1);v=dot(d,q)/a
    if v < -EPS or u+v>1+EPS:return None
    t=dot(e2,q)/a
    return t if t>=-EPS else None

def cast(parts,o,d,limit,roles=None):
    hits=[]
    for p in parts:
        if roles and p['role']not in roles:continue
        near=0.;far=limit;b=p['bounds'];skip=False
        for k in range(3):
            if abs(d[k])<1e-12:
                if not b[0][k]-EPS<=o[k]<=b[1][k]+EPS:skip=True;break
            else:
                v,w=sorted([(b[0][k]-o[k])/d[k],(b[1][k]-o[k])/d[k]]);near=max(near,v);far=min(far,w)
                if near>far+EPS:skip=True;break
        if skip:continue
        for t in triangles(p['bounds']):
            h=ray_triangle(o,d,t)
            if h is not None and h<=limit+EPS:hits.append((h,p['id']))
    return min(hits)if hits else None

def samples(a,b,spacing):
    n=max(1,math.ceil((b-a)/spacing))
    return [a+(i+.5)*(b-a)/n for i in range(n)]

def tile_edges(a,b,pitch):
    return sorted({a,b}|{round(k*pitch,8)for k in range(math.floor(a/pitch)+1,math.ceil(b/pitch)) if a+EPS<k*pitch<b-EPS})

def uncovered(rects, covers):
    """Continuous planar difference; catches narrow gaps between sample rays."""
    remaining=[box([r[0],r[1],0],[r[2],r[3],1]) for r in rects]
    for r in covers:
        cut=box([r[0],r[1],0],[r[2],r[3],1]);remaining=[p for q in remaining for p in subtract(q,cut)]
    return [[p[0][0],p[0][1],p[1][0],p[1][1]]for p in remaining if (p[1][0]-p[0][0])*(p[1][1]-p[0][1])>1e-9]

def validate_spec(s):
    if s.get('schema_version')!=1 or s.get('units')!='metres':raise ValueError('schema_version1 and metre units required')
    if not s.get('identity') or not s.get('authority'):raise ValueError('Location identity and source/design authority required')
    if not s.get('spaces'):raise ValueError('At least one explicit space required')
    for k in ['body_height_m','body_radius_m','slab_m','floor_module_m','wall_module_m','probe_spacing_m']:
        if not isinstance(s.get(k),(int,float)) or not math.isfinite(s[k]) or s[k]<=0:raise ValueError('Positive finite physical parameter required: '+k)
    if not .02<=s['wall_thickness_m']<=2:raise ValueError('Explicit reasonable wall thickness required')
    ids=set()
    for a in s['spaces']:
        if a['id']in ids:raise ValueError('Duplicate space ID')
        ids.add(a['id']);x0,y0,x1,y1=a['rect']
        if not all(math.isfinite(v) for v in [*a['rect'],a['floor'],a['ceiling']])or not(x1>x0 and y1>y0):raise ValueError('Finite ordered space bounds required')
        if a['ceiling']-a['floor']<s['body_height_m']:raise ValueError('Insufficient room headroom '+a['id'])
    portal_ids=set()
    for p in s.get('portals',[]):
        if p['id']in portal_ids or not valid(p['opening']):raise ValueError('Invalid/duplicate opening')
        portal_ids.add(p['id'])
        if len(p['spaces'])!=2 or not set(p['spaces'])<=ids:raise ValueError('Every portal needs two known neighbors')
        if p['axis']not in [0,1]:raise ValueError('Only rectilinear portal planes supported')
        if p['state']not in ['open','closed','locked','secret_closed']:raise ValueError('Explicit portal state required')
        if p['opening'][1][2]-p['opening'][0][2]<s['body_height_m']:raise ValueError('Portal too low')
        if p['opening'][1][1-p['axis']]-p['opening'][0][1-p['axis']]<2*s['body_radius_m']:raise ValueError('Portal too narrow for test body')
        neighbors=[v for v in s['spaces']if v['id']in p['spaces']];ax=p['axis'];cross=1-ax;lo,hi=p['opening'];faces=[]
        for space in neighbors:
            r=space['rect'];matching=[v for v in [r[ax],r[ax+2]]if min(abs(v-lo[ax]),abs(v-hi[ax]))<1e-6]
            if not matching or not(r[cross]-EPS<=lo[cross]<hi[cross]<=r[cross+2]+EPS):raise ValueError('Opening must meet both declared neighbor boundaries')
            faces.append(matching[0])
        if abs(abs(faces[0]-faces[1])-(hi[ax]-lo[ax]))>1e-6:raise ValueError('Opening must span the physical gap between neighbors')
    for a in s['spaces']:
        if 'stairs'in a:
            st=a['stairs']
            if st['axis']not in [0,1]or not isinstance(st['steps'],int)or st['steps']<=0:raise ValueError('Explicit stair axis and positive integer step count required')
            if st['top']<=a['floor']:raise ValueError('Reference flight must rise in positive axis')
        for h in a.get('pits',[]):
            x0,y0,x1,y1=a['rect'];u0,v0,u1,v1=h['rect']
            if not(x0<u0<u1<x1 and y0<v0<v1<y1 and h['bottom']<a['floor']):raise ValueError('Pit must be inside its source space')
    return s

def compile_plan(s):
    validate_spec(s);parts=[];t=s['wall_thickness_m'];slab=s['slab_m'];pitch=s['floor_module_m']
    def put(b,role,area,label):
        if not valid(b):return
        pieces=[b]
        # Shared walls have one physical owner. No duplicate overlapping wall solids.
        if role=='wall':
            for old in parts:
                if old['role']=='wall':pieces=[v for q in pieces for v in subtract(q,old['bounds'])]
        if role=='wall':
            tiled=[]
            for q in pieces:
                ax=0 if q[1][0]-q[0][0]>=q[1][1]-q[0][1]else 1;edges=tile_edges(q[0][ax],q[1][ax],s.get('wall_module_m',1.524))
                for u,v in zip(edges,edges[1:]):
                    vbox=[q[0][:],q[1][:]];vbox[0][ax]=u;vbox[1][ax]=v;tiled.append(vbox)
            pieces=tiled
        for n,q in enumerate(pieces):
            q=[[round(v,8)for v in p]for p in q]
            shape=[round(q[1][k]-q[0][k],8)for k in range(3)]
            parts.append({'id':area+'.'+label+'.'+str(n),'area':area,'role':role,'bounds':q,'family':role+'_'+digest(shape)[:12]})
    for a in s['spaces']:
        x0,y0,x1,y1=a['rect'];z=a['floor'];c=a['ceiling'];area=a['id']
        walls=[box([x0-t,y0-t,z-slab],[x1+t,y0,c+slab]),box([x0-t,y1,z-slab],[x1+t,y1+t,c+slab]),box([x0-t,y0,z-slab],[x0,y1,c+slab]),box([x1,y0,z-slab],[x1+t,y1,c+slab])]
        for i,b in enumerate(walls):
            pieces=[b]
            for p in s.get('portals',[]):
                if area in p['spaces']:pieces=[v for q in pieces for v in subtract(q,p['opening'])]
            for j,q in enumerate(pieces):put(q,'wall',area,f'wall{i}.{j}')
        # Floors extend beneath their masonry bearings; no floating slab-edge gaps.
        xx=tile_edges(x0-t,x1+t,pitch);yy=tile_edges(y0-t,y1+t,pitch)
        for i in range(len(xx)-1):
            for j in range(len(yy)-1):
                b=box([xx[i],yy[j],z-slab],[xx[i+1],yy[j+1],z]);qs=[b]
                for h in a.get('pits',[]):
                    u0,v0,u1,v1=h['rect'];qs=[v for q in qs for v in subtract(q,box([u0,v0,z-slab-1],[u1,v1,z+1]))]
                for k,q in enumerate(qs):put(q,'floor',area,f'floor{i}.{j}.{k}')
        put(box([x0-t,y0-t,c],[x1+t,y1+t,c+slab]),'ceiling',area,'ceiling')
        if 'stairs'in a:
            st=a['stairs'];ax=st['axis'];n=st['steps'];r=a['rect'];start=r[ax];end=r[ax+2]
            for i in range(n):
                lo=[x0,y0,z-slab];hi=[x1,y1,z+(i+1)*(st['top']-z)/n];lo[ax]=start+i*(end-start)/n;hi[ax]=start+(i+1)*(end-start)/n;put(box(lo,hi),'stairs',area,'step'+str(i))
        for hi,h in enumerate(a.get('pits',[])):
            u0,v0,u1,v1=h['rect'];bottom=h['bottom'];put(box([u0,v0,bottom-slab],[u1,v1,bottom]),'floor',area,'pitbottom'+str(hi))
            for k,b in enumerate([box([u0-t,v0-t,bottom-slab],[u1+t,v0,z]),box([u0-t,v1,bottom-slab],[u1+t,v1+t,z]),box([u0-t,v0,bottom-slab],[u0,v1,z]),box([u1,v0,bottom-slab],[u1+t,v1,z])]):put(b,'wall',area,f'pit{hi}.{k}')
    for p in s.get('portals',[]):
        if p['state']=='open':continue
        lo,hi=[v[:]for v in p['opening']];ax=p['axis'];mid=(lo[ax]+hi[ax])/2;lo[ax]=mid-.018;hi[ax]=mid+.018
        put(box(lo,hi),'door',p['spaces'][0],p['id'])
        parts[-1]['portal']=p['id'];parts[-1]['state']=p['state']
    return {'schema_version':1,'identity':s['identity'],'spec_sha256':digest(s),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'parts':parts,'features':s.get('features',[]),'gates':{'SOURCE':'UNVERIFIED','STRUCTURE':'UNVERIFIED','ART':'UNVERIFIED','NATIVE':'UNVERIFIED','PERFORMANCE':'UNVERIFIED','DM_ACCEPTED':'UNVERIFIED'}}

def floor_at(a,x,y):
    for h in a.get('pits',[]):
        u0,v0,u1,v1=h['rect']
        if u0<x<u1 and v0<y<v1:return h['bottom']
    if 'stairs'in a:
        st=a['stairs'];ax=st['axis'];v=[x,y][ax];r=a['rect'];f=min(st['steps'],max(1,math.floor((v-r[ax])/(r[ax+2]-r[ax])*st['steps'])+1))
        return a['floor']+f*(st['top']-a['floor'])/st['steps']
    return a['floor']

def check_assembly(s,assembly):
    validate_spec(s);parts=assembly['parts'];fail=[];counts={'floor':0,'ceiling':0,'wall':0,'portal_clearance':0,'route_body':0,'features':0,'continuous_surface':0,'door_inventory':0,'solid_coverage':0}
    def test(kind,ok,**data):
        counts[kind]+=1
        if not ok:fail.append({'kind':kind,**data})
    if assembly['spec_sha256']!=digest(s):fail.append({'kind':'stale_spec'})
    if len({p['id']for p in parts})!=len(parts):fail.append({'kind':'duplicate_component_id'})
    if any(not valid(p['bounds'])for p in parts):return {'ok':False,'failures':[{'kind':'invalid_solid'}]}
    static=[p for p in parts if p['role']!='door'];spacing=s.get('probe_spacing_m',.381)
    def covered_solid(required,roles,label):
        gaps=[required]
        for p in static:
            if p['role'] in roles:gaps=[v for q in gaps for v in subtract(q,p['bounds'])]
        test('solid_coverage',not gaps,label=label,gaps=gaps)
    for a in s['spaces']:
        x0,y0,x1,y1=a['rect'];c=a['ceiling']
        # Full thickness and pit shafts must survive, not merely their inner faces.
        t=s['wall_thickness_m'];slab=s['slab_m'];z=a['floor']
        enclosures=[box([x0-t,y0-t,z-slab],[x1+t,y0,c+slab]),box([x0-t,y1,z-slab],[x1+t,y1+t,c+slab]),box([x0-t,y0,z-slab],[x0,y1,c+slab]),box([x1,y0,z-slab],[x1+t,y1,c+slab])]
        for h in a.get('pits',[]):
            u0,v0,u1,v1=h['rect'];bottom=h['bottom']
            enclosures += [box([u0-t,v0-t,bottom-slab],[u1+t,v0,z]),box([u0-t,v1,bottom-slab],[u1+t,v1+t,z]),box([u0-t,v0,bottom-slab],[u0,v1,z]),box([u1,v0,bottom-slab],[u1+t,v1,z])]
        for required in enclosures:
            chunks=[required]
            for p in s.get('portals',[]):
                if a['id']in p['spaces']:chunks=[v for q in chunks for v in subtract(q,p['opening'])]
            for q in chunks:covered_solid(q,{'wall'},a['id']+'.enclosure')
        expected=[(a['rect'],a['floor'])]
        if 'stairs'in a:
            st=a['stairs'];ax=st['axis'];expected=[]
            for i in range(st['steps']):
                rect=a['rect'][:];length=rect[ax+2]-rect[ax];rect[ax]=a['rect'][ax]+i*length/st['steps'];rect[ax+2]=a['rect'][ax]+(i+1)*length/st['steps'];expected.append((rect,a['floor']+(i+1)*(st['top']-a['floor'])/st['steps']))
        for h in a.get('pits',[]):
            expected=[(q,z)for rect,z in expected for q in uncovered([rect],[h['rect']])]+[(h['rect'],h['bottom'])]
        for rect,z in expected:
            covered_solid(box([rect[0],rect[1],z-slab],[rect[2],rect[3],z]),{'floor','stairs'},a['id']+'.bearing')
            covers=[[p['bounds'][0][0],p['bounds'][0][1],p['bounds'][1][0],p['bounds'][1][1]]for p in static if p['role']in ['floor','stairs']and abs(p['bounds'][1][2]-z)<1e-6]
            gaps=uncovered([rect],covers);test('continuous_surface',not gaps,area=a['id'],surface='floor',z=z,gaps=gaps)
        covers=[[p['bounds'][0][0],p['bounds'][0][1],p['bounds'][1][0],p['bounds'][1][1]]for p in static if p['role']=='ceiling'and abs(p['bounds'][0][2]-c)<1e-6]
        covered_solid(box([x0,y0,c],[x1,y1,c+slab]),{'ceiling'},a['id']+'.ceiling')
        gaps=uncovered([a['rect']],covers);test('continuous_surface',not gaps,area=a['id'],surface='ceiling',gaps=gaps)
        for ax,pos,along0,along1,normal in [(0,x0,y0,y1,-1),(0,x1,y0,y1,1),(1,y0,x0,x1,-1),(1,y1,x0,x1,1)]:
            rects=[[along0,a['floor'],along1,c]];cuts=[]
            for p in s.get('portals',[]):
                if a['id']in p['spaces']and p['opening'][0][ax]-EPS<=pos<=p['opening'][1][ax]+EPS:cuts.append([p['opening'][0][1-ax],p['opening'][0][2],p['opening'][1][1-ax],p['opening'][1][2]])
            rects=uncovered(rects,cuts);plane=pos+normal*.002
            covers=[[p['bounds'][0][1-ax],p['bounds'][0][2],p['bounds'][1][1-ax],p['bounds'][1][2]]for p in static if p['role']=='wall'and p['bounds'][0][ax]-EPS<=plane<=p['bounds'][1][ax]+EPS]
            gaps=uncovered(rects,covers);test('continuous_surface',not gaps,area=a['id'],surface='wall',axis=ax,plane=plane,gaps=gaps)
        for x in samples(x0,x1,spacing):
            for y in samples(y0,y1,spacing):
                z=floor_at(a,x,y);h=cast(static,[x,y,z+.03],[0,0,-1],.06,{'floor','stairs'})
                test('floor',h is not None and abs(h[0]-.03)<.002,area=a['id'],at=[x,y,z])
                h=cast(static,[x,y,c-.03],[0,0,1],.06,{'ceiling'})
                test('ceiling',h is not None and abs(h[0]-.03)<.002,area=a['id'],at=[x,y,c])
        for ax,pos,along0,along1,normal in [(0,x0,y0,y1,-1),(0,x1,y0,y1,1),(1,y0,x0,x1,-1),(1,y1,x0,x1,1)]:
            for v in samples(along0,along1,spacing):
                xy=[pos,v]if ax==0 else[v,pos];floor=floor_at(a,*xy)
                for z in samples(floor+.03,c-.03,spacing):
                    expected=not any(all(p['opening'][0][k]-EPS <= [*xy,z][k] <= p['opening'][1][k]+EPS for k in range(3))for p in s.get('portals',[])if a['id']in p['spaces'])
                    o=[*xy,z];o[ax]-=normal*.02;direction=[0,0,0];direction[ax]=normal
                    hit=cast(static,o,direction,.02+s['wall_thickness_m']+.03,{'wall'})
                    test('wall',bool(hit)==expected,area=a['id'],at=[*xy,z],expected='sealed'if expected else'portal')
    for p in s.get('portals',[]):
        ax=p['axis'];cross=1-ax;lo,hi=p['opening']
        leaves=[v for v in parts if v.get('portal')==p['id']and v['role']=='door']
        if p['state']!='open':
            ok=len(leaves)==1
            if ok:
                leaf=leaves[0];b=leaf['bounds'];ok=leaf.get('state')==p['state']and abs((b[0][ax]+b[1][ax]-lo[ax]-hi[ax])/2)<.001 and all(abs(b[q][k]-p['opening'][q][k])<.001 for q in [0,1]for k in [cross,2])
            test('door_inventory',ok,portal=p['id'],reason='Declared closed/secret leaf must exist with correct state, pivot plane and full opening coverage')
        for v in samples(lo[cross]+.005,hi[cross]-.005,spacing):
            for z in samples(lo[2]+.005,hi[2]-.005,spacing):
                o=[0,0,z];o[ax]=lo[ax]-.01;o[cross]=v;direction=[0,0,0];direction[ax]=1
                test('portal_clearance',cast(static,o,direction,hi[ax]-lo[ax]+.02,{'wall','ceiling'})is None,portal=p['id'],at=o)
    radius=s['body_radius_m'];height=s['body_height_m'];body_margin=.025
    for route in s.get('routes',[]):
        for a,b in zip(route['points'],route['points'][1:]):
            distance=math.dist(a,b);n=max(1,math.ceil(distance/.075))
            for i in range(n+1):
                x,y=[a[k]+(b[k]-a[k])*i/n for k in range(2)];space=next((v for v in s['spaces']if v['rect'][0]-EPS<=x<=v['rect'][2]+EPS and v['rect'][1]-EPS<=y<=v['rect'][3]+EPS),None)
                if space:z=floor_at(space,x,y)
                else:
                    portal=next((p for p in s.get('portals',[])if all(p['opening'][0][k]-EPS <= [x,y][k] <= p['opening'][1][k]+EPS for k in [0,1])),None)
                    if not portal:test('route_body',False,route=route['id'],at=[x,y],reason='No authored space or opening');continue
                    z=portal['opening'][0][2]
                # Axis-aligned body volume tested against exact solid boxes, not mesh bounds.
                body=box([x-radius,y-radius,z+body_margin],[x+radius,y+radius,z+height]);bad=[]
                for p in static:
                    if p['role']in ['floor','stairs']and p['bounds'][1][2]<=z+s.get('maximum_step_m',.2032)+EPS:continue
                    q=p['bounds']
                    if all(min(body[1][k],q[1][k])-max(body[0][k],q[0][k])>EPS for k in range(3)):bad.append(p['id'])
                support=cast(static,[x,y,z+.02],[0,0,-1],.04,{'floor','stairs'})
                test('route_body',not bad and support is not None,route=route['id'],at=[x,y,z],obstructions=bad)
    available={p['id']for p in parts}|{f['id']for f in assembly.get('features',[])if f.get('delivery')in ['native_effect','native_clue_image','asset','deferred']}
    for f in s.get('features',[]):test('features',f['id']in available,feature=f['id'])
    return {'ok':not fail,'counts':counts,'failures':fail,'scope':'Exact intermediate rectilinear solids and real triangle rays. Finite probes, not arbitrary mesh/BIM/native certification.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('spec');p.add_argument('--out',required=True);args=p.parse_args();s=json.loads(Path(args.spec).read_text(encoding='utf-8'));out=Path(args.out);out.mkdir(parents=True,exist_ok=True);a=compile_plan(s);qa=check_assembly(s,a);a['gates']['STRUCTURE']='PASS'if qa['ok']else'FAIL'
    (out/'assembly.json').write_text(json.dumps(a,indent=2));(out/'structure.json').write_text(json.dumps(qa,indent=2));print(json.dumps({'structure':qa['ok'],'parts':len(a['parts']),'families':len({v['family']for v in a['parts']}),'probes':sum(qa['counts'].values()),'failures':qa['failures'][:5]}));raise SystemExit(0 if qa['ok']else 1)
if __name__=='__main__':main()
