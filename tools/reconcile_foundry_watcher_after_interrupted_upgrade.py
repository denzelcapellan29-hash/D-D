#!/usr/bin/env python3
"""Read-only Windows reconcile after an interrupted Acq guarded-watcher upgrade.

Never starts/stops a process, executes an updater, writes a file, queues a job,
or reads unrelated user data. Does not prove that GM browser polling works.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

PINNED = {
    "v0.3": {
        "acq_bridge_deployer.py": "25065507f4ec54669ace7e232b8febb7bc9ae0b7ff5728265bec98d0f141181c",
        "acq_deploy_watcher.py": "ccb845a4f43d08153b33d5242017d47451168bde8b022e29333a8fcc49e69b93",
    },
    "v0.4": {
        "acq_bridge_deployer.py": "cf46e478460ec99983a33b59c65cc8e323b3e35d7d448cdc7ea30b5f6d406ed6",
        "acq_deploy_watcher.py": "3f46f033076a08d8b504b84d8324c5c7585af1665ca60fae9b41a1ee5958baea",
    },
}
FILES = tuple(PINNED["v0.3"])


def version_from_hashes(hashes: dict) -> str:
    if all(hashes.get(n) == PINN[v][n] for n in FILES for v in ["v0.3"]):
        return "v0.3"
    if all(hashes.get(n) == PINN[v][n] for n in FILES for v in ["v0.4"]):
        return "v0.4"
    return "UNRECOGNIZED_OR_MIXED"


def classify(hashes: dict, procs: list[dict]) -> tuple[str, list[str]]:
    version = version_from_hashes(hashes)
    issues = []
    if version == "UNRECOGNIZED_OR_MIXED":
        issues.append("Installed watcher files do not match one pinned full version.")
    if len(procs) != 1:
        issues.append(f"Expected exactly one live watcher process; observed {len(procs)}.")
    for proc in procs:
        if not proc.get("allow_deploy", False):
            issues.append("Live watcher lacks explicit --allow-deploy approval flag.")
        if not proc.get("path_matches", False):
            issues.append("Live watcher command does not point to expected installed script.")
        if not proc.get("all_required_args", False):
            issues.append("Live watcher has an incomplete pinned argument set.")
        if not proc.get("started_after_install", False):
            issues.append("Cannot prove process started after installed watcher script was last modified.")
    if issues:
        return "STOP_UNVERIFIED", issues
    return version + "_INSTALLED_AND_PROCESS_PROVEN", issues


def _watcher_processes(expected_script: Path, script_mtime: float):
    # CIM is read only. The result includes only derived flags/PID/times,
    # never a full command line, passwords or tokens.
    ps = r"""
$matches = @(Get-CimInstance Win32_Process | Where-Object {
    $_.Name -in @('python.exe','pythonw.exe') -and
    $_.CommandLine -match 'acq_deploy_watcher[.]py'
} | ForEach-Object {
    [pscustomobject]@{
        pid = [int]$_.ProcessId
        command = [string]$_.CommandLine
        createdUtc = $_.CreationDate.ToUniversalTime().ToString('o')
    }
})
ConvertTo-Json -InputObject $matches -Depth 4 -Compress
"""
    try:
        res = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps],
            capture_output=True, text=True, timeout=15, check=True,
        )
        arr = json.loads(res.stdout) if res.stdout.strip() else []
        if isinstance(arr, dict):
            arr = [arr]
        out = []
        args = ["--repo", "--foundry-user-data", "--mcp-path", "--backup-root"]
        for item in arr:
            command = item.get("command", "")
            started = datetime.fromisoformat(item["createdUtc"].replace("Z", "+00:00")).timestamp()
            # Allow harmless filesystem timestamp granularity of three seconds.
            out.append({
                "pid": item.get("pid"),
                "started_utc": item["createdUtc"],
                "allow_deploy": "--allow-deploy" in command.split(),
                "path_matches": str(expected_script).casefold() in command.casefold(),
                "all_required_args": all(arg in command.split() for arg in args),
                "started_after_install": started + 3 >= script_mtime,
            })
        return out, None
    except (OSError, subprocess.SubprocessError, ValueError, KeyError) as e:
        return [], type(e).__name__ + ": " + str(e)[:180]


def inspect(root: Path) -> dict:
    installed = root / "app"
    hashes = {}
    metadata = {}
    for name in FILES:
        path = installed / name
        if path.is_file():
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
            metadata[name] = {"size": path.stat().st_size, "modified_utc":
                              datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()}
        else:
            hashes[name] = None
            metadata[name] = {"missing": True}
    watcher = installed / "acq_deploy_watcher.py"
    processes, process_error = _watcher_processes(watcher, watcher.stat().st_mtime if watcher.exists() else float("inf"))
    status, issues = classify(hashes, processes)
    if process_error:
        status = "STOP_UNVERIFIED"
        issues.append("Windows process inspection unavailable: " + process_error)
    backups = root.glob("app-backup-before-v04-*")
    backup_names = sorted(p.name for p in backups if p.is_dir())[-6:]
    logs = sorted((root / "logs").glob("watcher-v04-*.log")) if (root / "logs").is_dir() else []
    return {
        "audit_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "read_only_no_changes",
        "status": status,
        "issues": issues,
        "installed_version_by_hash": version_from_hashes(hashes),
        "installed_files_sha256": hashes,
        "installed_metadata": metadata,
        "watcher_processes": processes,
        "backup_directories": backup_names,
        "v04_log_files": [{"name": p.name, "size": p.stat().st_size} for p in logs[-8:]],
        "source_area8_scene": "NOT_QUERIED",
        "bridge_heartbeat": "NOT_QUERIED",
    }


def selftest():
    old, new = PINN["v0.3"], PINN["v0.4"]
    good = [{"allow_deploy": True, "path_matches": True,
             "all_required_args": True, "started_after_install": True}]
    assert version_from_hashes(old) == "v0.3"
    assert version_from_hashes(new) == "v0.4"
    assert version_from_hashes({**old, "acq_deploy_watcher.py": new["acq_deploy_watcher.py"]}) == "UNRECOGNIZED_OR_MIXED"
    assert classify(new, good)[0] == "v0.4_INSTALLED_AND_PROCESS_PROVEN"
    assert classify(old, good)[0] == "v0.3_INSTALLED_AND_PROCESS_PROVEN"
    assert classify(new, [])[0] == "STOP_UNVERIFIED"
    assert classify(new, [dict(good[0], allow_deploy=False)])[0] == "STOP_UNVERIFIED"
    assert classify(new, [dict(good[0], started_after_install=False)])[0] == "STOP_UNVERIFIED"
    assert classify(new, good + good)[0] == "STOP_UNVERIFIED"
    print(json.dumps({"selftest": "PASS", "cases": 9}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path.home() / "Acq3DDeployAgent")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    else:
        value = inspect(args.root)
        print(json.dumps(value, indent=2))
        sys.exit(0 if value["status"] == "v0.4_INSTALLED_AND_PROCESS_PROVEN" else 2)
