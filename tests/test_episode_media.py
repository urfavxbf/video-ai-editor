import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import wave
import math

SCRIPTS = Path(__file__).parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('episode_media', SCRIPTS / 'episode_media.py')
m = importlib.util.module_from_spec(spec)

class EpisodeMediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec.loader.exec_module(m)

    def fixture(self, root):
        (root/'audio').mkdir()
        wav=root/'audio/diagnostic.wav'
        with wave.open(str(wav),'wb') as f:
            f.setparams((1,2,16000,0,'NONE','not compressed'))
            f.writeframes(b''.join(struct.pack('<h',int(8000*math.sin(i*2*math.pi*440/16000))) for i in range(8000)))
        manifest={'schemaVersion':1,'episodeId':'fixture','language':'en','video':{'width':1920,'height':1080,'fps':30},
          'chapters':[{'id':'intro','title':'Diagnostic fixture','chapterNumber':1,'startFrame':0,'durationFrames':30}]}
        clip={'chapterId':'intro','speaker':'pix','file':'audio/diagnostic.wav','startFrame':3,
              'voiceProfile':'pix-cute-female-emily-v1','sha256':hashlib.sha256(wav.read_bytes()).hexdigest(),
              'provenance':'fixture-diagnostic'}
        return manifest,clip

    def test_measures_wav_and_offsets_without_claiming_generated_speech(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); manifest,clip=self.fixture(root)
            result=m.prepare_episode_media(manifest,[clip],root,allow_fixtures=True)
            event=result['manifest']['chapters'][0]['voiceEvents'][0]
            self.assertEqual((event['startFrame'],event['endFrame']),(3,18))
            self.assertEqual(len(event['rms']),5)
            self.assertEqual(result['captions'],{})
            self.assertEqual(result['evidence'][0]['voiceIdentity'],'diagnostic-nonspeech')
            self.assertGreater(result['evidence'][0]['rms'],0.1)

    def test_rejects_unapproved_fixture_profile_digest_and_overrun(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); manifest,clip=self.fixture(root)
            with self.assertRaises(ValueError): m.prepare_episode_media(manifest,[clip],root)
            for key,value in [('sha256','0'*64),('voiceProfile','different-speaker'),('startFrame',20)]:
                bad=copy.deepcopy(clip);bad[key]=value
                with self.subTest(key=key),self.assertRaises(ValueError):
                    m.prepare_episode_media(manifest,[bad],root,allow_fixtures=True)

    def test_imports_only_reviewed_audio_bound_word_timings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); manifest,clip=self.fixture(root)
            alignment={'schemaVersion':1,'audioSha256':clip['sha256'],'source':'human-reviewed','reviewed':True,
                       'words':[{'start':0.1,'end':0.3,'text':'Test'}]}
            clip['alignment']=alignment
            result=m.prepare_episode_media(manifest,[clip],root,allow_fixtures=True)
            self.assertEqual(result['captions']['intro'],[{'startFrame':6,'endFrame':12,'text':'Test'}])
            for key,value in [('audioSha256','0'*64),('reviewed',False),('words',[{'start':0,'end':1,'text':'too long'}])]:
                clip['alignment']={**alignment,key:value}
                with self.subTest(key=key),self.assertRaises(ValueError):
                    m.prepare_episode_media(manifest,[clip],root,allow_fixtures=True)

    def test_rejects_duplicate_speaker_overlap_instead_of_merging_audio(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); manifest,clip=self.fixture(root)
            with self.assertRaises(ValueError):
                m.prepare_episode_media(manifest,[clip,copy.deepcopy(clip)],root,allow_fixtures=True)

    def test_fractional_adjacent_word_boundaries_do_not_create_overlap(self):
        words=[{'start':i*0.31,'end':(i+1)*0.31,'text':'word'} for i in range(9)]
        cues=m.reviewed_captions({'schemaVersion':1,'audioSha256':'a'*64,'source':'human-reviewed',
           'reviewed':True,'words':words},'a'*64,3,0)
        self.assertTrue(all(a['endFrame']<=b['startFrame'] for a,b in zip(cues,cues[1:])))

    def test_measures_expected_active_windows_instead_of_treating_real_pauses_as_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);manifest,clip=self.fixture(root)
            wav=root/clip['file']
            with wave.open(str(wav),'rb') as f: raw=f.readframes(f.getnframes())
            with wave.open(str(wav),'wb') as f:
                f.setparams((1,2,16000,0,'NONE','not compressed'));f.writeframes(raw+b'\0'*16000+raw)
            measured=m.wav_measurements(wav)
            self.assertEqual(measured['activeRanges'],[[0,0.5],[1,1.5]])

    def test_exact_rational_wav_frame_count_does_not_round_up_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);manifest,clip=self.fixture(root)
            wav=root/clip['file']
            with wave.open(str(wav),'wb') as f:
                f.setparams((1,2,48000,0,'NONE','not compressed'));f.writeframes(struct.pack('<h',4000)*49600)
            clip['startFrame']=0;clip['sha256']=hashlib.sha256(wav.read_bytes()).hexdigest()
            manifest['chapters'][0]['durationFrames']=31
            result=m.prepare_episode_media(manifest,[clip],root,allow_fixtures=True)
            self.assertEqual(result['manifest']['chapters'][0]['voiceEvents'][0]['endFrame'],31)
