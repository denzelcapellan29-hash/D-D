"""Blender adapter for the reference contract. Run in background Blender only.

Builds shared collection instances and content-addressed one-scene GLB assets.
Exports draft native placements without touching Foundry. Reimports every GLB
and checks actual welded topology, dimensions and UV area before packaging.
"""
import argparse,collections,hashlib,json,math,struct,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent))
import architecture as engine

def run(spec_path,out_dir):
    s=json.loads(Path(spec_path).read_text(encoding='utf-8'));a=engine.compile_plan(s);qa=engine.check_assembly(s,a)
    if not qa['ok']:raise RuntimeError('Structural contract failed before export: '+str(qa['failures'][:3]))
    out=Path(out_dir).resolve();out.mkdir(parents=True,exist_ok=True);assets=out/'assets';assets.mkdir(exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;scene.name='Connected architecture — technical fixture';scene.unit_settings.system='METRIC'
    materials={}
    for role,color in {'floor':(.28,.25,.2,1),'wall':(.36,.32,.26,1),'ceiling':(.15,.11,.07,1),'stairs':(.3,.27,.22,1),'door':(.18,.07,.025,1)}.items():
        m=bpy.data.materials.new(role+' — technical review only');m.diffuse_color=color;m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=color;m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.85;materials[role]=m
    families={};area_collections={};placements=[]
    for p in a['parts']:
        role=p['role'];b=p['bounds'];dims=[b[1][k]-b[0][k]for k in range(3)];key=p['family']
        if role=='door':key+='_'+str(next(q['axis']for q in s['portals']if q['id']==p['portal']))
        if key not in families:
            c=bpy.data.collections.new(key);m=bpy.data.meshes.new(key);local=engine.vertices([[0,0,0],dims]);m.from_pydata(local,[],engine.FACES);m.update();o=bpy.data.objects.new(key,m);c.objects.link(o);m.materials.append(materials[role]);uv=m.uv_layers.new(name='UVMap')
            for face in m.polygons:
                axes={0:(1,2),1:(0,2),2:(0,1)}[max(range(3),key=lambda k:abs(face.normal[k]))]
                for li in face.loop_indices:
                    v=m.vertices[m.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]/1.524,v[axes[1]]/1.524)
            c.asset_mark();c.asset_data.description='Original parameterized '+role+'; technical fixture; finish/renderer acceptance pending'
            shift=Vector((0,0,0))
            if role=='door':
                ax=next(q['axis']for q in s['portals']if q['id']==p['portal']);shift=Vector((dims[0]/2,0,0)if ax==0 else(0,dims[1]/2,0));m.transform(__import__('mathutils').Matrix.Translation(-shift));o['isDoor']=True;o['doorId']='leaf';o['collision']=True;o['sight']=True
                # Whole Tile bounds are fitted independently of the leaf's hinge origin.
            temp=bpy.data.scenes.new('Export one family');bpy.context.window.scene=temp;temp.collection.children.link(c);o.select_set(True);bpy.context.view_layer.objects.active=o
            path=assets/(key+'.glb');bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_active_scene=True,export_yup=True,export_extras=True)
            sha=hashlib.sha256(path.read_bytes()).hexdigest();final=assets/(key+'_'+sha[:12]+'.glb');path.rename(final);bpy.context.window.scene=scene;bpy.data.scenes.remove(temp)
            families[key]={'collection':c,'file':'assets/'+final.name,'sha256':sha,'dimensions_m':dims,'local_min_m':list(-shift),'role':role}
        if p['area']not in area_collections:
            c=bpy.data.collections.new(p['area']);scene.collection.children.link(c);area_collections[p['area']]=c
        o=bpy.data.objects.new(p['id'],None);o.instance_type='COLLECTION';o.instance_collection=families[key]['collection'];area_collections[p['area']].objects.link(o);o.location=b[0]
        if role=='door':
            ax=next(q['axis']for q in s['portals']if q['id']==p['portal']);o.location[ax]+=dims[ax]/2
        o['semantic_id']=p['id'];o['role']=role
        placements.append({**p,'family':key,'asset':families[key]['file'],'asset_sha256':families[key]['sha256'],'origin_m':list(o.location),'fit_bounds_m':b,'native_role':{'collision':True,'sight':role in ['wall','door'],'cameraCollision':role in ['wall','door','ceiling'],'castShadow':True},'native_status':'UNVERIFIED'})
    for name,c in area_collections.items():
        area=bpy.data.scenes.new(name+' — editable');area.unit_settings.system='METRIC';area.collection.children.link(c)
    bpy.context.window.scene=scene;scene['acceptance']='TECHNICAL_FIXTURE: art/native/performance/source acceptance not established';bpy.ops.wm.save_as_mainfile(filepath=str(out/'architecture.blend'),compress=True)
    # Save a source-independent native adapter contract. It does not create Tiles.
    manifest={'schema_version':1,'identity':s['identity'],'spec_sha256':engine.digest(s),'generator_sha256':a['generator_sha256'],'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'parts':placements,'families':[{k:v for k,v in f.items()if k!='collection'}for f in families.values()],'features':a['features'],'gates':{'STRUCTURE':'PASS','GLB':'UNVERIFIED','SOURCE':'UNVERIFIED','ART':'UNVERIFIED','NATIVE':'UNVERIFIED','PERFORMANCE':'UNVERIFIED','DM_ACCEPTED':'UNVERIFIED'}}
    checks=[]
    for key,f in families.items():
        bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(out/f['file']));verts=[];tris=[];uv_ok=True
        for o in bpy.context.scene.objects:
            if o.type!='MESH':continue
            m=o.data;m.calc_loop_triangles()
            for tri in m.loop_triangles:
                coords=[tuple(round(x,6)for x in o.matrix_world@m.vertices[i].co)for i in tri.vertices];tris.append(tuple(coords));verts.extend(coords)
                if not m.uv_layers:uv_ok=False;continue
                pts=[m.uv_layers.active.data[i].uv for i in tri.loops];uv_ok&=abs(sum(u.x*v.y-v.x*u.y for u,v in zip(pts,pts[1:]+pts[:1])))>1e-12
        edges=collections.Counter(tuple(sorted((tri[i],tri[(i+1)%3])))for tri in tris for i in range(3));dimensions=[max(v[k]for v in verts)-min(v[k]for v in verts)for k in range(3)]if verts else[]
        signed_volume=sum(Vector(t[0]).dot(Vector(t[1]).cross(Vector(t[2])))/6 for t in tris)
        lo=f['local_min_m'];expected={tuple(round(v,6)for v in p)for p in engine.vertices([lo,[lo[k]+f['dimensions_m'][k]for k in range(3)]])}
        raw=(out/f['file']).read_bytes();chunk_len=struct.unpack_from('<I',raw,12)[0];gltf=json.loads(raw[20:20+chunk_len]);one_scene=len(gltf.get('scenes',[]))==1
        door_extras=f['role']!='door'or any(o.get('extras',{}).get('isDoor')is True and o.get('extras',{}).get('doorId')=='leaf'for o in gltf.get('nodes',[]))
        ok=set(verts)==expected and len(tris)==12 and all(v==2 for v in edges.values())and len({tuple(sorted(t))for t in tris})==12 and uv_ok and signed_volume>0 and one_scene and door_extras
        checks.append({'family':key,'ok':ok,'actual_vertices':len(set(verts)),'actual_triangles':len(tris),'closed_welded_edges':all(v==2 for v in edges.values()),'outward_volume_m3':signed_volume,'uv_faces':bool(uv_ok),'dimensions_m':dimensions,'exact_local_corners':set(verts)==expected,'one_glb_scene':one_scene,'door_extras':door_extras})
    bpy.ops.wm.open_mainfile(filepath=str(out/'architecture.blend'));master_checks=[]
    main=next(v for v in bpy.data.scenes if v.name.startswith('Connected architecture'));bpy.context.window.scene=main
    for p in a['parts']:
        o=main.objects.get(p['id']);points=[]
        if o and o.instance_collection:
            for member in o.instance_collection.objects:
                if member.type=='MESH':points.extend(o.matrix_world@member.matrix_world@v.co for v in member.data.vertices)
        actual=[[min(v[k]for v in points)for k in range(3)],[max(v[k]for v in points)for k in range(3)]]if points else[]
        ok=bool(actual)and all(abs(actual[q][k]-p['bounds'][q][k])<1e-5 for q in [0,1]for k in range(3));master_checks.append({'id':p['id'],'ok':ok})
    report={'ok':all(c['ok']for c in checks+master_checks),'families':checks,'master_reopen_placements':master_checks,'scope':'Actual GLB exact corners/topology/UV area/one scene/door extras, plus reopened master placements. No finish/native/art certification'}
    manifest['gates']['GLB']='PASS'if report['ok']else'FAIL';(out/'export_qa.json').write_text(json.dumps(report,indent=2));(out/'manifest.json').write_text(json.dumps(manifest,indent=2));(out/'assembly.json').write_text(json.dumps(a,indent=2));(out/'structure.json').write_text(json.dumps(qa,indent=2));print('REFERENCE_EXPORT',len(placements),'placements',len(families),'families','PASS'if report['ok']else'FAIL',flush=True)
    if not report['ok']:raise RuntimeError('Export roundtrip failed')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--out',required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);run(args.spec,args.out)
