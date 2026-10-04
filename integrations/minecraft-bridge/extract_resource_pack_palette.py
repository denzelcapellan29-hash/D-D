#!/usr/bin/env python3
"""
Extract representative colors from a Minecraft Java resource pack.

This is the fast visual-profile path. It scans block texture PNGs, computes an
alpha-weighted representative RGB/hex value, and emits a texture-color catalog.
A later resolver can map blockstate/model JSON to specific face textures.
"""

from __future__ import annotations

import argparse
import io
import json
import zipfile
from pathlib import Path

from PIL import Image


def average_rgba(data: bytes) -> tuple[int, int, int, float]:
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    rs = gs = bs = weight = alpha_total = 0.0
    for r, g, b, a in im.getdata():
        if a == 0:
            continue
        w = a / 255.0
        rs += r * w
        gs += g * w
        bs += b * w
        weight += w
        alpha_total += a / 255.0
    if weight == 0:
        return 0, 0, 0, 0.0
    pixels = im.width * im.height
    return (
        round(rs / weight),
        round(gs / weight),
        round(bs / weight),
        min(1.0, alpha_total / max(1, pixels)),
    )


def iter_pack_pngs(source: Path):
    prefix = "assets/minecraft/textures/block/"
    if source.is_file():
        with zipfile.ZipFile(source) as z:
            for name in z.namelist():
                if name.startswith(prefix) and name.endswith(".png"):
                    yield name, z.read(name)
    else:
        base = source / "assets" / "minecraft" / "textures" / "block"
        for path in sorted(base.rglob("*.png")):
            yield "assets/minecraft/textures/block/" + path.relative_to(base).as_posix(), path.read_bytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resource_pack", help="Resource-pack ZIP or extracted directory")
    ap.add_argument("--profile-id", default="resource-pack")
    ap.add_argument("--output", default="texture_palette.json")
    args = ap.parse_args()

    source = Path(args.resource_pack)
    textures = {}
    for name, data in iter_pack_pngs(source):
        r, g, b, opacity = average_rgba(data)
        key = name.removeprefix("assets/minecraft/textures/").removesuffix(".png")
        textures[key] = {
            "hex": f"#{r:02X}{g:02X}{b:02X}",
            "rgb": [r, g, b],
            "opacity": round(opacity, 4),
            "texture": name,
        }

    out = {
        "profile_id": args.profile_id,
        "source_pack": source.name,
        "texture_count": len(textures),
        "textures": textures,
        "notes": "Fast texture-color catalog; blockstate/model resolution is a separate step."
    }
    Path(args.output).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
