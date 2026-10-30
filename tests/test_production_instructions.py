"""Keep shipped agent guidance aligned with the approved production registry."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProductionInstructionTests(unittest.TestCase):
    def test_codex_and_skill_entrypoints_route_to_current_policy(self):
        for path in ('AGENTS.md', 'README.md', 'SKILL.md',
                     '.claude/skills/ai-video-editor/SKILL.md',
                     '.claude/skills/cineforge-pro/SKILL.md'):
            with self.subTest(path=path):
                text = (ROOT / path).read_text()
                self.assertIn('docs/PRODUCTION_POLICY.md', text)
                self.assertIn('characters/registry.json', text)

    def test_standalone_custom_skill_matches_active_registry(self):
        registry = json.loads((ROOT / 'characters/registry.json').read_text())
        manifest = json.loads((ROOT / registry['default_video']['character_asset_manifest']).read_text())
        text = (ROOT / '.claude/skills/ai-video-editor/SKILL.md').read_text()
        self.assertIn('English (en)', text)
        self.assertEqual(registry['production_language'], 'en')
        for character in registry['characters'].values():
            self.assertIn(character['english_voice']['identifier'], text)
        self.assertIn(registry['default_video']['default_character_composition'], text)
        for value in (registry['default_video']['width'], registry['default_video']['height'], registry['default_video']['fps']):
            self.assertIn(str(value), text)
        poses = sum(len(character['poses']) for character in manifest['characters'].values())
        self.assertIn(f'{poses} committed', text)
        self.assertIn('full-body', text.lower())
        self.assertIn('--verify-workspace', text)
        self.assertIn('opt-in', text)
        self.assertIn('No paid API or GPU', text)
        for obsolete in ('Tagalog/Taglish-default', 'not yet binary assets', 'keep the full-body sprites hidden',
                         'use ONLY the **animated super-pixel/glitch HEAD PORTRAITS**'):
            self.assertNotIn(obsolete, text)

    def test_superseded_policies_are_explicitly_historical(self):
        for name in ('MULTILINGUAL_PRODUCTION_POLICY.md', 'PIXEL_GLITCH_PORTRAITS_ONLY.md',
                     'PIXEL_GLITCH_CHARACTER_PACK.md', 'GLOBAL_CANONICAL_CHARACTER_SYSTEM.md',
                     'CANONICAL_CHARACTERS_2026-10-29.md', 'ZERO_BUDGET_TRUE_FRAME_WORKFLOW.md',
                     'CHIBI_V4_SPRITE_PACK.md', 'CANONICAL_FULLBODY_REVIEW_PACK.md'):
            with self.subTest(name=name):
                text = (ROOT / 'docs' / name).read_text()
                self.assertTrue(text.startswith('> **Historical'), name)
                self.assertIn('PRODUCTION_POLICY.md', text.split('\n\n', 1)[0])

    def test_active_voice_and_character_references_route_to_current_policy(self):
        for name in ('ENGLISH_PRODUCTION_POLICY.md', 'OFFICIAL_CHARACTERS.md',
                     'PRODUCTION_STANDARD.md', 'PIX_VOICE.md', 'CHATTERBOX_TTS.md',
                     'REMOTION_SKILLS.md'):
            with self.subTest(name=name):
                text = (ROOT / 'docs' / name).read_text()
                self.assertIn('PRODUCTION_POLICY.md', text)
                self.assertNotRegex(text, r'(?i)default to\s+\*\*Tagalog/Taglish')

    def test_cineforge_rebuild_matches_committed_instructions(self):
        build = script('build-cineforge-master-skill')
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'SKILL.md'
            out = Path(tmp) / 'out'
            with patch.object(build, 'DEST', dest), patch.object(build, 'OUT', out), contextlib.redirect_stdout(io.StringIO()):
                build.main()
            self.assertEqual(dest.read_bytes(), (ROOT / '.claude/skills/cineforge-pro/SKILL.md').read_bytes())
            with ZipFile(out / 'CineForge-Pro-One-Skill.zip') as archive:
                self.assertEqual(archive.read('SKILL.md'), dest.read_bytes())

    def test_packaged_custom_skill_and_metadata_keep_current_defaults(self):
        package = script('package-chatgpt-skills')
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'out'
            with patch.object(package, 'OUT', out), patch.object(package, 'PLUGIN', out / 'plugin'), contextlib.redirect_stdout(io.StringIO()):
                package.main()
            with ZipFile(out / 'Video-AI-Editor-13-Skills-Plugin.zip') as archive:
                text = archive.read('skills/ai-video-editor/SKILL.md').decode()
                self.assertEqual(text, (ROOT / '.claude/skills/ai-video-editor/SKILL.md').read_text())
                self.assertIn('English', archive.read('plugin.json').decode())
                self.assertNotIn('Tagalog Shorts workflow', archive.read('plugin.json').decode())


if __name__ == '__main__':
    unittest.main()
