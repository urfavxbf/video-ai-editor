#!/usr/bin/env python3
"""Extract real Chatterbox WAV RMS for deterministic speaker-aware puppet movement.

No ML inference, guessed transcripts or invented phonemes. Input WAV must be
16-bit PCM; stereo channels are folded into RMS together. The resulting event
can be passed to the Remotion CharacterPuppet voiceEvents prop.
"""
from __future__ import annotations

import argparse
from array import array
import json
import math
from pathlib import Path
import sys
import wave


def voice_event_from_wav(
    wav_path: Path,
    speaker: str,
    start_frame: int,
    fps: int = 30,
    samples_per_second: int = 10,
) -> dict:
    if speaker not in {"pix", "urfavxbf"}:
        raise ValueError("speaker must be pix or urfavxbf")
    if start_frame < 0 or fps <= 0 or not (2 <= samples_per_second <= 60):
        raise ValueError("invalid frame rate, start frame or envelope sampling rate")
    if not wav_path.is_file():
        raise ValueError(f"WAV missing: {wav_path}")
    energies = []
    with wave.open(str(wav_path), "rb") as audio:
        if audio.getcomptype() != "NONE" or audio.getsampwidth() != 2:
            raise ValueError("expected uncompressed 16-bit PCM WAV")
        sr = audio.getframerate()
        if sr < 8000:
            raise ValueError("sample rate too low")
        bucket_frames = max(1, round(sr / samples_per_second))
        while True:
            raw = audio.readframes(bucket_frames)
            if not raw:
                break
            values = array("h")
            values.frombytes(raw)
            if sys.byteorder != "little":
                values.byteswap()
            if not values:
                break
            rms = math.sqrt(sum(int(x) * int(x) for x in values) / len(values)) / 32768.0
            energies.append(rms)
        duration_frames = max(1, math.ceil(audio.getnframes() * fps / sr))
    if not energies:
        raise ValueError("empty WAV")
    sorted_levels = sorted(energies)
    percentile = sorted_levels[min(len(sorted_levels) - 1, int((len(sorted_levels) - 1) * 0.95))]
    ceiling = max(percentile, 1e-4)
    normalized = [round(min(1.0, max(0.0, x / ceiling)), 3) for x in energies]
    return {
        "speaker": speaker,
        "startFrame": start_frame,
        "endFrame": start_frame + duration_frames,
        "rms": normalized,
        "samplesPerSecond": samples_per_second,
    }


def main():
    p = argparse.ArgumentParser(description="Build a Chatterbox voice envelope from a real WAV")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--speaker", required=True, choices=("pix", "urfavxbf"))
    p.add_argument("--start-frame", type=int, required=True)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--samples-per-second", type=int, default=10)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    event = voice_event_from_wav(
        args.input, args.speaker, args.start_frame, args.fps, args.samples_per_second
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
    print(f"Saved measured audio envelope: {args.output} ({len(event['rms'])} buckets)")


if __name__ == "__main__":
    main()
