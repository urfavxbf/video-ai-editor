#!/usr/bin/env python3
"""Generate an original quiet synth score for UrFavXBF × PIX Y2038.

Copyright-safe original procedural audio, no third-party music samples.
Set music volume below narration during mix. Requires NumPy (audio tooling).
"""
from __future__ import annotations

import argparse
import math
import wave
from pathlib import Path

import numpy as np

FPS = 24000


def generate(out: Path, seconds: int) -> None:
    if not 10 <= seconds <= 3600:
        raise ValueError("Duration must be between 10 and 3600 seconds")
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(2038)
    with wave.open(str(out), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(FPS)
        for start in range(0, seconds, 10):
            count = min(10, seconds - start) * FPS
            t = start + np.arange(count, dtype=np.float64) / FPS
            # Slowly evolving minor chord; digital timer/click accents.
            music = (0.034 * np.sin(2 * math.pi * 73.42 * t + 0.2 * np.sin(t * 0.3))
                     + 0.020 * np.sin(2 * math.pi * 110.00 * t)
                     + 0.017 * np.sin(2 * math.pi * 146.83 * t)
                     + 0.010 * np.sin(2 * math.pi * 174.61 * t))
            music *= 0.84 + 0.16 * np.cos(2 * math.pi * 0.17 * t)
            click_phase = np.mod(t, 1.0)
            click = 0.022 * np.exp(-click_phase * 110.0) * rng.normal(size=count)
            fade = np.minimum(1.0, np.minimum(t / 2.0, (seconds - t) / 3.0))
            pcm = np.clip((music + click) * fade, -0.8, 0.8)
            wav.writeframes((pcm * 32767).astype("<i2").tobytes())
    print(f"Wrote {seconds}s original PCM score to {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=int, default=480)
    parser.add_argument("--output", type=Path, default=Path("public/audio/y2038-ambient.wav"))
    args = parser.parse_args()
    generate(args.output, args.seconds)
