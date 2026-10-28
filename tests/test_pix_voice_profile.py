"""Model-free regression checks for the PIX female Chatterbox voice candidate."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from chatterbox_voice_profile import DEFAULT_NARRATOR
from chatterbox_voiceover import build_parser
from pix_voice_profile import PIX_CANDIDATE, PIX_SAMPLE_SCRIPT


class PixVoiceTests(unittest.TestCase):
    def test_english_and_distinct_narrator(self):
        self.assertEqual(PIX_CANDIDATE.checkpoint, "v3")
        self.assertEqual(PIX_CANDIDATE.language, "en")
        self.assertNotEqual(PIX_CANDIDATE.identifier, DEFAULT_NARRATOR.identifier)
        self.assertEqual(DEFAULT_NARRATOR.identifier, "natural-storyteller-v1")
        self.assertIn("UrFavXBF", PIX_SAMPLE_SCRIPT)

    def test_reference_pinned_and_controls_compatible(self):
        self.assertIn("/915ae289340e10c6047f27f47e22eae9bf350c32/", PIX_CANDIDATE.reference_url)
        self.assertEqual(len(PIX_CANDIDATE.reference_git_blob_sha), 40)
        p = build_parser().parse_args([
            "--text", PIX_SAMPLE_SCRIPT,
            "--output", "out/pix-test.wav",
            "--language-id", PIX_CANDIDATE.language,
            "--voice-reference", "input/pix-reference.wav",
            "--exaggeration", str(PIX_CANDIDATE.exaggeration),
            "--cfg-weight", str(PIX_CANDIDATE.cfg_weight),
        ])
        self.assertEqual(p.language_id, "en")
        self.assertAlmostEqual(p.exaggeration, 0.65)
        self.assertAlmostEqual(p.cfg_weight, 0.35)
        self.assertEqual(str(p.voice_reference), "input/pix-reference.wav")


if __name__ == "__main__":
    unittest.main()
