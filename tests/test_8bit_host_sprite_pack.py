"""Fast 33-effect text sequence contract and separately authored host sprites."""
import json
import re
from pathlib import Path
import unittest
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
    def test_default_host_is_svg_and_pix_preserved(self):
        reg=json.loads((ROOT/'characters/registry.json').read_text())
        self.assertEqual(reg['character_hero_system']['host_action_count'],15)
        self.assertEqual(reg['character_hero_system']['host_frame_count'],116)
        self.assertTrue(reg['characters']['urfavxbf']['visual']['public_path'].endswith('.svg'))
        self.assertTrue(reg['characters']['pix']['visual']['public_path'].endswith('.png'))
        self.assertEqual(reg['characters']['urfavxbf']['english_voice']['identifier'],'natural-storyteller-v1')
        self.assertEqual(reg['characters']['pix']['english_voice']['identifier'],'pix-cute-female-emily-v1')
        src=(ROOT/'src/characters/PixelPoseCharacter.tsx').read_text()
        self.assertIn('hostFramePath',src)
        self.assertIn("imageRendering:'pixelated'",src)
    def test_all_33_effects_are_on_text_not_host(self):
        motions=json.loads((ROOT/'characters/8bit-host-motions.json').read_text())
        self.assertEqual(len(motions),33)
        self.assertEqual(len({m['id'] for m in motions}),33)
        src=(ROOT/'src/characters/Host33MotionShowcase.tsx').read_text()
        self.assertIn('HOST_MOTION_SCENE_FRAMES = 36;',src)
        self.assertIn('...textMotionStyle(item.id,local)',src)
        self.assertIn('voiceoverFile&&<Audio',src)
        self.assertIn('<PixelPoseCharacter id="urfavxbf"',src)
        self.assertEqual(len(re.findall(r"case '[a-z-]+':",src)),33)
        self.assertIn('Which one', (ROOT/'scripts/8bit-33-voiceover.txt').read_text())
if __name__=='__main__': unittest.main()
