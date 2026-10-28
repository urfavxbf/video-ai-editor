"""Both saved characters must route to distinct Chatterbox V3 speaker conditioning."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import character_voiceover as voice
from chatterbox_voice_profile import DEFAULT_NARRATOR
from pix_voice_profile import DEFAULT_PIX


class CharacterVoiceoverTests(unittest.TestCase):
    def test_host_narrates_without_reference(self):
        a = voice.build_parser().parse_args(["--character", "urfavxbf", "--text", "Hi.", "--output", "out/a.wav"])
        flags = voice.synth_args(a)
        self.assertNotIn("--voice-reference", flags)
        self.assertEqual(flags[flags.index("--language-id") + 1], "en")
        self.assertEqual(flags[flags.index("--exaggeration") + 1], str(DEFAULT_NARRATOR.exaggeration))

    def test_pix_requires_female_reference_and_own_settings(self):
        a = voice.build_parser().parse_args(["--character", "pix", "--text", "Hi.", "--output", "out/b.wav"])
        with self.assertRaisesRegex(ValueError, "requires"):
            voice.synth_args(a)
        flags = voice.synth_args(a, Path("input/pix-reference.wav"))
        self.assertEqual(flags[flags.index("--voice-reference") + 1], "input/pix-reference.wav")
        self.assertEqual(flags[flags.index("--exaggeration") + 1], str(DEFAULT_PIX.exaggeration))
        self.assertNotEqual(DEFAULT_PIX.identifier, DEFAULT_NARRATOR.identifier)

    def test_shortform_routing_with_mock_synth(self):
        a = voice.build_parser().parse_args(["--character", "pix", "--text", "Hello!", "--output", "out/pix.wav"])
        from prepare_pix_reference import prepare
        with patch("prepare_pix_reference.prepare", return_value=Path("input/pix-reference.wav")) as prep:
            with patch("chatterbox_voiceover.main", return_value=0) as synth:
                self.assertEqual(voice.main(["--character", "pix", "--text", "Hello!", "--output", "out/pix.wav"]), 0)
                prep.assert_called_once()
                self.assertIn("--voice-reference", synth.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
