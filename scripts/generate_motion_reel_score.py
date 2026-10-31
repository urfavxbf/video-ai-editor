#!/usr/bin/env python3
"""Original procedural electronic score — no sampled stock audio, speech or APIs.
Create a driving, beat-synced music bed to support real motion-graphic FX.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import wave

RATE=48000
BPM=124
BEAT=60.0/BPM

def create(seconds:float,target:Path):
    if not 0<seconds<600: raise ValueError("invalid reel duration")
    n=int(seconds*RATE)
    t=np.arange(n,dtype=np.float64)/RATE
    mix=np.zeros(n,dtype=np.float64)
    # Four-bar harmony. Shaped synth pulses, no recognizable external melody.
    chords=[
      (73.416,110.0,146.832),
      (65.406,97.999,130.813),
      (82.407,123.471,164.814),
      (55.0,82.407,110.0),
    ]
    for i,chord in enumerate(chords):
        bar=BEAT*4
        mask=(np.floor(t/bar).astype(np.int32)%4)==i
        tt=t[mask]
        signal=sum(.31*np.sin(2*np.pi*f*tt+.06*np.sin(2*np.pi*.23*tt)) for f in chord)
        signal+=.15*np.sin(2*np.pi*chord[0]*2*tt)
        pulse=.28+.72*np.minimum(1.0,np.mod(tt,BEAT)/(.18*BEAT))
        mix[mask]+=signal*pulse*.22
    # Kicks: descending frequency envelope, impact; snare and hats: seeded noise.
    rng=np.random.default_rng(20261031)
    for i in range(int(seconds/BEAT)+2):
        onset=int(i*BEAT*RATE)
        if onset>=n: break
        length=min(n-onset,int(RATE*.25))
        rt=np.arange(length)/RATE
        kick=np.sin(2*np.pi*(52*rt+57*(1-np.exp(-rt*19))/19))*np.exp(-rt*25)
        mix[onset:onset+length]+=.72*kick
        if i%2:
            snlen=min(n-onset,int(RATE*.14))
            noise=rng.standard_normal(snlen)
            hp=noise-np.convolve(noise,np.ones(35)/35,mode="same")
            mix[onset:onset+snlen]+=.17*hp*np.exp(-np.arange(snlen)/RATE*38)
    for i in range(int(seconds/(BEAT/2))+2):
        onset=int(i*(BEAT/2)*RATE)
        if onset>=n: break
        length=min(n-onset,int(RATE*.068))
        noise=rng.standard_normal(length)
        mix[onset:onset+length]+=.052*noise*np.exp(-np.arange(length)/RATE*85)
    # Continuous clean stereo with gentle master fade and slight stereo delay.
    fade=np.minimum(1.0,t/.65)
    fade*=np.minimum(1.0,np.maximum(0.0,(seconds-t)/1.6))
    mix=np.tanh(mix*1.35)*fade*.85
    delay=int(.007*RATE)
    right=.89*mix+.10*np.pad(mix[:-delay],(delay,0))
    output=np.column_stack((mix,right))
    pcm=(np.clip(output,-.96,.96)*32767).astype('<i2')
    target.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(target),"wb") as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(pcm.tobytes())
    print("Original synthesised showreel score",round(seconds,3),"seconds; peak",round(float(np.max(np.abs(output))),3))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--seconds",type=float,required=True)
    parser.add_argument("--output",type=Path,required=True)
    a=parser.parse_args()
    create(a.seconds,a.output)
