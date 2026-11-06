"""Least-privilege operations backed by existing Video AI Editor scripts.

The bridge is plain Python and does not import the MCP SDK; core regression
tests therefore run in the default repository environment without extra deps.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
MAX_OUTPUT = 4096
MAX_MEDIA_SIZE = 1024 * 1024 * 1024
SAFE_ROOTS = frozenset(("input", "out", "public"))
MEDIA_EXTENSIONS = frozenset((
    ".mp4", ".mov", ".m4v", ".mkv", ".webm", ".mp3", ".m4a",
    ".wav", ".flac", ".aac",
))
PROBE_FORMATS = "mov,mp4,m4a,3gp,3g2,mj2,matroska,webm,mp3,wav,flac,aac"
CATALOG = ".claude/skills/video-ai-orchestrator/references/skill-catalog.md"


class BridgeError(ValueError):
    """A sanitized, actionable error suitable for returning to an MCP host."""


def _environment() -> dict[str, str]:
    """Keep subprocesses from inheriting repository/provider API credentials."""
    names = ("PATH", "HOME", "TMPDIR", "LANG", "LC_ALL", "XDG_CACHE_HOME")
    return {name: os.environ[name] for name in names if name in os.environ}


def _run(command: list[str], *, label: str, timeout: int) -> str:
    """No shell, no remote command expansion, bounded runtime and response."""
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=_environment(),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise BridgeError(f"{label}: required local executable is not installed") from exc
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(f"{label}: exceeded the execution deadline") from exc
    if result.returncode != 0:
        raise BridgeError(
            f"{label}: local check failed (exit {result.returncode}); "
            "inspect the project checkout and prerequisites"
        )
    return result.stdout[:MAX_OUTPUT]


def project_status() -> dict:
    """Get current, machine-readable production defaults without stale demos."""
    try:
        registry = json.loads((ROOT / "characters/registry.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "characters/pixel-default-manifest.json").read_text(encoding="utf-8"))
        defaults = registry["default_video"]
        voices = {
            name: entry["english_voice"]["identifier"]
            for name, entry in registry["characters"].items()
        }
        count = sum(len(entry["poses"]) for entry in manifest["characters"].values())
        return {
            "project": registry["project"],
            "language": registry["production_language"],
            "width": defaults["width"],
            "height": defaults["height"],
            "fps": defaults["fps"],
            "composition": defaults["default_character_composition"],
            "voices": voices,
            "approved_pose_count": count,
            "source_of_truth": ["AGENTS.md", "docs/PRODUCTION_POLICY.md",
                                "characters/registry.json", "characters/pixel-default-manifest.json"],
            "note": "Metadata only: no media was rendered or validated.",
        }
    except (OSError, KeyError, ValueError, TypeError) as exc:
        raise BridgeError("Project registry or asset manifest is missing or invalid") from exc


def list_skills() -> dict:
    """Return central-router and existing reusable specialist skills."""
    try:
        text = (ROOT / CATALOG).read_text(encoding="utf-8")
        matches = re.findall(
            r"^\|[^\n]*?\| " + chr(96) + r"([a-z0-9-]+)" + chr(96) +
            r" \| " + chr(96) + r"([^" + chr(96) + r"]*SKILL\.md)" + chr(96) + r" \|$",
            text, flags=re.MULTILINE,
        )
        skills = [{"name": "video-ai-orchestrator",
                   "path": ".claude/skills/video-ai-orchestrator/SKILL.md"}]
        seen = {"video-ai-orchestrator"}
        for name, path in matches:
            if name in seen or not (ROOT / path).is_file():
                raise BridgeError("Skill catalog has duplicate or missing source paths")
            skills.append({"name": name, "path": path})
            seen.add(name)
        if len(skills) != 21:
            raise BridgeError("Skill catalog inventory differs from expected 21 modules")
        return {"count": len(skills), "skills": skills}
    except OSError as exc:
        raise BridgeError("Skill catalog is unavailable") from exc


def verify_character_assets() -> dict:
    """Hash and decode all 13 approved character assets via existing checker."""
    output = _run(
        [sys.executable, str(ROOT / "scripts/stage_pixel_default_pack.py"),
         "--verify-workspace"],
        label="approved character asset verification", timeout=90,
    )
    return {"ok": True, "verification": "approved PNG/hash checker ran",
            "output": output.strip(), "note": "Not an episode, render, or lip-sync proof."}


def validate_edit(media: bool = True) -> dict:
    """Run the existing ExampleEdit contract and optional local media preflight."""
    command = ["node", str(ROOT / "scripts/validate-edit.cjs"),
               "src/edit/edit.json"]
    if media:
        command.append("--media")
    output = _run(command, label="ExampleEdit validation", timeout=150)
    return {"ok": True, "media_checked": media, "output": output.strip(),
            "note": "Edit validation does not render or publish a video."}


def local_media_path(relative_path: str) -> Path:
    """Only local file types under input/, out/ or public/; no traversal."""
    if (not isinstance(relative_path, str) or
            not 1 <= len(relative_path) <= 240 or
            "\x00" in relative_path or "\\" in relative_path):
        raise BridgeError("Invalid local relative media path")
    path = Path(relative_path)
    parts = path.parts
    if (path.is_absolute() or not parts or parts[0] not in SAFE_ROOTS or
            any(part in ("..", ".") for part in parts) or len(parts) < 2):
        raise BridgeError("Only local paths under input/, out/ or public/ are accepted")
    try:
        resolved = (ROOT / path).resolve(strict=True)
        resolved.relative_to(ROOT.resolve())
        if not resolved.is_file() or (ROOT / path).is_symlink():
            raise BridgeError("Media must be a real, regular local file")
        if resolved.suffix.lower() not in MEDIA_EXTENSIONS:
            raise BridgeError("Unsupported local media file extension")
        if not 0 < resolved.stat().st_size <= MAX_MEDIA_SIZE:
            raise BridgeError("Media is empty or exceeds the 1 GiB inspection limit")
        return resolved
    except (OSError, ValueError) as exc:
        if isinstance(exc, BridgeError):
            raise
        raise BridgeError("Media file is missing or outside allowed local folders") from exc


def inspect_media(relative_path: str) -> dict:
    """Probe actual streams without allowing network protocols or URL schemes."""
    media = local_media_path(relative_path)
    raw = _run(
        ["ffprobe", "-v", "error", "-protocol_whitelist", "file",
         "-format_whitelist", PROBE_FORMATS,
         "-show_entries",
         "format=duration,size,format_name:"
         "stream=codec_type,codec_name,width,height,r_frame_rate,channels,sample_rate",
         "-of", "json", str(media)],
        label="FFprobe media inspection", timeout=30,
    )
    try:
        result = json.loads(raw)
        if not isinstance(result.get("streams"), list):
            raise ValueError("No stream information")
        return {
            "ok": True,
            "path": relative_path,
            "format": result.get("format", {}),
            "streams": result["streams"][:8],
            "note": "Metadata only. Check copyright, actual playback and audio before use.",
        }
    except (ValueError, TypeError) as exc:
        raise BridgeError("FFprobe returned invalid or incomplete media information") from exc


def preview_render(confirmed: bool = False) -> dict:
    """Bounded, local 30-frame pixel-art proof, never a full episode."""
    if not confirmed:
        return {"ok": False, "approval_required": True,
                "message": "Explicitly approve local CPU/disk use for the 30-frame Remotion proof render."}
    binary = ROOT / "node_modules/.bin/remotion"
    if not binary.exists():
        raise BridgeError("Remotion CLI missing: run npm ci in the repository first")
    directory = ROOT / "out/mcp"
    if directory.is_symlink():
        raise BridgeError("Refusing a symlinked render output directory")
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / ("pixel-production-proof-" + uuid.uuid4().hex[:12] + ".mp4")
    _run(
        [str(binary), "render", "PixelProductionProof",
         str(target), "--frames=165-194", "--scale=0.25",
         "--concurrency=2", "--codec=h264", "--pixel-format=yuv420p"],
        label="30-frame local proof render", timeout=240,
    )
    if not target.is_file() or target.stat().st_size < 1024:
        raise BridgeError("Remotion reported success but no usable proof file exists")
    return {"ok": True, "path": target.relative_to(ROOT).as_posix(),
            "frames": 30, "frame_size": "480x270", "fps": 30,
            "note": "PixelProductionProof is an artwork fixture, not a voiced episode."}


def inspect_online_source(url: str, approved_network: bool = False) -> dict:
    """Explicit opt-in metadata inspection; never downloads source footage."""
    if not approved_network:
        return {"ok": False, "approval_required": True,
                "message": "Confirm a network metadata request to this specific video URL first."}
    result = _run(
        [sys.executable, str(ROOT / "scripts/media_ingest.py"), "inspect", url],
        label="approved yt-dlp metadata inspection", timeout=110,
    )
    try:
        data = json.loads(result)
        if not isinstance(data, dict):
            raise ValueError("Not a single video metadata object")
        return {"ok": True, "metadata": data,
                "note": "No video was downloaded; source rights still require verification."}
    except (ValueError, TypeError) as exc:
        raise BridgeError("Media-source metadata was incomplete or invalid") from exc
