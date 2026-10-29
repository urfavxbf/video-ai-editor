"""The new green chibi direction is real and intentionally production-gated."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ChibiV4DesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design=json.loads((ROOT/"characters/chibi-v4-design.json").read_text())
        cls.registry=json.loads((ROOT/"characters/registry.json").read_text())

    def test_new_colors_and_identity(self):
        c=self.design["characters"]
        self.assertEqual(set(c),{"urfavxbf","pix"})
        self.assertIn("dark-green",self.design["visualVersion"])
        self.assertIn("green",c["urfavxbf"]["style"])
        self.assertIn("purple",c["pix"]["style"])
        self.assertEqual(self.registry["preferred_next_visual_style"],
                         self.design["visualVersion"])

    def test_truthful_frame_count_and_no_false_visemes(self):
        counts=self.design["recordedMotionCounts"]
        self.assertEqual((counts["urfavxbf"]["actions"],
                          counts["urfavxbf"]["frames"]),(23,85))
        self.assertEqual((counts["pix"]["actions"],
                          counts["pix"]["frames"]),(24,86))
        self.assertEqual(self.design["facialReferencesPerCharacter"],10)
        self.assertEqual(self.design["mouthReferenceTilesPerCharacter"],15)
        self.assertEqual(self.design["frameCanvas"],[64,78])
        self.assertTrue(self.design["gating"]["sourcePosesAreDraft"])
        self.assertTrue(self.design["gating"]["visemesAreNotFaceAligned"])
        self.assertFalse(self.design["gating"]["productionApproved"])

    def test_separate_review_integration(self):
        src=(ROOT/"src/characters/ChibiV4Sprite.tsx").read_text()
        root=(ROOT/"src/Root.tsx").read_text()
        self.assertIn("ChibiV4ReviewStage",root)
        self.assertIn("characters/animation-v4",src)
        self.assertIn("characters/animation-v4-normalized",src)
        self.assertNotIn("pixel-glitch/",src)
        self.assertTrue((ROOT/"docs/CHIBI_V4_SPRITE_PACK.md").is_file())


if __name__=="__main__":unittest.main()
