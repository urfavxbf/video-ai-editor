"""Selected pixel pose art contract. Binary art must be imported separately."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PixelDefaultTests(unittest.TestCase):
 def test_pixel_default_registry(self):
    reg=json.loads((ROOT/'characters/registry.json').read_text())
    m=json.loads((ROOT/'characters/pixel-default-manifest.json').read_text())
    self.assertEqual(reg['character_hero_system']['version'],'pixel-pose-default-2026-10-29')
    self.assertTrue(m['selectedAsDefaultByOwner'])
    self.assertFalse(m['assetDelivery']['assetReady'])
    for id,info in m['characters'].items():
        self.assertEqual(len(info['poses']),5)
        self.assertEqual(reg['characters'][id]['visual']['public_path'],info['poses']['idle']['path'])
        for pose,spec in info['poses'].items():
            self.assertEqual(spec['path'],f'public/characters/pixel-default/{id}/{pose}.png')
            self.assertEqual(len(spec['sha256']),64)
    s=(ROOT/'src/characters/PixelPoseCharacter.tsx').read_text()
    self.assertIn("imageRendering:'pixelated'",s)
    self.assertNotIn('animation-v4/',s)
if __name__=='__main__':unittest.main()
