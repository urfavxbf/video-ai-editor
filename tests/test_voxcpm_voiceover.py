"""Unit tests for the optional VoxCPM2 adapter; no GPU, model, or network needed."""
import argparse
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import voxcpm_voiceover as voice


class VoiceoverTests(unittest.TestCase):
    def args(self, *cli):
        return voice.create_parser().parse_args(["--text", "Kamusta, Pilipinas!", *cli])

    def test_tagalog_script_passes_unchanged(self):
        self.assertEqual(voice.prepare_text(self.args()), "Kamusta, Pilipinas!")

    def test_designed_voice_instruction(self):
        args = self.args("--style", "Warm Filipino female narrator")
        self.assertEqual(voice.prepare_text(args), "(Warm Filipino female narrator)Kamusta, Pilipinas!")

    def test_script_file(self):
        with tempfile.TemporaryDirectory() as directory:
            text = Path(directory) / "voice.txt"
            text.write_text("  Ano ang nangyari? \n", encoding="utf-8")
            args = voice.create_parser().parse_args(["--text-file", str(text)])
            self.assertEqual(voice.prepare_text(args), "Ano ang nangyari?")

    def test_empty_script_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            voice.prepare_text(voice.create_parser().parse_args(["--text", "   "]))

    def test_clone_requires_rights(self):
        with tempfile.TemporaryDirectory() as directory:
            clip = Path(directory) / "voice.wav"
            clip.write_bytes(b"RIFF")
            with self.assertRaisesRegex(ValueError, "consent"):
                voice.validate_args(self.args("--reference-audio", str(clip),
                                               "--output", str(Path(directory) / "out.wav")))
            validated = self.args("--reference-audio", str(clip), "--confirm-rights",
                                  "--output", str(Path(directory) / "out.wav"))
            self.assertIsNone(voice.validate_args(validated))

    def test_prompt_requires_transcript(self):
        with self.assertRaisesRegex(ValueError, "together"):
            voice.validate_args(self.args("--prompt-text", "reference transcript"))

    def test_non_destructive_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exists.wav"
            output.write_bytes(b"recording")
            with self.assertRaises(FileExistsError):
                voice.validate_args(self.args("--output", str(output)))

    def test_mux_preserves_video_and_ducks_audio(self):
        command = voice.build_mux_command(
            Path("clip.mp4"), Path("tts.wav"), Path("out.mp4"), 0.22, True
        )
        self.assertIn("copy", command)
        self.assertIn("0:v:0", command)
        graph = command[command.index("-filter_complex") + 1]
        self.assertIn("volume=0.22", graph)
        self.assertIn("amix", graph)
        self.assertIn("apad", graph)

    def test_silent_video_adds_audio(self):
        command = voice.build_mux_command(
            Path("clip.mp4"), Path("tts.wav"), Path("out.mp4"), 0.0, False
        )
        self.assertIn("[1:a:0]apad[aout]", command)

    def test_help_does_not_import_voxcpm(self):
        with self.assertRaises(SystemExit) as exit_:
            voice.main(["--help"])
        self.assertEqual(exit_.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
