#!/usr/bin/env python3
"""Actual offline diagnostic proof, explicitly tones rather than generated character speech."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import wave

spec=importlib.util.spec_from_file_location('produce_episode',Path(__file__).with_name('produce-episode.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def fixture(work_dir):
    work_dir=Path(work_dir).resolve();inputs=work_dir/'inputs';(inputs/'audio').mkdir(parents=True,exist_ok=True)
    manifest=json.loads((Path(__file__).resolve().parents[1]/'src/episodes/episode-proof-v1.json').read_text())
    clips=[]
    for i,(speaker,profile,frequency) in enumerate([
        ('urfavxbf','natural-storyteller-v1',440),('pix','pix-cute-female-emily-v1',660)]):
        wav=inputs/'audio'/f'{speaker}-diagnostic.wav'
        with wave.open(str(wav),'wb') as f:
            f.setparams((1,2,16000,0,'NONE','not compressed'))
            tone=b''.join(struct.pack('<h',int(8000*math.sin(n*2*math.pi*frequency/16000))) for n in range(8000))
            f.writeframes(tone+b'\0'*16000+tone if i==0 else tone)
        manifest['chapters'][i]['title']='Diagnostic tones: NOT character speech' if i==0 else 'Resumable local pipeline proof'
        clips.append({'chapterId':manifest['chapters'][i]['id'],'speaker':speaker,
          'voiceProfile':profile,'file':f'audio/{wav.name}','startFrame':6,
          'sha256':hashlib.sha256(wav.read_bytes()).hexdigest(),'provenance':'fixture-diagnostic'})
    mp=inputs/'manifest.json';cp=inputs/'clips.json'
    mp.write_text(json.dumps(manifest));cp.write_text(json.dumps({'schemaVersion':1,'clips':clips}))
    first=m.produce(mp,cp,inputs,work_dir/'run',render=True,diagnostic=True)
    second=m.produce(mp,cp,inputs,work_dir/'run',render=True,diagnostic=True)
    assert all(second[k]['cached'] for k in ('manifest','media','render','qa')), 'Resume repeated completed work'
    assert all(first[k]['resultHash']==second[k]['resultHash'] for k in ('manifest','media','render','qa'))
    print(json.dumps({'artifact':str(Path(second['render']['directory'])/'episode.mp4'),
       'qa':str(Path(second['qa']['directory'])/'qa.json'),'resume':'all four stages cached',
       'audio':'two generated diagnostic tones; NOT voices, speech or alignment'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work-dir',type=Path,required=True)
    fixture(p.parse_args().work_dir)
