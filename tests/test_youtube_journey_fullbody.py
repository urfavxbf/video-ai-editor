"""Offline asset-gate tests; never substitute character images."""
from __future__ import annotations

import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_youtube_journey_fullbody import (
    DEFAULT_ASSETS, authorize_props, check_png, safe_path, validate_assets,
)


def write_png(path: Path, width: int = 128, height: int = 160) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
    pixels = (b"\x00" + (b"\xff\xaa\x00\xff" * width)) * height
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n" +
        chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) +
        chunk(b"IDAT", zlib.compress(pixels)) +
        chunk(b"IEND", b"")
    )


class FullBodyAssetTests(unittest.TestCase):
    def test_missing_images_do_not_authorize_render(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, "Missing or empty"):
                authorize_props(Path(d), {"lines": [{"id": "YT-001"}]})

    def test_flat_sprites_enable_whole_body_motion_not_false_limb_rig(self):
        with tempfile.TemporaryDirectory() as d:
            public = Path(d)
            for a in DEFAULT_ASSETS.values():
                write_png(public / a["assetPath"])
            modes = validate_assets(public, DEFAULT_ASSETS)
            self.assertEqual(modes, {
                "urfavxbf": "single-sprite-whole-body",
                "pix": "single-sprite-whole-body",
            })
            result = authorize_props(public, {
                "lines": [{"id": "YT-001"}],
                "captionTiming": "estimated-unreviewed",
                "readyForPublishing": False,
            })
            self.assertTrue(result["assetsReady"])
            self.assertEqual(result["captionTiming"], "estimated-unreviewed")
            self.assertFalse(result["readyForPublishing"])

    def test_layered_rig_needs_six_aligned_transparent_pngs(self):
        with tempfile.TemporaryDirectory() as d:
            public = Path(d)
            for a in DEFAULT_ASSETS.values():
                write_png(public / a["assetPath"])
            rig = {
                p: f"characters/rigs/pix/{p}.png" for p in (
                    "body", "head", "leftArm", "rightArm", "leftLeg", "rightLeg")
            }
            assets = json.loads(json.dumps(DEFAULT_ASSETS))
            assets["pix"]["layeredRig"] = rig
            for n in rig.values():
                write_png(public / n)
            self.assertEqual(
                validate_assets(public, assets)["pix"],
                "independently-articulated-limbs",
            )
            write_png(public / rig["leftArm"], width=144)
            with self.assertRaisesRegex(ValueError, "same canvas size"):
                validate_assets(public, assets)

    def test_assets_must_be_under_characters_and_rgba(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                safe_path(Path(d), "characters/../../outside.png")
            with self.assertRaisesRegex(ValueError, "under characters"):
                safe_path(Path(d), "other/PIX.png")


if __name__ == "__main__":
    unittest.main()
