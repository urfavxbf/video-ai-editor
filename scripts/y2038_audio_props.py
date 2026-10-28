#!/usr/bin/env python3
"""Convert REAL VoxCPM2 WAV durations into synchronized Remotion render props.

Audio files must already be synthesized. This tool never fabricates dialogue.
Clip-level timing is based on measured audio duration, not estimates; word-level
subtitle alignment is a separate QA gate.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
sys.path.insert(0, str(ROOT / "scripts"))
from extract_voice_envelope import voice_event_from_wav


def wav_frames(path: Path, fps: int = 30) -> int:
    with wave.open(str(path), "rb") as source:
        if source.getcomptype() != "NONE" or source.getsampwidth() != 2:
            raise ValueError(f"Expected PCM16 WAV: {path}")
        if source.getframerate() < 16000:
            raise ValueError(f"Invalid sample rate in {path}")
        if source.getnframes() < source.getframerate() // 5:
            raise ValueError(f"Audio too short in {path}")
        return math.ceil(source.getnframes() * fps / source.getframerate())


def package(manifest_path: Path, out: Path, public_root: Path = PUBLIC, gap_frames: int = 5) -> dict:
    if not 0 <= gap_frames <= 45:
        raise ValueError("gap_frames must be 0..45")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("language") != "tl" or manifest.get("fps") != 30:
        raise ValueError("Only the reviewed 30fps Tagalog episode is supported")
    entries = manifest.get("cues")
    if not isinstance(entries, list) or len(entries) != 40:
        raise ValueError("Expected exactly 40 dialogue cues")
    voice_events, clips, timed_cues = [], [], []
    cursor = 0
    base = manifest_path.parent
    dest = public_root / "episodes" / "y2038" / "tl"
    # Validate ALL files first, so a missing cue never leaves a partial package.
    for entry in entries:
        path = base / entry["intended_wav"]
        if not path.is_file():
            raise FileNotFoundError(f"Missing generated voice WAV (nothing was synthesized): {path}")
        wav_frames(path)
    dest.mkdir(parents=True, exist_ok=True)
    for index, entry in enumerate(entries):
        if index != entry["index"]:
            raise ValueError("Manifest cues are out of order")
        wav = base / entry["intended_wav"]
        frames = wav_frames(wav)
        ending = cursor + frames
        relative = f"episodes/y2038/tl/{wav.name}"
        shutil.copy2(wav, dest / wav.name)
        clips.append({"cueIndex": index, "path": relative})
        timed_cues.append({"startFrame": cursor, "endFrame": ending + gap_frames})
        voice_events.append(voice_event_from_wav(wav, entry["speaker"], cursor, 30, 10))
        cursor = ending + gap_frames
    result = {
        "assetsReady": False,
        "voiceClips": clips,
        "timedCues": timed_cues,
        "voiceEvents": voice_events,
        "totalFrames": cursor + 15,
        "audioLanguage": "tl",
        "timingSource": "PCM16_WAV_duration_and_RMS",
        "captionAlignment": "cue_level_only",
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Packaged {len(clips)} real WAV files and {cursor / 30:.2f} seconds of timeline")
    print(f"Render props: {out}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=ROOT / "out/y2038/voice_manifest.json")
    parser.add_argument("--props", type=Path, default=ROOT / "out/y2038/remotion-voice-props.json")
    parser.add_argument("--public", type=Path, default=PUBLIC)
    parser.add_argument("--gap-frames", type=int, default=5)
    args = parser.parse_args()
    package(args.manifest, args.props, args.public, args.gap_frames)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
