"""Long-form text splitting tests that require no model, GPU or network."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from chatterbox_longform import split_script, build_parser, validate  # noqa: E402


class LongformTests(unittest.TestCase):
    def test_sentence_aware_chunks_round_trip(self):
        script = ("The Moon is gone. Yet the ocean continues. " * 30).strip()
        chunks = split_script(script, 170)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(c) <= 170 for c in chunks))
        self.assertEqual(" ".join(chunks), script)
        self.assertTrue(all(chunk[-1] in ".!?" for chunk in chunks[:-1]))

    def test_long_sentence_falls_back_to_words(self):
        source = " ".join(["gravitation"] * 50)
        chunks = split_script(source, 100)
        self.assertEqual(" ".join(chunks), source)
        self.assertTrue(all(len(c) <= 100 for c in chunks))

    def test_rejects_empty_and_unbreakable_input(self):
        with self.assertRaisesRegex(ValueError, "empty"):
            split_script("   ")
        with self.assertRaisesRegex(ValueError, "Word exceeds"):
            split_script("x" * 701, max_chars=200)

    def test_checks_output_safety_and_missing_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "script.txt"
            source.write_text("What if the Moon disappeared tonight?", encoding="utf-8")
            output = root / "narration.wav"
            args = build_parser().parse_args([
                "--text-file", str(source), "--output", str(output)
            ])
            self.assertEqual(validate(args), [source.read_text()])
            output.write_bytes(b"existing")
            with self.assertRaisesRegex(ValueError, "Output exists"):
                validate(args)
            args.overwrite = True
            validate(args)
            args.pause_ms = 4000
            with self.assertRaisesRegex(ValueError, "pause-ms"):
                validate(args)
            args.pause_ms = 200
            args.voice_reference = root / "not-owned.wav"
            with self.assertRaisesRegex(ValueError, "reference"):
                validate(args)


if __name__ == "__main__":
    unittest.main()
