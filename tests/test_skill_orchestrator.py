"""Contracts for the single video-task router and its complete skill catalog."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ROUTER = '.claude/skills/video-ai-orchestrator/SKILL.md'
CATALOG = '.claude/skills/video-ai-orchestrator/references/skill-catalog.md'
SKILLS = (
    'video-ai-orchestrator', 'ai-video-editor', 'video-effects',
    'senior-multidisciplinary-agent', 'remotion-best-practices',
    'remotion-create', 'remotion-markup', 'remotion-captions',
    'remotion-render', 'remotion-studio', 'remotion-interactivity',
    'remotion-multimedia', 'remotion-maps', 'remotion-docs',
    'remotion-upgrade', 'remotion-saas',
)

class SkillOrchestratorContracts(unittest.TestCase):
    def test_exact_inventory_without_generated_or_mirrored_duplicates(self):
        actual = list(ROOT.rglob('SKILL.md'))
        self.assertEqual(len(actual), 16, [str(p.relative_to(ROOT)) for p in actual])
        self.assertFalse((ROOT / '.claude/skills/cineforge-pro').exists())
        self.assertFalse((ROOT / '.github/skills/senior-multidisciplinary-agent').exists())
        self.assertFalse((ROOT / 'scripts/build-cineforge-master-skill.py').exists())
        self.assertFalse((ROOT / '.github/workflows/build-cineforge-pro.yml').exists())

    def test_catalog_routes_to_existing_files_and_unique_names(self):
        catalog = (ROOT / CATALOG).read_text(encoding='utf-8')
        rows = re.findall(r'^\|[^\n]*?\| \x60([a-z0-9-]+)\x60 \| \x60([^\x60]*SKILL\.md)\x60 \|$', catalog, re.M)
        self.assertEqual(len(rows), 15, rows)
        self.assertEqual(set(SKILLS) - {'video-ai-orchestrator'}, {name for name, _ in rows})
        for name, path in rows:
            with self.subTest(name=name):
                file = ROOT / path
                self.assertTrue(file.is_file(), path)
                self.assertTrue(file.read_text(encoding='utf-8').startswith('---\nname: ' + name + '\n'))
        self.assertTrue((ROOT / ROUTER).read_text().startswith('---\nname: video-ai-orchestrator\n'))

    def test_entrypoints_point_to_the_router(self):
        for path in ('AGENTS.md', 'README.md', '.github/copilot-instructions.md',
                     '.github/agents/senior-multidisciplinary.agent.md',
                     'docs/REMOTION_SKILLS.md'):
            with self.subTest(path=path):
                self.assertIn('video-ai-orchestrator', (ROOT / path).read_text())

if __name__ == '__main__':
    unittest.main()
