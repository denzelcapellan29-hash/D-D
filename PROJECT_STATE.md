# Project State

Updated: 2026-10-04

## Active runtime
Minecraft Java 26.3 + Fabric + WorldEdit is the primary campaign runtime.

## Bridge
- Live bridge transport is operational.
- Google Drive is used for durable state/results.
- GitHub queue is used for low-latency command batches.
- Bridge agent v0.1.3 fixed queue-cache behavior.
- Fabric bridge v0.2.0 has compiled successfully and adds compressed bulk `/region` inspection for up to 500,000 blocks.
- v0.2.0 still requires local install/restart before live region inspection can begin.

## Dock Ward vertical slice
First live build pass completed against `Acq Waterdeep — Dock Ward`.
- Initial revision: 184/211 commands completed before an unsupported decorative `minecraft:chain` block stopped the batch.
- Resume revision: 28/28 commands completed successfully.
- Readback probes confirmed expected roof, crane, street, and water blocks.
- Current slice includes continuous ground/street, attached rowhouses, warehouse frontage, quay, water, piers, cargo, lamps, and cranes.

## Immediate next milestone
Install Fabric bridge v0.2.0, read the live slice back as compressed region data, run structural QA, repair defects automatically, then iterate the Dock Ward generator before expanding scope.

## Scope gate
Do not expand to full Waterdeep or D&D gameplay systems until the Dock Ward waterfront → warehouse → fissure → dungeon vertical slice is convincingly playable and can be maintained autonomously.
