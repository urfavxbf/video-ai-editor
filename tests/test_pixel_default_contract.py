"""Current owner-selected 16-pose art contract. Binary production gate is separate."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
class PixelDefaultTests(unittest.TestCase):
    def test_16_published_poses_are_named_and_sha_pinned(self):
        reg=json.loads((ROOT/"characters/registry.json").read_text())
        m=json.loads((ROOT/"characters/pixel-default-manifest.json").read_text())
        self.assertEqual(reg["character_hero_system"]["version"],"pixel-pose-default-2026-11-06")
        self.assertTrue(m["selectedAsDefaultByOwner"])
        self.assertEqual(m["assetDelivery"]["assetReady"],m["assetDelivery"]["assetsCommitted"])
        if m["assetDelivery"]["assetReady"]:
            for character in m["characters"].values():
                for pose in character["poses"].values():
                    self.assertTrue((ROOT/pose["path"]).is_file())
        self.assertEqual(set(m["characters"]),{"urfavxbf","pix"})
        self.assertEqual({c:len(x["poses"]) for c,x in m["characters"].items()},{"urfavxbf":9,"pix":7})
        self.assertIn("surprised",m["characters"]["urfavxbf"]["poses"])
        self.assertIn("question",m["characters"]["pix"]["poses"])
        self.assertIn("surprised",m["characters"]["pix"]["poses"])
        self.assertFalse((ROOT/"public/characters/pixel-default/urfavxbf").exists())
        hashes=[]
        for who,record in m["characters"].items():
            self.assertEqual(reg["characters"][who]["visual"]["public_path"],record["poses"][record["defaultPose"]]["path"])
            for pose,info in record["poses"].items():
                self.assertTrue((ROOT/info["path"]).is_file())
                self.assertEqual(len(info["sha256"]),64)
                self.assertEqual((info["width"],info["height"]),(1280,960) if who=="urfavxbf" else (1254,1254))
                hashes.append(info["sha256"])
        self.assertEqual(len(set(hashes)),8)

    def test_pose_selector_and_glitch_proof_are_installed(self):
        src=(ROOT/"src/characters/PixelPoseCharacter.tsx").read_text()
        self.assertIn("imageRendering:'pixelated'",src)
        self.assertIn("reaction==='surprised'",src)
        self.assertIn("return 'question'",src)
        self.assertNotIn("animation-v4/",src)
        root=(ROOT/"src/Root.tsx").read_text()
        self.assertIn('id="PixelProductionProof"',root)
        self.assertIn('defaultProps={{assetsReady:true} satisfies PixelProductionProofProps}',root)
        self.assertIn('defaultProps={{assetsReady:true,artApproved:true,voiceEvents:[],chapter:1} satisfies HeroStageProps}',root)
        proof=(ROOT/"src/characters/PixelProductionProof.tsx").read_text()
        self.assertIn("if(!assetsReady)throw",proof)
        self.assertIn("glitch",proof)

    def test_superseded_installer_cannot_restore_old_host(self):
        self.assertFalse((ROOT/'.github/workflows/install-pixel-pose-pack.yml').exists())
        self.assertFalse((ROOT/'scripts/activate_pixel_default.py').exists())

    def test_selected_voices_and_zero_budget(self):
        reg=json.loads((ROOT/"characters/registry.json").read_text())
        self.assertEqual(reg["production_language"],"en")
        self.assertEqual(reg["characters"]["urfavxbf"]["english_voice"]["identifier"],"kitten-mini-jasper-en-v1")
        self.assertEqual(reg["characters"]["pix"]["english_voice"]["identifier"],"kitten-mini-kiki-en-v1")
        self.assertEqual(reg["character_hero_system"]["maximumExternalSpriteSpendUsd"],0)

if __name__=="__main__":unittest.main()
