#!/usr/bin/env python3
"""Create deterministic ORIGINAL four-second PCM audio and measured 30fps RMS.
No user media or cloud voice/audio service. The JSON is the audio-reactive
contract checked into the repo; publishing does not require this demo sound.
"""
import argparse, json, math, struct, wave
from pathlib import Path

RATE=48000
FPS=30
FRAMES=120
SECONDS=FRAMES/FPS

def sample(i):
    t=i/RATE
    beat=60/120
    amplitude=0.16+0.23*abs(math.cos(math.pi*t/beat))**12
    return amplitude*math.sin(math.tau*110*t)

def generate(output):
    output.parent.mkdir(parents=True,exist_ok=True)
    energy=[]
    with wave.open(str(output),'wb') as handle:
        handle.setnchannels(2);handle.setsampwidth(2);handle.setframerate(RATE)
        for frame in range(FRAMES):
            acc=0.0
            samples=bytearray()
            for i in range(RATE//FPS):
                x=sample(frame*(RATE//FPS)+i)
                acc+=x*x
                v=int(max(-1,min(1,x))*32767)
                samples.extend(struct.pack('<hh',v,v))
            energy.append(round(math.sqrt(acc/(RATE//FPS)),6))
            handle.writeframesraw(samples)
        handle.writeframes(b'')
    return energy

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,default=Path('public/sample/advanced-reactive.wav'))
    p.add_argument('--envelope',type=Path,default=Path('src/fx/advanced/reactive-envelope.json'))
    args=p.parse_args()
    rms=generate(args.output)
    existing=json.loads(args.envelope.read_text())
    if rms!=existing:
        raise SystemExit('Committed waveform data differs from real synthesized PCM RMS')
    print('Verified 120 frames of 30fps RMS aligned with original 4-second stereo WAV')
