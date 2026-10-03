# Acq Foundry Bridge v0.1

A local pseudo-connector for Foundry VTT v14 + 3D Canvas.

## Architecture

```
ChatGPT
  ↕
Google Drive / D&D / Foundry Bridge
  ↕  Google Drive for Desktop sync
Acq Bridge Agent (Python, localhost only)
  ↕  HTTP on 127.0.0.1:18747
Acq Foundry Bridge module
  ↕
Foundry Scene + 3D Canvas
```

The bridge is declarative and revision-checked. It does not use `eval`, arbitrary JavaScript execution, shell commands, or direct Foundry database edits.

### v0.1 operations

- snapshot / ping
- set_3d_environment
- scene_update
- embedded_create / embedded_update / embedded_delete
- tile_set_model3d
- asset_upload

State, commands, results and automatic pre-command backups live in the synced `D&D/Foundry Bridge` transport folder.

The packaged installation kit is persisted in Google Drive under Build Artifacts and can also be generated from this source.
