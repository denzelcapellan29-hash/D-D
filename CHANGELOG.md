# Changelog

## 2026-10-04

### Minecraft Bridge
- Established live ChatGPT → GitHub queue → local bridge agent → Fabric mod → Minecraft command path.
- Established Minecraft → bridge agent → Google Drive result/state path.
- Changed health heartbeat to write only on state changes, avoiding Drive sync churn.
- Added cache-busting queue polling in bridge agent v0.1.3.
- Added Fabric bridge v0.2.0 `/region` endpoint with palette + run-length compressed live block-state readback for bounded regions.

### Dock Ward
- Executed first live Dock Ward waterfront build batch.
- Built a bounded continuous street/quay slice with attached rowhouses, warehouse frontage, water, piers, cargo, lighting, and crane structures.
- Recovered from unsupported `minecraft:chain` block without rebuilding the region.
- Completed resumed build and block-level readback probes successfully.
