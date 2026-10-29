"""Regression checks for canonical characters and preserved English voice identities."""
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

    def test_only_two_named_recurring_characters_and_multilingual_policy(self):
        d = self.data
        self.assertEqual(d["main_character"], "urfavxbf")
        self.assertEqual(d["companion_character"], "pix")
        self.assertEqual(set(d["characters"]), {"urfavxbf", "pix"})
        self.assertEqual(d["production_language"], "en")
        self.assertEqual(d["supported_production_languages"], ["tl", "en"])

    def test_longform_landscape_delivery_default(self):
        v = self.data["default_video"]
        self.assertEqual(v["type"], "long-form-youtube")
        self.assertEqual(v["aspect_ratio"], "16:9")
        self.assertEqual((v["width"], v["height"], v["fps"]), (1920, 1080, 30))
        self.assertEqual(v["language"], "en")
        for field in ("script_language", "caption_language", "metadata_language"):
            self.assertEqual(v[field], "en")
        self.assertEqual(v["character_layout"], "canonical-chibi-full-body-animated")
        self.assertTrue(v["legacy_portrait_demos_not_default"])
        self.assertTrue(v["full_body_rendering_default"])
        self.assertEqual(self.data["character_hero_system"]["version"], "procedural-3d-v1")
        self.assertTrue(self.data["character_hero_system"]["no_legacy_visual_fallback"])
        self.assertTrue(self.data["character_hero_system"]["runtime_assets_ready"])

    def test_enlarged_head_portraits_and_asset_provenance_unchanged(self):
        v = self.data["default_video"]
        p = v["portrait_size"]
        self.assertEqual((p["width"], p["height"]), (414, 468))
        self.assertEqual((p["left"], p["right"], p["top"]), (64, 64, 202))
        a = self.data["characters"]
        self.assertNotEqual(a["urfavxbf"]["visual"]["reference_source_sha256"], a["pix"]["visual"]["reference_source_sha256"])
        for c in a.values():
            visual = c["visual"]
            self.assertEqual(len(visual["reference_source_sha256"]), 64)
            self.assertTrue(visual["model_path"].startswith("public/characters/3d/"))
            self.assertEqual(visual["model_format"], "gltf-2.0-embedded")
            self.assertTrue(visual["production_rig_ready"])
            self.assertNotIn("public_path", visual)
        self.assertIsNone(a["pix"]["visual"]["official_full_body_reference"])

    def test_tagalog_profiles_and_legacy_english_voices(self):
        chars = self.data["characters"]
        first = chars["urfavxbf"]
        second = chars["pix"]
        self.assertEqual(first["voice"]["identifier"], "urfavxbf-neon-storyteller-tl-v1")
        self.assertEqual(second["voice"]["identifier"], "pix-pixel-spark-tl-v1")
        for c in chars.values():
            self.assertEqual(c["voice"]["language"], "tl")
            self.assertEqual(c["voice"]["engine"], "voxcpm2")
            self.assertEqual(c["voice"]["model_id"], "openbmb/VoxCPM2")
            self.assertTrue(c["voice"]["voice_design_prompt"])
            self.assertIn("no real Tagalog WAV", c["voice"]["sample_status"])
            self.assertEqual(c["english_voice"]["language"], "en")
            self.assertEqual(len(c["english_voice"]["sample_sha256"]), 64)
        self.assertEqual(first["english_voice"]["identifier"], DEFAULT_NARRATOR.identifier)
        self.assertEqual(second["english_voice"]["identifier"], DEFAULT_PIX.identifier)
        self.assertEqual(second["english_voice"]["reference_source"],
                         "devnen/Chatterbox-TTS-Server @ 915ae289340e10c6047f27f47e22eae9bf350c32 voices/Emily.wav")
        self.assertNotEqual(first["voice"]["identifier"], second["voice"]["identifier"])


if __name__ == "__main__":
    unittest.main()
