#!/usr/bin/env python3
"""Offline showreel audio: real approved WAVs, measured utterance captions, original score.

No TTS imports, remote processing, account connections or paid services.
The owner-selected, pinned Kitten Mini CPU adapter performs synthesis separately.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import wave
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
FPS=30
MANIFEST=ROOT/'src/showcase/showreel-audio.json'
DEST=ROOT/'public/voiceovers/showreel-kitten'
SCRIPT=ROOT/'src/showcase/showreel-script.json'


def digest(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def voice_request(row:dict)->dict:
    config=json.loads((ROOT/'src/showcase/showreel-voices.json').read_text())
    voice=config['voices'][row['character']]
    return {'text':row['text'],'character':row['character'],'language':'en',
            'profile':'kitten-mini-'+voice.lower()+'-en-v1','engine':config['engine'],
            'model':config['model'],'modelRevision':config['modelRevision'],
            'sdkCommit':config['sdkCommit'],'voice':voice,'speed':config['speed']}


def validate_receipt(path:Path,row:dict)->None:
    receipt_path=path.with_suffix('.voice.json')
    if not receipt_path.is_file():
        raise ValueError('Missing voice generation receipt: '+path.name)
    receipt=json.loads(receipt_path.read_text())
    if receipt.get('request')!=voice_request(row):
        raise ValueError('Voice receipt is stale for current script/speaker: '+path.name)
    if not path.is_file() or receipt.get('sha256')!=digest(path):
        raise ValueError('Voice recording changed since generation: '+path.name)


def envelope(samples:np.ndarray,rate:int)->list[float]:
    """30fps RMS of real PCM, normalized to that recording's measured peak RMS."""
    values=np.array([np.sqrt(np.mean(samples[int(i*rate/FPS):int((i+1)*rate/FPS)]**2))
                     for i in range(math.ceil(len(samples)/rate*FPS))])
    scale=max(float(np.max(values)),1e-7)
    return [round(float(v/scale),5) for v in values]


def load_voice(path:Path,max_frames:int)->tuple[np.ndarray,int]:
    if not path.is_file():
        raise ValueError(f'Missing approved narration: {path}')
    try:
        with wave.open(str(path),'rb') as w:
            if w.getsampwidth()!=2 or w.getframerate()<16000 or w.getnchannels() not in (1,2):
                raise ValueError('Expected 16-bit PCM WAV at >=16kHz')
            rate=w.getframerate(); channels=w.getnchannels()
            samples=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float64)/32768
            samples=samples.reshape(-1,channels).mean(axis=1)
    except (wave.Error, EOFError, ValueError) as exc:
        raise ValueError(f'Invalid WAV: {path.name}: {exc}') from exc
    active=np.flatnonzero(np.abs(samples)>.008)
    if not len(active):
        raise ValueError(f'Voice is silent: {path.name}')
    pad=int(.075*rate)
    samples=samples[max(0,int(active[0])-pad):min(len(samples),int(active[-1])+pad+1)]
    if math.ceil(len(samples)/rate*FPS)>max_frames:
        raise ValueError(f'Voice {path.name} exceeds {max_frames/FPS:.2f}s slot: {len(samples)/rate:.2f}s')
    peak=float(np.max(np.abs(samples)))
    samples=samples*.83/peak
    return samples,rate


def write_wav(path:Path,samples:np.ndarray,rate:int)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate)
        w.writeframes((np.clip(samples,-.99,.99)*32767).astype('<i2').tobytes())


def timeline()->dict:
    return json.loads(subprocess.check_output(['node',str(ROOT/'scripts/showreel-manifest.cjs')],cwd=ROOT,text=True))


def original_score(duration:float,shots:list[dict],rate:int=48000)->np.ndarray:
    """Original 120 BPM synth score and procedural drums; reproducible seeded noise."""
    rng=np.random.default_rng(20261106)
    n=round(duration*rate); out=np.zeros(n,dtype=np.float64)
    notes=[55,65.4064,73.4162,82.4069]
    def add(start:float,clip:np.ndarray,gain:float=1):
        at=round(start*rate)
        if at>=n:return
        count=min(len(clip),n-at)
        out[at:at+count]+=clip[:count]*gain
    for b,start in enumerate(np.arange(0,duration,.5)):
        phrase=notes[(b//16)%4]
        t=np.arange(round(.47*rate))/rate
        bass=(np.sin(2*np.pi*phrase*t)+.22*np.sin(4*np.pi*phrase*t))*np.minimum(1,t/.008)*np.exp(-t*6)
        add(float(start),bass,.14)
        k=np.arange(round(.3*rate))/rate
        kick=np.sin(2*np.pi*(46*k+15*(1-np.exp(-k*36))))*np.exp(-k*18)
        add(float(start),kick,.22)
        if b%2:
            s=np.arange(round(.12*rate))/rate
            clap=rng.normal(size=len(s))*np.exp(-s*42)
            add(float(start),clap,.025)
        for offset in (0,.25):
            h=np.arange(round(.06*rate))/rate
            noise=rng.normal(size=len(h)); hat=np.diff(np.r_[0,noise])*np.exp(-h*70)
            add(float(start)+offset,hat,.009 if offset else .006)
        a=np.arange(round(.4*rate))/rate
        pitch=phrase*([8,12,16,12][b%4])
        arp=(np.sin(2*np.pi*pitch*a)+.2*np.sin(4*np.pi*pitch*a))*np.exp(-a*10)*np.minimum(a/.01,1)
        add(float(start)+.25,arp,.035)
    # Original procedural transition Foley; no imported/reference soundtrack assets.
    for shot in shots:
        kind=('shatter' if shot['id']=='glass-shatter' else 'whip' if 'zoom' in shot['id'] or 'whip' in shot['id']
              else 'typing' if shot['id']=='chat-takeover' else 'reveal' if 'film' in shot['id'] else 'whoosh')
        t=np.arange(round(.7*rate))/rate
        white=rng.normal(size=len(t))
        smooth=np.convolve(white,np.ones(11)/11,mode='same')
        sweep=np.sin(np.pi*np.minimum(t/.7,1))**3
        if kind=='shatter':
            cue=(white*.13+np.sin(2*np.pi*3600*t)*.05)*np.exp(-t*11)
            for delay in (.06,.11,.19):
                add(shot['at']/FPS+delay,cue,.3)
        elif kind=='typing':
            cue=np.sin(2*np.pi*1400*t)*np.exp(-(t%.09)*170)*(t<.55)
        elif kind=='reveal':
            cue=(smooth*.8+np.sin(2*np.pi*(220*t+1800*t**3))*.06)*sweep
        elif kind=='whip':
            cue=(white*.04+smooth*.8)*sweep
        else:
            cue=smooth*sweep
        add(shot['at']/FPS,cue,.12)
    fade=np.minimum(np.arange(n)/rate/2,1)*np.minimum((n-np.arange(n))/rate/2,1)
    out*=fade
    out*=.68/max(float(np.max(np.abs(out))),1e-7)
    return out


def prepare(source_dir:Path)->dict:
    t=timeline(); definitions=json.loads(SCRIPT.read_text());voices=[]
    for row in definitions:
        source=source_dir/f"{row['name']}.wav"
        validate_receipt(source,row)
        samples,rate=load_voice(source,row['maxFrames'])
        target=DEST/f"{row['name']}.wav"
        write_wav(target,samples,rate)
        frames=math.ceil(len(samples)/rate*FPS)
        if row['at']+frames>t['durationFrames']:
            raise ValueError('Voice extends beyond showreel: '+row['name'])
        voices.append({**row,'file':str(target.relative_to(ROOT/'public')),'frames':frames,
                       'sampleRate':rate,'samples':len(samples),'sha256':digest(target),
                       'sourceSha256':digest(source),'generationRequest':voice_request(row),'envelope':envelope(samples,rate)})
    for left,right in zip(voices,voices[1:]):
        if left['at']+left['frames']>right['at']:
            raise ValueError('Overlapping voice slots')
    score=original_score(t['durationFrames']/FPS,t['shots'])
    score_path=DEST/'score.wav';write_wav(score_path,score,48000)
    result={'version':1,'ready':True,'fps':FPS,'durationFrames':t['durationFrames'],
            'score':str(score_path.relative_to(ROOT/'public')),'scoreSha256':digest(score_path),
            'scoreProvenance':'Original deterministic 120 BPM synthesis + procedural transition Foley',
            'captionTiming':'Whole utterances at measured WAV boundaries; no word-alignment claim',
            'envelope':envelope(score,48000),'voices':voices}
    MANIFEST.write_text(json.dumps(result,indent=2)+'\n')
    out=ROOT/'out/showreel';out.mkdir(parents=True,exist_ok=True)
    (out/'coverage.json').write_text(json.dumps(t,indent=2)+'\n')
    return result


def check()->dict:
    data=json.loads(MANIFEST.read_text()); t=timeline()
    if not data.get('ready') or data.get('durationFrames')!=t['durationFrames']:
        raise ValueError('Showreel audio is not prepared for this timeline')
    expected=json.loads(SCRIPT.read_text())
    if len(data.get('voices',[]))!=len(expected):
        raise ValueError('Missing showreel voice lines')
    for row,want in zip(data['voices'],expected):
        if any(row.get(key)!=want[key] for key in ('name','character','at','text','maxFrames')):
            raise ValueError('Narration script changed: regenerate showreel audio')
        if row.get('generationRequest')!=voice_request(want):
            raise ValueError('Voice engine/profile changed: regenerate showreel audio')
        path=ROOT/'public'/row['file']
        if not path.is_file() or digest(path)!=row['sha256']:
            raise ValueError('Missing or changed voice asset: '+row['name'])
        with wave.open(str(path),'rb') as w:
            frames=math.ceil(w.getnframes()/w.getframerate()*FPS)
            if frames!=row['frames'] or frames>row['maxFrames']:
                raise ValueError('Voice media bounds do not match manifest')
        if len(row['envelope'])!=frames:
            raise ValueError('Voice envelope does not cover the actual WAV')
    score=ROOT/'public'/data['score']
    if not score.is_file() or digest(score)!=data['scoreSha256']:
        raise ValueError('Missing or changed original score')
    with wave.open(str(score),'rb') as w:
        if abs(w.getnframes()/w.getframerate()*FPS-t['durationFrames'])>.01:
            raise ValueError('Score does not cover the complete timeline')
    return data


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-dir',type=Path,default=ROOT/'input/showreel-voices-kitten')
    p.add_argument('--check',action='store_true');args=p.parse_args()
    try:
        data=check() if args.check else prepare(args.source_dir)
    except (ValueError,OSError,subprocess.CalledProcessError) as exc:
        print(f'Showreel preflight failed: {exc}');return 2
    print(f"Verified {len(data['voices'])} actual voice clips; {data['durationFrames']/FPS:.2f}s original score")
    return 0

if __name__=='__main__':
    raise SystemExit(main())
