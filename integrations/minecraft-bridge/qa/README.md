# Minecraft QA Infrastructure

This layer exists so campaign generation does not depend on manually opening Minecraft.

## Fast renderer
`vtk_render_world.py` reads the real Java Anvil save and emits deterministic off-screen `iso.png`, `top.png`, and `metrics.json`. It builds visible voxel faces only, so it is materially faster and clearer than the earlier point renderer.

The renderer preserves full block-state parsing in `world_reader.py`; its current color table is only the fast engineering material profile. Resource-pack/model resolution is a separate higher-fidelity stage.

## BlueMap
`bluemap_qa.ps1` pins BlueMap CLI 5.28, which supports Minecraft through 26.3. It can render the actual save and optionally load a resource pack from BlueMap's `config/packs` directory.

BlueMap requires Mojang client resources. The script intentionally does not set `accept-download: true` without explicit user agreement.

## Amulet
`amulet_probe.py` is non-destructive: it copies a world to a temporary directory, performs an Amulet load/save/reopen cycle, and leaves the source untouched.

The stable probe target is Amulet Core 1.9.49 (Python >=3.11). The current 2.0 development branch declares Python >=3.14, so it is not yet the compiler default.

## CI
`.github/workflows/minecraft-infra-smoke.yml` continuously verifies:
- BlueMap 5.28 starts on Java 25.
- stable Amulet imports on Python 3.13.
- PyVista off-screen rendering works.

## Production order
semantic world model -> deterministic geometry -> Minecraft save compiler -> fast VTK/PyVista QA -> BlueMap resource-pack-aware QA -> release ZIP.
