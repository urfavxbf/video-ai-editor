"""Static guardrails for human-triggered free render job."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/openmontage-manual-demo.yml"


class ManualAutomationTests(unittest.TestCase):
    def test_only_manual_runs_render_and_permissions_read_only(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("github.event_name == 'workflow_dispatch'", source)
        self.assertIn("permissions:\n  contents: read", source)
        self.assertIn("timeout-minutes: 35", source)
        self.assertNotIn("schedule:", source)
        self.assertNotIn("OPENAI_API_KEY", source)

    def test_demo_is_allowlisted_not_shell_interpolated(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('case "$DEMO_NAME" in', source)
        self.assertIn('bash integrations/openmontage/scripts/demo.sh "$DEMO_NAME"', source)
        self.assertIn("if-no-files-found: error", source)
        self.assertIn("retention-days: 3", source)


if __name__ == "__main__":
    unittest.main()
