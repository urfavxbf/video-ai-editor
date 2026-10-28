"""Tests for deterministic measured-voice puppet envelopes."""
import importlib.util
import math
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import wave

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "extract_voice_envelope", ROOT / "scripts/extract_voice_envelope.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def wav_file(path, seconds=1.0, sr=16000, amplitude=12000):
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(sr)
        count = int(seconds * sr)
        out.writeframes(b"".join(struct.pack("<h", int(
            amplitude * math.sin(i * 2 * math.pi * 220 / sr)
        )) for i in range(count)))


class VoiceEnvelopeTests(unittest.TestCase):
    def test_measure_real_wav_and_timeline(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "voice.wav"
            wav_file(p, seconds=1.0)
            e = MODULE.voice_event_from_wav(p, "pix", 90, 30, 10)
            self.assertEqual(e["speaker"], "pix")
            self.assertEqual((e["startFrame"], e["endFrame"]), (90, 120))
            self.assertEqual(len(e["rms"]), 10)
            self.assertTrue(all(0 <= v <= 1 for v in e["rms"]))
            self.assertTrue(max(e["rms"]) > 0.9)

    def test_silence_has_zero_envelope(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "silence.wav"
            wav_file(p, seconds=0.5, amplitude=0)
            e = MODULE.voice_event_from_wav(p, "urfavxbf", 20)
            self.assertTrue(all(v == 0 for v in e["rms"]))

    def test_invalid_identity_and_missing_audio_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.voice_event_from_wav(Path("/missing.wav"), "kuri", 0)
        with self.assertRaises(ValueError):
            MODULE.voice_event_from_wav(Path("/missing.wav"), "pix", -1)
        with self.assertRaises(ValueError):
            MODULE.voice_event_from_wav(Path("/missing.wav"), "pix", 0)

if __name__ == "__main__":
    unittest.main()
