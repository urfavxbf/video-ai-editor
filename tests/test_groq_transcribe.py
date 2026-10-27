"""Unit tests for Groq subtitle formatting; no API calls required."""
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "scripts/groq_transcribe.py"
spec = importlib.util.spec_from_file_location("groq_transcribe", path)
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)

class CaptionFormattingTests(unittest.TestCase):
    def test_timestamps(self):
        self.assertEqual(editor.srt_time(61.205), "00:01:01,205")
        self.assertEqual(editor.srt_time(0), "00:00:00,000")

    def test_taglish_word_timing(self):
        data = {"words": [
            {"word": "Ang", "start": 0, "end": .2},
            {"word": "ganda", "start": .3, "end": .6},
            {"word": "nito!", "start": .65, "end": 1.0},
            {"word": "Really.", "start": 1.1, "end": 1.4},
        ]}
        srt = editor.render_srt(data)
        self.assertIn("Ang ganda nito!", srt)
        self.assertIn("00:00:00,000 --> 00:00:01,000", srt)
        self.assertIn("Really.", srt)

    def test_segment_fallback(self):
        data = {"segments": [{"start": 2, "end": 3, "text": " Kumusta! "}]}
        self.assertIn("00:00:02,000 --> 00:00:03,000", editor.render_srt(data))

    def test_missing_timestamps(self):
        with self.assertRaises(ValueError):
            editor.render_srt({"text": "no timestamps"})

if __name__ == "__main__":
    unittest.main()
