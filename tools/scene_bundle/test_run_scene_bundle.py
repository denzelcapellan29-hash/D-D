"""Fresh-process and stale-report controls for the explicit Blender runner."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_scene_bundle


class RunnerControls(unittest.TestCase):
    def inputs(self, directory):
        root = Path(directory)
        blender = root / "trusted-blender.fixture"
        blender.write_bytes(b"fixture-only")
        (root / "master.blend").write_bytes(b"fixture-only")
        manifest = root / "bundle.json"
        manifest.write_text(json.dumps({"asset_root": str(root), "master": {"path": "master.blend"}}), encoding="utf-8")
        output = root / "fresh-report.json"
        argv = ["run_scene_bundle.py", "--blender", str(blender), "--manifest", str(manifest), "--output", str(output)]
        return output, argv

    def test_fresh_pass_report_cannot_override_failed_process(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            output, argv = self.inputs(directory)

            def failed_process(command, **kwargs):
                self.assertIn("--disable-autoexec", command)
                self.assertIs(kwargs["shell"], False)
                output.write_text(json.dumps({"preflight": "PASS", "release": "UNVERIFIED", "exit_code": 0}), encoding="utf-8")
                return subprocess.CompletedProcess(command, 9, stdout="interrupted", stderr="")

            with patch.object(sys, "argv", argv), patch.object(subprocess, "run", side_effect=failed_process):
                self.assertEqual(run_scene_bundle.main(), 3)

    def test_existing_report_rejected_before_launch(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            output, argv = self.inputs(directory)
            output.write_text('{"preflight":"PASS","exit_code":0}', encoding="utf-8")
            with patch.object(sys, "argv", argv), patch.object(subprocess, "run") as launch:
                with self.assertRaises(SystemExit) as raised:
                    run_scene_bundle.main()
                self.assertEqual(raised.exception.code, 2)
                launch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
