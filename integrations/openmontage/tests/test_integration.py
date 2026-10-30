"""Non-network contract tests for the isolated OpenMontage integration."""
import json
import re
import subprocess
import unittest
from pathlib import Path


INTEGRATION = Path(__file__).resolve().parents[1]
REPO = INTEGRATION.parents[1]


class OpenMontageIntegrationTests(unittest.TestCase):
    def test_upstream_revision_is_immutable_sha(self):
        revision = (INTEGRATION / "UPSTREAM_COMMIT").read_text().strip()
        self.assertRegex(revision, r"^[0-9a-f]{40}$")
        self.assertEqual(revision, "195eab24478dc9363326aec437aefc3701635ddf")

    def test_runtime_and_secrets_are_gitignored(self):
        ignored = (INTEGRATION / ".gitignore").read_text().splitlines()
        self.assertIn(".runtime/", ignored)

    def test_separate_codespaces_configuration(self):
        profile_path = REPO / ".devcontainer/openmontage/devcontainer.json"
        profile = json.loads(profile_path.read_text())
        self.assertIn("integrations/openmontage/scripts/codespace-setup.sh", profile["postCreateCommand"])
        self.assertIn("javascript-node", profile["image"])
        self.assertNotEqual(profile_path, REPO / ".devcontainer/devcontainer.json")

    def test_scripts_pass_bash_syntax_check(self):
        for name in ("setup.sh", "codespace-setup.sh", "doctor.sh", "demo.sh"):
            with self.subTest(script=name):
                script = INTEGRATION / "scripts" / name
                result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_installer_is_pinned_and_isolated(self):
        script = (INTEGRATION / "scripts/setup.sh").read_text()
        self.assertIn('git -C "$runtime_dir" fetch --depth 1 origin "$pinned_commit"', script)
        self.assertIn('actual_commit="$(git -C "$runtime_dir" rev-parse HEAD)"', script)
        self.assertIn('integration_dir/.runtime/openmontage', script)
        self.assertNotIn("git submodule add", script)


if __name__ == "__main__":
    unittest.main()
