"""Chatterbox adapter tests: no model download, network, Torch, or GPU needed."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "chatterbox_voiceover.py"
sys.path.insert(0, str(MODULE_PATH.parent))  # Resolve shared narrator configuration.
SPEC = importlib.util.spec_from_file_location("chatterbox_voiceover", MODULE_PATH)
voiceover = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(voiceover)


class ChatterboxVoiceoverTests(unittest.TestCase):
    def args(self, *options):
        return voiceover.build_parser().parse_args([
            "--text", "Hello, this is a voice-over.",
            "--output", "out/voiceovers/test.wav", *options
        ])

    def test_normalizes_narration(self):
        text, destination = voiceover.validate_request(self.args(
            "--text", " Hello,\n  world!  "
        ))
        self.assertEqual(text, "Hello, world!")
        self.assertEqual(destination.suffix, ".wav")

    def test_unsupported_tagalog_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.args("--language-id", "tl")

    def test_blank_and_long_scripts_fail(self):
        with self.assertRaisesRegex(ValueError, "contain text"):
            voiceover.validate_request(self.args("--text", "  "))
        with self.assertRaisesRegex(ValueError, "Split longer"):
            voiceover.validate_request(
                self.args("--text", "a" * (voiceover.MAX_TEXT_LENGTH + 1))
            )

    def test_invalid_controls_and_missing_reference_fail(self):
        with self.assertRaisesRegex(ValueError, "exaggeration"):
            voiceover.validate_request(self.args("--exaggeration", "1.5"))
        with self.assertRaisesRegex(ValueError, "Reference audio"):
            voiceover.validate_request(
                self.args("--voice-reference", "/missing/reference.wav")
            )
        with self.assertRaisesRegex(ValueError, "wav"):
            voiceover.validate_request(
                self.args("--output", "output.mp3")
            )

    def test_overwrite_protection_and_utf8_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / "narration.txt"
            output = root / "narration.wav"
            script.write_text("Kumusta, mundo!", encoding="utf-8")
            parsed = voiceover.build_parser().parse_args([
                "--text-file", str(script), "--output", str(output),
                "--language-id", "ms"
            ])
            self.assertEqual(
                voiceover.validate_request(parsed)[0], "Kumusta, mundo!"
            )
            output.write_bytes(b"dummy")
            with self.assertRaisesRegex(ValueError, "already exists"):
                voiceover.validate_request(parsed)
            parsed.overwrite = True
            voiceover.validate_request(parsed)

    def test_generate_with_mocked_model(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output.wav"
            audio_reference = Path(directory) / "reference.wav"
            audio_reference.write_bytes(b"fixture")
            calls = {}

            class Wave:
                def detach(self):
                    return self

                def cpu(self):
                    return self

            class Model:
                sr = 24000

                @classmethod
                def from_pretrained(cls, device: str, t3_model: str | None = None):
                    calls["load"] = {"device": device, "t3_model": t3_model}
                    return cls()

                def generate(self, narration, **kwargs):
                    calls["generation"] = (narration, kwargs)
                    return Wave()

            torch = types.ModuleType("torch")
            torch.cuda = types.SimpleNamespace(is_available=lambda: False)
            torch.backends = types.SimpleNamespace(
                mps=types.SimpleNamespace(is_available=lambda: False)
            )
            torchaudio = types.ModuleType("torchaudio")

            def fake_save(path, tensor, rate, **kwargs):
                calls["encoding"] = kwargs.get("encoding")
                calls["bits"] = kwargs.get("bits_per_sample")
                calls["save_rate"] = rate
                Path(path).write_bytes(b"RIFF" + b"\0" * 60)

            torchaudio.save = fake_save
            chatterbox = types.ModuleType("chatterbox")
            chatterbox.__path__ = []
            multilingual = types.ModuleType("chatterbox.mtl_tts")
            multilingual.ChatterboxMultilingualTTS = Model

            with patch.dict(sys.modules, {
                "torch": torch,
                "torchaudio": torchaudio,
                "chatterbox": chatterbox,
                "chatterbox.mtl_tts": multilingual,
            }):
                result = voiceover.generate(voiceover.build_parser().parse_args([
                    "--text", "Hello, world!",
                    "--output", str(output),
                    "--voice-reference", str(audio_reference),
                    "--language-id", "en",
                ]))
            self.assertEqual(result, output)
            self.assertTrue(output.is_file())
            self.assertEqual(calls["load"], {"device": "cpu", "t3_model": "v3"})
            self.assertEqual(calls["save_rate"], 24000)
            self.assertEqual(calls["encoding"], "PCM_S")
            self.assertEqual(calls["bits"], 16)
            self.assertEqual(
                calls["generation"][1]["audio_prompt_path"],
                str(audio_reference)
            )
            self.assertEqual(calls["generation"][1]["language_id"], "en")
            self.assertEqual(list(output.parent.glob(".chatterbox-*.wav")), [])


if __name__ == "__main__":
    unittest.main()
