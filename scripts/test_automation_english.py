#!/usr/bin/env python3
"""Dependency-free tests; no fake narration is used in the finished MP4."""
import json
import sys
import tempfile
import unittest
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from generate_automation_english import DEFAULT_SCRIPT,load_cues,wav_duration
from package_automation_english import package

class AutomationEnglishTests(unittest.TestCase):
    def test_script_has_correct_approved_english_voices(self):
        doc=json.loads(DEFAULT_SCRIPT.read_text(encoding="utf-8"))
        self.assertEqual(doc["language"],"en")
        self.assertEqual(doc["voiceEngine"],"Chatterbox Multilingual V3")
        self.assertEqual(doc["voices"],{
            "urfavxbf":"natural-storyteller-v1",
            "pix":"pix-cute-female-emily-v1",
        })
        cues=load_cues(DEFAULT_SCRIPT)
        self.assertGreaterEqual(len(cues),30)
        self.assertEqual({c["speaker"] for c in cues},{"urfavxbf","pix"})
        self.assertGreater(sum(len(c["text"].split()) for c in cues),900)
        self.assertTrue(any("2027" in c["stat"] for c in cues))
        self.assertTrue(any("two hundred dollars" in c["text"] for c in cues))

    def test_existing_english_character_defaults_preserved(self):
        from character_voiceover import default_language
        from chatterbox_voice_profile import DEFAULT_NARRATOR
        from pix_voice_profile import DEFAULT_PIX
        self.assertEqual(default_language(),"en")
        self.assertEqual(DEFAULT_NARRATOR.identifier,"natural-storyteller-v1")
        self.assertEqual(DEFAULT_PIX.identifier,"pix-cute-female-emily-v1")
        self.assertEqual(DEFAULT_NARRATOR.language,"en")
        self.assertEqual(DEFAULT_PIX.language,"en")

    def test_missing_real_voice_files_are_hard_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            with self.assertRaises(FileNotFoundError):
                package(DEFAULT_SCRIPT,root/"voices",root/"public",root/"props.json")

    def test_real_wav_duration_creates_clip_level_timeline(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            voices=root/"voices"
            voices.mkdir()
            for i,_ in enumerate(load_cues(DEFAULT_SCRIPT)):
                path=voices/f"{i:02d}.wav"
                with wave.open(str(path),"wb") as w:
                    w.setnchannels(1)
                    w.setsampwidth(2)
                    w.setframerate(16000)
                    w.writeframes(bytes(16000))
                self.assertAlmostEqual(wav_duration(path),0.5)
            props=package(DEFAULT_SCRIPT,voices,root/"public",root/"props.json")
            self.assertEqual(props["audioEngine"],"Chatterbox Multilingual V3")
            self.assertEqual(len(props["voiceClips"]),len(load_cues(DEFAULT_SCRIPT)))
            self.assertEqual(len(props["voiceEvents"]),len(load_cues(DEFAULT_SCRIPT)))
            self.assertEqual(props["captionAlignment"],"cue-level")
            self.assertGreater(props["totalFrames"],len(load_cues(DEFAULT_SCRIPT))*15)
            self.assertTrue(all((root/"public"/c["path"]).is_file() for c in props["voiceClips"]))

if __name__=="__main__":
    unittest.main()
