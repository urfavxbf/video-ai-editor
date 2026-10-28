"""Model-free tests for eight-beat visual outline and 68-turn voice timeline."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_youtube_journey_full import assemble_full
from test_youtube_journey_preview import wav_fixture

EPISODE = ROOT / "productions/youtube-beginner-journey"


class FullVisualEpisodeTests(unittest.TestCase):
    def test_storyboard_has_exact_user_timing_and_complete_script_coverage(self):
        b = json.loads((EPISODE / "visual-aid.json").read_text())["beats"]
        self.assertEqual(
            [(x["startSeconds"], x["endSeconds"]) for x in b],
            [(0,40),(40,130),(130,230),(230,310),
             (310,430),(430,520),(520,600),(600,690)]
        )
        self.assertEqual([n for x in b for n in x["scenes"]], list(range(1, 10)))
        self.assertTrue(all(x["visual"] for x in b))

    def test_all_68_real_wavs_drive_full_episode_timing(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            source = json.loads((EPISODE / "dialogue.json").read_text())
            audio = work / "wavs"
            for line in source["lines"]:
                wav_fixture(audio / line["speaker"] / (line["id"] + ".wav"),
                            seconds=0.85 if line["speaker"] == "pix" else 1.4)
            result = assemble_full(EPISODE / "dialogue.json",
                                   EPISODE / "visual-aid.json",
                                   audio, work / "public")
            self.assertEqual(len(result["lines"]), 68)
            self.assertEqual(len(result["voiceEvents"]), 68)
            self.assertEqual(len(result["chapters"]), 9)
            self.assertEqual([c["beat"] for c in result["chapters"]],
                             [1,2,3,4,5,6,7,8,8])
            self.assertFalse(result["assetsReady"])
            self.assertFalse(result["readyForPublishing"])
            self.assertEqual(result["captionTiming"], "estimated-unreviewed")
            self.assertEqual(result["storyboardDurationSeconds"], 690)
            self.assertNotEqual(result["durationSeconds"], 690)
            self.assertEqual(result["lines"][0]["startFrame"], 0)
            self.assertEqual(result["lines"][-1]["scene"], 9)
            self.assertEqual(result["chapters"][0]["driftSeconds"], 0)
            for line, event in zip(result["lines"], result["voiceEvents"]):
                self.assertEqual(line["startFrame"], event["startFrame"])
                self.assertEqual(line["endFrame"], event["endFrame"])
                self.assertTrue((work / "public" / line["file"]).is_file())

    def test_missing_audio_never_generates_fake_timeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "Missing regular WAV"):
                assemble_full(EPISODE / "dialogue.json", EPISODE / "visual-aid.json",
                              root, root / "public")


if __name__ == "__main__":
    unittest.main()
