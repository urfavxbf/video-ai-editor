"""English production default, explicit optional Tagalog and verified speaker profiles."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import character_voiceover as voice
from chatterbox_voice_profile import DEFAULT_NARRATOR
from pix_voice_profile import DEFAULT_PIX


class CharacterVoiceoverTests(unittest.TestCase):
    def test_kitten_voice_plan_needs_no_optional_inference_dependencies(self):
        import json,subprocess
        result=subprocess.run([sys.executable,'-S',str(Path(voice.__file__)),
            '--character','pix','--text','Hello.','--output','out/dry-run.wav','--dry-run'],text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual(json.loads(result.stdout)['voice'],'Kiki')

    def test_default_english_engine_uses_owner_selected_kitten_voices(self):
        import contextlib,io,json
        for who,expected in [('urfavxbf','Jasper'),('pix','Kiki')]:
            args=voice.build_parser().parse_args(['--character',who,'--text','Hello!','--output','out/a.wav'])
            self.assertEqual(args.engine,'kitten')
            output=io.StringIO()
            with contextlib.redirect_stdout(output):
                code=voice.main(['--character',who,'--text','Hello!','--output','out/a.wav','--dry-run'])
            self.assertEqual(code,0)
            self.assertEqual(json.loads(output.getvalue())['voice'],expected)

    def test_new_videos_default_to_current_english_character_voices(self):
        args = voice.build_parser().parse_args([
            "--character", "urfavxbf", "--text", "Alam mo ba?", "--output", "out/a.wav"
        ])
        self.assertEqual(args.language, "en")
        flags = voice.synth_args(args)
        self.assertEqual(flags[flags.index("--language-id")+1], "en")
        self.assertNotIn("--voice-reference", flags)

    def test_explicit_tagalog_routes_to_voxcpm_without_speaker_reference(self):
        with patch("voxcpm_voiceover.main", return_value=0) as synth:
            code = voice.main(["--character", "pix", "--language", "tl",
                               "--text", "Hala, seryoso?!",
                               "--output", "out/pix-tl.wav", "--dry-run"])
        self.assertEqual(code, 0)
        self.assertIn("--character", synth.call_args.args[0])
        self.assertIn("pix", synth.call_args.args[0])
        self.assertIn("--dry-run", synth.call_args.args[0])
        self.assertNotIn("--voice-reference", synth.call_args.args[0])

    def test_english_host_narrates_with_original_approved_profile(self):
        a = voice.build_parser().parse_args([
            "--character", "urfavxbf", "--language", "en",
            "--text", "Hi.", "--output", "out/a.wav"
        ])
        flags = voice.synth_args(a)
        self.assertNotIn("--voice-reference", flags)
        self.assertEqual(flags[flags.index("--language-id") + 1], "en")
        self.assertEqual(flags[flags.index("--exaggeration") + 1], str(DEFAULT_NARRATOR.exaggeration))

    def test_english_pix_requires_independent_reference(self):
        a = voice.build_parser().parse_args([
            "--character", "pix", "--language", "en",
            "--text", "Hi.", "--output", "out/b.wav"
        ])
        with self.assertRaisesRegex(ValueError, "requires"):
            voice.synth_args(a)
        flags = voice.synth_args(a, Path("input/pix-reference.wav"))
        self.assertEqual(flags[flags.index("--voice-reference") + 1], "input/pix-reference.wav")
        self.assertEqual(flags[flags.index("--exaggeration") + 1], str(DEFAULT_PIX.exaggeration))
        self.assertNotEqual(DEFAULT_PIX.identifier, DEFAULT_NARRATOR.identifier)

    def test_explicit_legacy_pix_routing_still_requires_reference(self):
        with patch("prepare_pix_reference.prepare", return_value=Path("input/pix-reference.wav")) as prep:
            with patch("chatterbox_voiceover.main", return_value=0) as synth:
                code = voice.main(["--character", "pix", "--language", "en",
                                   "--text", "Hello!", "--output", "out/pix-en.wav", "--engine", "chatterbox"])
        self.assertEqual(code, 0)
        prep.assert_called_once()
        self.assertIn("--voice-reference", synth.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
