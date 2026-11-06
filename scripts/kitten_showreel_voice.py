#!/usr/bin/env python3
"""Pinned local CPU KittenTTS Mini adapter for owner-selected showreel voices."""
import json
from pathlib import Path
from urllib.request import urlopen
from prepare_showreel import ROOT, digest

PROFILE=ROOT/'src/showcase/showreel-voices.json'

def config():return json.loads(PROFILE.read_text())

def verify_model(directory:Path):
    for name,expected in config()['files'].items():
        path=directory/name
        if not path.is_file() or digest(path)!=expected:
            raise ValueError('Kitten model hash mismatch: '+name)

def stage_model(directory:Path):
    profile=config();directory.mkdir(parents=True,exist_ok=True)
    for name,expected in profile['files'].items():
        path=directory/name
        if path.is_file() and digest(path)==expected:continue
        url='https://huggingface.co/'+profile['model']+'/resolve/'+profile['modelRevision']+'/'+name
        with urlopen(url,timeout=120) as response:payload=response.read(100_000_001)
        if len(payload)>100_000_000:raise ValueError('Unexpected Kitten model size')
        import hashlib
        if hashlib.sha256(payload).hexdigest()!=expected:raise ValueError('Kitten download hash mismatch: '+name)
        path.write_bytes(payload)
    verify_model(directory)

def verify_sdk(directory:Path|None=None):
    if directory is None:
        from importlib.util import find_spec
        module=find_spec('kittenml')
        if module is None or module.origin is None:raise ValueError('Missing Kitten SDK; install pinned ONNX requirements')
        directory=Path(module.origin).parent
    for name,expected in config()['sdkFiles'].items():
        path=directory/name
        if not path.is_file() or digest(path)!=expected:
            raise ValueError('Kitten SDK hash mismatch: '+name+'; install the pinned SDK commit')


def load_model(directory:Path):
    verify_model(directory)
    verify_sdk()
    from kittenml import KittenTTS
    import onnxruntime as ort
    model=KittenTTS(str(directory),backend='cpu')
    options=ort.SessionOptions();options.intra_op_num_threads=config()['threads'];options.inter_op_num_threads=1
    model.model.session=ort.InferenceSession(model.model.model_path,sess_options=options,providers=['CPUExecutionProvider'])
    return model

def generate(model,text:str,character:str,output:Path):
    import numpy as np
    import soundfile as sf
    profile=config();voice=profile['voices'][character]
    audio=np.asarray(model.generate(text,voice=voice,speed=profile['speed'],clean_text=False)).reshape(-1)
    if not len(audio) or not np.isfinite(audio).all():raise ValueError('Kitten produced invalid PCM')
    output.parent.mkdir(parents=True,exist_ok=True)
    temporary=output.with_name('.'+output.stem+'-kitten.wav')
    try:
        sf.write(str(temporary),audio,profile['sampleRate'],subtype='PCM_16')
        temporary.replace(output)
    finally:temporary.unlink(missing_ok=True)
