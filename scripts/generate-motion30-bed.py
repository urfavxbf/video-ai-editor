#!/usr/bin/env python3
"""Create original synthetic ambient music for the motion showcase."""
from pathlib import Path
import wave
import numpy as np

rate = 48000
length = rate * 30
t = np.arange(length, dtype=np.float64) / rate
pulse = np.maximum(0, np.sin(2*np.pi*(100/60)*t))**3
audio = 0.06*(np.sin(2*np.pi*55*t)+.3*np.sin(2*np.pi*110*t))*(.22+.78*pulse)
for time in np.arange(0,30,.6):
    start = int(time*rate)
    n = min(int(.18*rate),length-start)
    x = np.arange(n)/rate
    audio[start:start+n] += .14*np.sin(2*np.pi*70*x)*np.exp(-24*x)
for time in [0,6,12,18,24]:
    start = int(time*rate)
    n = min(rate,length-start)
    x = np.arange(n)/rate
    audio[start:start+n] += .17*np.sin(2*np.pi*(85-38*x)*x)*np.exp(-8*x)
audio *= np.minimum(1,t/1.2)*np.minimum(1,(30-t)/1.3)
stereo = np.stack([audio,np.roll(audio,16)],axis=1)
dest = Path("public/voiceovers/motion30-bed.wav")
dest.parent.mkdir(parents=True,exist_ok=True)
with wave.open(str(dest),"wb") as out:
    out.setnchannels(2)
    out.setsampwidth(2)
    out.setframerate(rate)
    out.writeframes(np.clip(stereo*32767,-32768,32767).astype("<i2").tobytes())
print("Created original soundtrack:", dest)
