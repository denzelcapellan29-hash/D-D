# Roadmap

## Now — vertical slice quality gate
0. ~~Compile a direct-import world save from headless data and validate chunk integrity.~~
0a. ~~Structural cleanup / controlled-envelope world: remove unsupported geometry and vanilla terrain bleed.~~
0b. ~~World-context shell: replace the visible sandbox plate with continuous urban/harbor surroundings across the pregenerated footprint.~~
0c. ~~Lower Dock Ward scope lock + organic-city pass: curved streets, attached frontage, elevation, harbor context and structural cleanup.~~
1. ~~Install Fabric bridge v0.2.0.~~
2. ~~Read the live Dock Ward slice through compressed region inspection.~~
3. ~~Run structural QA from actual runtime data.~~
4. ~~Repair the first detected street-connectivity defect live.~~
5. Keep automatic structural readback active during edits.
6. ~~Replace Minecraft-camera dependency with headless colored voxel reconstruction for visual QA.~~
6a. ~~Infrastructure QA v0.1: read-only Anvil reader, direct VTK renderer, BlueMap runner, Amulet probe, and CI smoke validation.~~
7. BlueMap-render the actual lower-Dock save with resource-pack support after explicit Mojang asset-download approval.
8. Run the Amulet load/save/reopen probe against the actual world before considering replacement of the current low-level compiler.
9. Upgrade live region readback to include block-state properties for stairs/slabs/panes/orientation.
10. Add resource-pack/model resolution so visual profiles can be swapped without rebuilding geometry.
11. Continue bounded world-feel iteration:
   - stronger skyline/roof variation
   - richer alleys and loading yards
   - more harbor traffic and props
   - background architecture that prevents hard visual edges
12. Integrate the existing Episode 1 warehouse/fissure/dungeon build with the improved surface district.
13. Run end-to-end QA from Dock Ward street → warehouse → fissure → Area 1 → Area 2.
14. ~~Package an initial direct-import world release.~~ Promote to session-ready release only after the remaining visual/material and end-to-end Episode 1 QA gates pass.

## Stretch goal
- Full Waterdeep expansion only if later campaign needs justify it.

## Later
- WorldEdit-backed schematic operations, revision/undo safety, biome control, and queued large edits.
- Persistent broader Dock Ward and Waterdeep expansion.
- Optional D&D gameplay layer: initiative, actors, encounters, regions, journals, secrets, and encounter state.
