#!/usr/bin/env python3
"""Generate the owner-requested Jasper example locally, with per-WAV receipts."""
import json,os
from pathlib import Path
from kitten_showreel_voice import load_model,generate
from prepare_host_word_poses import host_voice_request,digest
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
rows=json.loads(Path('src/characters/word-poses/script.json').read_text())
request=host_voice_request()
model=load_model(Path('input/kitten-tts-mini-0.8'))
receipts=[]
for i,row in enumerate(rows):
    path=Path(f'input/host-word-poses/line-{i}.wav')
    generate(model,row['text'],'urfavxbf',path)
    receipts.append({'text':row['text'],'generationRequest':request,'sha256':digest(path)})
    print(i,row['text'],flush=True)
Path('input/host-word-poses/generation.json').write_text(json.dumps(receipts,indent=2)+'\n')
