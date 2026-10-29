"""V4 face rig contract, old-model separation and aligned-alpha art checks."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v4qa',ROOT/'scripts/validate_v4_facial_assets.py')
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)
CONTRACT=json.loads((ROOT/'characters/facial-v4-rig.json').read_text())

def build_fake_art(root):
    for character in ('urfavxbf','pix'):
        folder=root/character
        (folder/'expressions').mkdir(parents=True)
        (folder/'mouth').mkdir(parents=True)
        for i,path in enumerate([folder/'base.png']+
                               [folder/'expressions'/f'{x}.png' for x in CONTRACT['expressionIds']]+
                               [folder/'mouth'/f'{x}.png' for x in CONTRACT['mouthIds']]):
            im=Image.new('RGBA',(512,512))
            d=ImageDraw.Draw(im)
            base=i+(0 if character=='urfavxbf' else 80)
            d.rectangle((160+base%30,160,185+base%30,190),
                        fill=(base%256,255,100,255))
            im.save(path)

class V4FacialTests(unittest.TestCase):
    def test_manifest_covers_both_new_models(self):
        s=mod.validate_contract(CONTRACT)
        self.assertEqual((s['characters'],s['expressionsPerCharacter'],s['mouthsPerCharacter']),(2,10,7))
        self.assertEqual(s['qualityStatus'],'ART_PENDING_NOT_PRODUCTION_READY')
        self.assertTrue(all('no pixel reuse' in c['legacyReferenceOnly']['provenance']
                            for c in CONTRACT['characters'].values()))

    def test_all_aligned_art_is_technically_valid_not_production_approved(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            build_fake_art(root)
            s=mod.validate_art(CONTRACT,root)
            self.assertEqual(s['layerCount'],36)
            self.assertIn('AWAITING_OWNER_ART_REVIEW',s['status'])

    def test_missing_layer_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            build_fake_art(root)
            (root/'pix/mouth/fv.png').unlink()
            with self.assertRaisesRegex(ValueError,'Missing/new V4'):
                mod.validate_art(CONTRACT,root)

    def test_must_be_transparent_and_same_canvas(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            build_fake_art(root)
            p=root/'urfavxbf/expressions/neutral.png'
            Image.new('RGB',(384,384),(255,0,0)).save(p)
            with self.assertRaisesRegex(ValueError,'Expected 512x512 RGBA'):
                mod.validate_art(CONTRACT,root)

    def test_legacy_checksum_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            build_fake_art(root)
            p=root/'urfavxbf/base.png'
            sha=__import__('hashlib').sha256(p.read_bytes()).hexdigest()
            mod.BLOCKED_OLD_FINGERPRINTS.add(sha)
            try:
                with self.assertRaisesRegex(ValueError,'LEGACY V2 PNG DETECTED'):
                    mod.validate_art(CONTRACT,root)
            finally:
                mod.BLOCKED_OLD_FINGERPRINTS.remove(sha)
            self.assertIn('b11936a4ace7c6cba1ee391ff768fce93bee80b2adf81b3a44a89cbaa4cf01b4',
                          mod.BLOCKED_OLD_FINGERPRINTS)

    def test_review_does_not_use_old_asset_paths(self):
        comp=(ROOT/'src/characters/V4FacialPortrait.tsx').read_text()
        controller=(ROOT/'src/characters/V4FacialController.ts').read_text()
        root=(ROOT/'src/Root.tsx').read_text()
        self.assertIn('characters/facial-v4',comp)
        self.assertNotIn('pixel-glitch/',comp)
        self.assertIn('artApproved',comp)
        self.assertIn("'no-lipsync'",controller)
        self.assertIn('V4FacialReviewStage',root)

if __name__=='__main__':
    unittest.main()
