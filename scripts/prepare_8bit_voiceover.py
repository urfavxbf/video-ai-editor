#!/usr/bin/env python3
"""Normalize real, measured Chatterbox WAV to the 39.6s Remotion timeline.

Never synthesize fake speech or silently speed up unintelligibly.
Requires ffmpeg+ffprobe. Input must be actual non-silent generated PCM audio.
"""
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

TARGET_SECONDS=39.6
MIN_TEMPO=.75
MAX_TEMPO=1.45

def probe(path:Path):
    raw=subprocess.check_output(['ffprobe','-v','error','-show_entries',
         'format=duration:stream=codec_type,codec_name,sample_rate',
         '-of','json',str(path)],text=True)
    result=json.loads(raw)
    audio=[s for s in result['streams'] if s['codec_type']=='audio']
    if len(audio)!=1: raise ValueError('Expected exactly one real audio stream')
    duration=float(result['format']['duration'])
    if not math.isfinite(duration) or duration<=3 or duration>=100:
        raise ValueError('Unexpected voice duration: '+str(duration))
    return duration

def normalize(source:Path,destination:Path):
    if not source.is_file() or source.stat().st_size<50000:
        raise ValueError('Recorded voice WAV missing or too small')
    raw_duration=probe(source)
    # A small natural-paced gap at the end is preferable to clipping speech.
    tempo=raw_duration/(TARGET_SECONDS-0.4)
    if not MIN_TEMPO<=tempo<=MAX_TEMPO:
        raise ValueError(f'Chatterbox duration {raw_duration:.2f}s requires unnatural tempo {tempo:.2f}')
    destination.parent.mkdir(parents=True,exist_ok=True)
    filters=(f'atempo={tempo:.6f},apad=whole_dur={TARGET_SECONDS},'
             f'afade=t=out:st=39.25:d=0.35')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-i',str(source),'-vn','-af',filters,'-t',str(TARGET_SECONDS),
        '-ar','24000','-ac','1','-c:a','pcm_s16le',str(destination)],check=True)
    duration=probe(destination)
    if abs(duration-TARGET_SECONDS)>.05:raise ValueError('Unexpected normalized audio length')
    # Silence detection: reject pure zeros masquerading as voice.
    audio=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error',
         '-i',str(destination),'-f','s16le','-ac','1','-ar','24000','-'])
    if not audio or not any(audio):raise ValueError('Voice recording is digital silence')
    print(f'Validated voice: {raw_duration:.2f}s original, {duration:.2f}s aligned, tempo={tempo:.3f}')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('input',type=Path)
    p.add_argument('output',type=Path)
    args=p.parse_args()
    try: normalize(args.input,args.output)
    except (OSError,ValueError,subprocess.CalledProcessError) as exc:
        print('Voice alignment failed:',exc,file=sys.stderr)
        sys.exit(2)
