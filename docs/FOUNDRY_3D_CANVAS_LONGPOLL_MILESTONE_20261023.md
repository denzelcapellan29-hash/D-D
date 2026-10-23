# Foundry / native 3D Canvas tool registry and browser command reliability milestone — 2026-10-23
**Status:** CONNECTOR SCHEMA PASS; FIRST-PARTY LONG-POLL DEPLOYED & LIVE END-TO-END READ-ONLY QA PASS; native 3D visual/gameplay QA NOT CERTIFIED.

## Effective authority and ownership
The DM requires full use of **existing native Foundry V14, D&D5e and 3D Canvas 9.0.36 + Premium 9.0.3, Mapmaking Pack 10.0.1 / Token Pack**, without rebuilding physics, camera, sight, doors, editor, particles or cinematics in custom code. Foundry+3D Canvas is primary target, Godot exploratory. This milestone updates only our first-party `acq-foundry-bridge.js` and `acq_bridge_agent.py`; no third-party source, Foundry game documents, scene art, Blender source or Godot files were edited.

## Actual tool surface
On a newly refreshed project chat the **ChatGPT Acq_3D_Map registry exposes all 14 native wrapper actions** (previous chat held a stale eight-action schema). Foundry_MCP remains 121 tools. A previously hidden `inspect_3d_native_workflows` was called directly successfully, with stable source revision. This is a host schema/cache issue resolved by user refresh plus new chat, not a missing 3D Canvas module feature.

## Root-cause telemetry: background-throttled browser polling
Installed client used JavaScript `setInterval(pollCommand, pollMs)`, default one second, with GET `/bridge/next` requesting immediate HTTP204 if no job. After installing only our agent-side heartbeat, real GETs were logged **09:26:14, 09:27:14, 09:28:14 local time**, once per minute, while RPC timed out HTTP504 in between. This strongly matches Chromium background timer throttling; the browser's internal `document.visibilityState` was not directly read, so document visibility is inferred, not proven. Windows also showed a minimized Chrome window titled Acq 3D Map but that does not identify the GM polling tab by itself. Simple HTTP200 health was not proof of GM command readiness.

## Firstparty agent heartbeat deployment (PASS)
- Source candidate from feature `feature/foundry-3d-poll-telemetry-20261023`, GitHub draft PR [#3](https://github.com/denzelcapellan29-hash/D-D/pull/3); isolated fixture tests **4/4 PASS**, Python syntax PASS.
- SHA-guarded firstparty agent upgrade with immutable backup and one rollback path (not a vendor or scene update). Installed SHA256 `93edf24c0bcc60f3a3a63fe611b83303fec024fff4f5289194203b23184f49d2`; backup `bridge-agent-heartbeat-20261023T132601Z`; native GM polling observed after restart. Optional `ACQ_REQUIRE_RECENT_GM_POLL=1` remains **disabled** by default.
- The persistent, DM-authorized guarded **v0.4 watcher** remained installed and verified; its own schema only permits first-party module JS/Python MCP deploy jobs, **not** the agent Python file. Do not describe a standalone scoped agent deploy as a v0.4 watcher job.

## Solution: pending HTTP long polling, not a duplicate 3D engine (LIVE PASS)
- Source-bounded patcher [`tools/patch_bridge_longpoll_20261023.py`](https://github.com/denzelcapellan29-hash/D-D/blob/feature/bridge-native-longpoll-20261023/tools/patch_bridge_longpoll_20261023.py) and scoped [deployment script](https://github.com/denzelcapellan29-hash/D-D/blob/feature/bridge-native-longpoll-20261023/tools/guarded_bridge_longpoll_deploy_20261023.py); staging branch `feature/bridge-native-longpoll-20261023`.
- Agent `GET /bridge/next?wait_ms=20000` supports a bounded 20-second pending HTTP request, capped server-side at 22 seconds; old requests without wait_ms remain immediate. Agent uses a thread-local sleep/recheck of its **existing command queue**, no custom native 3D logic. `/health` adds `active_browser_longpoll_requests`. Native JS `continuousBridgePoll()` awaits each pending GET and immediately launches the next—**no `setInterval` for normal command delivery**; bounded failed-request backoff only.
- Strict pinned source SHAs, Node `--check` PASS, Python AST PASS and isolated `ThreadingHTTPServer` fixture PASS: idle longpoll HTTP204 after expected wait, enqueued RPC immediately delivered HTTP200 and result unblocks waiter, active count returns zero. No fixture touched live world or module.
- **Real dry-run pass** before writes, original accepted Scene SHA pinned, no pending/inflight commands; immutable checkpoint and single rollback: `longpoll-bridge-20261023T134050Z`.
- Installed first-party agent SHA256 `a44aeb6ba646b3d99532ab2816fc8007d47101243c0c4fdf3063e9d94f96c2ec`; installed first-party browser JS SHA256 `a0085c1f437c5da57feb5bd9e8554803f80226ca5ff7d6cf341bb689745bf443`. Agent restarted with native local port18747 HTTP200. Source Scene `NUEDEFAULTSCENE0` SHA **`e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f` unchanged. Foundry's HTTP module route served the new JS byte-for-byte.
- Initial Windows PostMessage F5 alone did not activate browser script. One guarded foreground-verified F5 to the exact Foundry window PID42440 sent. Delayed readback at **09:47:38 local** confirmed multiple real `GET /bridge/next?wait_ms=20000` requests, active longpoll=1 and last-poll age0.6sec. This supersedes earlier checks before browser startup completed.
- Live agent idle `wait_ms=750` fixture HTTP204 in ~772ms while production browser simultaneously maintained its own longpoll.
- Direct **ChatGPT-host native MCP QA**, all `ok=true`, source SHA exactly unchanged before/after:
  - `inspect_3d_native_workflows` ~**3.95 sec**
  - `inspect_3d_settings` ~**2.86 sec**
  - `inspect_3d_capabilities` ~**1.43 sec**
  Zero HTTP504 over this short three-call acceptance sample. **Do not claim indefinite reliability**, 3D runtime currently `active=false,ready=false`, no player-eye movement/doors/vision/GLB full import tested in this milestone.

## Version/checkpoint labels
- `v0.4 watcher` — persistent first-party deploy watcher version, distinct from agent and browser source.
- `heartbeat` agent source superseded by `longpoll` agent source; both checkpoints remain available.
- `SAVED/DEPLOYED AND CONNECTIVITY QA PASS` does **not** imply `DM ACCEPTED` visuals or full native 3D playability.
- Restarts and 3D UI writes require a fresh revision checkpoint, no third-party module patching, and safe QA clone per playability skill.

## Next development
1. Maintain exact canonical first-party source and script provenance; ensure GitHub/Drive/installed workflow skill reflect this recovery. Do not revert to interval polling or request multiple F5 retries by default.
2. QA native operations on inactive clone: native firstperson and GameCamera with selected QA token, Tile collision/sight flags, doors, Foundry v14 Surfaces separately from 3D Canvas BVH; non-GM view and 3D renderer must actually be ready.
3. Benchmark longpoll under minimized/background GM for repeated commands and cold reload. If it regresses, inspect `active_browser_longpoll_requests`, `browser_poll`, `browser_result`, and source hashes before any restart.
