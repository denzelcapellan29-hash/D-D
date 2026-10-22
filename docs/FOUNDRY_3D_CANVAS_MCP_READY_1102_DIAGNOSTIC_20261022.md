# 3D Canvas MCP verification after DM "ready" — 2026-10-22 approximately 11:02 EDT

**Status: NEW MCP TOOL REGISTRY CONFIRMED; GM COMMAND EXECUTION NOT VERIFIED; NO SCENE WRITES.**

## Evidence
1. At beginning of current turn, `ALL_TOOLS` exposed **eight** `mcp__Acq_3D_Map__` operations including the newly deployed `inspect_3d_capabilities(scene_id?)`. This verifies the ChatGPT secure tunnel / MCP tool schema refresh succeeded. This is a real improvement over previous seven-tool snapshot.
2. `mcp__Acq_3D_Map__inspect_3d_scene({})` failed with the connector generic `INVALID_ARGUMENT / Error executing tool inspect_3d_scene`; `inspect_3d_capabilities({})` failed with the same generic outer error. Root cause/error response hidden at this boundary. Do not claim 3D Canvas is active or that the native APIs were inspected. No additional 3D runtime attempts made afterward.
3. Hosted `mcp__Foundry_MCP__world_info({})` succeeds: V14.368, dnd5e 6.0.5. This verifies a different Foundry MCP integration is alive, not the first-party Acq GM browser polling path.
4. Live Windows diagnostic agent processed `automation/results/health-20261022-after-ready.json`: ports 18747 (Acq agent), 18748 (Acq MCP), and 8083 (Foundry) **listening**; `levels-3d-preview`, `canvas3d-premium`, `canvas3dcompendium`, `acq-foundry-bridge` module directories present.
5. Live installed first-party bridge SHA256 in `automation/results/bridge-js-hash-after-ready-20261022.json` is still expected **0129dbefea404c56fb7d5206355f4f896fe26e30820fc824e8a38c305aed3ad9**, 40,874 bytes. No unexpected disk regression after restarts.
6. Source review of current first-party Foundry module `integrations/foundry-bridge/module/acq-foundry-bridge/scripts/acq-foundry-bridge.js` shows `Hooks.once("ready")` only calls `startPolling()` if `game.user.isGM` **and** `game.settings.get("acq-foundry-bridge","enabled")` is true. Client-side `pollCommand` calls local `http://127.0.0.1:18747/bridge/next`; server agent `enqueue_rpc` blocks until GM consumes and posts result; the exposed Python method does not bypass client polling.
7. `acq_bridge_agent.py` Origin allowlist is **localhost/127.0.0.1 only**. If the GM browser is opened from a different hostname/origin (e.g. LAN IP or external domain), browser-origin CORS may block its calls to local agent despite listening ports. This is a hypothesis requiring a live nonsecret diagnostic, not a proven cause.
8. Earlier 3D inspect (previous turn) was successful when runtime reported `levels3d_active:false`, scene `NUEDEFAULTSCENE0` revision `e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`. Last known document state intact; current revision **unverified** because Acq inspection is failing. No scene writes or GM view changes attempted in this turn.

## Next verified narrow diagnostic — USER READ-ONLY CHECK (no new installations)
In Foundry **GM browser** with world open, open F12 DevTools Console and paste:

```js
(async () => {
 const id="acq-foundry-bridge";
 let enabled=null,url=null,configError=null;
 try{enabled=game.settings.get(id,"enabled");url=game.settings.get(id,"agentUrl");}
 catch(e){configError=String(e);}
 let agentStatus=null;
 try{const r=await fetch((url||"http://127.0.0.1:18747").replace(/\/$/,"")+"/health",{cache:"no-store"});
   agentStatus={httpStatus:r.status,ok:r.ok};}
 catch(e){agentStatus={error:String(e)};}
 const report={gm:!!game.user?.isGM,bridgeModuleActive:!!game.modules?.get(id)?.active,
  bridgeLoaded:!!globalThis.AcqFoundryBridge,bridgeEnabled:enabled,
  canvas3dActive:!!game.Levels3DPreview?._active,
  originIsLocal:/^(localhost|127\.0\.0\.1)$/.test(location.hostname),
  localAgentUrl:(url||"").startsWith("http://127.0.0.1:18747"),
  configError,agentStatus};
 console.log("ACQ_BRIDGE_DIAG",report);
})();
```

No secrets, API tokens, actor data, or full URLs are exposed by that report. Use output to distinguish missing GM permissions, disabled module, missing ready hook, browser-origin CORS, and agent disconnect. This diagnostic is not an instruction to change settings before root cause is known.

## Safety / subsequent steps
No further runtime calls until nonsecret GM browser diagnostic or equivalent trusted live telemetry identifies the cause. Do not trigger arbitrary JS via bridge, modify vendor modules, overwrite installed FPS stabilization or Scene documents. Preserve v0.3 rollback backup `capability-20261022T135404.612515Z`. Once diagnosed/repaired, re-run first-party `inspect_3d_scene` and new `inspect_3d_capabilities` and inspect camera, assets, renderer before implementing live adapter. Godot still primary until fair 3D Canvas benchmark.
