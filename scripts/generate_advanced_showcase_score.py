#!/usr/bin/env python3
"""Original offline electronic showcase score; no licensed samples/cloud API.

Beat-driven audio bed and effect-boundary impacts for the 12 full-frame effects.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import wave
import numpy as np

SR = 48000
FPS = 30
FX_DURATIONS = (72, 75, 72, 80, 75, 75, 70, 75, 72, 75, 75, 120)
BEAT = 60 / 126

def render(path: Path) -> None:
    frame_count = sum(FX_DURATIONS)
    size = frame_count * SR // FPS
    seconds = size / SR
    t = np.arange(size, dtype=np.float64) / SR
    out = np.zeros(size, dtype=np.float64)

    # Original four-bar tonic/chord movement, shape each note by a soft pulse.
    chord_basses = (73.416, 65.406, 82.407, 55.0)
    bar_index = np.floor(t / (BEAT * 4)).astype(np.int32) % 4
    for i, bass in enumerate(chord_basses):
        selection = bar_index == i
        tt = t[selection]
        sidechain = 0.38 + .62 * np.minimum(1., (tt % BEAT) / (.29 * BEAT))
        chord = (.32 * np.sin(2 * np.pi * bass * tt) +
                 .16 * np.sin(2 * np.pi * bass * 1.5 * tt) +
                 .12 * np.sin(2 * np.pi * bass * 2 * tt))
        out[selection] += chord * sidechain * .29

    rng = np.random.default_rng(20261101)
    for beat in range(int(seconds / BEAT) + 1):
        at = round(beat * BEAT * SR)
        if at >= size:
            break
        length = min(int(.24 * SR), size - at)
        tt = np.arange(length) / SR
        phase = 2 * np.pi * (51 * tt + 60 * (1 - np.exp(-tt * 24)) / 24)
        out[at:at + length] += .70 * np.sin(phase) * np.exp(-tt * 23)
        if beat % 2:
            sn_len = min(int(.13 * SR), size - at)
            noise = rng.standard_normal(sn_len)
            out[at:at + sn_len] += .14 * (noise - np.convolve(noise, np.ones(21) / 21, mode='same')) * np.exp(-np.arange(sn_len) / SR * 34)

    for n in range(int(seconds / (BEAT / 2)) + 1):
        at = round(n * BEAT / 2 * SR)
        if at >= size:
            break
        length = min(int(.05 * SR), size - at)
        tt = np.arange(length) / SR
        noise = rng.standard_normal(length)
        out[at:at + length] += .044 * noise * np.exp(-tt * 86)

    # One short synthetic accent at the exact start of every new effect.
    cumulative = 0
    for duration in FX_DURATIONS[1:]:
        cumulative += duration
        at = cumulative * SR // FPS
        if at >= size:
            continue
        length = min(int(.21 * SR), size - at)
        tt = np.arange(length) / SR
        out[at:at + length] += .27 * np.sin(2 * np.pi * (330 * tt - 210 * tt * tt)) * np.exp(-tt * 23)

    fade = np.minimum(1., t / .45) * np.minimum(1., (seconds - t) / 1.1)
    out = np.tanh(out * 1.23) * fade * .80
    right = .91 * out + .09 * np.pad(out[:-330], (330, 0))
    stereo = np.column_stack((out, right))
    audio = (np.clip(stereo, -.97, .97) * 32767).astype('<i2')

    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        wav.writeframes(audio.tobytes())
    print(f'Generated {seconds:.2f}s original stereo PCM soundtrack with {len(FX_DURATIONS)} synchronized effect sections; peak={np.abs(stereo).max():.3f}')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, default=Path('out/advanced-showcase/score.wav'))
    a = p.parse_args()
    render(a.output)
