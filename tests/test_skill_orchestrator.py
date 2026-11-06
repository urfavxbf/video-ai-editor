"""Contracts for the single video-task router and its complete skill catalog."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ROUTER = '.claude/skills/video-ai-orchestrator/SKILL.md'
CATALOG = '.claude/skills/video-ai-orchestrator/references/skill-catalog.md'
SKILLS = (
    'video-ai-orchestrator', 'ai-video-editor', 'video-effects',
    'hyperframes-motion-graphics', 'character-voice-production',
    'transcription-captions', 'animation-import', 'media-source-ingestion',
    'senior-multidisciplinary-agent', 'remotion-best-practices',
    'remotion-create', 'remotion-markup', 'remotion-captions',
    'remotion-render', 'remotion-studio', 'remotion-interactivity',
    'remotion-multimedia', 'remotion-maps', 'remotion-docs',
    'remotion-upgrade', 'remotion-saas',
)

class SkillOrchestratorContracts(unittest.TestCase):
    def test_exact_inventory_without_generated_or_mirrored_duplicates(self):
        actual = ([ROOT / 'SKILL.md']
                  + list((ROOT / '.agents/skills').rglob('SKILL.md'))
                  + list((ROOT / '.claude/skills').rglob('SKILL.md')))
        self.assertEqual(len(actual), 21, [str(p.relative_to(ROOT)) for p in actual])
        self.assertFalse((ROOT / '.claude/skills/cineforge-pro').exists())
        self.assertFalse((ROOT / '.github/skills/senior-multidisciplinary-agent').exists())
        self.assertFalse((ROOT / 'scripts/build-cineforge-master-skill.py').exists())
        self.assertFalse((ROOT / '.github/workflows/build-cineforge-pro.yml').exists())

    def test_catalog_routes_to_existing_files_and_unique_names(self):
        catalog = (ROOT / CATALOG).read_text(encoding='utf-8')
        rows = re.findall(r'^\|[^\n]*?\| \x60([a-z0-9-]+)\x60 \| \x60([^\x60]*SKILL\.md)\x60 \|$', catalog, re.M)
        self.assertEqual(len(rows), 20, rows)
        self.assertEqual(set(SKILLS) - {'video-ai-orchestrator'}, {name for name, _ in rows})
        for name, path in rows:
            with self.subTest(name=name):
                file = ROOT / path
                self.assertTrue(file.is_file(), path)
                self.assertTrue(file.read_text(encoding='utf-8').startswith('---\nname: ' + name + '\n'))
        self.assertTrue((ROOT / ROUTER).read_text().startswith('---\nname: video-ai-orchestrator\n'))

    def test_external_integrations_have_scoped_workflows_and_real_entrypoints(self):
        integrations = {
            'hyperframes-motion-graphics': (
                'scripts/render-hyperframes.mjs',
                'docs/HYPERFRAMES_PRODUCTION.md', 'npm run hyperframes:render',
                'node --test tests/hyperframes-bridge.test.cjs',
            ),
            'character-voice-production': (
                'scripts/character_voiceover.py', 'docs/CHATTERBOX_TTS.md',
                'Kiki', 'VoxCPM2',
            ),
            'transcription-captions': (
                'scripts/groq_transcribe.py', 'docs/AI_VIDEO_TOOLS.md',
                'GROQ_API_KEY', 'scripts/episode_media.py',
            ),
            'animation-import': (
                'scripts/import_duik_baked_lottie.py',
                'docs/AFTER_EFFECTS_LOTTIE.md', 'docs/DUIK_ANGELA_IMPORT.md',
                'test_duik_baked_lottie.py',
            ),
            'media-source-ingestion': (
                'scripts/media_ingest.py',
                'requirements-media-ingestion.txt',
                'docs/MEDIA_SOURCE_INGESTION.md',
                '--confirm-rights',
            ),
        }
        router = (ROOT / ROUTER).read_text(encoding='utf-8')
        for name, tokens in integrations.items():
            with self.subTest(name=name):
                path = ROOT / '.claude' / 'skills' / name / 'SKILL.md'
                content = path.read_text(encoding='utf-8')
                self.assertIn(name, router)
                self.assertIn('docs/PRODUCTION_POLICY.md', content)
                self.assertIn('AGENTS.md', content)
                for token in tokens:
                    self.assertIn(token, content)
                self.assertNotIn('hyperframes cloud render' + ' --execute', content)
        for relpath in (
            'scripts/render-hyperframes.mjs',
            'scripts/character_voiceover.py',
            'scripts/groq_transcribe.py',
            'scripts/import_duik_baked_lottie.py',
            'scripts/media_ingest.py',
            'docs/MEDIA_SOURCE_INGESTION.md',
            'requirements-media-ingestion.txt',
            'docs/HYPERFRAMES_PRODUCTION.md',
            'docs/CHATTERBOX_TTS.md',
            'docs/AI_VIDEO_TOOLS.md',
            'docs/AFTER_EFFECTS_LOTTIE.md',
            'docs/DUIK_ANGELA_IMPORT.md',
        ):
            with self.subTest(path=relpath):
                self.assertTrue((ROOT / relpath).is_file())

    def test_entrypoints_point_to_the_router(self):
        for path in ('AGENTS.md', 'README.md', '.github/copilot-instructions.md',
                     '.github/agents/senior-multidisciplinary.agent.md',
                     'docs/REMOTION_SKILLS.md'):
            with self.subTest(path=path):
                self.assertIn('video-ai-orchestrator', (ROOT / path).read_text())

if __name__ == '__main__':
    unittest.main()
