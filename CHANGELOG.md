# Changelog

## 2026-10-04

### Minecraft Bridge
- Established live ChatGPT → local bridge agent → Fabric mod → Minecraft world mutation.
- Established Minecraft → bridge agent → Google Drive result/state readback.
- Added Fabric bridge v0.2.0 `/region` endpoint with palette + run-length compressed live block-state inspection.
- Added bridge agent v0.2.4 Drive filename-encoded live write transport, removing GitHub queue dependency for active world edits.

### Dock Ward
- Completed first live waterfront build and recovery pass.
- Added attached rowhouses, warehouse frontage, quay, piers, cargo, cranes, lamps, and market awnings.
- Added a moored merchant vessel with mast, sails, cabin, cargo, gangplank, and mooring posts.
- Extended inland with a continuous second street/frontage and four attached multi-story buildings.
- Added curbs, street lamps, market stalls, roofline variation, chimneys, and working clutter.
- Combined live readback covered 133,590 blocks.
- Structural QA detected a one-block north/south street pinch; repaired it live into a covered passage.

### QA / world-feel follow-up
- Expanded live QA to 179,340 blocks spanning harbor through deeper background context.
- Repaired four detached legacy roof strips, one isolated chain, and a disconnected bowsprit.
- Final structural graph contains exactly two intentional non-water components: city + moored vessel.
- Extended the cross street through the older background row and added a deeper skyline mass.
- Restored crane rigging with the correct 26.3 block ID: `minecraft:iron_chain`.

### Headless rendering / resource-pack workflow
- Formalized geometry/material separation for Minecraft world generation.
- Added visual profile schema for block color/texture/opacity/emissive metadata.
- Added resource-pack palette extractor for rapid aesthetic comparison.
- Changed intended release workflow toward prebuilt validated Minecraft world saves for direct import.

### Offline world compiler / release v0.2
- Compiled `Acq_Waterdeep_DockWard_WORLD_v0_2.zip` as a direct-import Minecraft save.
- Patched 179,340 live-readback cells into the prebuilt Episode 1 world with zero post-build mismatches.
- Removed visible vanilla grass from the authored context envelope without overwriting non-grass authored surfaces.
- Added 35 deterministic background urban masses in previously empty cells.
- Validated all 300 pregenerated chunks after rewrite; zero chunk/NBT parse failures.
- Persisted the release to Google Drive Build Artifacts.

### Offline world compiler / release v0.3
- Added strict support-graph validation for authored above-ground geometry.
- Removed 82 unsupported non-vessel components (6,258 blocks) from the controlled working envelope.
- Preserved only two explicit small sail-vessel components as intentionally unsupported over water.
- Cleared uncontrolled terrain and legacy above-ground geometry outside the coordinate-defined envelope, leaving a neutral lower datum instead of vanilla grass/legacy clutter.
- Eliminated all remaining `grass_block` cells in the pregenerated surface volume.
- Replaced 23 obsolete `minecraft:chain` block states with `minecraft:iron_chain`.
- Revalidated all 300 pregenerated chunks with zero parse failures.
- Confirmed the verified live corridor still matches exactly with zero block mismatches.
- Persisted `Acq_Waterdeep_DockWard_WORLD_v0_3.zip` to Google Drive Build Artifacts.

### Offline world compiler / release v0.4
- Replaced the visible neutral sandbox plate with a continuous city/harbor context shell across the full 320×240 pregenerated footprint.
- Added 111 deterministic background buildings, 3 skyline towers, 6 piers, 3 context vessels and 5 cranes.
- Added continuous street paving and irregularized harbor shoreline outside the protected Episode 1 core.
- Changed future flat-world generation to bedrock + stone datum only, eliminating new dirt/grass superflat bleed.
- Preserved the protected Episode 1 core exactly with zero block mismatches.
- Structural QA found only the two previously allowed small sail-vessel components unsupported; no new floating architectural components were introduced.
- Validated all 300 pregenerated chunks with zero parse failures.
- Persisted `Acq_Waterdeep_DockWard_WORLD_v0_4.zip` to Google Drive Build Artifacts.
