"""Self-contained tests for private V4 facial artwork staging (no public art)."""
from __future__ import annotations
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile,ZIP_DEFLATED
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('stagefacial',ROOT/'scripts/stage_v4_facial_art.py')
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

CONTRACT=json.loads((ROOT/'characters/facial-v4-rig.json').read_text())
PREFIX=mod.PREFIX

def make_zip(target:Path,bad_hash=False):
    names=[]
    for ch in ('urfavxbf','pix'):
        names.append(f'{ch}/base.png')
        names.extend(f'{ch}/expressions/{n}.png' for n in CONTRACT['expressionIds'])
        names.extend(f'{ch}/mouth/{n}.png' for n in CONTRACT['mouthIds'])
    metadata={'schema':'video-ai-editor/facial-v4-art-draft/1',
              'status':'DRAFT_ART_PENDING_USER_VISUAL_APPROVAL','files':{}}
    with ZipFile(target,'w',ZIP_DEFLATED) as z:
        for i,name in enumerate(names):
            im=Image.new('RGBA',(512,512))
            d=ImageDraw.Draw(im)
            x=135+i
            d.rectangle((x,194,x+10,222),fill=(i*7%256,220,120,255))
            f=io.BytesIO();im.save(f,format='PNG')
            data=f.getvalue();hash=hashlib.sha256(data).hexdigest()
            metadata['files'][name]={'sha256':'f'*64 if bad_hash and i==0 else hash}
            z.writestr(PREFIX+name,data)
        z.writestr(mod.ART_MANIFEST,json.dumps(metadata))

class TestV4Staging(unittest.TestCase):
    def test_sha_verified_stage_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            t=Path(td);p=t/'sample.zip';make_zip(p)
            dest=t/'stage'/'facial-v4'
            result=mod.stage(p,dest)
            self.assertEqual(result['staged'],36)
            self.assertFalse(result['productionApproved'])
            self.assertTrue((dest/'pix/mouth/round.png').exists())
            with self.assertRaises(FileExistsError):mod.stage(p,dest)

    def test_reject_mismatched_hash(self):
        with tempfile.TemporaryDirectory() as td:
            t=Path(td);p=t/'sample.zip';make_zip(p,bad_hash=True)
            with self.assertRaisesRegex(ValueError,'SHA mismatch'):
                mod.stage(p,t/'dest')

    def test_reject_missing_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            t=Path(td);p=t/'bad.zip'
            with ZipFile(p,'w') as z:z.writestr('README.txt','test')
            with self.assertRaisesRegex(ValueError,'manifest not in archive'):
                mod.stage(p,t/'dest')

if __name__=='__main__':unittest.main()
