"""Regression tests for the Blender-authored, Foundry-scaled darkvision adapter."""
import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from vision_scale import VisionScale, nearest_ring_wall_feet


class VisionScaleTest(unittest.TestCase):
    def setUp(self):
        self.area8 = VisionScale(75, 100, 1)

    def test_area8_sixty_feet_and_gridless_conversion(self):
        self.assertAlmostEqual(self.area8.feet_to_pixels(60), 1371.6)
        self.assertAlmostEqual(self.area8.feet_to_scene_distance(60), 13.716)
        self.assertAlmostEqual(self.area8.configured_scene_units_to_real_feet(13.716), 60)

    def test_native_sixty_scene_units_is_not_sixty_feet(self):
        report = self.area8.diagnostic(60, 60)
        self.assertEqual(report["token_sight_current_radius_px"], 6000)
        self.assertEqual(report["token_sight_expected_radius_px"], 1371.6)
        self.assertTrue(report["scale_mismatch"])
        self.assertEqual(report["recommended_default_token_angle_deg"], 360)

    def test_cardinal_and_diagonal_radius_identical(self):
        r = self.area8.feet_to_pixels(60)
        for theta in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = math.radians(theta)
            xy = (r * math.cos(rad), r * math.sin(rad))
            self.assertAlmostEqual(math.hypot(*xy), r)

    def test_standard_five_foot_grid_is_a_different_calibration(self):
        standard = VisionScale(100 / 1.524, 100, 1)
        self.assertAlmostEqual(standard.feet_to_scene_distance(60), 12)
        self.assertNotAlmostEqual(standard.feet_to_scene_distance(60), 13.716)

    def test_nearby_foundry_wall_explains_shorter_observed_vision(self):
        distance = nearest_ring_wall_feet(1970, 585, 1920, 960, 800, 75)
        self.assertGreater(distance, 18)
        self.assertLess(distance, 19)

    def test_rejects_unmeasured_or_negative_calibrations(self):
        with self.assertRaises(ValueError):
            VisionScale(0, 100, 1)
        with self.assertRaises(ValueError):
            self.area8.feet_to_scene_distance(-60)


if __name__ == "__main__":
    unittest.main()
