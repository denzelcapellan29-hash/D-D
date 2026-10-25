"""Synthetic contract controls; contains no campaign paths or source material."""
import copy
import unittest

from validate_scene_bundle import validate


def fixture():
    manifest = {
        "schema_version": 1,
        "bundle_id": "fixture.bundle-a",
        "identity": {"adventure_id": "fixture-adventure", "site_id": "fixture-site", "source_ref": "fixture-map",
                     "area_ids": ["fixture.area-a"]},
        "asset_root": "/fixture",
        "master": {"path": "master.blend", "bytes": 10},
        "sources": [{"area_id": "fixture.area-a", "path": "source-a.blend", "bytes": 20,
                     "collections": [
                         {"name": "selected_finish", "min_meshes": 2, "min_visible_meshes": 2,
                          "visible_mesh_names": ["finish_floor", "finish_wall"]},
                         {"name": "selected_roof", "min_meshes": 1, "min_visible_meshes": 1,
                          "visible_mesh_names": ["roof_panel"]}]}],
        "unit_scale_length": 1.0,
        "exclusions": {"absent_collections": ["standalone_duplicate_cap"], "visible_name_patterns": ["^private_"],
                       "visible_property_values": {"gm_only": [True]}},
        "review_gates": {"source": {"status": "UNVERIFIED"}, "art": {"status": "UNVERIFIED"},
                         "native": {"status": "UNVERIFIED"}, "dm": {"status": "UNVERIFIED"}},
    }
    inventory = {
        "inventory_schema": 1,
        "master": {"path": "/fixture/master.blend", "exists": True, "bytes": 10, "sha256": "a" * 64},
        "libraries": [{"path": "/fixture/source-a.blend", "exists": True, "bytes": 20, "sha256": "b" * 64}],
        "collections": [
            {"name": "selected_finish", "library_path": "/fixture/source-a.blend", "scene_reachable": True,
             "mesh_names": ["finish_floor", "finish_wall"], "visible_mesh_names": ["finish_floor", "finish_wall"]},
            {"name": "selected_roof", "library_path": "/fixture/source-a.blend", "scene_reachable": True,
             "mesh_names": ["roof_panel"], "visible_mesh_names": ["roof_panel"]}],
        "objects": [{"name": name, "render_visible": True, "properties": {}}
                    for name in ["finish_floor", "finish_wall", "roof_panel"]],
        "images": [], "unit_scale_length": 1.0,
    }
    return manifest, inventory


class BundleControls(unittest.TestCase):
    def assert_fails(self, manifest, inventory, check_id):
        report = validate(manifest, inventory)
        self.assertEqual(report["preflight"], "FAIL")
        self.assertEqual(report["exit_code"], 2)
        self.assertIn(check_id, [item["id"] for item in report["checks"] if item["status"] == "FAIL"])

    def test_positive_inventory_does_not_grant_release(self):
        manifest, inventory = fixture()
        report = validate(manifest, inventory)
        self.assertEqual(report["preflight"], "PASS")
        self.assertEqual(report["release"], "UNVERIFIED")
        self.assertEqual(report["gates"]["native"]["status"], "UNVERIFIED")

    def test_omitted_selected_collection_cannot_pass_on_prefix(self):
        manifest, inventory = fixture()
        inventory["collections"][0]["name"] = "selected_finish_legacy_proxy"
        self.assert_fails(manifest, inventory, "collection:selected_finish")

    def test_loaded_but_unlinked_collection_fails(self):
        manifest, inventory = fixture()
        inventory["collections"][0]["scene_reachable"] = False
        self.assert_fails(manifest, inventory, "collection:selected_finish")

    def test_hidden_intended_floor_fails(self):
        manifest, inventory = fixture()
        inventory["collections"][0]["visible_mesh_names"] = ["finish_wall"]
        self.assert_fails(manifest, inventory, "intended_visible_objects:selected_finish")

    def test_wrong_source_area_fails_even_with_same_collection_names(self):
        manifest, inventory = fixture()
        inventory["libraries"][0]["path"] = "/fixture/unrelated-area-a.blend"
        for collection in inventory["collections"]:
            collection["library_path"] = "/fixture/unrelated-area-a.blend"
        self.assert_fails(manifest, inventory, "source_link:fixture.area-a")

    def test_declared_area_mismatch_fails(self):
        manifest, inventory = fixture()
        manifest["sources"][0]["area_id"] = "fixture.area-b"
        self.assert_fails(manifest, inventory, "source_area_identity")

    def test_missing_library_file_fails(self):
        manifest, inventory = fixture()
        inventory["libraries"][0]["exists"] = False
        self.assert_fails(manifest, inventory, "file_exists:fixture.area-a")

    def test_pinned_source_changed_fails(self):
        manifest, inventory = fixture()
        manifest["sources"][0]["sha256"] = "c" * 64
        self.assert_fails(manifest, inventory, "file_sha256:fixture.area-a")

    def test_standalone_duplicate_cap_fails(self):
        manifest, inventory = fixture()
        inventory["collections"].append({"name": "standalone_duplicate_cap", "scene_reachable": True})
        self.assert_fails(manifest, inventory, "excluded_collection:standalone_duplicate_cap")

    def test_visible_private_marker_fails(self):
        manifest, inventory = fixture()
        inventory["objects"].append({"name": "private_reveal", "render_visible": True, "properties": {}})
        self.assert_fails(manifest, inventory, "known_player_exposure_markers")

    def test_visible_private_property_fails(self):
        manifest, inventory = fixture()
        inventory["objects"][0]["properties"] = {"gm_only": True}
        self.assert_fails(manifest, inventory, "known_player_exposure_markers")

    def test_blocked_intent_is_not_an_open_route(self):
        manifest, inventory = fixture()
        manifest["connections"] = [{"id": "fixture.branch", "from": "fixture.area-a", "to": "fixture.area-a", "state": "BLOCKED"}]
        report = validate(manifest, inventory)
        self.assertEqual(report["preflight"], "PASS")
        self.assertEqual(report["gates"]["route_completion"]["status"], "UNVERIFIED")

    def test_unmodeled_required_route_holds_release(self):
        manifest, inventory = fixture()
        manifest["connections"] = [{"id": "fixture.route", "from": "fixture.area-a", "to": "fixture.area-a",
                                    "state": "NOT_MODELED", "required_for_release": True}]
        report = validate(manifest, inventory)
        self.assertEqual(report["preflight"], "PASS")
        self.assertEqual(report["release"], "FAIL")


if __name__ == "__main__":
    unittest.main()
