#!/usr/bin/env python3
"""Read-only, secret-free inventory of OpenMontage project checkpoint states.

Intentionally prints no checkpoint contents, text prompts, asset URLs, credentials,
or full local file paths. Nothing is uploaded or modified.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / ".runtime" / "openmontage" / "projects"
SLUG = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$")
KNOWN_STATES = frozenset({"completed", "awaiting_human", "in_progress", "failed", "cancelled", "pending"})
MAX_CHECKPOINT_BYTES = 1024 * 1024
MAX_PROJECTS = 100
MAX_CHECKPOINTS = 50


def read_status(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        return "unreadable"
    try:
        if path.stat().st_size > MAX_CHECKPOINT_BYTES:
            return "oversize"
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return "invalid"
        status = data.get("status")
        return status if status in KNOWN_STATES else "unknown"
    except (OSError, ValueError, UnicodeError, TypeError):
        return "invalid"


def inspect_render(project: Path) -> dict:
    output = project / "renders" / "final.mp4"
    if output.is_symlink() or not output.is_file():
        return {"present": False}
    result = {"present": True, "bytes": output.stat().st_size, "probe": "unavailable"}
    if not shutil.which("ffprobe"):
        return result
    try:
        completed = subprocess.run(
            [
                "ffprobe", "-v", "error", "-show_entries",
                "format=duration", "-of", "json", str(output),
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=12,
        )
        metadata = json.loads(completed.stdout)
        duration = float(metadata["format"]["duration"])
        if 0 < duration < 86400:
            result.update({"probe": "ok", "duration_seconds": round(duration, 2)})
        else:
            result["probe"] = "invalid"
    except (OSError, ValueError, KeyError, subprocess.SubprocessError):
        result["probe"] = "invalid"
    return result


def inspect_project(project: Path) -> dict:
    stages: dict[str, str] = {}
    checkpoints = sorted(project.glob("checkpoint_*.json"))[:MAX_CHECKPOINTS]
    for checkpoint in checkpoints:
        if checkpoint.is_symlink() or not checkpoint.is_file():
            continue
        stage = checkpoint.name[len("checkpoint_"):-len(".json")]
        if SLUG.fullmatch(stage):
            stages[stage] = read_status(checkpoint)
    assets = project / "assets"
    has_assets = assets.is_dir() and not assets.is_symlink()
    return {
        "project_id": project.name,
        "has_project_manifest": (project / "project.json").is_file()
        and not (project / "project.json").is_symlink(),
        "checkpoints": stages,
        "has_assets_directory": has_assets,
        "final_render": inspect_render(project),
    }


def report(root: Path, name: str | None = None) -> dict:
    """Return only metadata, not private scripts, provenance, credentials or content."""
    result = {"format_version": 1, "projects": [], "not_found": False}
    if not root.is_dir():
        result["not_found"] = True
        return result
    if name:
        if not SLUG.fullmatch(name):
            raise ValueError("Invalid project ID: expected a simple slug")
        candidate = root / name
        candidates = [candidate] if candidate.is_dir() and not candidate.is_symlink() else []
    else:
        candidates = sorted(
            (p for p in root.iterdir()
             if p.is_dir() and not p.is_symlink() and SLUG.fullmatch(p.name)),
            key=lambda p: p.name
        )[:MAX_PROJECTS]
    result["projects"] = [inspect_project(project) for project in candidates]
    result["not_found"] = len(candidates) == 0
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Project directory (for tests)")
    parser.add_argument("--project", default=None, help="Optional project ID to inspect")
    args = parser.parse_args()
    try:
        print(json.dumps(report(args.root, args.project), indent=2, sort_keys=True))
    except (ValueError, OSError) as exc:
        print(f"Progress report failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
