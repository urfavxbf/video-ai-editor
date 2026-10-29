"""Zero-cost, honest frame-by-frame source QA for both canonical protagonists."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import true_frame_action_pipeline as pipeline

def make_frames(folder:Path,n:int,duplicates:bool=False,opaque:bool=False,wrong_canvas:bool=False):
    folder.mkdir(parents=True)
    for i in range(n):
        im=Image.new("RGBA",(320+(i==n-1 if wrong_canvas else 0),384),
                     (0,0,0,255) if opaque else (0,0,0,0))
        drawer=ImageDraw.Draw(im)
        shift=0 if duplicates else i*3
        drawer.ellipse((75+shift,65,195+shift,200),fill=(120,245,100,255))
        drawer.rectangle((100,202,180,346),fill=(20,86,55,255))
        im.save(folder/f"{i:03d}.png")

class ZeroCostTrueActionTests(unittest.TestCase):
    def setUp(self):
        self.policy,self.spec=pipeline.load_contracts()

    def test_no_billed_provider_can_run_as_default(self):
        self.assertEqual(self.policy["maximumExternalSpendUsd"],0)
        self.assertFalse(self.policy["allowPaidApis"])
        self.assertFalse(self.policy["allowGpuRental"])
        self.assertFalse(self.policy["autoGenerateSprites"])
        self.assertTrue(self.policy["forbidProductionCutoutFallback"])
        self.assertEqual(self.policy["animationMode"],"independent-whole-character-frames")

    def test_all_both_character_actions_have_explicit_frame_targets(self):
        self.assertEqual(set(self.spec["characters"]),{"urfavxbf","pix"})
        self.assertEqual(len(self.spec["characters"]["urfavxbf"]),15)
        self.assertEqual(len(self.spec["characters"]["pix"]),15)
        for who,catalog in self.spec["characters"].items():
            self.assertIn("walk",catalog)
            self.assertIn("jump",catalog)
            self.assertIn("laugh",catalog)
            for action,entry in catalog.items():
                self.assertGreaterEqual(entry["frames"],6)

    def test_unique_source_frames_can_be_staged_as_unapproved(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);source=base/"input"
            make_frames(source,8)
            frames=pipeline.validate_frames(source,"urfavxbf","point_camera",self.spec)
            self.assertEqual(len(frames),8)
            manifest=pipeline.stage(source,base/"export","urfavxbf","point_camera",self.spec,12)
            self.assertFalse(manifest["artApproved"])
            self.assertFalse(manifest["motionReviewed"])
            self.assertEqual(manifest["technique"],"independent-whole-character-frames")
            self.assertTrue((base/"export/urfavxbf/point_camera/000.png").is_file())
            with self.assertRaises(FileExistsError):
                pipeline.stage(source,base/"export","urfavxbf","point_camera",self.spec,12)

    def test_reject_duplicate_pixels_even_when_files_have_unique_names(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)/"dup";make_frames(folder,8,duplicates=True)
            with self.assertRaisesRegex(ValueError,"Duplicate image frame"):
                pipeline.validate_frames(folder,"urfavxbf","point_camera",self.spec)

    def test_reject_opaque_or_misaligned_sources(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)
            a=base/"opaque";make_frames(a,8,opaque=True)
            with self.assertRaisesRegex(ValueError,"Not transparent"):
                pipeline.validate_frames(a,"urfavxbf","point_camera",self.spec)
            b=base/"sizes";make_frames(b,8,wrong_canvas=True)
            with self.assertRaisesRegex(ValueError,"Canvas sizes not aligned"):
                pipeline.validate_frames(b,"urfavxbf","point_camera",self.spec)

    def test_reject_partial_sequences_and_unknown_actions(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"partial";make_frames(p,2)
            with self.assertRaisesRegex(ValueError,"Expected 12"):
                pipeline.validate_frames(p,"pix","walk",self.spec)
            with self.assertRaisesRegex(ValueError,"Unknown canonical"):
                pipeline.validate_frames(p,"pix","attack",self.spec)

if __name__=="__main__":
    unittest.main()
