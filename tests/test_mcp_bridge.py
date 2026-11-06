"""Offline safety and behavior tests. The MCP SDK is intentionally not required."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from mcp_server import bridge


class BridgeTests(unittest.TestCase):
    def test_project_status_reads_approved_registry(self):
        status = bridge.project_status()
        self.assertEqual(status["language"], "en")
        self.assertEqual((status["width"], status["height"], status["fps"]), (1920, 1080, 30))
        self.assertEqual(status["approved_pose_count"], 13)
        self.assertEqual(status["voices"]["urfavxbf"], "natural-storyteller-v1")
        self.assertEqual(status["voices"]["pix"], "pix-cute-female-emily-v1")
        self.assertIn("Metadata only", status["note"])

    def test_catalog_is_complete_without_duplicate_names(self):
        result = bridge.list_skills()
        self.assertEqual(result["count"], 21)
        names = [item["name"] for item in result["skills"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertIn("video-ai-orchestrator", names)
        self.assertIn("media-source-ingestion", names)

    def test_input_paths_cannot_escape_sandbox(self):
        for path in ("", "/etc/passwd", "../public/abc.mp4", "public/../input/test.mp4",
                     "private/file.mp4", "https://evil.example/movie.mp4", "input\\video.mp4",
                     "input/file.txt", "out/not-existing.mp4", "input/file.mp4\x00"):
            with self.subTest(path=path), self.assertRaises(bridge.BridgeError):
                bridge.local_media_path(path)

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "input").mkdir()
            external = root.parent / ("outside-" + root.name + ".mp4")
            external.write_bytes(b"fake")
            try:
                (root / "input" / "linked.mp4").symlink_to(external)
                with patch.object(bridge, "ROOT", root):
                    with self.assertRaises(bridge.BridgeError):
                        bridge.local_media_path("input/linked.mp4")
            finally:
                external.unlink(missing_ok=True)

    def test_valid_media_path_and_probe_are_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "input").mkdir()
            media = root / "input/test.mp4"
            media.write_bytes(b"fake-media-for-command-contract-only")
            response = subprocess.CompletedProcess(
                args=[], returncode=0,
                stdout=json.dumps({"streams": [{"codec_type": "video", "codec_name": "h264"}],
                                   "format": {"duration": "1.000"}}),
                stderr="",
            )
            with patch.object(bridge, "ROOT", root), \
                 patch.object(bridge.subprocess, "run", return_value=response) as call:
                data = bridge.inspect_media("input/test.mp4")
            self.assertTrue(data["ok"])
            self.assertEqual(data["streams"][0]["codec_name"], "h264")
            argv = call.call_args.args[0]
            self.assertIn("-protocol_whitelist", argv)
            self.assertIn("file", argv)
            self.assertEqual(call.call_args.kwargs["timeout"], 30)
            self.assertIs(call.call_args.kwargs["stdin"], subprocess.DEVNULL)
            self.assertNotIn("shell", call.call_args.kwargs)

    def test_external_keys_are_not_forwarded_to_subprocesses(self):
        with patch.dict(os.environ, {"GROQ_API_KEY": "private", "GITHUB_TOKEN": "private"}):
            env = bridge._environment()
        self.assertNotIn("GROQ_API_KEY", env)
        self.assertNotIn("GITHUB_TOKEN", env)

    def test_existing_script_validation_is_reused(self):
        with patch.object(bridge, "_run", return_value="Valid edit contract: 120 frames") as runner:
            response = bridge.validate_edit(media=True)
        self.assertTrue(response["media_checked"])
        argv = runner.call_args.args[0]
        self.assertIn("scripts/validate-edit.cjs", argv[1])
        self.assertIn("--media", argv)

    def test_render_needs_approval_before_software_invocation(self):
        with patch.object(bridge, "_run") as runner:
            result = bridge.preview_render(confirmed=False)
        self.assertTrue(result["approval_required"])
        runner.assert_not_called()

    def test_online_metadata_requires_approval_before_network(self):
        with patch.object(bridge, "_run") as runner:
            result = bridge.inspect_online_source("https://vimeo.com/123")
        self.assertTrue(result["approval_required"])
        runner.assert_not_called()

    def test_subprocess_failure_is_sanitized(self):
        fake = subprocess.CompletedProcess([], 12, stdout="", stderr="PRIVATE_TOKEN=abc123")
        with patch.object(bridge.subprocess, "run", return_value=fake):
            with self.assertRaises(bridge.BridgeError) as cm:
                bridge._run(["not-a-real-tool"], label="sample", timeout=3)
        self.assertNotIn("PRIVATE_TOKEN", str(cm.exception))
        self.assertIn("exit 12", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
