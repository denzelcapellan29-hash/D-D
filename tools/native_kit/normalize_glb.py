"""Create an immutable, grid-unit runtime derivative of a metric static GLB.

No re-export: preserve material definitions, UVs, normals, topology and images.
Only float POSITION data and node translations are uniformly scaled. This
deliberately rejects animation, skins, morphs and compression rather than
silently damaging them. Originals are never overwritten.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, struct
from pathlib import Path

JSON_CHUNK=0x4E4F534A
BIN_CHUNK=0x004E4942
SCALE=1/1.524
NATIVE_ROLE_KEYS={'collision','sight','cameraCollision','isDoor','doorId','doorStyle','doorAnimateAngle'}

def digest(data): return hashlib.sha256(data).hexdigest()

def read_glb(data):
    if len(data)<28: raise ValueError('Complete GLB2 required')
    magic,version,length=struct.unpack_from('<III',data)
    if magic!=0x46546C67 or version!=2 or length!=len(data): raise ValueError('Valid GLB2 required')
    offset=12;chunks=[]
    while offset<len(data):
        if offset+8>len(data): raise ValueError('Incomplete chunk header')
        size,kind=struct.unpack_from('<II',data,offset);offset+=8
        if size%4 or offset+size>len(data): raise ValueError('Invalid chunk bounds/alignment')
        chunks.append((kind,data[offset:offset+size]));offset+=size
    if [x[0] for x in chunks]!=[JSON_CHUNK,BIN_CHUNK]: raise ValueError('One JSON and binary chunk required')
    return json.loads(chunks[0][1]),bytearray(chunks[1][1])

def encode_glb(doc,binary):
    header=json.dumps(doc,separators=(',',':'),ensure_ascii=False).encode();header+=b' '*((-len(header))%4)
    binary=bytes(binary)+b'\0'*((-len(binary))%4)
    return struct.pack('<III',0x46546C67,2,28+len(header)+len(binary))+struct.pack('<II',len(header),JSON_CHUNK)+header+struct.pack('<II',len(binary),BIN_CHUNK)+binary

def position_accessors(doc):
    ids=set()
    for mesh in doc.get('meshes',[]):
        if mesh.get('weights'): raise ValueError('Morph weights unsupported')
        for p in mesh.get('primitives',[]):
            if p.get('targets') or p.get('extensions'): raise ValueError('Morph/compressed/extended primitive unsupported')
            ids.add(p['attributes']['POSITION'])
    if not ids:raise ValueError('Nonempty POSITION geometry required')
    return ids

def locations(doc,index,binary):
    a=doc['accessors'][index]
    if a.get('sparse') or a.get('componentType')!=5126 or a.get('type')!='VEC3': raise ValueError('Dense float VEC3 POSITION required')
    v=doc['bufferViews'][a['bufferView']]
    if v.get('buffer',0)!=0 or v.get('extensions'): raise ValueError('Uncompressed internal buffer required')
    stride=v.get('byteStride',12);start=v.get('byteOffset',0)+a.get('byteOffset',0)
    if a.get('count',0)<=0 or start<0 or stride%4 or start%4: raise ValueError('Positive aligned POSITION required')
    end=start+max(0,a['count']-1)*stride+12
    if stride<12 or end>len(binary) or end>v.get('byteOffset',0)+v['byteLength']: raise ValueError('Accessor outside buffer view')
    return [start+i*stride for i in range(a['count'])]

def validate_position_aliases(doc,binary):
    """Position changes must not change another channel or an embedded image."""
    positions=position_accessors(doc);changed=set();starts=set()
    for mesh in doc.get('meshes',[]):
        for primitive in mesh.get('primitives',[]):
            if primitive.get('indices') in positions or any(index in positions for key,index in primitive['attributes'].items() if key!='POSITION'):
                raise ValueError('POSITION accessor reused by another channel')
    for index in positions:
        for offset in locations(doc,index,binary):
            block=set(range(offset,offset+12))
            if offset not in starts and changed.intersection(block):raise ValueError('Partially overlapping POSITION records')
            starts.add(offset);changed.update(block)
    component_bytes={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4}
    components={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT2':4,'MAT3':9,'MAT4':16}
    for index,a in enumerate(doc.get('accessors',[])):
        if index in positions:continue
        if a.get('sparse'):raise ValueError('Sparse non-position accessor unsupported')
        if 'bufferView' not in a:continue
        v=doc['bufferViews'][a['bufferView']]
        size=component_bytes[a['componentType']]*components[a['type']]
        start=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',size)
        for i in range(a['count']):
            if changed.intersection(range(start+i*stride,start+i*stride+size)):
                raise ValueError('POSITION aliases another accessor')
    for image in doc.get('images',[]):
        if 'bufferView' in image:
            v=doc['bufferViews'][image['bufferView']];start=v.get('byteOffset',0)
            if changed.intersection(range(start,start+v['byteLength'])):raise ValueError('POSITION aliases an image')

def normalize(data,scale=SCALE):
    if not math.isfinite(scale) or scale<=0: raise ValueError('Positive finite scale required')
    doc,binary=read_glb(data);out=copy.deepcopy(doc)
    if doc.get('animations') or doc.get('skins') or doc.get('extensionsRequired'): raise ValueError('Only static uncompressed assets supported')
    if len(doc.get('buffers',[]))!=1 or doc['buffers'][0].get('uri'): raise ValueError('Internal binary required')
    if len(doc.get('scenes',[]))!=1 or not doc['scenes'][0].get('nodes') or not doc.get('meshes'):raise ValueError('One nonempty static scene required')
    validate_position_aliases(doc,binary)
    changed=set()
    for index in sorted(position_accessors(doc)):
        for offset in locations(doc,index,binary):
            vals=struct.unpack_from('<fff',binary,offset)
            if not all(map(math.isfinite,vals)): raise ValueError('Non-finite geometry')
            if offset not in changed: struct.pack_into('<fff',binary,offset,*(v*scale for v in vals));changed.add(offset)
        for key in ['min','max']:
            if key in out['accessors'][index]:out['accessors'][index][key]=[v*scale for v in out['accessors'][index][key]]
    for node in out.get('nodes',[]):
        if 'matrix' in node:
            for k in [12,13,14]:node['matrix'][k]*=scale
        if 'translation' in node:node['translation']=[v*scale for v in node['translation']]
    return encode_glb(out,binary)

def verify(original,candidate,scale=SCALE,tolerance=2e-6):
    if not math.isfinite(scale) or scale<=0 or not math.isfinite(tolerance) or tolerance<0:raise ValueError('Finite positive scale and nonnegative tolerance required')
    a,ab=read_glb(original);b,bb=read_glb(candidate);expected=copy.deepcopy(a);mask=set();vertices=0
    if len(ab)!=len(bb):raise ValueError('Binary size changed')
    for i in position_accessors(a):
        for offset in locations(a,i,ab):
            old=struct.unpack_from('<fff',ab,offset);new=struct.unpack_from('<fff',bb,offset)
            if not all(map(math.isfinite,old+new)) or any(abs(new[k]-old[k]*scale)>tolerance for k in range(3)):raise ValueError('Scaled vertex mismatch')
            mask.update(range(offset,offset+12));vertices+=1
        for k in ['min','max']:
            if k in expected['accessors'][i]:expected['accessors'][i][k]=[v*scale for v in expected['accessors'][i][k]]
    for n in expected.get('nodes',[]):
        if 'matrix' in n:
            for k in [12,13,14]:n['matrix'][k]*=scale
        if 'translation' in n:n['translation']=[v*scale for v in n['translation']]
    if expected!=b:raise ValueError('Unexpected document/material/UV/node change')
    if any(x!=y for i,(x,y) in enumerate(zip(ab,bb)) if i not in mask):raise ValueError('Non-position binary data changed')
    return {'vertices':vertices,'scale':scale,'unchanged_nonposition_bytes':len(ab)-len(mask),'source_sha256':digest(original),'runtime_sha256':digest(candidate)}

def uniform_tile_roles(data,*,declared_uniform_role=None):
    """For uniform-role static pieces only, let native Tile flags own collision.

    3D Canvas9.0.36 initMerged creates new meshes without source userData.
    Keeping a source hasTags marker then excludes those new meshes from its
    native collision groups. Never use this on mixed-role or sub-door assets.
    """
    if declared_uniform_role not in {'floor','wall','whole-tile-prop','whole-tile-door'}:raise ValueError('Explicit uniform consumer role required')
    doc,binary=read_glb(data);out=copy.deepcopy(doc);removed=[]
    if doc.get('animations') or doc.get('skins'):raise ValueError('Static uniform-role derivative required')
    extras=[node.get('extras',{}) for collection in ['nodes','meshes'] for node in doc.get(collection,[])]
    if declared_uniform_role!='whole-tile-door' and any(e.get('isDoor') or e.get('doorId') for e in extras):raise ValueError('Embedded door is not a uniform static role')
    if any(len({json.dumps(e[k],sort_keys=True) for e in extras if k in e})>1 for k in ['collision','sight','cameraCollision']):raise ValueError('Conflicting per-mesh roles require independent preservation')
    for collection in ['nodes','meshes']:
        for i,node in enumerate(out.get(collection,[])):
            extras=node.get('extras',{})
            for k in sorted(NATIVE_ROLE_KEYS & extras.keys()):removed.append([collection,i,k,extras.pop(k)])
            if not extras:node.pop('extras',None)
    result=encode_glb(out,binary);check,bb=read_glb(result)
    if bytes(binary)!=bytes(bb) or check!=out:raise ValueError('Uniform role adaptation damaged payload')
    return result,{'declared_uniform_role':declared_uniform_role,'removed_native_role_metadata':removed,'binary_sha256':digest(binary),'scope':'Only declared uniform-role Tile-owned static or whole-Tile door derivative; original per-mesh semantics preserved separately'}

def build(source,target):
    source=Path(source).resolve();target=Path(target).resolve()
    if source==target or target.exists():raise ValueError('New versioned output required')
    raw=source.read_bytes();candidate=normalize(raw);report=verify(raw,candidate)
    doc,_=read_glb(raw);deps=[];pending=[]
    for image in doc.get('images',[]):
        uri=image.get('uri')
        if not uri:continue
        if '://' in uri or uri.startswith(('data:','/')):raise ValueError('Only relative local image dependencies supported')
        original=(source.parent/uri).resolve();dest=(target.parent/uri).resolve()
        if not original.is_relative_to(source.parent) or not dest.is_relative_to(target.parent):raise ValueError('Image dependency escapes pack')
        data=original.read_bytes()
        if dest.exists() and dest.read_bytes()!=data:raise ValueError('Shared dependency collision')
        pending.append((dest,data));deps.append({'path':uri,'sha256':digest(data),'bytes':len(data)})
    target.parent.mkdir(parents=True,exist_ok=True)
    for dest,data in pending:
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():dest.write_bytes(data)
    with target.open('xb') as stream:stream.write(candidate)
    return {**report,'source':str(source),'runtime':str(target),'images':deps}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('target');a=p.parse_args()
    print(json.dumps(build(a.source,a.target),indent=2))
