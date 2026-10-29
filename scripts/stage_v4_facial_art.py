#!/usr/bin/env python3
"""Stage the privately saved V4 facial-art draft ZIP (no generated art in Git).

The ZIP is produced from newly drawn individual art; NOT cropped legacy sheets.
Archives must contain 36 aligned 512px RGBA PNGs and matching SHA256 manifest.
This stages files for *private visual review only*, not production approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import tempfile
from zipfile import ZipFile

from validate_v4_facial_assets import validate_art

ROOT=Path(__file__).resolve().parents[1]
PREFIX='public/characters/facial-v4/'
ART_MANIFEST=PREFIX+'facial-art-draft-manifest.json'


def verify_zip(zip_file:Path)->tuple[dict,list[str]]:
    with ZipFile(zip_file) as z:
        files={entry.filename:entry for entry in z.infolist()}
        if ART_MANIFEST not in files:
            raise ValueError('V4 art manifest not in archive')
        manifest=json.loads(z.read(ART_MANIFEST))
        if manifest.get('schema')!='video-ai-editor/facial-v4-art-draft/1':
            raise ValueError('Unknown V4 draft-art schema')
        if manifest.get('status')!='DRAFT_ART_PENDING_USER_VISUAL_APPROVAL':
            raise ValueError('Imported art must remain draft until owner approves')
        contract=json.loads((ROOT/'characters/facial-v4-rig.json').read_text())
        expected=set()
        for who in ('urfavxbf','pix'):
            expected.add(f'{who}/base.png')
            for name in contract['expressionIds']:
                expected.add(f'{who}/expressions/{name}.png')
            for name in contract['mouthIds']:
                expected.add(f'{who}/mouth/{name}.png')
        listed=manifest.get('files',{})
        if set(listed)!=expected or len(listed)!=36:
            raise ValueError('Missing/unexpected art layers (36 required)')
        total_size=0
        for rel,metadata in listed.items():
            path=PREFIX+rel
            if path not in files:
                raise ValueError(f'Missing asset in ZIP: {path}')
            item=files[path]
            if item.is_dir() or item.file_size>10*1024*1024:
                raise ValueError(f'Invalid ZIP member: {path}')
            total_size+=item.file_size
            if total_size>80*1024*1024:
                raise ValueError('ZIP too large')
            if hashlib.sha256(z.read(path)).hexdigest()!=metadata['sha256']:
                raise ValueError(f'SHA mismatch: {path}')
        return manifest,sorted(expected)


def stage(zip_file:Path,dest:Path,overwrite:bool=False)->dict:
    manifest,assets=verify_zip(zip_file)
    if dest.is_symlink():
        raise ValueError('Destination must not be symlink')
    if dest.exists() and not overwrite:
        raise FileExistsError(f'Refusing to overwrite private V4 assets: {dest}')
    dest.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.v4-facial-import-',dir=dest.parent) as tmp:
        staging=Path(tmp)/'stage'
        staging.mkdir()
        with ZipFile(zip_file) as z:
            for rel in assets:
                target=staging/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(z.read(PREFIX+rel))
        contract=json.loads((ROOT/'characters/facial-v4-rig.json').read_text())
        report=validate_art(contract,staging)
        (staging/'facial-art-draft-manifest.json').write_text(
            json.dumps(manifest,indent=2)+'\n')
        if dest.exists():
            # Deliberately no in-place overwrite; requires explicit backup first.
            raise FileExistsError(f'Refusing to replace staged artwork: {dest}')
        shutil.move(str(staging),str(dest))
    return {'staged':len(assets),'destination':str(dest),'status':report['status'],
            'productionApproved':False}


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pack',type=Path,required=True)
    p.add_argument('--dest',type=Path,default=ROOT/'public/characters/facial-v4')
    a=p.parse_args()
    try:
        result=stage(a.pack,a.dest)
    except (ValueError,OSError,KeyError) as e:
        p.exit(2,f'V4 import blocked: {e}\n')
    print(json.dumps(result,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
