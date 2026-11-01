"""CPU-only, model-free regression tests for authorized UrFavXBF voice reference cloning."""
import contextlib
from array import array
import io
import math
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import types
import wave

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import voxcpm_voiceover as tts
import character_voiceover as router


def make_reference(path: Path, seconds: int = 6):
    """Generate a structurally valid WAV fixture (silence is never a voice reference)."""
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(16000)
        samples = array("h", (round(3200 * math.sin(2 * math.pi * 170 * i / 16000)) for i in range(16000 * seconds)))
        handle.writeframes(samples.tobytes())


class AuthorizedTagalogVoiceReferenceTests(unittest.TestCase):
    def test_unchanged_voice_design_has_no_reference(self):
        kwargs = tts.generation_kwargs("Kamusta!", tts.profile_for("urfavxbf"), None, seed=42)
        self.assertNotIn("reference_wav_path", kwargs)
        self.assertIn("young adult Filipino male", kwargs["text"])

    def test_silent_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            wav = Path(folder) / "silent.wav"
            with wave.open(str(wav), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(16000)
                handle.writeframes(b"\x00\x00" * 16000 * 6)
            with self.assertRaisesRegex(ValueError, "silent"):
                tts.validate_reference(wav)

    def test_cloning_uses_exact_local_reference_for_every_chunk(self):
        with tempfile.TemporaryDirectory() as folder:
            wav = Path(folder) / "ref.wav"
            make_reference(wav)
            self.assertEqual(len(tts.validate_reference(wav)), 64)
            a = tts.generation_kwargs("Kumusta ka?", tts.profile_for("urfavxbf"), wav, seed=41)
            b = tts.generation_kwargs("Paano kaya?", tts.profile_for("urfavxbf"), wav, seed=42)
            self.assertEqual(a["reference_wav_path"], str(wav.resolve()))
            self.assertEqual(a["reference_wav_path"], b["reference_wav_path"])
            self.assertIn("Filipino", a["text"])
            self.assertNotIn("reference_wav_path", tts.generation_kwargs("Hi.", tts.profile_for("pix"), None, 1))

    def test_no_unauthorized_reference_cloning(self):
        with tempfile.TemporaryDirectory() as folder:
            wav = Path(folder) / "ref.wav"
            make_reference(wav)
            output = Path(folder) / "out.wav"
            with contextlib.redirect_stderr(io.StringIO()) as logs:
                code = tts.main(["--character", "urfavxbf", "--text", "Kumusta?",
                                 "--reference-audio", str(wav), "--output", str(output), "--dry-run"])
            self.assertEqual(code, 2)
            self.assertIn("rights", logs.getvalue())
            self.assertFalse(output.exists())

    def test_pix_cannot_inherit_urfavxbf_voice(self):
        with tempfile.TemporaryDirectory() as folder:
            wav = Path(folder) / "ref.wav"
            make_reference(wav)
            with contextlib.redirect_stderr(io.StringIO()) as logs:
                code = tts.main(["--character", "pix", "--text", "Hi!",
                                 "--reference-audio", str(wav), "--confirm-voice-rights",
                                 "--output", str(Path(folder) / "out.wav"), "--dry-run"])
            self.assertEqual(code, 2)
            self.assertIn("UrFavXBF", logs.getvalue())

    def test_reference_requires_five_to_thirty_seconds(self):
        with tempfile.TemporaryDirectory() as folder:
            wav = Path(folder) / "short.wav"
            make_reference(wav, seconds=2)
            with self.assertRaisesRegex(ValueError, "5–30 seconds"):
                tts.validate_reference(wav)

    def test_clone_dry_run_is_cpu_only_and_generates_no_audio(self):
        with tempfile.TemporaryDirectory() as folder:
            wav = Path(folder) / "ref.wav"
            make_reference(wav)
            output = Path(folder) / "out.wav"
            with patch.object(tts, "synthesize", side_effect=AssertionError("No model call")):
                with contextlib.redirect_stdout(io.StringIO()) as out:
                    code = tts.main(["--character", "urfavxbf", "--text", "Bakit nga ba?",
                                     "--reference-audio", str(wav), "--confirm-voice-rights",
                                     "--output", str(output), "--dry-run"])
            self.assertEqual(code, 0)
            data = json.loads(out.getvalue())
            self.assertEqual(data["device"], "cpu")
            self.assertEqual(data["voice_mode"], "reference-clone")
            self.assertEqual(len(data["reference_sha256"]), 64)
            self.assertFalse(data["audio_generated"])
            self.assertFalse(output.exists())

    def test_reference_route_writes_wav_and_manifest_with_mock_cpu_model(self):
        import numpy as np

        class FakeModel:
            tts_model = types.SimpleNamespace(sample_rate=16000)

            def generate(self, **kwargs):
                if "reference_wav_path" not in kwargs:
                    raise AssertionError("Reference required for signature voice")
                return np.full(6400, 0.075, dtype=np.float32)

        class FakeVoxCPM:
            @staticmethod
            def from_pretrained(model_id, **options):
                if model_id != "openbmb/VoxCPM2" or options.get("device") != "cpu":
                    raise AssertionError("Wrong model or device")
                if options.get("load_denoiser") is not False:
                    raise AssertionError("Denoiser must be off")
                return FakeModel()

        def fake_write(path, audio, rate, subtype):
            with wave.open(path, "wb") as wav:
                wav.setnchannels(1)
                wav.setframerate(rate)
                wav.setsampwidth(2)
                wav.writeframes(array("h", (round(float(a) * 32767) for a in audio)).tobytes())

        with tempfile.TemporaryDirectory() as folder:
            reference = Path(folder) / "reference.wav"
            output = Path(folder) / "generated.wav"
            make_reference(reference)
            modules = {
                "voxcpm": types.SimpleNamespace(VoxCPM=FakeVoxCPM),
                "soundfile": types.SimpleNamespace(write=fake_write),
            }
            with patch.dict(sys.modules, modules):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = tts.main(["--character", "urfavxbf", "--text", "Magandang gabi.",
                                     "--reference-audio", str(reference), "--confirm-voice-rights",
                                     "--device", "cpu", "--output", str(output)])
            self.assertEqual(code, 0)
            with wave.open(str(output), "rb") as wav:
                self.assertEqual(wav.getframerate(), 16000)
                self.assertGreater(wav.getnframes(), 3000)
            manifest = json.loads(output.with_suffix(".json").read_text())
            self.assertEqual(manifest["voice_mode"], "reference-clone")
            self.assertEqual(manifest["reference_sha256"], tts.validate_reference(reference))
            self.assertNotIn(str(reference), output.with_suffix(".json").read_text())

    def test_router_passes_reference_only_to_tagalog(self):
        with tempfile.TemporaryDirectory() as folder:
            wav = Path(folder) / "ref.wav"
            make_reference(wav)
            with patch("voxcpm_voiceover.main", return_value=0) as synth:
                code = router.main(["--character", "urfavxbf", "--language", "tl",
                                    "--reference-audio", str(wav), "--confirm-voice-rights",
                                    "--text", "Magandang gabi.", "--output", "out/voice.wav", "--dry-run"])
            self.assertEqual(code, 0)
            opts = synth.call_args.args[0]
            self.assertIn("--reference-audio", opts)
            self.assertIn("--confirm-voice-rights", opts)
            with contextlib.redirect_stdout(io.StringIO()):
                code = router.main(["--character", "urfavxbf", "--language", "en",
                                    "--reference-audio", str(wav), "--text", "Hello",
                                    "--output", "out/a.wav"])
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
