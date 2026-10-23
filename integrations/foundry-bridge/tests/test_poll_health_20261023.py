"""Regression: first-party bridge poll telemetry is observable without executing GM commands."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "agent" / "acq_bridge_agent.py"
spec = importlib.util.spec_from_file_location("acq_bridge_agent_poll_test", SOURCE)
agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent)


class BrowserPollingHealthTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.TemporaryDirectory(prefix="acq_poll_health_test_")
        self.addCleanup(self.root.cleanup)
        self.store = agent.BridgeStore(Path(self.root.name))

    def test_no_poll_not_mistaken_for_online(self):
        status = self.store.queue_status()
        self.assertEqual(status["browser_poll"]["total_polls"], 0)
        self.assertFalse(status["browser_poll"]["recent_within_10s"])
        self.assertIsNone(status["browser_poll"]["age_seconds"])

    def test_observed_poll_records_scene_without_command(self):
        self.store.mark_browser_poll("world-fixture", "scene-fixture")
        status = self.store.queue_status()
        self.assertTrue(status["browser_poll"]["recent_within_10s"])
        self.assertEqual(status["browser_poll"]["scene_id"], "scene-fixture")
        self.assertEqual(status["browser_poll"]["world_id"], "world-fixture")
        self.assertEqual(status["browser_poll"]["total_polls"], 1)
        self.assertEqual(status["queued"], [])
        self.assertEqual(status["rpc_queued"], [])
        self.assertEqual(status["inflight"], [])

    def test_result_telemetry_distinct_from_poll(self):
        self.store.mark_browser_poll("world-fixture", "scene-fixture")
        self.assertEqual(self.store.queue_status()["browser_result"]["total_results"], 0)
        self.store.write_result({"command_id": "fixture-result", "ok": True})
        status = self.store.queue_status()
        self.assertEqual(status["browser_poll"]["total_polls"], 1)
        self.assertEqual(status["browser_result"]["total_results"], 1)
        self.assertTrue((Path(self.root.name) / "results" / "fixture-result_result.json").is_file())


if __name__ == "__main__":
    unittest.main()
