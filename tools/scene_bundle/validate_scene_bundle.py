"""Read-only Blender scene-bundle preflight; no artistic or gameplay certification.

Run in Blender with --python, or validate a previously collected inventory with
ordinary Python and --snapshot. The manifest contains all project-specific data.
Only JSON reports are written. No scene/file is opened, changed or saved here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


VALID_STATES = {"PASS", "FAIL", "UNVERIFIED"}


def normal_path(value):
    value = posixpath.normpath(str(value).replace("\\", "/"))
    return value.casefold() if os.name == "nt" or re.match(r"^[A-Za-z]:", value) else value


def asset_path(root, relative):
    if str(relative).startswith("/") or re.match(r"^[A-Za-z]:", str(relative)):
        return normal_path(relative)
    return normal_path(str(root).rstrip("/\\") + "/" + str(relative))


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_file(path):
    record = {"path": normal_path(path), "exists": os.path.isfile(path)}
    if record["exists"]:
        info = os.stat(path)
        record.update(bytes=info.st_size, mtime_ns=info.st_mtime_ns, sha256=sha256(path))
    return record


def collect_blender_snapshot(manifest):
    """Inspect the already-open scene. Do not call bpy operators or mutate IDs."""
    import bpy

    scene = bpy.context.scene
    dirty_before = bool(bpy.data.is_dirty)
    tracked = {}

    def file_record(path):
        path = os.path.abspath(path)
        key = normal_path(path)
        if key not in tracked:
            tracked[key] = inspect_file(path)
        return tracked[key]

    def library_path(library):
        if library is None:
            return None
        return normal_path(bpy.path.abspath(library.filepath, library=getattr(library, "parent", None)))

    master = file_record(bpy.data.filepath) if bpy.data.filepath else {"path": "", "exists": False}
    libraries = []
    for library in bpy.data.libraries:
        absolute = library_path(library)
        record = dict(file_record(absolute))
        record["declared_path"] = library.filepath
        libraries.append(record)

    render_layer_collections = set()
    enabled_layers = []

    def layer_walk(layer_collection, excluded=False):
        excluded = excluded or bool(layer_collection.exclude)
        if not excluded:
            render_layer_collections.add(layer_collection.collection.as_pointer())
        for child in layer_collection.children:
            layer_walk(child, excluded)

    for layer in scene.view_layers:
        if getattr(layer, "use", True):
            enabled_layers.append(layer.name)
            layer_walk(layer.layer_collection)

    scene_objects = {obj.as_pointer(): obj for obj in scene.objects}
    collection_records = []
    render_visible = set()

    def collection_walk(collection, inherited_hidden=False, parents=()):
        hidden = inherited_hidden or bool(collection.hide_render)
        visible_here = not hidden and collection.as_pointer() in render_layer_collections
        direct_visible = set()
        if visible_here:
            for obj in collection.objects:
                if obj.as_pointer() in scene_objects and not obj.hide_render:
                    direct_visible.add(obj.name)
                    render_visible.add(obj.as_pointer())
        descendants_visible = set(direct_visible)
        for child in collection.children:
            descendants_visible.update(collection_walk(child, hidden, parents + (collection.name,)))
        meshes = [obj for obj in collection.all_objects if obj.type == "MESH" and obj.as_pointer() in scene_objects]
        collection_records.append({
            "name": collection.name,
            "library_path": library_path(collection.library),
            "parents": list(parents),
            "scene_reachable": True,
            "hide_render": bool(collection.hide_render),
            "inherited_render_hidden": hidden,
            "object_count": len(collection.all_objects),
            "mesh_names": sorted(obj.name for obj in meshes),
            "visible_mesh_names": sorted(obj.name for obj in meshes if obj.name in descendants_visible),
        })
        return descendants_visible

    collection_walk(scene.collection)
    property_keys = manifest.get("inspection", {}).get("property_keys", [])

    def properties(identifier):
        values = {}
        for key in property_keys:
            if key in identifier:
                value = identifier[key]
                if isinstance(value, (str, bool, int, float)):
                    values[key] = value
        return values

    objects = [{
        "name": obj.name,
        "type": obj.type,
        "library_path": library_path(obj.library),
        "collections": sorted(col.name for col in obj.users_collection),
        "hide_render": bool(obj.hide_render),
        "render_visible": obj.as_pointer() in render_visible,
        "properties": properties(obj),
    } for obj in scene.objects]
    images = []
    for image in bpy.data.images:
        packed = bool(image.packed_file) or bool(getattr(image, "packed_files", []))
        record = {"name": image.name, "source": image.source, "packed": packed}
        if image.source == "FILE" and not packed and image.filepath:
            record["path"] = normal_path(bpy.path.abspath(image.filepath, library=image.library))
            record["exists"] = os.path.isfile(record["path"])
        images.append(record)

    # Independently record whether disk sources changed during this inspection.
    for record in tracked.values():
        if record["exists"]:
            after = inspect_file(record["path"])
            record["unchanged_during_inspection"] = (
                after.get("sha256") == record.get("sha256") and after.get("bytes") == record.get("bytes")
            )
    for record in libraries:
        record["unchanged_during_inspection"] = tracked[record["path"]].get("unchanged_during_inspection")

    return {
        "inventory_schema": 1,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "blender_version": bpy.app.version_string,
        "master": master,
        "libraries": libraries,
        "collections": collection_records,
        "objects": objects,
        "images": images,
        "unit_scale_length": scene.unit_settings.scale_length,
        "unit_system": scene.unit_settings.system,
        "scene_properties": properties(scene),
        "cameras": sorted(obj.name for obj in scene.objects if obj.type == "CAMERA"),
        "active_camera": scene.camera.name if scene.camera else None,
        "enabled_render_layers": enabled_layers,
        "dirty_before": dirty_before,
        "dirty_after": bool(bpy.data.is_dirty),
        "scene_saved_by_validator": False,
    }


def validate(manifest, inventory, asset_root=None):
    """Pure-data checks, usable with synthetic fixtures outside Blender."""
    checks = []

    def check(identifier, condition, detail, scope="preflight"):
        checks.append({"id": identifier, "status": "PASS" if condition else "FAIL", "scope": scope, "detail": detail})

    root = asset_root or manifest.get("asset_root", "")
    identity = manifest.get("identity", {})
    areas = identity.get("area_ids", [])
    source_ids = [source.get("area_id") for source in manifest.get("sources", [])]
    check("manifest_schema", manifest.get("schema_version") == 1, "Supported bundle schema is 1.")
    check("bundle_identity", all(identity.get(key) for key in ("adventure_id", "site_id", "source_ref", "area_ids")),
          "Identity is explicitly declared, not inferred from an area-number prefix.")
    check("source_area_identity", len(source_ids) == len(set(source_ids)) and set(source_ids) == set(areas),
          {"declared_areas": areas, "source_areas": source_ids})
    check("asset_root", bool(root), "An explicit bundle root is required.")
    check("inventory_schema", inventory.get("inventory_schema") == 1, "Only normalized inventory schema 1 is accepted.")
    for key, expected in manifest.get("expected_scene_properties", {}).items():
        observed = inventory.get("scene_properties", {}).get(key)
        if observed is None:
            checks.append({"id": "identity_property:" + key, "status": "UNVERIFIED", "scope": "provenance",
                           "detail": {"expected": expected, "observed": None, "meaning": "No scene tag was authored by this inspection."}})
        else:
            check("identity_property:" + key, observed == expected, {"expected": expected, "observed": observed})

    files = {normal_path(item.get("path", "")): item for item in inventory.get("libraries", [])}
    master = inventory.get("master", {})
    expected_master = asset_path(root, manifest.get("master", {}).get("path", ""))
    check("master_selection", normal_path(master.get("path", "")) == expected_master,
          {"expected": expected_master, "observed": master.get("path")})

    file_specs = [("master", manifest.get("master", {}), master)]
    for source in manifest.get("sources", []):
        expected = asset_path(root, source.get("path", ""))
        record = files.get(expected, {})
        file_specs.append((source.get("area_id", "unknown"), source, record))
        check("source_link:" + source.get("area_id", "unknown"), bool(record), {"expected_library": expected})
    expected_libraries = {asset_path(root, source.get("path", "")) for source in manifest.get("sources", [])}
    if not manifest.get("allow_extra_libraries", False):
        extra = sorted(set(files) - expected_libraries)
        check("library_allowlist", not extra, {"unexpected_libraries": extra})

    unpinned = []
    for label, spec, record in file_specs:
        check("file_exists:" + label, record.get("exists") is True, record.get("path", spec.get("path")))
        if spec.get("bytes") is not None:
            check("file_bytes:" + label, record.get("bytes") == spec["bytes"],
                  {"expected": spec["bytes"], "observed": record.get("bytes")})
        if spec.get("sha256"):
            check("file_sha256:" + label, record.get("sha256") == spec["sha256"],
                  {"expected": spec["sha256"], "observed": record.get("sha256")})
        else:
            unpinned.append(label)
        if "unchanged_during_inspection" in record:
            check("file_stable:" + label, record["unchanged_during_inspection"] is True, "Before/after source hash comparison.")
    checks.append({"id": "source_hash_pins", "status": "UNVERIFIED" if unpinned else "PASS", "scope": "provenance",
                   "detail": {"unpinned_artifacts": unpinned, "meaning": "Observed hashes do not confer artistic or source approval."}})

    collections = inventory.get("collections", [])
    object_records = inventory.get("objects", [])
    for source in manifest.get("sources", []):
        expected_library = asset_path(root, source.get("path", ""))
        for required in source.get("collections", []):
            name = required["name"]
            matches = [item for item in collections if item.get("name") == name
                       and normal_path(item.get("library_path") or "") == expected_library
                       and item.get("scene_reachable") is True]
            check("collection:" + name, len(matches) == 1,
                  {"expected_exact_name": name, "expected_library": expected_library, "matches": len(matches)})
            if len(matches) != 1:
                continue
            actual = matches[0]
            mesh_names = set(actual.get("mesh_names", []))
            visible_names = set(actual.get("visible_mesh_names", []))
            check("object_inventory:" + name, actual.get("object_count", 0) >= required.get("min_objects", 0),
                  {"minimum": required.get("min_objects", 0), "observed": actual.get("object_count", 0)})
            check("mesh_inventory:" + name, len(mesh_names) >= required.get("min_meshes", 0),
                  {"minimum": required.get("min_meshes", 0), "observed": len(mesh_names)})
            check("visible_mesh_inventory:" + name, len(visible_names) >= required.get("min_visible_meshes", 0),
                  {"minimum": required.get("min_visible_meshes", 0), "observed": len(visible_names)})
            absent = sorted(set(required.get("visible_mesh_names", [])) - visible_names)
            check("intended_visible_objects:" + name, not absent, {"missing_or_hidden_exact_objects": absent})

    exclusions = manifest.get("exclusions", {})
    for name in exclusions.get("absent_collections", []):
        included = [item for item in collections if item.get("name") == name and item.get("scene_reachable")]
        check("excluded_collection:" + name, not included, "This collection must not be linked into this assembly audience.")
    for name in exclusions.get("hidden_collections", []):
        visible = [item for item in collections if item.get("name") == name and item.get("visible_mesh_names")]
        check("hidden_legacy_collection:" + name, not visible, "Legacy art may be retained, but must not substitute for the selected visible finish.")
    flagged = []
    for obj in object_records:
        if not obj.get("render_visible"):
            continue
        for pattern in exclusions.get("visible_name_patterns", []):
            if re.search(pattern, obj.get("name", ""), flags=re.IGNORECASE):
                flagged.append({"object": obj["name"], "rule": pattern})
        for key, forbidden in exclusions.get("visible_property_values", {}).items():
            if key in obj.get("properties", {}) and obj["properties"][key] in forbidden:
                flagged.append({"object": obj["name"], "property": key})
    check("known_player_exposure_markers", not flagged, {"flagged_visible_objects": flagged,
          "limit": "Metadata/name scan only. It does not prove concealed geometry is visually safe."})

    if "unit_scale_length" in manifest:
        value = inventory.get("unit_scale_length")
        check("unit_scale_length", isinstance(value, (int, float)) and abs(value - manifest["unit_scale_length"]) <= 1e-9,
              {"expected": manifest["unit_scale_length"], "observed": value})
    missing_images = [item.get("name") for item in inventory.get("images", []) if item.get("source") == "FILE"
                      and not item.get("packed") and item.get("exists") is False]
    check("external_image_files", not missing_images, {"missing": missing_images,
          "limit": "No rendered material correctness or sequence/UDIM completeness claimed."})

    route_blockers = []
    for connection in manifest.get("connections", []):
        check("connection_identity:" + connection["id"], connection.get("from") in areas and connection.get("to") in areas,
              {"from": connection.get("from"), "to": connection.get("to")})
        check("connection_intent:" + connection["id"], connection.get("state") in {"OPEN_CANDIDATE", "BLOCKED", "NOT_MODELED"},
              {"declared_state": connection.get("state"), "limit": "Intent only; physical passage is not measured by this preflight."})
        if connection.get("required_for_release") and connection.get("state") == "NOT_MODELED":
            route_blockers.append(connection["id"])

    preflight = "FAIL" if any(item["scope"] == "preflight" and item["status"] == "FAIL" for item in checks) else "PASS"
    gates = {"assembly_inventory": {"status": preflight, "scope": "Exact membership/visibility/library subset only"}}
    for name, specification in manifest.get("review_gates", {}).items():
        # Review gates are recorded evidence, never automatically certified by an inventory pass.
        status = specification.get("status", "UNVERIFIED")
        gates[name] = {"status": status if status in VALID_STATES else "UNVERIFIED",
                       "scope": "Recorded review state; not rerun by this validator", "evidence": specification.get("evidence"),
                       "reason": specification.get("reason")}
    gates["route_completion"] = {"status": "FAIL" if route_blockers else "UNVERIFIED", "blockers": route_blockers,
                                  "scope": "Declared route contracts, not native physical traversal"}
    release = "FAIL" if any(gate["status"] == "FAIL" for gate in gates.values()) else "UNVERIFIED"
    return {"report_schema": 1, "bundle_id": manifest.get("bundle_id"), "identity": identity,
            "preflight": preflight, "release": release, "exit_code": 2 if preflight == "FAIL" else 0,
            "checks": checks, "gates": gates,
            "statement": "A preflight PASS certifies only the listed inventory checks; no artistic, source, player-safety or gameplay acceptance is granted."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--snapshot", help="Use normalized inventory JSON instead of live bpy inspection.")
    parser.add_argument("--asset-root", help="Explicit relocated asset root; all source paths remain relative.")
    parser.add_argument("--output", required=True, help="Write report and full read-only inventory JSON.")
    args = parser.parse_args(argv)
    output = Path(args.output).resolve()
    protected_inputs = {Path(args.manifest).resolve()}
    if args.snapshot:
        protected_inputs.add(Path(args.snapshot).resolve())
    if output.suffix.lower() != ".json" or output in protected_inputs:
        parser.error("--output must be a separate .json report, not an input or scene file.")
    try:
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8-sig"))
        if args.asset_root:
            manifest["asset_root"] = args.asset_root
        inventory = (json.loads(Path(args.snapshot).read_text(encoding="utf-8-sig")) if args.snapshot
                     else collect_blender_snapshot(manifest))
        report = validate(manifest, inventory)
        report["inventory"] = inventory
    except Exception as error:
        report = {"report_schema": 1, "preflight": "FAIL", "release": "UNVERIFIED", "exit_code": 3,
                  "error": {"type": type(error).__name__, "message": str(error)}}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    failures = [item["id"] for item in report.get("checks", []) if item["status"] == "FAIL"]
    print(json.dumps({"report": str(output), "preflight": report["preflight"], "release": report["release"],
                      "failed_checks": failures, "exit_code": report["exit_code"]}))
    return report["exit_code"]


if __name__ == "__main__":
    arguments = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    raise SystemExit(main(arguments))
