"""Run the read-only validator in an explicitly selected background Blender."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blender", required=True, help="Absolute path of an existing trusted Blender executable.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--asset-root", help="Explicit relocated bundle root.")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    if not Path(args.blender).is_absolute():
        parser.error("--blender must be an absolute executable path.")
    executable = Path(args.blender).resolve()
    manifest_path = Path(args.manifest).resolve()
    output_path = Path(args.output).resolve()
    if output_path.exists():
        parser.error("Choose a new output report filename for each run; an existing report cannot prove a fresh result.")
    if not executable.is_file() or not executable.is_absolute():
        parser.error("--blender must identify an existing executable.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    root = Path(args.asset_root or manifest["asset_root"])
    master = root / manifest["master"]["path"]
    if not master.is_file():
        parser.error("The selected master does not exist at the explicit asset root.")
    script = Path(__file__).with_name("validate_scene_bundle.py").resolve()
    command = [str(executable), "--background", "--disable-autoexec", str(master), "--python-exit-code", "3", "--python", str(script),
               "--", "--manifest", str(manifest_path), "--output", str(output_path)]
    if args.asset_root:
        command.extend(["--asset-root", str(root)])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    try:
        completed = subprocess.run(command, shell=False, capture_output=True, text=True,
                                   timeout=args.timeout, creationflags=flags)
    except subprocess.TimeoutExpired:
        print(json.dumps({"preflight": "FAIL", "error": "Background Blender timed out; no scene save was requested."}))
        return 3
    # A unique output filename per run prevents an old report from masquerading as a new result.
    if not output_path.is_file():
        print(json.dumps({"preflight": "FAIL", "process_exit": completed.returncode,
                          "error": completed.stderr[-2000:] or completed.stdout[-2000:]}))
        return 3
    report = json.loads(output_path.read_text(encoding="utf-8"))
    if report.get("preflight") == "PASS" and (report.get("exit_code") != 0 or completed.returncode != 0):
        print(json.dumps({"report": str(output_path), "preflight": "FAIL", "process_exit": completed.returncode,
                          "error": "A PASS report cannot override a failed or incomplete Blender process.", "exit_code": 3}))
        return 3
    print(json.dumps({"report": str(output_path), "preflight": report.get("preflight"),
                      "release": report.get("release"), "process_exit": completed.returncode,
                      "failed_checks": [item["id"] for item in report.get("checks", []) if item["status"] == "FAIL"]}))
    return int(report.get("exit_code", 3))


if __name__ == "__main__":
    raise SystemExit(main())
