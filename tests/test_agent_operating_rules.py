"""Guard the canonical agent policy, prompt routing and current registry.

These are model-free contracts. They do not synthesize speech or publish media.
"""
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
POLICY = (ROOT / "docs/PRODUCTION_POLICY.md").read_text(encoding="utf-8")
PROMPTS = (ROOT / "docs/AI_AGENT_PROMPTS.md").read_text(encoding="utf-8")
REGISTRY = json.loads((ROOT / "characters/registry.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((ROOT / "characters/pixel-default-manifest.json").read_text(encoding="utf-8"))


class AgentPolicyContracts(unittest.TestCase):
    def test_all_five_required_entries_are_in_agent_policy(self):
        for path in ("AGENTS.md", "docs/PRODUCTION_POLICY.md",
                     "characters/registry.json",
                     "characters/pixel-default-manifest.json",
                     ".claude/skills/ai-video-editor/SKILL.md"):
            with self.subTest(path=path):
                self.assertIn(path, AGENT)
        self.assertIn("docs/AI_AGENT_PROMPTS.md", AGENT)
        self.assertIn("AGENTS.md", POLICY)
        self.assertIn("AGENTS.md", (ROOT / ".github/copilot-instructions.md").read_text())

    def test_machine_defaults_and_approved_identities_match_text(self):
        video = REGISTRY["default_video"]
        self.assertEqual(REGISTRY["production_language"], "en")
        self.assertEqual((video["width"], video["height"], video["fps"]), (1920, 1080, 30))
        self.assertEqual(video["aspect_ratio"], "16:9")
        self.assertEqual(video["default_character_composition"], "HeroCharacterStage")
        for char in REGISTRY["characters"].values():
            self.assertIn(char["english_voice"]["identifier"], AGENT)
        self.assertEqual(sum(len(v["poses"]) for v in MANIFEST["characters"].values()), 13)
        self.assertIn("PixelProductionProof", AGENT)
        self.assertIn("--verify-workspace", AGENT)

    def test_all_21_current_effect_ids_have_explicit_guidance(self):
        ids = (
            "orbit", "chat-takeover", "frame-escape", "snap-zoom", "checklist-pop",
            "headline-storm", "zoom-portal", "growth-curve", "broll-overlay",
            "paper-cutout", "magazine-cover", "liquid-glass", "zoom-through-cut",
            "green-screen", "frame-break", "digital-zoom", "phone-mockup",
            "checklist-tally", "glass-widgets", "checklist", "split",
        )
        self.assertEqual(len(ids), 21)
        section = AGENT.split("## 4. Choose an FX", 1)[1].split("## 5.", 1)[0]
        for effect_id in ids:
            with self.subTest(effect_id=effect_id):
                self.assertIn(f"| `{effect_id}` |", section)
        self.assertIn("seven", section.lower())
        self.assertIn("five-bar", section.lower())

    def test_production_guardrails_and_truthful_limitations(self):
        for token in ("EpisodeProduction", "EpisodeTimelineProof", "ExampleEdit",
                      "DudutPremium", "DudutV2", "FxPreview", "FxShowcase",
                      "AfterEffectsLottieProof", "DuikBakedCharacterProof",
                      "input/pix-reference.wav", "groq_transcribe.py",
                      "--language en --device cpu", "ffprobe", "No paid",
                      "main", "not", "RMS"):
            with self.subTest(token=token):
                self.assertIn(token.lower(), AGENT.lower())
        self.assertIn("VoxCPM2 is opt-in", AGENT)
        self.assertIn("do not", AGENT.lower())

    def test_prompt_playbook_has_usable_tasks_and_no_policy_override(self):
        self.assertIn("AGENTS.md", PROMPTS)
        self.assertGreaterEqual(len(re.findall(r"(?m)^## [0-9]+[.] ", PROMPTS)), 14)
        for marker in ("HeroCharacterStage", "ExampleEdit", "DudutPremium",
                       "FxPreview", "Chatterbox", "Duik", "Lottie",
                       "FFprobe", "scripts/character_voiceover.py",
                       "node scripts/validate-edit.cjs", "python3 scripts/stage_pixel_default_pack.py"):
            with self.subTest(marker=marker):
                self.assertIn(marker, PROMPTS)
        self.assertIn("never", PROMPTS.lower())


if __name__ == "__main__":
    unittest.main()
