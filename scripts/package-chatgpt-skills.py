#!/usr/bin/env python3
"""Prepare a portable skills-only Plugin plus 13 single-skill upload archives.
Never publishes, connects or installs the package in a ChatGPT account.
"""
from __future__ import annotations
from pathlib import Path
import json
import re
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".claude" / "skills"
OUT = ROOT / "out" / "chatgpt-skills"
PLUGIN = OUT / "video-ai-editor-skills"
SKILLS = (
    "ai-video-editor",
    "remotion-best-practices",
    "remotion-captions",
    "remotion-create",
    "remotion-docs",
    "remotion-interactivity",
    "remotion-maps",
    "remotion-markup",
    "remotion-multimedia",
    "remotion-render",
    "remotion-saas",
    "remotion-studio",
    "remotion-upgrade",
)
OFFICIAL_COMMIT = "30d4553ecd46fbc5212fd0ff006ae43af522158b"


def create_zip(base: Path, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", ZIP_DEFLATED, compresslevel=9) as z:
        for file in sorted(base.rglob("*")):
            if not file.is_file():
                continue
            # Avoid treating untrusted repository symlinks as file content.
            if file.is_symlink():
                raise RuntimeError("Refusing symlink in packaged skill: " + str(file))
            arcname = file.relative_to(base).as_posix()
            z.write(file, arcname)
    with ZipFile(target) as z:
        invalid = z.testzip()
        if invalid:
            raise RuntimeError("Corrupted skill ZIP: " + invalid)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for name in SKILLS:
        folder = SOURCE / name
        meta = folder / "SKILL.md"
        if not meta.is_file():
            raise RuntimeError(f"Missing required skill: {name}")
        header = meta.read_text(encoding="utf-8")
        if not header.startswith("---\n") or not re.search(r"(?m)^name:\s*",header):
            raise RuntimeError(f"Skill manifest invalid: {name}")
        shutil.copytree(folder, PLUGIN / "skills" / name)
        print("Packaged skill:", name)

    actual = {f.name for f in (PLUGIN / "skills").iterdir() if f.is_dir()}
    if actual != set(SKILLS):
        raise RuntimeError("Skill count mismatch")
    (PLUGIN / ".codex-plugin").mkdir(parents=True)
    portable = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": "video-ai-editor-skills",
        "version": "0.1.0",
        "description": "Thirteen AI editing skills: twelve official Remotion skills plus the Video AI Editor podcast and Tagalog Shorts workflow.",
        "repository": "https://github.com/urfavxbf/video-ai-editor",
    }
    compat = {
        "name": portable["name"], "version": portable["version"],
        "description": portable["description"], "skills": "./skills/"
    }
    (PLUGIN / "plugin.json").write_text(json.dumps(portable,indent=2)+"\n",encoding="utf-8")
    (PLUGIN / ".codex-plugin" / "plugin.json").write_text(json.dumps(compat,indent=2)+"\n",encoding="utf-8")

    lic = ROOT / "THIRD_PARTY_NOTICES.md"
    if lic.exists():
        shutil.copy2(lic,PLUGIN / "THIRD_PARTY_NOTICES.md")
    notice = ROOT / "licenses/video-effects-skill-MIT.txt"
    if notice.exists():
        target = PLUGIN / "licenses" / notice.name
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(notice,target)
    (PLUGIN / "README.md").write_text(
        "# Video AI Editor Skills\n\n"
        "This is a **skills-only** bundle; it does not install video runtime packages, connect services or grant terminal access.\n\n"
        "Included: 12 official Remotion Agent Skills at source commit "+OFFICIAL_COMMIT+
        ", plus the custom ai-video-editor skill from urfavxbf/video-ai-editor.\n\n"
        "Source: https://github.com/remotion-dev/skills\n"
        "Project: https://github.com/urfavxbf/video-ai-editor\n\n"
        "To use it, install the plugin in a supporting ChatGPT/Codex host or upload the individual skills from the separate ZIP bundle. "
        "A user must approve installation in their own account; upload support is subject to account/workspace eligibility.\n",
        encoding="utf-8"
    )
    combined = OUT / "Video-AI-Editor-13-Skills-Plugin.zip"
    create_zip(PLUGIN,combined)
    upload = OUT / "individual-skill-uploads"
    upload.mkdir(parents=True)
    for name in SKILLS:
        create_zip(PLUGIN / "skills" / name,upload / f"{name}.zip")
    with ZipFile(OUT / "Video-AI-Editor-13-Individual-Skills.zip","w",ZIP_DEFLATED,compresslevel=9) as z:
        for file in sorted(upload.iterdir()):
            z.write(file,file.name)
    assert len(list(upload.glob("*.zip"))) == 13
    with ZipFile(combined) as z:
        nested = [name for name in z.namelist() if re.match(r"skills/[^/]+/SKILL[.]md$",name)]
        assert len(nested)==13,nested
    print("Ready:",combined)
    print("Ready: 13 individual skills upload bundle")
    print("INSTALL STATUS: not installed in ChatGPT; user approval/account setup required")


if __name__ == "__main__":
    main()
