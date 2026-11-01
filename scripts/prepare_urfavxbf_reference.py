#!/usr/bin/env python3
"""Prepare a speaker-authorized, gitignored UrFavXBF reference without GPU/cloud."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from voxcpm_voiceover import validate_reference

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DEST = ROOT / "input" / "urfavxbf-reference.wav"


def prepare(source: Path, output: Path, start_seconds: float, duration_seconds: float, overwrite: bool) -> Path:
    if not source.is_file():
        raise ValueError(f"Source MP3/audio not found: {source}")
    if source.resolve() == output.resolve():
        raise ValueError("Refusing to overwrite source recording")
    if not 0 <= start_seconds <= 3600 or not 5 <= duration_seconds <= 30:
        raise ValueError("Reference selection requires start >= 0 and 5–30 seconds")
    executable = shutil.which("ffmpeg")
    if not executable:
        raise RuntimeError("FFmpeg is required to prepare a private reference")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not overwrite:
        raise ValueError("Output exists (pass --overwrite to replace)")
    with tempfile.NamedTemporaryFile(prefix=".urfavxbf-", suffix=".wav", dir=output.parent, delete=False) as file:
        staged = Path(file.name)
    try:
        subprocess.run([
            executable, "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", str(start_seconds), "-t", str(duration_seconds),
            "-i", str(source), "-vn", "-ac", "1", "-ar", "16000",
            "-c:a", "pcm_s16le", str(staged)
        ], capture_output=True, text=True, check=True)
        validate_reference(staged)
        staged.replace(output)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("Failed to convert voice reference; verify source format and selection") from exc
    finally:
        staged.unlink(missing_ok=True)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage local UrFavXBF Tagalog voice reference, no cloud/GPU.")
    parser.add_argument("--source-audio", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=PRIVATE_DEST)
    parser.add_argument("--start-seconds", type=float, default=29.4)
    parser.add_argument("--duration-seconds", type=float, default=12.2)
    parser.add_argument("--confirm-voice-rights", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    if not args.confirm_voice_rights:
        parser.error("Speaker authorization required: --confirm-voice-rights")
    try:
        out = prepare(args.source_audio, args.output, args.start_seconds, args.duration_seconds, args.overwrite)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Reference preparation error: {exc}", file=sys.stderr)
        return 2
    print(f"Private voice reference prepared: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
