"""Physical feet -> native Foundry Token Vision Range (Scene units).

Do not copy Actor darkvision's numeric feet directly to token.sight.range
when a Scene's grid.distance/units disagree with the Blender-world scale.
Read-only and engine-neutral: this NEVER mutates a Foundry or Blender scene.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isfinite

FEET_TO_METRES = 0.3048


@dataclass(frozen=True)
class VisionScale:
    """Source scene calibration, not a global preset.

    physical pixels_per_blender_metre comes from the versioned Blender import
    manifest. grid_distance is the numeric scene-distance units per grid cell
    (even in a gridless Scene, which still exposes a grid size/distance).
    """

    pixels_per_blender_metre: float
    scene_grid_size_pixels: float
    scene_grid_distance: float

    def __post_init__(self) -> None:
        for key, val in vars(self).items():
            if not isfinite(val) or val <= 0:
                raise ValueError(f"{key} must be finite and greater than zero")

    @property
    def pixels_per_scene_distance(self) -> float:
        return self.scene_grid_size_pixels / self.scene_grid_distance

    def feet_to_scene_distance(self, feet: float) -> float:
        if not isfinite(feet) or feet < 0:
            raise ValueError("sight range in feet must be finite and nonnegative")
        return (
            feet * FEET_TO_METRES * self.pixels_per_blender_metre
        ) / self.pixels_per_scene_distance

    def scene_distance_to_pixels(self, units: float) -> float:
        return units * self.pixels_per_scene_distance

    def feet_to_pixels(self, feet: float) -> float:
        return self.scene_distance_to_pixels(self.feet_to_scene_distance(feet))

    def configured_scene_units_to_real_feet(self, units: float) -> float:
        return self.scene_distance_to_pixels(units) / (
            FEET_TO_METRES * self.pixels_per_blender_metre
        )

    def diagnostic(self, actor_darkvision_ft: float, token_sight_range: float) -> dict:
        expected = self.feet_to_scene_distance(actor_darkvision_ft)
        actual_px = self.scene_distance_to_pixels(token_sight_range)
        expected_px = self.feet_to_pixels(actor_darkvision_ft)
        return {
            "actor_darkvision_ft": actor_darkvision_ft,
            "token_sight_current_scene_units": token_sight_range,
            "token_sight_expected_scene_units": round(expected, 6),
            "token_sight_current_radius_px": round(actual_px, 4),
            "token_sight_expected_radius_px": round(expected_px, 4),
            "current_radius_equivalent_ft": round(
                self.configured_scene_units_to_real_feet(token_sight_range), 4
            ),
            "scale_mismatch": abs(actual_px - expected_px) > 0.01,
            "directions_do_not_divide_radius": True,
            "recommended_default_token_angle_deg": 360,
        }


def nearest_ring_wall_feet(
    token_x_px: float, token_y_px: float,
    ring_center_x_px: float, ring_center_y_px: float,
    ring_radius_px: float, pixels_per_blender_metre: float
) -> float:
    """Shortest 2D distance to ring edge, not a visibility guarantee."""
    if ring_radius_px <= 0 or pixels_per_blender_metre <= 0:
        raise ValueError("ring radius and map scale must be positive")
    closest_px = abs(
        hypot(token_x_px - ring_center_x_px, token_y_px - ring_center_y_px)
        - ring_radius_px
    )
    return closest_px / pixels_per_blender_metre / FEET_TO_METRES


if __name__ == "__main__":
    import json

    area8 = VisionScale(
        pixels_per_blender_metre=75,
        scene_grid_size_pixels=100,
        scene_grid_distance=1
    )
    report = area8.diagnostic(actor_darkvision_ft=60, token_sight_range=60)
    report["qa_druid_nearest_ring_wall_ft"] = round(
        nearest_ring_wall_feet(1970, 585, 1920, 960, 800, 75), 3
    )
    print(json.dumps(report, indent=2))
