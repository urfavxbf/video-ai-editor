#!/usr/bin/env python3
"""Model-free regression tests for bilingual voice routing and real-WAV video integration."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
import wave
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from character_voiceover import default_language, synth_args
from voxcpm_voiceover import profile_for, split_text
from y2038_export_voice_cues import read_cues, write_manifest
from y2038_audio_props import package

from argparse import Namespace


class BilingualVoicesTest(unittest.TestCase):
    def test_english_is_default_without_removing_tagalog_option(self):
        self.assertEqual(default_language(), "en")
        for character in ("urfavxbf", "pix"):
            p = profile_for(character)
            self.assertEqual(p["engine"], "voxcpm2")
            self.assertEqual(p["language"], "tl")
            self.assertEqual(p["model_id"], "openbmb/VoxCPM2")

    def test_original_english_profiles_remain(self):
        from chatterbox_voice_profile import DEFAULT_NARRATOR
        from pix_voice_profile import DEFAULT_PIX
        self.assertEqual(DEFAULT_NARRATOR.identifier, "natural-storyteller-v1")
        self.assertEqual(DEFAULT_NARRATOR.language, "en")
        self.assertEqual(DEFAULT_PIX.identifier, "pix-cute-female-emily-v1")
        self.assertEqual(DEFAULT_PIX.language, "en")
        for speaker in ("urfavxbf", "pix"):
            args = Namespace(language="en", character=speaker, text="Hello!",
                             text_file=None, device="cpu", output=Path("/tmp/en.wav"), overwrite=False)
            options = synth_args(args, Path("/tmp/approved-reference.wav"))
            self.assertIn("--language-id", options)
            self.assertIn("en", options)

    def test_character_voice_text_chunking(self):
        chunks = split_text("Kumusta, PIX? Bakit nagkaroon ng problemang ito?", max_chars=45)
        self.assertGreaterEqual(len(chunks), 1)
        self.assertTrue(all(len(s) <= 45 for s in chunks))
        self.assertIn("PIX?", " ".join(chunks))

    def test_manifest_40_dialogues(self):
        with tempfile.TemporaryDirectory() as td:
            cues = read_cues()
            self.assertEqual(len(cues), 40)
            entries = write_manifest(cues, Path(td))
            self.assertEqual(len(entries), 40)
            manifest = json.loads((Path(td) / "voice_manifest.json").read_text())
            self.assertEqual(manifest["language"], "tl")
            self.assertEqual({c["speaker"] for c in entries}, {"pix", "urfavxbf"})
            self.assertTrue(all(not x["timings_verified"] for x in entries))

    def test_real_pcm16_wav_drives_remotion_cues(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            entries = write_manifest(read_cues(), root)
            with self.assertRaises(FileNotFoundError):
                package(root / "voice_manifest.json", root / "props.json", root / "public")
            for entry in entries:
                wav = root / entry["intended_wav"]
                wav.parent.mkdir(parents=True, exist_ok=True)
                with wave.open(str(wav), "wb") as handle:
                    handle.setnchannels(1)
                    handle.setsampwidth(2)
                    handle.setframerate(16000)
                    handle.writeframes(bytes(16000))
            props = package(root / "voice_manifest.json", root / "props.json", root / "public")
            self.assertEqual(props["audioLanguage"], "tl")
            self.assertEqual(props["captionAlignment"], "cue_level_only")
            self.assertEqual(len(props["voiceClips"]), 40)
            self.assertEqual(len(props["voiceEvents"]), 40)
            self.assertTrue(all(e["rms"] for e in props["voiceEvents"]))
            self.assertTrue(all(e["endFrame"] > e["startFrame"] for e in props["voiceEvents"]))
            self.assertGreater(props["totalFrames"], 40 * 15)
            for item in props["voiceClips"]:
                self.assertTrue((root / "public" / item["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
