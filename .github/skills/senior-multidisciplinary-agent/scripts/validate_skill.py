#!/usr/bin/env python3
"""Offline skill integrity check; standard library only."""
from __future__ import annotations
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "references/terminal-and-devops.md",
    "references/ai-engineering.md",
    "references/motion-graphics.md",
    "references/information-and-research.md",
    "references/software-engineering.md",
    "references/safety-and-quality.md",
    "assets/acceptance-report.md",
    "assets/AGENTS-template.md",
    "scripts/doctor.py",
]
def check() -> int:
    issues = []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            issues.append(f"Missing: {name}")
    manifest = ROOT / "SKILL.md"
    if manifest.is_file():
        body = manifest.read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---\n", body, re.S)
        if not front:
            issues.append("Missing YAML frontmatter")
        else:
            if not re.search(r"^name: senior-multidisciplinary-agent$", front.group(1), re.M):
                issues.append("Wrong skill name")
            if not re.search(r"^description: \S+", front.group(1), re.M):
                issues.append("Missing description")
        for path in set(re.findall(r"`((?:references|assets|scripts)/[^`\n]+)`", body)):
            if not (ROOT / path).is_file():
                issues.append(f"Broken reference: {path}")
    other = [str(p) for p in ROOT.rglob("*") if p.is_file() and p.name == "SKILL.md" and p != manifest]
    if other:
        issues.append("Nested SKILL.md not allowed: " + ", ".join(other))
    if issues:
        for issue in issues:
            print("FAIL:", issue)
        return 1
    print("PASS: senior-multidisciplinary-agent structure and references")
    return 0
if __name__ == "__main__":
    sys.exit(check())
