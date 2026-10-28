#!/usr/bin/env python3
"""Produce deterministic Tagalog voice recording inputs from the Y2038 episode.

No TTS inference in default mode: the output is a voice manifest and one text file
per cue. --generate delegates to the existing approved VoxCPM2 character engine
and requires the model, Python environment and compute. No audio is fabricated.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src/episodes/y2038Dialogues.ts"


def read_cues() -> list[dict]:
    source = DATA.read_text(encoding="utf-8")
    match = re.search(r"const raw:[^\n]*=\s*(\[[\s\S]*?\]);", source)
    if not match:
        raise ValueError("Could not locate JSON-backed Y2038 dialogue data")
    cues = json.loads(match.group(1))
    if len(cues) < 35:
        raise ValueError(f"Expected full episode, got {len(cues)} cues")
    for index, cue in enumerate(cues):
        if cue.get("speaker") not in {"pix", "urfavxbf"}:
            raise ValueError(f"Bad speaker at cue {index}")
        if cue.get("chapter") not in range(1, 9) or not cue.get("text", "").strip():
            raise ValueError(f"Bad chapter or empty dialogue at cue {index}")
    return cues


def write_manifest(cues: list[dict], output: Path) -> list[dict]:
    text_dir = output / "voice_inputs"
    text_dir.mkdir(parents=True, exist_ok=True)
    start_frame = 0
    entries = []
    for i, cue in enumerate(cues):
        duration = max(135, int(-(-(len(cue["text"].split()) / 2.12 + 1.2) * 30 // 1)))
        # Keep integer frame bounds in sync with y2038Dialogues.ts ceil().
        text_file = text_dir / f"{i:03d}_{cue['speaker']}.txt"
        text_file.write_text(cue["text"] + "\n", encoding="utf-8")
        entries.append({
            "index": i, "speaker": cue["speaker"], "chapter": cue["chapter"],
            "text_file": str(text_file.relative_to(output)),
            "intended_wav": f"voices/{i:03d}_{cue['speaker']}.wav",
            "estimated_start_frame": start_frame, "estimated_end_frame": start_frame + duration,
            "timings_verified": False,
        })
        start_frame += duration
    (output / "voice_manifest.json").write_text(json.dumps({
        "language": "tl", "fps": 30, "cues": entries,
        "estimated_total_frames": start_frame,
        "warning": "Estimates only. Derive final cues, captions and RMS envelope from actual audio."
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "out/y2038")
    parser.add_argument("--generate", action="store_true", help="Run approved Tagalog VoxCPM2 voice synthesis")
    parser.add_argument("--device", choices=("auto", "cuda", "cpu", "mps"), default="auto")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    cues = read_cues()
    manifest = write_manifest(cues, args.output)
    duration = manifest[-1]["estimated_end_frame"] / 30
    print(f"Prepared {len(manifest)} cues, {duration:.1f}s estimated. WAVs not yet generated.")
    if args.generate:
        voices = args.output / "voices"
        voices.mkdir(parents=True, exist_ok=True)
        for item in manifest:
            destination = args.output / item["intended_wav"]
            if destination.exists() and not args.overwrite:
                print(f"Skip existing {destination}")
                continue
            command = [
                sys.executable, str(ROOT / "scripts/character_voiceover.py"),
                "--character", item["speaker"], "--language", "tl",
                "--text-file", str(args.output / item["text_file"]),
                "--output", str(destination), "--device", args.device,
            ]
            if args.overwrite:
                command += ["--overwrite"]
            subprocess.run(command, check=True)
        print("Synthesized audio candidates. Listen and verify before use.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
