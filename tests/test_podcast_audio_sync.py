"""No-network regression tests: captions must follow supplied acoustic word times."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render-synced-podcast.py"
spec = importlib.util.spec_from_file_location("podcast_audio_sync", SCRIPT)
assert spec and spec.loader
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)


class WordSyncTests(unittest.TestCase):
    def setUp(self):
        # Fake test data, NOT an actual celebrity quote or transcription.
        self.raw = {"words": [
            {"word": "This", "start": 12.20, "end": 12.51},
            {"word": "is", "start": 12.63, "end": 12.81},
            {"word": "only", "start": 13.20, "end": 13.60},
            {"word": "a", "start": 13.72, "end": 13.81},
            {"word": "test.", "start": 13.93, "end": 14.32},
        ]}

    def test_missing_word_timing_is_fatal(self):
        for value in ({"text": "This is only a test."}, {"segments": []}, {"words": []}):
            with self.assertRaises(ValueError):
                editor.get_audio_words(value)

    def test_word_order_and_duration_validation(self):
        transcript = {"words": [
            {"word": "first", "start": 1.20, "end": 1.40},
            {"word": "second", "start": 1.00, "end": 1.30},
        ]}
        with self.assertRaises(ValueError):
            editor.get_audio_words(transcript)

    def test_exact_asr_word_onsets_are_preserved(self):
        words = editor.get_audio_words(self.raw)
        ass, groups = editor.render_ass(words, 12.0, 3.0, [(1.0, 2.6)])
        self.assertEqual([round(w["start"], 2)
            for group in groups for w in group["words"]],
            [0.20, 0.63, 1.20, 1.72, 1.93])
        # 'only' starts at 1.20 in the video, not an estimated evenly spaced time.
        self.assertIn("Dialogue: 20,0:00:01.20", ass)
        self.assertIn("Dialogue: 20,0:00:00.20", ass)
        self.assertIn("Dialogue: 20,0:00:01.93", ass)
        self.assertNotIn("The version nobody heard", ass)

    def test_paper_card_switches_only_on_stated_source_time(self):
        words = editor.get_audio_words(self.raw)
        groups = editor.group_words(words, 12.0, 3.0, [(1.0, 2.6)])
        self.assertEqual(groups[0]["paper"], False)
        self.assertTrue(any(g["paper"] for g in groups[1:]))
        ass, _ = editor.render_ass(words, 12.0, 3.0, [(1.0, 2.6)])
        self.assertIn("0:00:01.00,0:00:02.60,Paper", ass)

    def test_no_speech_in_clip_is_rejected(self):
        with self.assertRaises(ValueError):
            editor.group_words(editor.get_audio_words(self.raw), 60.0, 3.0, [])

    def test_window_bounds_and_crop_sequence(self):
        self.assertEqual(editor.parse_windows(["13:14"], 12, 3), [(1.0, 2.0)])
        with self.assertRaises(ValueError):
            editor.parse_windows(["12:15", "14:15"], 12, 3)
        expr = editor.parse_crop_switches(["13:1770", "14:800"], 12, 3, 800)
        self.assertIn("gte(n\\,30)", expr)
        self.assertIn("gte(n\\,60)", expr)
        with self.assertRaises(ValueError):
            editor.parse_crop_switches(["11.9:800"], 12, 3, 800)

    def test_no_manual_interpolation_from_phrase_length(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("phrase_window", source)
        self.assertNotIn("duration / len(words)", source)
        self.assertIn("timestamp_granularities", Path(__file__).resolve().parents[1].joinpath(
            "scripts/groq_transcribe.py").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
