"""Model-free tests for Tagalog/Taglish voice design and chunked synthesis wiring."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import voxcpm_voiceover as tts


class VoxCPMVoiceoverTests(unittest.TestCase):
    def test_tagalog_voice_profiles_are_distinct(self):
        a = tts.profile_for("urfavxbf")
        b = tts.profile_for("pix")
        self.assertEqual(a["model_id"], "openbmb/VoxCPM2")
        self.assertEqual(a["language"], "tl")
        self.assertEqual(b["language"], "tl")
        self.assertNotEqual(a["identifier"], b["identifier"])
        self.assertIn("male", a["voice_design_prompt"].lower())
        self.assertIn("female", b["voice_design_prompt"].lower())

    def test_sentence_aware_chunking_handles_tagalog_and_taglish(self):
        chunks = tts.split_text("Alam mo ba? May paliwanag tayo. " * 12, max_chars=70)
        self.assertGreater(len(chunks), 2)
        self.assertTrue(all(len(s) <= 70 for s in chunks))
        self.assertEqual(" ".join(chunks), ("Alam mo ba? May paliwanag tayo. " * 12).strip())

    def test_invalid_long_token_rejected(self):
        with self.assertRaisesRegex(ValueError, "Single token"):
            tts.split_text("a" * 500, max_chars=100)

    def test_dry_run_does_not_generate_or_write_audio(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "voice.wav"
            with patch.object(tts, "synthesize", side_effect=AssertionError("TTS must not run")):
                with contextlib.redirect_stdout(io.StringIO()) as stream:
                    code = tts.main(["--character", "pix", "--text", "Hala, seryoso?!", "--output",
                                     str(output), "--dry-run"])
            data = json.loads(stream.getvalue())
            self.assertEqual(code, 0)
            self.assertEqual(data["language"], "tl")
            self.assertEqual(data["engine"], "voxcpm2")
            self.assertFalse(data["audio_generated"])
            self.assertFalse(output.exists())

    def test_output_must_be_wav(self):
        self.assertEqual(tts.main(["--character", "urfavxbf", "--text", "Kamusta?",
                                   "--output", "bad.mp3", "--dry-run"]), 2)


if __name__ == "__main__":
    unittest.main()
