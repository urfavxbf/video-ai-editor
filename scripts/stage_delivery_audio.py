#!/usr/bin/env python3
"""Restore approved WAVs from owner-downloaded Drive archives; audio is not in public Git."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def expected_audio(root=ROOT):
    root=Path(root);expected={}
    reel=json.loads((root/'src/showcase/showreel-audio.json').read_text())
    expected['public/'+reel['score']]=reel['scoreSha256']
    for line in reel['voices']:expected['public/'+line['file']]=line['sha256']
    for p in (root/'input/showreel-voices-kitten').glob('*.voice.json'):
        expected[str(p.with_suffix('.wav').relative_to(root)).replace('.voice.wav','.wav')]=json.loads(p.read_text())['sha256']
    host=json.loads((root/'src/characters/word-poses/performance.json').read_text())
    expected['public/'+host['audio']]=host['audioSha256']
    for i,line in enumerate(json.loads((root/'input/host-word-poses/generation.json').read_text())):expected[f'input/host-word-poses/line-{i}.wav']=line['sha256']
    return expected

def stage_archive(archive,expected,root=ROOT):
    root=Path(root).resolve();verified={}
    with zipfile.ZipFile(archive) as z:
        for name in set(z.namelist())&expected.keys():
            target=root/name
            if not target.resolve().is_relative_to(root) or Path(name).suffix!='.wav':raise ValueError('Unsafe audio destination')
            info=z.getinfo(name)
            if info.file_size>16_000_000:raise ValueError('Oversized audio asset')
            raw=z.read(name)
            if hashlib.sha256(raw).hexdigest()!=expected[name]:raise ValueError('Audio hash mismatch: '+name)
            if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()!=expected[name]:raise ValueError('Different audio already exists: '+name)
            verified[name]=raw
    if not verified:raise ValueError('No approved audio found in archive')
    for name,raw in verified.items():
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    return len(verified)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archives',type=Path,nargs='+');args=parser.parse_args()
    for archive in args.archives:print('Verified/staged WAVs:',stage_archive(archive,expected_audio()))
