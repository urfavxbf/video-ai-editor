#!/usr/bin/env python3
"""Read-only local environment diagnosis; makes no network calls."""
from __future__ import annotations
import os
from pathlib import Path
import platform
import shutil
import subprocess

TOOLS = {
    "terminal": ["bash", "zsh", "git", "gh", "docker", "podman", "shellcheck"],
    "software": ["python3", "node", "npm", "pnpm", "java", "gradle", "go", "rustc", "cargo"],
    "motion": ["ffmpeg", "ffprobe", "blender", "convert", "magick"],
    "data": ["sqlite3", "psql", "jq"],
}

def main() -> None:
    print("Senior multidisciplinary agent: read-only environment report")
    print("Platform:", platform.platform())
    print("Working directory:", Path.cwd())
    print("Codespaces environment:", bool(os.getenv("CODESPACES")))
    for category, programs in TOOLS.items():
        print(f"\n{category}:")
        for program in programs:
            print(f"  {program:12} {shutil.which(program) or '(not found)'}")
    if shutil.which("git"):
        result = subprocess.run(["git", "status", "--short", "--branch"],
                                capture_output=True, text=True, timeout=5, check=False)
        print("\nGit status:")
        print(result.stdout.rstrip() if result.returncode == 0 else "Not a repository or status unavailable")
    print("\nReport is informational only: it does not install tools or models.")

if __name__ == "__main__":
    main()
