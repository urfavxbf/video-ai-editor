import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
import sys
sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))

spec=importlib.util.spec_from_file_location('episode_qa',Path(__file__).parents[1]/'scripts/episode_qa.py')
m=importlib.util.module_from_spec(spec)
class EpisodeQATests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): spec.loader.exec_module(m)
 def test_accepts_measured_fixture_but_rejects_missing_audio_wrong_size_and_black(self):
  with tempfile.TemporaryDirectory() as tmp:
   f=Path(tmp)/'fixture.mp4'
   subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=480x270:r=30:d=1',
    '-f','lavfi','-i','sine=duration=1','-c:v','libx264','-c:a','aac','-shortest',str(f)],check=True)
   result=m.verify_delivery(f,30,480,270,True)
   self.assertEqual(result['video']['codec_name'],'h264')
   self.assertLess(result['audio']['maxDb'],0)
   self.assertTrue(-40 < result['audio']['integratedLufs'] < 0)
   self.assertTrue(-40 < result['audio']['truePeakDbfs'] < 0)
   self.assertIn('LUFS', ' '.join(result['limitations']))
   with self.assertRaises(ValueError):m.verify_delivery(f,30,1920,1080,True)
   for kind in ('black','silent'):
    f=Path(tmp)/f'{kind}.mp4'
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',f"color=c={'black' if kind=='black' else 'blue'}:s=480x270:r=30:d=1",
     '-c:v','libx264',str(f)],check=True)
    with self.assertRaises(ValueError):m.verify_delivery(f,30,480,270,True)
    if kind=='black':
     with self.assertRaises(ValueError):m.verify_delivery(f,30,480,270,False)
 def test_rejects_audio_eof_before_expected_narration_finishes(self):
  with tempfile.TemporaryDirectory() as tmp:
   f=Path(tmp)/'short-audio.mp4'
   subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=480x270:r=30:d=2',
    '-f','lavfi','-i','sine=duration=0.5','-c:v','libx264','-c:a','aac',str(f)],check=True)
   with self.assertRaises(ValueError):m.verify_delivery(f,60,480,270,True,[(0,2)])

 def test_lufs_and_true_peak_are_source_audio_measurements(self):
  with tempfile.TemporaryDirectory() as tmp:
   f=Path(tmp)/'tone.mp4'
   subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i',
    'color=c=blue:s=480x270:r=30:d=2','-f','lavfi','-i',
    'sine=frequency=440:duration=2','-c:v','libx264','-pix_fmt','yuv420p',
    '-c:a','aac','-shortest',str(f)],check=True)
   result=m.verify_delivery(f,60,480,270,True,[(0,2)])
   audio=result['audio']
   self.assertIsInstance(audio['integratedLufs'],float)
   self.assertIsInstance(audio['truePeakDbfs'],float)
   self.assertLess(audio['integratedLufs'],-10)
   self.assertGreater(audio['integratedLufs'],-35)
   self.assertGreaterEqual(audio['truePeakDbfs'],audio['maxDb']-1)
   self.assertLessEqual(audio['truePeakDbfs'],0)
   self.assertTrue(result['manualReviewRequired'])
