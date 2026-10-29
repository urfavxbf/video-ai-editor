"""Generated V2 cutout rig: reject noncanonical art, preserve neutral pixels.

Uses deterministic synthetic 560x768 RGBA images with test-only SHA patches.
The real source binaries remain in the owner's private Library, not GitHub.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import rig_official_v2_characters as rig
import validate_youtube_journey_fullbody as gate


def fake_art(path:Path,seed:int)->None:
    art=Image.new("RGBA",(560,768),(0,0,0,0))
    d=ImageDraw.Draw(art)
    d.rectangle((28,20,534,745),fill=(18,17+seed,31,255))
    d.ellipse((65,110,496,560),fill=(160+seed,116,209,255))
    d.rounded_rectangle((110,430,469,738),radius=80,fill=(240,182,47+seed,255))
    d.rectangle((200,200,350,500),fill=(30,32,68+seed,255))
    path.parent.mkdir(parents=True,exist_ok=True)
    art.save(path)


class ActualRigExtractionTests(unittest.TestCase):
    def test_exact_neutral_and_all_real_articulated_layers(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            host=root/"urfavxbf.png"
            pix=root/"pix.png"
            fake_art(host,1);fake_art(pix,2)
            patch_hashes={
                "urfavxbf":{**rig.OFFICIAL["urfavxbf"],
                    "hash":hashlib.sha256(host.read_bytes()).hexdigest()},
                "pix":{**rig.OFFICIAL["pix"],
                    "hash":hashlib.sha256(pix.read_bytes()).hexdigest()},
            }
            with patch.dict(rig.OFFICIAL,patch_hashes):
                result=rig.generate(host,pix,root/"public"/"characters"/"pixel-glitch")
            self.assertEqual(set(result),{"urfavxbf","pix"})
            for name,source in (("urfavxbf",host),("pix",pix)):
                self.assertEqual(result[name]["neutralPixelMismatchRate"],0)
                self.assertEqual(result[name]["canvas"],[560,768])
                folder=root/"public"/"characters"/"pixel-glitch"/name
                self.assertEqual((folder/"base.png").read_bytes(),
                                 source.read_bytes())
                original=Image.open(source).convert("RGBA")
                neutral=Image.open(folder/"rig"/"neutral-reconstruction.png").convert("RGBA")
                self.assertEqual(original.tobytes(),neutral.tobytes())
                for part in ("body","head","leftArm","rightArm","underlay"):
                    image=Image.open(folder/"rig"/(part+".png")).convert("RGBA")
                    self.assertEqual(image.size,(560,768))
                    self.assertGreater(image.getchannel("A").getbbox()[2],0)
            self.assertTrue((root/"public"/"characters"/"pixel-glitch"/"urfavxbf"/"rig"/"leftLeg.png").exists())
            self.assertTrue((root/"public"/"characters"/"pixel-glitch"/"urfavxbf"/"rig"/"rightLeg.png").exists())
            self.assertTrue((root/"public"/"characters"/"pixel-glitch"/"pix"/"rig"/"tail.png").exists())
            self.assertFalse((root/"public"/"characters"/"pixel-glitch"/"pix"/"rig"/"leftLeg.png").exists())
            generated=json.loads((root/"public"/"characters"/"pixel-glitch"/"rig-assets.json").read_text())
            self.assertIn("underlay",generated["urfavxbf"]["layeredRig"])
            self.assertIn("tail",generated["pix"]["layeredRig"])
            # Validate source authenticity and exact layer dimensions at the
            # existing render gate, using test fixture hashes only.
            patch_base={"urfavxbf":hashlib.sha256(host.read_bytes()).hexdigest(),
                        "pix":hashlib.sha256(pix.read_bytes()).hexdigest()}
            with patch.dict(gate.OFFICIAL_V2_SHA256,patch_base):
                modes=gate.validate_assets(root/"public",generated)
            self.assertEqual(modes["urfavxbf"],"independently-articulated-limbs")
            self.assertEqual(modes["pix"],"independently-articulated-limbs")

    def test_substituted_artwork_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            fake_art(root/"fake.png",3)
            with self.assertRaisesRegex(ValueError,"SHA-256 mismatch"):
                rig.extract("urfavxbf",root/"fake.png",root/"public"/"characters"/"pixel-glitch")

    def test_missing_original_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            with self.assertRaisesRegex(ValueError,"absent"):
                rig.extract("pix",root/"missing.png",root/"public")


if __name__=="__main__":
    unittest.main()
