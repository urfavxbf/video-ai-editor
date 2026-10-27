"""Real FFmpeg integration checks for VoxCPM2 WAV-to-video mixdown (no AI/GPU)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import wave
import math
import struct


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import voxcpm_voiceover as voice


def run(*args: str) -> None:
    subprocess.run(
        list(args), check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=30,
    )


def probe(path: Path) -> dict:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True, timeout=15,
    )
    return json.loads(result.stdout)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg unavailable")
class MediaMuxIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.voice = self.root / "synthetic-narration.wav"
        # This is not AI narration: pure test tone to verify the media plumbing.
        with wave.open(str(self.voice), "wb") as wav:
            rate = 16000
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(rate)
            samples = bytearray()
            for n in range(rate):
                y = int(5000 * math.sin(2 * math.pi * 440 * n / rate))
                samples.extend(struct.pack("<h", y))
            wav.writeframes(bytes(samples))

    def make_video(self, has_audio: bool) -> Path:
        path = self.root / ("with-bed.mp4" if has_audio else "silent.mp4")
        args = [
            "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "color=c=black:s=160x96:r=15:d=2",
        ]
        if has_audio:
            args.extend(["-f", "lavfi", "-i", "sine=frequency=200:sample_rate=16000:duration=2"])
        args.extend(["-map", "0:v:0"])
        if has_audio:
            args.extend(["-map", "1:a:0"])
        args.extend(["-c:v", "mpeg4", "-q:v", "8", "-pix_fmt", "yuv420p", "-t", "2"])
        if has_audio:
            args.extend(["-c:a", "aac", "-b:a", "96k"])
        args.append(str(path))
        run(*args)
        return path

    def check_output(self, output: Path, video: Path):
        streams = probe(output)["streams"]
        self.assertEqual(sum(s["codec_type"] == "video" for s in streams), 1)
        self.assertEqual(sum(s["codec_type"] == "audio" for s in streams), 1)
        self.assertEqual(next(s["codec_name"] for s in streams if s["codec_type"] == "audio"), "aac")
        self.assertEqual(next(s["codec_name"] for s in streams if s["codec_type"] == "video"),
                         next(s["codec_name"] for s in probe(video)["streams"] if s["codec_type"] == "video"))
        self.assertAlmostEqual(float(probe(output)["format"]["duration"]), 2.0, delta=0.15)
        self.assertGreater(output.stat().st_size, 1000)

    def test_add_narration_to_video_without_existing_audio(self):
        video = self.make_video(False)
        original_sha = sha256(video)
        self.assertFalse(voice.contains_audio(video))
        output = self.root / "silent-narrated.mp4"
        voice.mux_video(video, self.voice, output, 0.22)
        self.assertEqual(original_sha, sha256(video), "Source video must be untouched")
        self.check_output(output, video)

    def test_mix_narration_with_existing_audio_bed(self):
        video = self.make_video(True)
        original_sha = sha256(video)
        self.assertTrue(voice.contains_audio(video))
        output = self.root / "mixed.mp4"
        voice.mux_video(video, self.voice, output, 0.22)
        self.assertEqual(original_sha, sha256(video), "Source video must be untouched")
        self.check_output(output, video)

    def test_import_external_voxcpm_wav_through_cli(self):
        video = self.make_video(True)
        original_sha = sha256(video)
        output = self.root / "external-voxcpm.wav-voiced.mp4"
        status = voice.main([
            "--audio-file", str(self.voice),
            "--video", str(video),
            "--video-output", str(output),
            "--original-volume", "0.15",
        ])
        self.assertEqual(status, 0)
        self.assertEqual(original_sha, sha256(video))
        self.check_output(output, video)

    def test_replace_audio_without_mutating_source(self):
        video = self.make_video(True)
        source_hash = sha256(video)
        output = self.root / "replaced.mp4"
        voice.mux_video(video, self.voice, output, 0.0)
        self.assertEqual(source_hash, sha256(video))
        self.check_output(output, video)


if __name__ == "__main__":
    unittest.main()
