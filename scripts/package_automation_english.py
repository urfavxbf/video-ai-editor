#!/usr/bin/env python3
"""Build English Remotion timing/character events from actual PCM16 Chatterbox clips.

Never substitutes another voice engine or pretends to align individual words.
All 34 WAV files are required, and the final assets are copied into public/.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from extract_voice_envelope import voice_event_from_wav
from generate_automation_english import load_cues,wav_duration

def package(cues_path:Path,voice_dir:Path,public:Path,output:Path,gap_frames:int=7):
    if not 0<=gap_frames<=30: raise ValueError("gap_frames must be 0..30")
    cues=load_cues(cues_path)
    clips=[]
    events=[]
    timing=[]
    position=0
    for index,cue in enumerate(cues):
        wav=voice_dir/f"{index:02d}.wav"
        if not wav.is_file():raise FileNotFoundError(f"Missing REAL Chatterbox voice cue: {wav}")
        seconds=wav_duration(wav)
        if not math.isfinite(seconds) or seconds>70:
            raise ValueError(f"Unexpected duration in {wav}: {seconds}")
        frames=math.ceil(seconds*30)
        timing.append(dict(startFrame=position,endFrame=position+frames+gap_frames))
        clips.append(dict(cueIndex=index,path=f"episodes/youtube-automation/voices/{index:02d}.wav"))
        events.append(voice_event_from_wav(wav,cue["speaker"],position,30,10))
        position+=frames+gap_frames
    destination=public/"episodes"/"youtube-automation"/"voices"
    destination.mkdir(parents=True,exist_ok=True)
    for index in range(len(cues)):
        shutil.copy2(voice_dir/f"{index:02d}.wav",destination/f"{index:02d}.wav")
    data=dict(assetsReady=False,voiceClips=clips,voiceEvents=events,timedCues=timing,
              totalFrames=position+24,audioLanguage="en",audioEngine="Chatterbox Multilingual V3",
              timingSource="measured-PCM16-WAV",captionAlignment="cue-level")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(f"Verified {len(clips)} genuine Chatterbox V3 voices, {position/30:.2f} seconds.")
    return data

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--episode",type=Path,default=ROOT/"episodes"/"youtube-automation-en.json")
    parser.add_argument("--voices",type=Path,default=ROOT/"out"/"youtube-automation"/"voices")
    parser.add_argument("--props",type=Path,default=ROOT/"out"/"youtube-automation"/"voice-props.json")
    parser.add_argument("--public",type=Path,default=ROOT/"public")
    args=parser.parse_args()
    package(args.episode,args.voices,args.public,args.props)
if __name__=="__main__":main()
