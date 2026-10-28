"""Lock the October 2026 approved Chatterbox V3 built-in narrator defaults."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from chatterbox_voice_profile import DEFAULT_NARRATOR  # noqa: E402
from chatterbox_voiceover import build_parser as short_parser  # noqa: E402
from chatterbox_longform import build_parser as long_parser  # noqa: E402


class DefaultNarratorTests(unittest.TestCase):
    def test_approved_sample_identity_and_voice_settings(self):
        self.assertEqual(DEFAULT_NARRATOR.identifier, "natural-storyteller-v1")
        self.assertEqual(DEFAULT_NARRATOR.source, "chatterbox-v3-builtin")
        self.assertEqual(DEFAULT_NARRATOR.checkpoint, "v3")
        self.assertEqual(DEFAULT_NARRATOR.language, "en")
        self.assertEqual(DEFAULT_NARRATOR.exaggeration, 0.5)
        self.assertEqual(DEFAULT_NARRATOR.cfg_weight, 0.5)

    def test_shortform_defaults_match_approved_voice(self):
        args = short_parser().parse_args([
            "--text", "The Moon vanished tonight.",
            "--output", "out/test.wav",
        ])
        self.assertEqual(args.language_id, DEFAULT_NARRATOR.language)
        self.assertIsNone(args.voice_reference)
        self.assertEqual(args.exaggeration, DEFAULT_NARRATOR.exaggeration)
        self.assertEqual(args.cfg_weight, DEFAULT_NARRATOR.cfg_weight)

    def test_longform_defaults_match_approved_voice(self):
        args = long_parser().parse_args([
            "--text-file", "input/narration.txt",
            "--output", "out/test.wav",
        ])
        self.assertEqual(args.language_id, DEFAULT_NARRATOR.language)
        self.assertIsNone(args.voice_reference)
        self.assertEqual(args.exaggeration, DEFAULT_NARRATOR.exaggeration)
        self.assertEqual(args.cfg_weight, DEFAULT_NARRATOR.cfg_weight)


if __name__ == "__main__":
    unittest.main()
