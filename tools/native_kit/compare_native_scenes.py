"""Compare generated environment payloads without hiding semantic changes.

Read-only and provider-independent except for one explicitly named generation-ID
field. This checks native construction data, not art, traversal, performance,
full-world installation, permissions outside these scenes or source fidelity.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


GENERATOR = "baileywiki-3d-building-generator"
COLLECTIONS = ("tiles", "lights", "walls", "regions", "drawings", "sounds", "notes", "templates")
CONFIGURATION = ("width", "height", "padding", "grid", "levels", "initialLevel", "environment",
                 "tokenVision", "fog", "weather", "ownership")
REMOVED = ("document._id", "document._stats", f"document.flags.{GENERATOR}.gen")


def serialized(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def normalized_document(document):
    """Remove only creation identity, audit metadata and this generator's ID."""
    result = copy.deepcopy(document)
    result.pop("_id", None)
    result.pop("_stats", None)
    flags = result.get("flags", {}).get(GENERATOR, {})
    if isinstance(flags, dict):
        flags.pop("gen", None)
    return result


def environment_payload(scene):
    if not isinstance(scene, dict):
        raise ValueError("A raw native Scene JSON object is required")
    if scene.get("tokens"):
        raise ValueError("Environment comparison requires no live/temporary tokens")
    result = {"configuration": {key: scene[key] for key in CONFIGURATION if key in scene}}
    # Native renderer settings are construction-relevant. History, scene names
    # and recipe identities are not silently used as substitutes for geometry.
    result["native_settings"] = copy.deepcopy(scene.get("flags", {}).get("levels-3d-preview", {}))
    for name in COLLECTIONS:
        values = scene.get(name, [])
        if not isinstance(values, list):
            raise ValueError(f"Scene {name} must be an exported document list")
        result[name] = sorted(serialized(normalized_document(value)) for value in values)
    return result


def fingerprint(value):
    return hashlib.sha256(serialized(value).encode("utf-8")).hexdigest()


def compare(first, second):
    a, b = environment_payload(first), environment_payload(second)
    changed = [key for key in a if a[key] != b[key]]
    return {
        "equal": not changed,
        "changed_sections": changed,
        "sha256_a": fingerprint(a),
        "sha256_b": fingerprint(b),
        "counts_a": {key: len(a[key]) for key in COLLECTIONS},
        "counts_b": {key: len(b[key]) for key in COLLECTIONS},
        "removed_fields": list(REMOVED),
        "configuration_fields": list(CONFIGURATION),
        "scope": "Declared environment configuration, native renderer settings and complete embedded environment document payloads. Not source, art, gameplay or full-world acceptance.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    args = parser.parse_args()
    result = compare(json.loads(args.first.read_text(encoding="utf-8-sig")),
                     json.loads(args.second.read_text(encoding="utf-8-sig")))
    print(json.dumps(result, indent=2))
    return 0 if result["equal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
