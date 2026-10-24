"""Offline semantic/native 3D Canvas Tile role contract tests; no Foundry writes."""
import unittest
from import_chunks_v02 import semantic_flags

def chunk(role, *, door=False, extras=None):
    ob={"acq_role":role}
    if extras: ob.update(extras)
    return {"chunk_id":"qa_semantics","source_objects":[ob],
            "interactive_door":door}

class NativeTileSemantics(unittest.TestCase):
    def test_support_not_sight(self):
        for role in ("walkable_floor","stair"):
            with self.subTest(role=role):
                self.assertEqual(semantic_flags(chunk(role)), (role,(True,False,False)))

    def test_opaque(self):
        for role in ("opaque_wall","roof"):
            with self.subTest(role=role):
                self.assertEqual(semantic_flags(chunk(role))[1],(True,True,True))

    def test_door_leaf_not_frame(self):
        self.assertEqual(semantic_flags(chunk("door_leaf",door=True))[1],
                         (True,True,True))
        for role,door in (("door_leaf",False),("opaque_wall",True)):
            with self.subTest(role=role,door=door):
                with self.assertRaises(RuntimeError):
                    semantic_flags(chunk(role,door=door))

    def test_nonblocking_visual(self):
        for role in ("decorative_prop","foliage"):
            self.assertEqual(semantic_flags(chunk(role))[1],(False,False,False))
        self.assertEqual(semantic_flags(chunk("solid_prop"))[1],(True,False,True))

    def test_legacy_untagged_must_fail(self):
        with self.assertRaises(RuntimeError):
            semantic_flags({"chunk_id":"legacy","source_objects":[{}],
                            "interactive_door":False})

    def test_mixed_roles_must_fail(self):
        item=chunk("stair")
        item["source_objects"].append({"acq_role":"opaque_wall"})
        with self.assertRaises(RuntimeError):
            semantic_flags(item)

    def test_partial_override_must_fail(self):
        item=chunk("stair",extras={"sight":True})
        with self.assertRaises(RuntimeError):
            semantic_flags(item)
        item["semantic_override_reason"]="Opaque stone stairs intentionally block LOS."
        self.assertEqual(semantic_flags(item)[1],(True,True,False))

    def test_invalid_boolean_rejected(self):
        for value in ("true",2,0.5):
            with self.subTest(value=value):
                with self.assertRaises(RuntimeError):
                    semantic_flags(chunk("stair",extras={"collision":value}))

    def test_conflicting_per_mesh_flags_rejected(self):
        item=chunk("opaque_wall",extras={"sight":True})
        item["source_objects"].append({"acq_role":"opaque_wall","sight":False})
        with self.assertRaises(RuntimeError):
            semantic_flags(item)

if __name__=="__main__":
    unittest.main()
