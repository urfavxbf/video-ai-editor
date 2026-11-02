"""New active host SVG pack; legacy PNGs remain verifiable."""
import json
from pathlib import Path
import unittest
import tempfile
import os
import subprocess
import hashlib
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class EightBitHostTests(unittest.TestCase):
    def test_frames_are_present_and_valid_svg(self):
        m=json.loads((ROOT/'characters/8bit-host-sprite-manifest.json').read_text())
        actions=m['characters']['urfavxbf']['actions']
        self.assertEqual(len(actions),15)
        self.assertEqual(sum(v['frames'] for v in actions.values()),116)
        self.assertEqual(m['frameRate'],8)
        for action,v in actions.items():
            for i in range(v['frames']):
                path=ROOT/f'public/characters/8bit-host/urfavxbf/{action}/frame-{i:02d}.svg'
                self.assertTrue(path.is_file(),str(path))
                root=ET.parse(path).getroot()
                self.assertEqual(root.attrib['viewBox'],'0 0 72 82')
                self.assertTrue(root.tag.endswith('svg'))
    def test_generator_reproduces_committed_frames_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(
                ['node', str(ROOT/'scripts/generate_8bit_host_sprites.mjs')],
                env={**os.environ,'SPRITE_OUTPUT_ROOT':temp},
                check=True, timeout=20,
            )
            m=json.loads((ROOT/'characters/8bit-host-sprite-manifest.json').read_text())
            for action,v in m['characters']['urfavxbf']['actions'].items():
                for i in range(v['frames']):
                    rel=f'public/characters/8bit-host/urfavxbf/{action}/frame-{i:02d}.svg'
                    actual=(Path(temp)/rel).read_bytes()
                    expected=(ROOT/rel).read_bytes()
                    self.assertEqual(hashlib.sha256(actual).digest(),hashlib.sha256(expected).digest(),rel)
    def test_episode_pipeline_stages_every_active_sprite_frame(self):
        import importlib.util
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        spec=importlib.util.spec_from_file_location('production',ROOT/'scripts/produce-episode.py')
        production=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(production)
        staged=production.approved_assets()
        host={key for key in staged if key.startswith('characters/8bit-host/urfavxbf/')}
        self.assertEqual(len(host),116)
        self.assertIn('characters/8bit-host/urfavxbf/idle/frame-00.svg',host)
        self.assertIn('characters/pixel-default/pix/idle.png',staged)
    def test_default_host_is_svg_and_pix_preserved(self):
        reg=json.loads((ROOT/'characters/registry.json').read_text())
        self.assertEqual(reg['character_hero_system']['host_action_count'],15)
        self.assertEqual(reg['character_hero_system']['host_frame_count'],116)
        self.assertTrue(reg['characters']['urfavxbf']['visual']['public_path'].endswith('.svg'))
        self.assertTrue(reg['characters']['pix']['visual']['public_path'].endswith('.png'))
        self.assertEqual(reg['characters']['urfavxbf']['english_voice']['identifier'],'natural-storyteller-v1')
        self.assertEqual(reg['characters']['pix']['english_voice']['identifier'],'pix-cute-female-emily-v1')
        motions=json.loads((ROOT/"characters/8bit-host-motions.json").read_text())
        self.assertEqual(len(motions),33)
        self.assertEqual(len({m["id"] for m in motions}),33)
        self.assertTrue(all(m["narration"] for m in motions))
        self.assertIn('id="Host33MotionShowcase"',(ROOT/"src/Root.tsx").read_text())
        src=(ROOT/'src/characters/PixelPoseCharacter.tsx').read_text()
        self.assertIn('hostFramePath',src)
        self.assertIn("imageRendering:'pixelated'",src)
if __name__=='__main__':unittest.main()
