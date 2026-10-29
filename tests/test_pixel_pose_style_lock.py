"""Test the pixel pose design gate; staging is separate and never auto-approved."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
class PixelPoseStyleLockTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/"characters/pixel-pose-style-lock.json").read_text())
    def test_owner_locked_style_and_draft_only(self):
        self.assertTrue(self.data["lockedStyle"])
        self.assertEqual(self.data["artApprovalStatus"],"DRAFT_AWAITING_OWNER_VISUAL_REVIEW")
        self.assertFalse(self.data["productionAutoApproval"])
        self.assertEqual(self.data["maxExternalSpendUsd"],0)
    def test_independent_pose_hashes_and_no_blur(self):
        d=self.data
        self.assertEqual(d["delivery"]["pixelNativeSize"],[256,256])
        self.assertEqual(d["delivery"]["exportSize"],[1024,1024])
        self.assertIn("nearest",d["delivery"]["exportUpscale"])
        self.assertEqual(set(d["characterPoses"]),{"urfavxbf","pix"})
        self.assertEqual(set(d["characterPoses"]["urfavxbf"]),{"idle","talk","point_camera","point_side","laugh"})
        self.assertEqual(set(d["characterPoses"]["pix"]),{"idle","curious","talk","paw_point","happy"})
        hashes=[]
        for character,poses in d["characterPoses"].items():
            for pose,entry in poses.items():
                self.assertEqual(len(entry["sha256"]),64)
                self.assertEqual(entry["exportPath"],f"poses/{character}/{pose}.png")
                hashes.append(entry["sha256"])
        self.assertEqual(len(hashes),10)
        self.assertEqual(len(set(hashes)),10)
    def test_existing_voices_not_replaced(self):
        registry=json.loads((ROOT/"characters/registry.json").read_text())
        self.assertEqual(registry["production_language"],"en")
        self.assertEqual(registry["characters"]["urfavxbf"]["english_voice"]["identifier"],"natural-storyteller-v1")
        self.assertEqual(registry["characters"]["pix"]["english_voice"]["identifier"],"pix-cute-female-emily-v1")

if __name__=="__main__": unittest.main()
