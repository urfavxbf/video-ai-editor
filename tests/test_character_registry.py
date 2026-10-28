"""Check official character identity and stable Chatterbox voice configuration."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from chatterbox_voice_profile import DEFAULT_NARRATOR
from pix_voice_profile import DEFAULT_PIX


class OfficialCharacterRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "characters/registry.json").read_text(encoding="utf-8"))

    def test_only_two_named_recurring_characters(self):
        d = self.data
        self.assertEqual(d["main_character"], "urfavxbf")
        self.assertEqual(d["companion_character"], "pix")
        self.assertEqual(set(d["characters"]), {"urfavxbf", "pix"})
        self.assertEqual(d["production_language"], "en")

    def test_longform_landscape_delivery_default(self):
        video = self.data["default_video"]
        self.assertEqual(video["type"], "long-form-youtube")
        self.assertEqual(video["aspect_ratio"], "16:9")
        self.assertEqual((video["width"], video["height"], video["fps"]), (1920, 1080, 30))
        self.assertEqual(video["language"], "en")
        self.assertTrue(video["legacy_portrait_demos_not_default"])
        self.assertEqual(video["duration_policy"], "script-and-chapter-driven")

    def test_both_visuals_have_distinct_transparent_asset_footprints(self):
        a = self.data["characters"]
        self.assertNotEqual(a["urfavxbf"]["visual"]["sha256"], a["pix"]["visual"]["sha256"])
        for char in a.values():
            v = char["visual"]
            self.assertEqual(len(v["sha256"]), 64)
            self.assertTrue(v["public_path"].startswith("public/characters/"))
            self.assertTrue(v["library_path"].startswith("/UrFavXBF Video Characters/"))
            self.assertGreater(v["width"], 500)
            self.assertGreater(v["height"], 500)
            self.assertNotEqual(v["kind"], "background-image")

    def test_default_speakers_match_profile_modules(self):
        speakers = self.data["characters"]
        self.assertEqual(speakers["urfavxbf"]["voice"]["identifier"], DEFAULT_NARRATOR.identifier)
        self.assertEqual(speakers["pix"]["voice"]["identifier"], DEFAULT_PIX.identifier)
        self.assertEqual(DEFAULT_PIX.language, DEFAULT_NARRATOR.language)
        self.assertEqual(DEFAULT_PIX.checkpoint, DEFAULT_NARRATOR.checkpoint)
        self.assertNotEqual(DEFAULT_PIX.identifier, DEFAULT_NARRATOR.identifier)
        self.assertEqual(DEFAULT_PIX.reference_git_blob_sha, "a6f9c9f04fdf7bbb4b0de35e6a7111ea0f5a2fa0")
        self.assertTrue(all(len(c["voice"]["sample_sha256"]) == 64 for c in speakers.values()))


if __name__ == "__main__":
    unittest.main()
