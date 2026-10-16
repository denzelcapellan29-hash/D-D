# Acq Windows Agent v0.2 guarded bridge diagnostics (2026-10-15)

Created tested v0.2 agent bundle in current conversation: Acq_Windows_Dev_Agent_v0.2.zip. Existing v0.1 was proven running on DM PC; v0.2 is NOT installed until DM upgrades it.

V0.2 keeps health, list_files, hash_file, first-party read_file. Adds ONLY deploy_bridge_diagnostics, guarded by --allow-deploy start flag, exact installed first-party bridge SHA256 c6f0a4e21beae724abe8a751033df201001276874d097c056d02b17267352008, exact candidate Git blob 8b922667d17994433217d9f2a42ae83678a1813a, module owner/path allowlist, Foundry process guard, immutable time-stamped backup, atomic replace, post-write digest comparison. It neither executes arbitrary PowerShell nor modifies third-party code. Native Windows deployment remains UNTESTED.

Staged candidate source tools/foundry3d/acq-foundry-bridge-v029-mesh-diagnostics.js was JavaScript-syntax validated via V8 (without executing JS), length 37,790 characters. Not installed; no renderer-level QA. Its inspection changes add bounded per-Tile mesh_evidence, which should distinguish a real descendant Three.Mesh with geometry from only Tile document/world bounding box.

Internal safety tests passed: blocked unsupported shell op, traversal source path and deploy when --allow-deploy absent. Other runtime, Foundry-process detection, rollback of crash and code integration remain untested. The existing Windows agent requires one manual update and restart; do not suggest autonomous deployment already exists.

The non-Draco diagnostic Tile was removed, original test scene revision d93c7518ac199375b7705715c1faf124b5cd35136ba8e8707ddc326ac15546ad restored, and custom inspect later reported tile_count 0. Latest intermittent manifest failure means no live further writing now. Built-in Mapmaking Pack Wall_Modular.glb is discoverable and reserved for a small known-good calibration comparison after safe tool health.

DM-approved Blender Area8 v082 remains untouched, Area9 frozen. Preserve existing work and no live-session changes.
