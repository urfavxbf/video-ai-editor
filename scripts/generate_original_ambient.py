#!/usr/bin/env python3
"""Generate an original gentle 8-second ambient bed using local Python PCM only.
No voice generation, cloud service, downloaded samples, or paid audio library.
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
import struct
import wave

SAMPLE_RATE = 48000
SECONDS = 8

def generate(target: Path) -> None:
    if target.is_symlink():
        raise ValueError("Refusing to overwrite symlink")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise FileExistsError(f"Target already exists: {target}")
    n = SAMPLE_RATE * SECONDS
    with wave.open(str(target), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        chunk = bytearray()
        frequencies = (130.813, 155.563, 195.998, 261.626)
        for i in range(n):
            t = i / SAMPLE_RATE
            fade = max(0.0,min(1.0, t / 1.1, (SECONDS - t) / 1.4))
            breathing = .78 + .22 * math.sin(2 * math.pi * t / 5.7)
            tone = sum(math.sin(2 * math.pi * f0 * t + math.sin(t * .35) * .04)
                       for f0 in frequencies) / len(frequencies)
            overtone = math.sin(2 * math.pi * 392 * t) * .08
            signal = (tone * .16 + overtone * .11) * breathing * fade
            left = int(max(-1, min(1, signal * .91)) * 32767)
            right = int(max(-1, min(1, signal * 1.02)) * 32767)
            chunk.extend(struct.pack("<hh",left,right))
            if len(chunk) >= 32768:
                f.writeframesraw(chunk)
                chunk.clear()
        if chunk:
            f.writeframesraw(chunk)
        f.writeframes(b"")

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=Path("out/resources/original-ambient-bed.wav"))
    args=p.parse_args()
    generate(args.output)
    print("Generated original quiet ambient cue:",args.output,SECONDS,"seconds PCM16")
