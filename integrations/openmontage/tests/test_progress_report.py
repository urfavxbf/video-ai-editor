"""Read-only recovery report contract tests; no third-party runtime required."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "report_progress.py"
spec = importlib.util.spec_from_file_location("report_progress", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RecoveryReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = self.root / "outer-space-mysteries"
        self.project.mkdir()
        (self.project / "project.json").write_text('{"title":"secret subject"}', encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_reports_only_stage_status_not_script_or_secret(self):
        (self.project / "checkpoint_scene_plan.json").write_text(
            json.dumps({"status": "completed", "artifacts": {
                "scene_plan": {"script": "PRIVATE NARRATION", "key": "TOP_SECRET_API_KEY"}
            }}), encoding="utf-8"
        )
        (self.project / "checkpoint_assets.json").write_text(
            json.dumps({"status": "awaiting_human", "metadata": {
                "media_url": "https://private.invalid/secret"
            }}), encoding="utf-8"
        )
        result = module.report(self.root)
        payload = json.dumps(result)
        self.assertEqual(result["projects"][0]["checkpoints"],
                         {"assets": "awaiting_human", "scene_plan": "completed"})
        self.assertNotIn("TOP_SECRET_API_KEY", payload)
        self.assertNotIn("PRIVATE NARRATION", payload)
        self.assertNotIn("private.invalid", payload)
        self.assertNotIn("secret subject", payload)

    def test_unreadable_checkpoint_is_not_exposed(self):
        (self.project / "checkpoint_assets.json").write_text("{ bad json")
        self.assertEqual(module.report(self.root)["projects"][0]["checkpoints"]["assets"], "invalid")

    def test_unknown_checkpoint_status_is_not_trusted(self):
        (self.project / "checkpoint_assets.json").write_text('{"status":"secret text"}')
        self.assertEqual(module.report(self.root)["projects"][0]["checkpoints"]["assets"], "unknown")

    def test_no_projects_has_clear_status(self):
        result = module.report(self.root / "absent")
        self.assertEqual(result["projects"], [])
        self.assertTrue(result["not_found"])

    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            module.report(self.root, "../private")

    def test_skips_symlinked_projects(self):
        (self.root / "fake").symlink_to(self.project, target_is_directory=True)
        result = module.report(self.root)
        self.assertEqual([p["project_id"] for p in result["projects"]],
                         ["outer-space-mysteries"])

    def test_reports_missing_final_mp4(self):
        self.assertFalse(module.report(self.root)["projects"][0]["final_render"]["present"])

    def test_does_not_inspect_non_final_files(self):
        renders = self.project / "renders"
        renders.mkdir()
        (renders / "preview.mp4").write_bytes(b"not an mp4")
        self.assertFalse(module.report(self.root)["projects"][0]["final_render"]["present"])


if __name__ == "__main__":
    unittest.main()
