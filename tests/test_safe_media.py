import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import sys

spec = importlib.util.spec_from_file_location('safe_media', Path(__file__).parents[1] / 'scripts/safe_media.py')
m = importlib.util.module_from_spec(spec)

class SafeMediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec.loader.exec_module(m)

    def test_real_wav_probe_and_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'audio').mkdir()
            wav = root / 'audio/tone.wav'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=frequency=440:duration=0.2',str(wav)], check=True)
            p = m.probe_local_media(root, 'audio/tone.wav')
            self.assertAlmostEqual(p['duration'], 0.2, places=2)
            for value in ['https://evil.test/x.wav', '../x.wav', '/tmp/x.wav', 'audio/%2e/x.wav', 'fonts/x.wav', 'audio/../x.wav']:
                with self.subTest(value=value), self.assertRaises(ValueError):
                    m.probe_local_media(root, value)
            (root / 'audio/link.wav').symlink_to(wav)
            with self.assertRaises(ValueError):
                m.probe_local_media(root, 'audio/link.wav')
            with self.assertRaises(ValueError):
                m.probe_local_media(root, 'audio/missing.wav')

    def test_rejects_probe_failure_without_leaking_media_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'audio').mkdir()
            (root / 'audio/fake.wav').write_text('not media')
            with self.assertRaisesRegex(ValueError, 'probe failed'):
                m.probe_local_media(root, 'audio/fake.wav')

    def test_preflight_uses_video_stream_duration_not_longer_container_audio(self):
        sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
        check_spec = importlib.util.spec_from_file_location('check_edit_media', Path(__file__).parents[1] / 'scripts/check-edit-media.py')
        check = importlib.util.module_from_spec(check_spec)
        check_spec.loader.exec_module(check)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'takes').mkdir()
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=32x32:r=30:d=1',
                '-f','lavfi','-i','sine=duration=2','-c:v','libx264','-c:a','aac',str(root/'takes/unequal.mp4')], check=True)
            edit = {'source':{'video':'takes/unequal.mp4','frames':60,'matte':'takes/unused','sticker':'takes/unused'},
                    'segments':[{'kind':'aroll','at':30,'frames':30}]}
            with self.assertRaisesRegex(ValueError, 'measured duration'):
                check.verify(edit, root)
            edit['source']['frames'] = 30
            edit['segments'] = [{'kind':'aroll','at':0,'frames':30}]
            check.verify(edit, root)
            edit['segments'] = [{'kind':'fx','id':'snap-zoom','at':0,'frames':30}]
            check.verify(edit, root)  # This effect reads only video, no derived cutouts.
