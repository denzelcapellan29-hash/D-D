#!/usr/bin/env python3
"""First-party only: source-pinned long-poll patch for Acq Foundry Bridge.

Patch returns candidate source only; never writes to Foundry or runs deployment.
Purpose: replace background-throttled setInterval GET /bridge/next polling with
one pending HTTP request, allowing GM browser IO callbacks instead of timers.

The built-in 3D Canvas module and Premium module are NOT modified.
"""
from __future__ import annotations
import ast
import hashlib

EXPECTED_AGENT_SHA = "93edf24c0bcc60f3a3a63fe611b83303fec024fff4f5289194203b23184f49d2"
EXPECTED_BROWSER_SHA = "82cf6f20b10825ca09578d6103ede742174423b8db23956994ad4cd5fae189f1"

def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf8")).hexdigest()

def once(s: str, old: str, new: str, name: str) -> str:
    n = s.count(old)
    if n != 1:
        raise ValueError(f"STOP {name}: expected exactly one exact source occurrence, got {n}")
    return s.replace(old, new, 1)

def patch_agent(s: str) -> str:
    if sha(s) != EXPECTED_AGENT_SHA:
        raise ValueError("STOP: installed agent source SHA does not match pinned heartbeat v1")
    s = once(s,
        '        self.browser_result_count = 0\n',
        '        self.browser_result_count = 0\n'
        '        self.active_longpoll_count = 0\n',
        "agent init")
    s = once(s,
        '                "browser_result": {\n',
        '                "active_browser_longpoll_requests": self.active_longpoll_count,\n'
        '                "browser_result": {\n',
        "agent health")
    s = once(s,
        '                recent = self.last_browser_poll_monotonic is not None and (\n'
        '                    time.monotonic() - self.last_browser_poll_monotonic <= 10.0\n'
        '                )\n',
        '                recent = self.active_longpoll_count > 0 or (\n'
        '                    self.last_browser_poll_monotonic is not None and\n'
        '                    time.monotonic() - self.last_browser_poll_monotonic <= 10.0\n'
        '                )\n',
        "agent opt-in health guard")
    needle='    def write_result(self, result: dict) -> None:\n'
    added='''    def wait_next(self, world_id: str | None, scene_id: str | None,
                  wait_seconds: float = 0.0) -> dict | None:
        """Return a claimed native Foundry command, optionally waiting for arrival.

        A bounded pending GET keeps the browser command channel live even when
        background tabs throttle JavaScript timers. No new gameplay logic.
        """
        bounded = max(0.0, min(float(wait_seconds), 22.0))
        deadline = time.monotonic() + bounded
        self.mark_browser_poll(world_id, scene_id)
        if bounded:
            with self.lock:
                self.active_longpoll_count += 1
        try:
            while True:
                command = self.claim_next(world_id, scene_id)
                if command is not None:
                    return command
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return None
                time.sleep(min(0.15, remaining))
        finally:
            if bounded:
                with self.lock:
                    self.active_longpoll_count -= 1

'''
    s=once(s,needle,added+needle,"agent wait helper")
    before='''        if parsed.path == "/bridge/next":
            qs = parse_qs(parsed.query)
            world_id = (qs.get("world_id") or [None])[0]
            scene_id = (qs.get("scene_id") or [None])[0]
            try:
                self.store.mark_browser_poll(world_id, scene_id)
                command = self.store.claim_next(world_id, scene_id)
            except Exception as exc:
                return self._json(500, {"ok": False, "error": str(exc)})
            if command is None:
                return self._empty(204)
            return self._json(200, command)
'''
    after='''        if parsed.path == "/bridge/next":
            qs = parse_qs(parsed.query)
            world_id = (qs.get("world_id") or [None])[0]
            scene_id = (qs.get("scene_id") or [None])[0]
            try:
                # Old callers (without wait_ms) retain the same immediate API.
                # Long poll is capped so dead browser connections cannot tie up
                # this standard-library threaded HTTP agent indefinitely.
                wait_ms = max(0, min(int((qs.get("wait_ms") or ["0"])[0]), 22000))
                command = self.store.wait_next(world_id, scene_id, wait_ms / 1000.0)
            except Exception as exc:
                return self._json(500, {"ok": False, "error": str(exc)})
            if command is None:
                return self._empty(204)
            return self._json(200, command)
'''
    s=once(s,before,after,"agent HTTP handler")
    ast.parse(s)
    return s

def patch_browser(s: str) -> str:
    if sha(s) != EXPECTED_BROWSER_SHA:
        raise ValueError("STOP: installed first-party browser source SHA mismatch")
    # Leave proprietary 3D Canvas source, settings and document code untouched.
    s=once(s,
      'let pollTimer = null;\n',
      'let pollTimer = null;\nlet pollEpoch = 0;\n',
      "browser poll state")
    s=once(s,
      '  if (inFlight || !game.user?.isGM) return;\n',
      '  if (inFlight || !game.user?.isGM) return false;\n',
      "browser GM guard")
    s=once(s,
      '  if (!scene) return;\n  inFlight = true;\n',
      '  if (!scene) return false;\n  inFlight = true;\n',
      "browser scene guard")
    s=once(s,
      '    const qs = new URLSearchParams({world_id: game.world?.id ?? "", scene_id: scene.id});\n'
      '    const response = await request(`/bridge/next?${qs.toString()}`, {method: "GET", timeoutMs: 6000});\n'
      '    if (response.status === 204) return;\n',
      '    const qs = new URLSearchParams({world_id: game.world?.id ?? "", scene_id: scene.id, wait_ms: 20000});\n'
      '    const response = await request(`/bridge/next?${qs.toString()}`, {method: "GET", timeoutMs: 26000});\n'
      '    if (response.status === 204) return true;\n',
      "browser HTTP request")
    s=once(s,
      '    await postState("command-complete");\n'
      '  } catch (err) {\n'
      '    console.debug(`${MODULE_ID} poll failed`, err);\n'
      '  } finally {\n'
      '    inFlight = false;\n'
      '  }\n'
      '}\n\n'
      'function startPolling() {\n'
      '  clearInterval(pollTimer);\n'
      '  const interval = Math.max(500, Number(game.settings.get(MODULE_ID, "pollMs") || 1000));\n'
      '  pollTimer = setInterval(pollCommand, interval);\n'
      '  postState("bridge-start");\n'
      '}\n',
      '    await postState("command-complete");\n'
      '    return true;\n'
      '  } catch (err) {\n'
      '    console.debug(`${MODULE_ID} poll failed`, err);\n'
      '    return false;\n'
      '  } finally {\n'
      '    inFlight = false;\n'
      '  }\n'
      '}\n\n'
      'async function continuousBridgePoll(epoch) {\n'
      '  while (epoch === pollEpoch && game.user?.isGM && game.settings.get(MODULE_ID, "enabled")) {\n'
      '    if (!activeScene()) {\n'
      '      await new Promise(resolve => setTimeout(resolve, 1500));\n'
      '      continue;\n'
      '    }\n'
      '    // The pending HTTP request itself supplies the wait; NO browser\n'
      '    // setInterval timer is needed on the normal command delivery path.\n'
      '    const healthy = await pollCommand();\n'
      '    if (!healthy) await new Promise(resolve => setTimeout(resolve, 2000));\n'
      '  }\n'
      '}\n\n'
      'function startPolling() {\n'
      '  clearInterval(pollTimer);\n'
      '  const epoch = ++pollEpoch;\n'
      '  postState("bridge-start");\n'
      '  void continuousBridgePoll(epoch);\n'
      '}\n',
      "browser poll loop")
    if "setInterval(pollCommand" in s:
        raise AssertionError("Old throttled interval still present")
    return s
