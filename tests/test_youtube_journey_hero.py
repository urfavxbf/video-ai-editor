"""Reusable protagonist contract tests, including actual WAV timing and asset identity."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import wave
import zlib

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import prepare_hero_stage as hero
from validate_youtube_journey_fullbody import DEFAULT_ASSETS, OFFICIAL_V2_SHA256


def write_fixture_png(path:Path) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    def chunk(tag:bytes,data:bytes)->bytes:
        return struct.pack(">I",len(data))+tag+data+struct.pack(">I",zlib.crc32(tag+data)&0xffffffff)
    w,h=128,192
    pixels=(b"\x00"+b"\xff\xc0\x20\xff"*w)*h
    path.write_bytes(b"\x89PNG\r\n\x1a\n"+
                     chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+
                     chunk(b"IDAT",zlib.compress(pixels))+
                     chunk(b"IEND",b""))


def write_fixture_wav(path:Path,duration:float):
    path.parent.mkdir(parents=True,exist_ok=True)
    rate=24000
    # A modest real non-silent PCM16 fixture (never a production voice).
    with wave.open(str(path),"wb") as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate)
        frames=round(duration*rate)
        wav.writeframes(b"".join(struct.pack("<h", int(2800*(__import__('math').sin(i*0.09))))
                                  for i in range(frames)))


class HeroIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=json.loads((ROOT/"characters/registry.json").read_text())

    def test_official_v2_identity_is_one_shared_source_of_truth(self):
        self.assertEqual(self.registry["default_video"]["character_layout"],
                         "super-pixel-v2-full-body-animated")
        self.assertEqual(self.registry["character_hero_system"]["protagonists"],
                         ["urfavxbf","pix"])
        self.assertEqual(set(OFFICIAL_V2_SHA256),{"urfavxbf","pix"})
        typescript=(ROOT/"src/characters/HeroPerformance.ts").read_text()
        for name in ("urfavxbf","pix"):
            manifest_path=self.registry["visual_variant_package"]["characters"][name]["base_path"]
            self.assertEqual(manifest_path, "public/"+DEFAULT_ASSETS[name]["assetPath"])
            self.assertIn(OFFICIAL_V2_SHA256[name],typescript)
            self.assertIn(DEFAULT_ASSETS[name]["assetPath"],typescript)

    def test_missing_or_wrong_art_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            with self.assertRaisesRegex(ValueError,"Missing approved V2 PNG"):
                hero.prepare(root/"not-there.png",root/"not-there2.png",
                             root/"host.wav",root/"pix.wav",root/"public")
            a=root/"a.png";b=root/"b.png"
            write_fixture_png(a);write_fixture_png(b)
            with self.assertRaisesRegex(ValueError,"SHA-256 mismatch"):
                hero.prepare(a,b,root/"host.wav",root/"pix.wav",root/"public")

    def test_two_validated_sources_produce_real_speaker_timeline(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            a=root/"host.png";b=root/"pix.png"
            write_fixture_png(a);write_fixture_png(b)
            host=root/"host.wav";pix=root/"pix.wav"
            write_fixture_wav(host,0.5);write_fixture_wav(pix,0.8)
            fixture_sha=hashlib.sha256(a.read_bytes()).hexdigest()
            # Tests ONLY: substitute both reference fingerprints with fixtures.
            # Production pins always stay the official V2 hashes.
            with patch.dict(OFFICIAL_V2_SHA256,{"urfavxbf":fixture_sha,"pix":fixture_sha}):
                manifest=hero.prepare(a,b,host,pix,root/"public",2,20,require_rig=False)
            self.assertEqual([e["speaker"] for e in manifest["voiceEvents"]],
                             ["urfavxbf","pix"])
            self.assertEqual([e["startFrame"] for e in manifest["voiceEvents"]],[2,20])
            self.assertEqual([e["endFrame"] for e in manifest["voiceEvents"]],[17,44])
            self.assertTrue(all(e["rms"] for e in manifest["voiceEvents"]))
            self.assertEqual(manifest["durationFrames"],84)
            self.assertTrue(manifest["assetsReady"])
            self.assertEqual(manifest["projectStatus"],"character-motion-review-only")
            self.assertEqual(manifest["assets"],hero.DEFAULT_ASSETS)
            for name in ("urfavxbf","pix"):
                self.assertTrue((root/"public"/DEFAULT_ASSETS[name]["assetPath"]).exists())

    def test_overlapping_speech_requires_a_real_edit(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            a=root/"host.png";b=root/"pix.png"
            write_fixture_png(a);write_fixture_png(b)
            h=root/"host.wav";p=root/"pix.wav"
            write_fixture_wav(h,1.0);write_fixture_wav(p,0.5)
            fake=hashlib.sha256(a.read_bytes()).hexdigest()
            with patch.dict(OFFICIAL_V2_SHA256,{"urfavxbf":fake,"pix":fake}):
                with self.assertRaisesRegex(ValueError,"Voices overlap"):
                    hero.prepare(a,b,h,p,root/"public",2,10,require_rig=False)


if __name__=="__main__":unittest.main()
