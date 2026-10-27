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

    def test_separate_repo_audio_requires_existing_wav_and_video(self):
        with tempfile.TemporaryDirectory() as directory:
            wav = Path(directory) / "narration.wav"
            wav.write_bytes(b"RIFF")
            video = Path(directory) / "video.mp4"
            video.write_bytes(b"test video")
            output = Path(directory) / "voiced.mp4"
            args = voice.create_parser().parse_args([
                "--audio-file", str(wav), "--video", str(video),
                "--video-output", str(output),
            ])
            self.assertEqual(voice.validate_args(args), output)
            with self.assertRaisesRegex(ValueError, "requires --video"):
                voice.validate_args(voice.create_parser().parse_args([
                    "--audio-file", str(wav),
                ]))
            with self.assertRaisesRegex(ValueError, "existing WAV"):
                voice.validate_args(voice.create_parser().parse_args([
                    "--audio-file", str(Path(directory) / "missing.wav"),
                    "--video", str(video),
                ]))

    def test_separate_repo_audio_cannot_overwrite_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            wav = Path(directory) / "narration.wav"
            wav.write_bytes(b"RIFF")
            video = Path(directory) / "video.mp4"
            video.write_bytes(b"test video")
            for target in [wav, video]:
                with self.assertRaisesRegex(ValueError, "overwrite an input"):
                    voice.validate_args(voice.create_parser().parse_args([
                        "--audio-file", str(wav),
                        "--video", str(video),
                        "--video-output", str(target),
                        "--overwrite",
                    ]))

    def test_separate_repo_audio_skips_model_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            wav = Path(directory) / "narration.wav"
            wav.write_bytes(b"RIFF")
            video = Path(directory) / "clip.mp4"
            video.write_bytes(b"dummy mp4")
            output = Path(directory) / "voiced.mp4"
            with patch.object(voice, "synthesize", side_effect=AssertionError("TTS imported")):
                with patch.object(voice, "mux_video") as mux:
                    code = voice.main([
                        "--audio-file", str(wav), "--video", str(video),
                        "--video-output", str(output),
                    ])
            self.assertEqual(code, 0)
            mux.assert_called_once_with(video, wav, output, 0.22)

    def test_help_does_not_import_voxcpm(self):
        with self.assertRaises(SystemExit) as exit_:
            voice.main(["--help"])
        self.assertEqual(exit_.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
