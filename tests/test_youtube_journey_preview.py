"""Offline, model-free tests for the YouTube beginner journey preview contract."""
from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
import wave
from array import array

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_youtube_journey_preview import (
    FPS, PREVIEW_SECTIONS, assemble, caption_blocks, inspect_wav, validate_script,
)


def wav_fixture(path: Path, seconds: float = 1.2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rate = 16000
    count = round(seconds * rate)
    samples = array("h", [
        round(8000 * math.sin(i * 2 * math.pi * 220 / rate))
        for i in range(count)
    ])
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(rate)
        out.writeframes(samples.tobytes())


class PreviewTimelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads(
            (ROOT / "productions/youtube-beginner-journey/dialogue.json").read_text(encoding="utf-8")
        )

    def test_script_contract(self):
        lines = validate_script(self.source)
        self.assertEqual(len(lines), 68)
        self.assertEqual(lines["YT-001"]["speaker"], "pix")
        self.assertEqual(lines["YT-002"]["speaker"], "urfavxbf")
        broken = json.loads(json.dumps(self.source))
        broken["lines"][0]["voice_profile"] = "some-other-voice"
        with self.assertRaisesRegex(ValueError, "voice identity"):
            validate_script(broken)

    def test_preview_is_measured_and_speaker_separated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "dialogue.json"
            script.write_text(json.dumps(self.source), encoding="utf-8")
            audio = root / "audio"
            selected = [ident for _, ids in PREVIEW_SECTIONS for ident in ids]
            index = {entry["id"]: entry for entry in self.source["lines"]}
            for ident in selected:
                wav_fixture(audio / index[ident]["speaker"] / f"{ident}.wav")
            result = assemble(script, audio, root / "public")
            self.assertEqual([line["id"] for line in result["lines"]], selected)
            self.assertEqual([s["scene"] for s in result["sections"]], [1, 5, 6])
            self.assertEqual(len(result["voiceEvents"]), len(selected))
            self.assertEqual(result["captionTiming"], "estimated-unreviewed")
            self.assertGreater(result["totalFrames"], len(selected) * 36)
            for line, event in zip(result["lines"], result["voiceEvents"]):
                self.assertEqual(event["startFrame"], line["startFrame"])
                self.assertEqual(event["endFrame"], line["endFrame"])
                self.assertEqual(event["speaker"], line["speaker"])
                self.assertTrue((root / "public" / line["file"]).is_file())
                self.assertEqual(line["captions"][0]["startFrame"], line["startFrame"])
                self.assertEqual(line["captions"][-1]["endFrame"], line["endFrame"])
                self.assertTrue(event["rms"])
            for first, second in zip(result["lines"], result["lines"][1:]):
                self.assertLessEqual(first["endFrame"], second["startFrame"])
            self.assertEqual(result["targetDurationMet"], False)  # deliberately short fixtures

    def test_no_missing_wav_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            script = root / "dialogue.json"
            script.write_text(json.dumps(self.source), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing regular WAV"):
                assemble(script, root / "missing", root / "public")

    def test_caption_chunks_cover_text_without_claiming_word_sync(self):
        text = "A useful video needs a person, a clear promise, and a reason to watch."
        chunks = caption_blocks(text, 13, 101, limit=28)
        self.assertEqual(" ".join(x["text"] for x in chunks), text)
        self.assertEqual(chunks[0]["startFrame"], 13)
        self.assertEqual(chunks[-1]["endFrame"], 101)
        self.assertTrue(all(x["endFrame"] > x["startFrame"] for x in chunks))

    def test_wave_contract_rejects_incomplete_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "silent.wav"
            wav_fixture(path, seconds=0.1)
            with self.assertRaisesRegex(ValueError, "malformed WAV"):
                inspect_wav(path)


if __name__ == "__main__":
    unittest.main()
