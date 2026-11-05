import copy
import unittest

import compare_native_scenes as comparison


def original_scene():
    return {
        "_id": "fixture-a", "name": "Original fixture", "width": 2000, "height": 2000,
        "grid": {"size": 100, "distance": 5, "units": "ft"}, "tokens": [],
        "flags": {"levels-3d-preview": {"mirrorLevels": False}},
        "tiles": [{"_id": "door-a", "x": 100, "y": 100, "width": 200, "height": 20,
                   "_stats": {"modifiedTime": 1}, "flags": {
                       "levels-3d-preview": {"model3d": "original-fixture.glb", "collision": True,
                                             "modelDoors": {"fixture-hinge": {"ds": 0}}},
                       comparison.GENERATOR: {"gen": "generation-a", "part": "door"}}}],
        "lights": [{"_id": "light-a", "x": 200, "y": 200, "config": {"bright": 10}}],
    }


class SceneComparisonTests(unittest.TestCase):
    def test_new_identity_and_reordered_documents_can_repeat(self):
        a = original_scene()
        a["tiles"].append({"_id": "floor-a", "x": 0, "flags": {"collision": True}})
        b = copy.deepcopy(a)
        b.update(_id="fixture-b", name="Independent repeat")
        b["tiles"][0]["_id"] = "new-door"
        b["tiles"][0]["_stats"]["modifiedTime"] = 42
        b["tiles"][0]["flags"][comparison.GENERATOR]["gen"] = "generation-b"
        b["tiles"].reverse()
        self.assertTrue(comparison.compare(a, b)["equal"])
    def assert_change(self, mutate, section):
        a = original_scene()
        b = copy.deepcopy(a)
        mutate(b)
        result = comparison.compare(a, b)
        self.assertFalse(result["equal"])
        self.assertIn(section, result["changed_sections"])
    def test_closed_door_becoming_open_is_a_real_change(self):
        self.assert_change(lambda s: s["tiles"][0]["flags"]["levels-3d-preview"]["modelDoors"]["fixture-hinge"].update(ds=1), "tiles")
    def test_lost_collision_is_not_generation_metadata(self):
        self.assert_change(lambda s: s["tiles"][0]["flags"]["levels-3d-preview"].update(collision=False), "tiles")
    def test_same_count_displaced_tile_fails(self):
        self.assert_change(lambda s: s["tiles"][0].update(x=101), "tiles")
    def test_missing_light_fails(self):
        self.assert_change(lambda s: s.update(lights=[]), "lights")
    def test_grid_scale_change_fails(self):
        self.assert_change(lambda s: s["grid"].update(distance=10), "configuration")
    def test_presentation_change_is_reported(self):
        self.assert_change(lambda s: s["flags"]["levels-3d-preview"].update(mirrorLevels=True), "native_settings")
    def test_nested_semantic_ids_are_preserved(self):
        self.assert_change(lambda s: s["tiles"][0]["flags"].update(source={"_id": "different-source"}), "tiles")
    def test_live_tokens_require_separate_review(self):
        a = original_scene()
        a["tokens"] = [{"_id": "live-character"}]
        with self.assertRaisesRegex(ValueError, "no live"):
            comparison.compare(a, a)
    def test_inputs_are_not_modified(self):
        a = original_scene()
        before = copy.deepcopy(a)
        comparison.compare(a, a)
        self.assertEqual(a, before)


if __name__ == "__main__":
    unittest.main()
