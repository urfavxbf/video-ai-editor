"""No-cost real-pose grid extraction with explicit clip and provenance flags."""
from pathlib import Path
import sys
import tempfile
import unittest
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import extract_drawn_pose_grid as grid

class TruePoseGridTests(unittest.TestCase):
    def test_extracts_distinct_rgba_art_without_inventing_animation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p=root/"sheet.png"
            img=Image.new("RGB",(512,512),(248,3,249))
            d=ImageDraw.Draw(img)
            for i in range(4):
                x=(i%2)*256;y=(i//2)*256
                d.ellipse((x+60+i,y+50,x+190+i,y+220),fill=(23+i*20,250,85))
            img.save(p)
            result=grid.extract(p,2,2,root/"frames","urfavxbf")
            self.assertEqual(len(result["frames"]),4)
            self.assertFalse(result["isAnimationLoop"])
            self.assertFalse(result["artApproved"])
            with Image.open(root/"frames/000.png") as first:
                self.assertEqual(first.mode,"RGBA")
                self.assertEqual(first.getpixel((0,0))[3],0)
                self.assertEqual(first.getpixel((100,100))[3],255)

    def test_rejects_missing_chroma_or_wrong_grid(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p=root/"sheet.png"
            Image.new("RGB",(512,512),(120,200,145)).save(p)
            with self.assertRaisesRegex(ValueError,"chroma corners"):
                grid.extract(p,2,2,root/"frames","pix")
            with self.assertRaisesRegex(ValueError,"grid"):
                grid.extract(p,7,3,root/"other","pix")

if __name__=="__main__":
    unittest.main()
