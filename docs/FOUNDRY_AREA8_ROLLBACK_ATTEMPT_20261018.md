# Area 8 rollback attempt — 2026-10-18

DM explicitly authorizes restoring last working Area8 over retaining incomplete Episode2 experiments.

Last good visually rendered Area8 first-person screenshot: 2026-10-16 23:15 EDT, and live inspector 23:21 EDT. Those successes already used the custom patched 3D Canvas camera scripts; reverting to pristine vendor JS would NOT recreate that exact last-good state.

Episode2 hourly and older Area8 scheduled tasks are confirmed disabled.

Blender native and CLI MCP both returned Session terminated, preventing local Windows module-file rollback or backup inspection in this run. Drive targeted backup/snapshot searches surfaced documentation only; no independently verified full-world Oct16 snapshot found.

Foundry scene_list before showed Test active, original Area8 inactive. Executed Foundry scene_activate original NUEDEFAULTSCENE0 SUCCESS. Readback: original Area8 active, Test inactive, both scenes preserved.

Acq 3D inspector after activation returned ok true, levels3d_active true, 161 3D Tiles, revision f50519b24f54284977740fe8a5db6bee8f5b26ac6dc64c7e6edbaa58bdf5c05c. This is NOT visual QA.

Actual Area8 3D Canvas capture_3d_view failed RuntimeException. Foundry ordinary scene_get succeeded, with 2 QA tokens, 6 lights, 36 walls, 13 regions. NO rendered image pass.

Attempt to inspect inactive Test for controlled cleanup failed RuntimeException; no QA Tiles were deleted. No third-party script edits or Area8 document changes this turn besides original scene activation.

Native plugin main.js was previously found locally patched since Oct16 22:43 EDT and already working at Oct16 23:15. No evidence same-code restore will cure current shader initialization failure. Current local file-control MCP session is disconnected, and hosted Foundry tool surface has no direct desktop file restore / process restart operation.

Next safe action after local control restoration: backup current world, patch+backup files; locate real last-good snapshot if one exists; controlled client restart and renderer capture. If still failed, reversible native-module A/B including GameCamera.js with actual renderer/movement QA and documented 404/WebGL client errors. Do not blindly overwrite current patched main.js or world database.

Status: Scene activation rollback DONE, full 3D runtime restoration NOT CERTIFIED. All previous Area8 originals and Episode2 artifacts preserved, automations disabled.
