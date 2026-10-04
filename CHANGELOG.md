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
