"""Free Spritesheets.ai companion-inspired import; no paid generation used."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sprite_import',ROOT/'scripts/import_sprite_animation.py')
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)

class SpriteImportTests(unittest.TestCase):
    def test_real_rgba_pngs_and_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'frames';source.mkdir()
            for i in range(3):
                im=Image.new('RGBA',(512,512))
                im.putpixel((10+i,20),(0,240,100,255))
                im.save(source/f'{i:03}.png')
            m=mod.write_import(source,root/'out','urfavxbf','idle_normal',
                               None,None,None,8,True)
            self.assertEqual(m['frameCount'],3)
            self.assertEqual(m['durationsMs'],[125]*3)
            self.assertTrue(m['realTransparencyVerified'])
            self.assertIn('draft',m['qualityStatus'])
            self.assertTrue((root/'out/urfavxbf/idle_normal/002.png').exists())
            self.assertEqual(json.loads((root/'out/urfavxbf/idle_normal/manifest.json').read_text())['frameCount'],3)

    def test_reject_opaque_background_and_unsafe_path(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'opaque.png'
            Image.new('RGB',(512,512),'purple').save(p)
            with self.assertRaisesRegex(ValueError,'opaque'):
                mod.write_import(p,root/'out','pix','idle',None,None,None,None,True)
            with self.assertRaisesRegex(ValueError,'Unsafe'):
                mod.write_import(p,root/'out','../pix','idle',None,None,None,None,True)

    def test_png_grid_exact_frame_count_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'grid.png'
            im=Image.new('RGBA',(1024,512))
            for x in (100,700):im.putpixel((x,80),(0,255,0,255))
            im.save(p)
            m=mod.write_import(p,root/'out','pix','walk',2,1,None,8,True)
            self.assertEqual((m['frameCount'],m['nativeWidth']),(2,512))
            with self.assertRaises(FileExistsError):
                mod.write_import(p,root/'out','pix','walk',2,1,None,8,True)

    def test_gif_frames_and_original_durations(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);g=root/'idle.gif';pics=[]
            for i in range(3):
                im=Image.new('RGBA',(512,512))
                for y in range(100,130):
                    for x in range(100+i*10,150+i*10): im.putpixel((x,y),(0,255,0,255))
                pics.append(im)
            pics[0].save(g,save_all=True,append_images=pics[1:],
                         duration=[80,120,160],loop=0,disposal=2,optimize=False)
            m=mod.write_import(g,root/'out','urfavxbf','idle',None,None,None,None,True)
            self.assertEqual(m['frameCount'],3)
            self.assertEqual(m['durationsMs'],[80,120,160])

    def test_low_native_resolution_is_not_labelled_1080p(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'tiny.png'
            Image.new('RGBA',(64,78)).save(p)
            m=mod.write_import(p,root/'out','pix','idle',None,None,None,None,False)
            self.assertTrue(any('1080p' in x for x in m['warnings']))

if __name__=='__main__': unittest.main()
