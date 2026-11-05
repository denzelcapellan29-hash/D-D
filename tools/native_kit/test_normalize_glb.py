"""Portable fixtures authored here; no campaign or third-party models required."""
import copy
import struct
import tempfile
import unittest
from pathlib import Path
import normalize_glb as n


def fixture():
    # Interleaved positions/normals, then UVs. The hierarchy includes a hinge.
    values=[(0,0,0,0,1,0),(1.524,0,0,0,1,0),(0,1.524,0,0,1,0)]
    binary=b''.join(struct.pack('<6f',*row) for row in values)+struct.pack('<6f',0,0,1,0,0,1)
    doc={'asset':{'version':'2.0'},'scene':0,'scenes':[{'nodes':[0]}],
         'nodes':[{'translation':[1.524,0,0],'children':[1]},
                  {'name':'hinge','mesh':0,'extras':{'collision':True,'author':'original fixture'}}],
         'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'TEXCOORD_0':2},'material':0}]}],
         'materials':[{'pbrMetallicRoughness':{'baseColorFactor':[.2,.3,.4,1],'metallicFactor':0}}],
         'buffers':[{'byteLength':len(binary)}],
         'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':72,'byteStride':24},
                        {'buffer':0,'byteOffset':72,'byteLength':24}],
         'accessors':[{'bufferView':0,'byteOffset':0,'componentType':5126,'count':3,'type':'VEC3','min':[0,0,0],'max':[1.524,1.524,0]},
                      {'bufferView':0,'byteOffset':12,'componentType':5126,'count':3,'type':'VEC3'},
                      {'bufferView':1,'componentType':5126,'count':3,'type':'VEC2'}]}
    return n.encode_glb(doc,binary)


class SyntheticNormalizationTests(unittest.TestCase):
    def setUp(self):self.raw=fixture()
    def mutate(self,work):
        d,b=n.read_glb(self.raw);work(d,b);return n.encode_glb(d,b)
    def test_interleaved_channels_and_hierarchy_preserved(self):
        out=n.normalize(self.raw);report=n.verify(self.raw,out);d,b=n.read_glb(out)
        self.assertEqual(report['vertices'],3)
        self.assertEqual(d['nodes'][0]['translation'],[1,0,0])
        self.assertEqual(d['nodes'][0]['children'],[1])
        self.assertEqual(struct.unpack_from('<3f',b,12),(0,1,0))
        self.assertEqual(struct.unpack_from('<6f',b,72),(0,0,1,0,0,1))
    def test_nonposition_alias_rejected(self):
        raw=self.mutate(lambda d,b:d['accessors'][1].update(byteOffset=0))
        with self.assertRaisesRegex(ValueError,'aliases'):n.normalize(raw)
    def test_image_alias_rejected(self):
        raw=self.mutate(lambda d,b:d.update(images=[{'bufferView':0,'mimeType':'image/png'}]))
        with self.assertRaisesRegex(ValueError,'aliases'):n.normalize(raw)
    def test_multiple_scenes_rejected(self):
        raw=self.mutate(lambda d,b:d['scenes'].append({'nodes':[0]}))
        with self.assertRaisesRegex(ValueError,'One nonempty'):n.normalize(raw)
    def test_empty_position_rejected(self):
        raw=self.mutate(lambda d,b:d['accessors'][0].update(count=0))
        with self.assertRaisesRegex(ValueError,'Positive aligned'):n.normalize(raw)
    def test_nonfinite_position_rejected(self):
        raw=self.mutate(lambda d,b:struct.pack_into('<f',b,0,float('nan')))
        with self.assertRaisesRegex(ValueError,'Non-finite'):n.normalize(raw)
    def test_nan_candidate_cannot_pass_verification(self):
        d,b=n.read_glb(n.normalize(self.raw));struct.pack_into('<f',b,0,float('nan'))
        with self.assertRaisesRegex(ValueError,'vertex mismatch'):n.verify(self.raw,n.encode_glb(d,b))
    def test_empty_primitive_list_is_not_a_model(self):
        raw=self.mutate(lambda d,b:d['meshes'][0].update(primitives=[]))
        with self.assertRaisesRegex(ValueError,'Nonempty POSITION'):n.normalize(raw)
    def test_material_edit_is_detected(self):
        out=n.normalize(self.raw);d,b=n.read_glb(out);d['materials'][0]['doubleSided']=True
        with self.assertRaisesRegex(ValueError,'Unexpected document'):n.verify(self.raw,n.encode_glb(d,b))
    def test_missing_dependency_leaves_no_output(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            root=Path(tmp);source=root/'source.glb';target=root/'runtime'/'model.glb'
            source.write_bytes(self.mutate(lambda d,b:d.update(images=[{'uri':'missing.png'}])))
            with self.assertRaises(FileNotFoundError):n.build(source,target)
            self.assertFalse(target.exists());self.assertFalse(target.parent.exists())
    def test_dependency_traversal_leaves_no_output(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            root=Path(tmp);source=root/'source.glb';target=root/'runtime'/'model.glb'
            source.write_bytes(self.mutate(lambda d,b:d.update(images=[{'uri':'../escape.png'}])))
            with self.assertRaisesRegex(ValueError,'escapes'):n.build(source,target)
            self.assertFalse(target.exists())
    def test_existing_output_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            root=Path(tmp);source=root/'source.glb';target=root/'runtime.glb';source.write_bytes(self.raw);target.write_bytes(b'keep')
            with self.assertRaisesRegex(ValueError,'New versioned'):n.build(source,target)
            self.assertEqual(target.read_bytes(),b'keep')
    def test_role_conversion_is_deterministic_and_preserves_binary(self):
        a,ar=n.uniform_tile_roles(self.raw,declared_uniform_role='wall');b,br=n.uniform_tile_roles(self.raw,declared_uniform_role='wall')
        self.assertEqual(a,b);self.assertEqual(ar,br)
        doc,binary=n.read_glb(a);original,old=n.read_glb(self.raw)
        self.assertEqual(binary,old);self.assertEqual(doc['materials'],original['materials'])
        self.assertEqual(doc['nodes'][1]['extras'],{'author':'original fixture'})
    def test_same_accessor_cannot_be_position_and_normal(self):
        raw=self.mutate(lambda d,b:d['meshes'][0]['primitives'][0]['attributes'].update(NORMAL=0))
        with self.assertRaisesRegex(ValueError,'reused'):n.normalize(raw)
    def test_role_conversion_requires_an_explicit_contract(self):
        with self.assertRaisesRegex(ValueError,'Explicit uniform'):n.uniform_tile_roles(self.raw)
    def test_embedded_door_roles_cannot_be_erased_as_wall(self):
        raw=self.mutate(lambda d,b:d['nodes'][1]['extras'].update(isDoor=True,doorId='original-fixture'))
        with self.assertRaisesRegex(ValueError,'Embedded door'):n.uniform_tile_roles(raw,declared_uniform_role='wall')
    def test_conflicting_collision_roles_cannot_be_flattened(self):
        raw=self.mutate(lambda d,b:d['nodes'][0].update(extras={'collision':False}))
        with self.assertRaisesRegex(ValueError,'Conflicting'):n.uniform_tile_roles(raw,declared_uniform_role='wall')


if __name__=='__main__':unittest.main()
