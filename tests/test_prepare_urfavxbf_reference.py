"""Offline CPU WAV staging tests. No model download, cloud upload or GPU."""
from array import array
import math
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import wave

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prepare_urfavxbf_reference as staging
from voxcpm_voiceover import validate_reference


@unittest.skipUnless(shutil.which("ffmpeg"), "FFmpeg not installed")
class PrivateReferenceStagingTests(unittest.TestCase):
    def test_real_ffmpeg_converts_private_audio_and_keeps_source_intact(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.wav"
            dest = Path(folder) / "private" / "ref.wav"
            tone = array("h", (round(3100 * math.sin(2 * math.pi * 165 * i / 16000)) for i in range(16000 * 7)))
            with wave.open(str(source), "wb") as out:
                out.setnchannels(1)
                out.setsampwidth(2)
                out.setframerate(16000)
                out.writeframes(tone.tobytes())
            staging.prepare(source, dest, 0.25, 6.0, False)
            self.assertTrue(source.exists())
            with wave.open(str(dest), "rb") as reference:
                self.assertEqual(reference.getframerate(), 16000)
                self.assertEqual(reference.getnchannels(), 1)
                self.assertAlmostEqual(reference.getnframes() / 16000, 6.0, places=1)
            self.assertEqual(len(validate_reference(dest)), 64)
            with self.assertRaisesRegex(ValueError, "exists"):
                staging.prepare(source, dest, 0.25, 6.0, False)

    def test_invalid_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "not found"):
                staging.prepare(Path(folder) / "missing.wav", Path(folder) / "ref.wav", 0, 6, False)


if __name__ == "__main__":
    unittest.main()
