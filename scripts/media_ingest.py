#!/usr/bin/env python3
"""Rights-gated, single-video yt-dlp source ingestion.

No third-party site is contacted until an explicit inspect/download command.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "input" / "ingested"
MAX_METADATA_BYTES = 2 * 1024 * 1024
MAX_VIDEO_BYTES = 500 * 1024 * 1024
ALLOWED_HOSTS = frozenset({
    "youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com",
    "youtu.be", "www.youtu.be", "vimeo.com", "www.vimeo.com",
    "archive.org", "www.archive.org", "commons.wikimedia.org",
})
MP4_FORMAT = "bv*[ext=mp4][height<=1080]+ba[ext=m4a]/b[ext=mp4][height<=1080]"


def validate_url(url: str) -> str:
    """Disallow local/network-control targets, URL credentials and non-HTTPS hosts."""
    if not isinstance(url, str) or not 1 <= len(url) <= 2048:
        raise ValueError("Expected one supported HTTPS video URL")
    if any(ord(ch) <= 32 or ord(ch) == 127 for ch in url):
        raise ValueError("URL contains whitespace or a control character")
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Invalid video URL") from exc
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Unsupported video host or URL scheme")
    if parsed.username is not None or parsed.password is not None or port not in (None, 443):
        raise ValueError("URL credentials and nonstandard ports are forbidden")
    if parsed.fragment:
        raise ValueError("URL fragments are not accepted")
    return url


def command_for(action: str, url: str, output_dir: Path, subtitles: bool = False) -> list[str]:
    """Use constant yt-dlp arguments, not shell concatenation or arbitrary flags."""
    validate_url(url)
    base = [sys.executable, "-m", "yt_dlp", "--ignore-config", "--no-playlist",
            "--max-downloads", "1", "--no-progress", "--socket-timeout", "20",
            "--retries", "2", "--fragment-retries", "2"]
    if action == "inspect":
        return [*base, "--dump-single-json", "--simulate", url]
    if action != "download":
        raise ValueError("Unknown ingestion action")
    options = ["--no-simulate", "--max-filesize", "500M", "--no-overwrites",
               "--restrict-filenames", "--trim-filenames", "80",
               "--format", MP4_FORMAT, "--merge-output-format", "mp4",
               "--paths", f"home:{output_dir.resolve()}",
               "--output", "%(extractor_key)s_%(id)s.%(ext)s",
               "--print", "after_move:filepath"]
    if subtitles:
        options += ["--write-subs", "--sub-langs", "en.*,tl.*",
                    "--sub-format", "vtt/srt/best"]
    return [*base, *options, url]


def safe_metadata(raw: str) -> dict:
    """Never print yt-dlp's raw stream URLs, cookies or provider metadata."""
    if len(raw.encode("utf-8")) > MAX_METADATA_BYTES:
        raise ValueError("Metadata exceeds the configured limit")
    data = json.loads(raw)
    if not isinstance(data, dict) or data.get("_type") in ("playlist", "multi_video"):
        raise ValueError("Expected a single video, not a playlist")
    return {
        "id": data.get("id"),
        "title": data.get("title"),
        "extractor": data.get("extractor_key"),
        "duration_seconds": data.get("duration"),
        "uploader": data.get("uploader"),
        "license_claim": data.get("license"),
        "note": "Source metadata does not establish downloading or reuse rights.",
    }


def verified_download(stdout: str, output_dir: Path) -> Path:
    """Accept exactly one completed regular video inside ignored local storage."""
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise ValueError("Expected one completed video path")
    target = Path(lines[0])
    if not target.is_absolute():
        target = ROOT / target
    try:
        actual = target.resolve(strict=True)
        actual.relative_to(output_dir.resolve())
    except (OSError, ValueError) as exc:
        raise ValueError("Video path must remain under input/ingested") from exc
    if target.is_symlink() or not target.is_file():
        raise ValueError("Video is not a regular local file")
    if actual.suffix.lower() not in {".mp4", ".webm", ".mkv"}:
        raise ValueError("Unsupported downloaded video container")
    if not 0 < actual.stat().st_size <= MAX_VIDEO_BYTES:
        raise ValueError("Video is empty or exceeds 500 MiB")
    return actual


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect or download one rights-cleared source.")
    actions = parser.add_subparsers(dest="action", required=True)
    inspect = actions.add_parser("inspect", help="Metadata-only network request")
    inspect.add_argument("url")
    download = actions.add_parser("download", help="Authorized media download")
    download.add_argument("url")
    download.add_argument("--confirm-rights", action="store_true",
                          help="Confirm source rights, permission and site terms")
    download.add_argument("--subtitles", action="store_true",
                          help="Request available English/Tagalog subtitles")
    args = parser.parse_args(argv)
    try:
        validate_url(args.url)
        if args.action == "download" and not args.confirm_rights:
            raise ValueError("Downloads require --confirm-rights")
        if args.action == "download":
            if OUTPUT_DIR.is_symlink():
                raise ValueError("Refusing a symlinked output directory")
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cmd = command_for(args.action, args.url, OUTPUT_DIR,
                          subtitles=getattr(args, "subtitles", False))
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True,
            timeout=90 if args.action == "inspect" else 900,
        )
        if args.action == "inspect":
            print(json.dumps(safe_metadata(result.stdout), indent=2, ensure_ascii=False))
        else:
            path = verified_download(result.stdout, OUTPUT_DIR)
            print(f"Verified local source: {path}")
            print("Validate streams with ffprobe and reuse rights before editing.")
        return 0
    except (ValueError, OSError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        # Subprocess stderr can include private URL parameters; do not expose it.
        print(f"Media ingestion failed ({type(exc).__name__}). "
              "Check source authorization, URL, dependency and format.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
