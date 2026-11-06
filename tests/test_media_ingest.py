"""Model-free contracts for the optional yt-dlp source ingestion bridge."""
from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("media_ingest", ROOT / "scripts/media_ingest.py")
ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingest)


class MediaIngestTests(unittest.TestCase):
    URL = "https://www.youtube.com/watch?v=example01"

    def test_accept_supported_https_video_pages(self):
        for url in (self.URL, "https://youtu.be/123", "https://vimeo.com/123",
                    "https://archive.org/details/foo",
                    "https://commons.wikimedia.org/wiki/File:Example.webm"):
            with self.subTest(url=url):
                self.assertEqual(ingest.validate_url(url), url)

    def test_reject_untrusted_url_shapes(self):
        bad = ("", "ftp://youtube.com/a", "http://youtu.be/a",
               "https://127.0.0.1/", "https://169.254.169.254/",
               "https://youtube.com.evil.example/a",
               "https://user:pass@www.youtube.com/watch?v=a",
               "https://www.youtube.com:8443/watch?v=a",
               "https://www.youtube.com/watch?v=a#fragment",
               "https://www.youtube.com/watch?v=a\n--exec", "x" * 2049)
        for url in bad:
            with self.subTest(url=url[:80]), self.assertRaises(ValueError):
                ingest.validate_url(url)

    def test_inspection_fixed_flags(self):
        cmd = ingest.command_for("inspect", self.URL, Path("/tmp/dummy"))
        self.assertEqual(cmd[:3], [ingest.sys.executable, "-m", "yt_dlp"])
        for flag in ("--ignore-config", "--no-playlist", "--dump-single-json", "--simulate"):
            self.assertIn(flag, cmd)
        self.assertNotIn("--cookies-from-browser", cmd)
        self.assertEqual(cmd[-1], self.URL)

    def test_download_requires_rights_and_makes_no_request(self):
        with patch.object(ingest.subprocess, "run") as runner:
            with contextlib.redirect_stderr(io.StringIO()):
                code = ingest.main(["download", self.URL])
        self.assertEqual(code, 1)
        runner.assert_not_called()

    def test_inspection_redacts_raw_stream_urls(self):
        raw = ('{"id":"id","title":"My clip","duration":14.5,'
               '"formats":[{"url":"https://secret/?token=private"}],'
               '"description":"secret description"}')
        with patch.object(ingest.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, raw, "")) as runner:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = ingest.main(["inspect", self.URL])
        self.assertEqual(code, 0)
        self.assertIn("My clip", out.getvalue())
        self.assertNotIn("private", out.getvalue())
        self.assertNotIn("secret description", out.getvalue())
        self.assertEqual(runner.call_args.kwargs["timeout"], 90)
        self.assertNotIn("shell", runner.call_args.kwargs)

    def test_playlist_and_large_metadata_rejected(self):
        with self.assertRaises(ValueError):
            ingest.safe_metadata('{"_type":"playlist","entries":[]}')
        with self.assertRaises(ValueError):
            ingest.safe_metadata("x" * (ingest.MAX_METADATA_BYTES + 1))

    def test_download_command_scope_and_subtitles(self):
        with tempfile.TemporaryDirectory() as tmp:
            cmd = ingest.command_for("download", self.URL, Path(tmp), subtitles=True)
            for flag in ("--ignore-config", "--no-playlist", "--max-filesize",
                         "--no-overwrites", "--write-subs", "--restrict-filenames",
                         "--print", "--merge-output-format"):
                self.assertIn(flag, cmd)
            self.assertIn("after_move:filepath", cmd)
            self.assertIn(f"home:{Path(tmp).resolve()}", cmd)
            self.assertEqual(cmd[-1], self.URL)

    def test_accepted_file_is_within_ignored_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "input" / "ingested"
            folder.mkdir(parents=True)
            video = folder / "Youtube_example01.mp4"
            video.write_bytes(b"fake media: path contract only")
            response = subprocess.CompletedProcess([], 0, str(video) + "\n", "")
            with patch.object(ingest, "OUTPUT_DIR", folder), \
                 patch.object(ingest.subprocess, "run", return_value=response):
                with contextlib.redirect_stdout(io.StringIO()):
                    code = ingest.main(["download", self.URL, "--confirm-rights"])
            self.assertEqual(code, 0)
            self.assertEqual(ingest.verified_download(str(video), folder), video.resolve())

    def test_reject_outside_path_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            folder = base / "ingested"
            folder.mkdir()
            outside = base / "outside.mp4"
            outside.write_bytes(b"content")
            with self.assertRaises(ValueError):
                ingest.verified_download(str(outside), folder)
            symlink = folder / "inside.mp4"
            symlink.symlink_to(outside)
            with self.assertRaises(ValueError):
                ingest.verified_download(str(symlink), folder)

    def test_no_private_stderr_leaks_on_remote_failure(self):
        failed = subprocess.CalledProcessError(1, ["yt-dlp"], stderr="auth=secret")
        with patch.object(ingest.subprocess, "run", side_effect=failed):
            out = io.StringIO()
            with contextlib.redirect_stderr(out):
                code = ingest.main(["inspect", self.URL])
        self.assertEqual(code, 1)
        self.assertNotIn("auth=secret", out.getvalue())


if __name__ == "__main__":
    unittest.main()
