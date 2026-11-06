"""Actual WAV preflight: missing, corrupt, overlong and silent speech must fail closed."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import wave
import numpy as np

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/prepare_showreel.py'

class ShowreelAudioTests(unittest.TestCase):
    def test_preparer_exists(self):
        self.assertTrue(SCRIPT.is_file(), 'missing showreel audio preparation')

    def setUp(self):
        if not SCRIPT.is_file():
            return
        spec=importlib.util.spec_from_file_location('prepare_showreel',SCRIPT)
        self.m=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def test_rejects_missing_silent_and_corrupt_speech(self):
        if not SCRIPT.is_file():
            self.skipTest('preparer not implemented yet')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'voice.wav'
            with self.assertRaisesRegex(ValueError, 'Missing'):
                self.m.load_voice(p, 100)
            p.write_bytes(b'not a recording')
            with self.assertRaisesRegex(ValueError, 'Invalid WAV'):
                self.m.load_voice(p, 100)
            with wave.open(str(p),'wb') as w:
                w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(bytes(48000))
            with self.assertRaisesRegex(ValueError, 'silent'):
                self.m.load_voice(p, 100)

    def test_measures_and_trims_real_pcm_not_text_length(self):
        if not SCRIPT.is_file():
            self.skipTest('preparer not implemented yet')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'voice.wav'; sr=24000
            signal=np.concatenate([np.zeros(sr//2), .2*np.sin(2*np.pi*220*np.arange(sr)/sr), np.zeros(sr//2)])
            with wave.open(str(p),'wb') as w:
                w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((signal*32767).astype('<i2').tobytes())
            samples,rate=self.m.load_voice(p, 60)
            self.assertEqual(rate,sr)
            self.assertGreater(len(samples),sr)
            self.assertLess(len(samples),1.3*sr)
            self.assertLessEqual(np.max(np.abs(samples)),.831)
            envelope=self.m.envelope(samples,rate)
            self.assertEqual(len(envelope),int(np.ceil(len(samples)/rate*30)))
            self.assertTrue(all(0<=v<=1 for v in envelope))
            with self.assertRaisesRegex(ValueError, 'exceeds'):
                self.m.load_voice(p, 10)

    def test_rejects_stale_voice_text_speaker_and_changed_wav(self):
        self.assertTrue(hasattr(self.m, 'validate_receipt'), 'missing source voice provenance validation')
        import json
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'sample.wav';path.write_bytes(b'actual-wave-bytes')
            row={'text':'Approved words.', 'character':'pix'}
            receipt={'request':self.m.voice_request(row),'sha256':self.m.digest(path)}
            path.with_suffix('.voice.json').write_text(json.dumps(receipt))
            self.m.validate_receipt(path,row)
            for changed in ({**row,'text':'Different words.'},{**row,'character':'urfavxbf'}):
                with self.assertRaisesRegex(ValueError,'stale'):
                    self.m.validate_receipt(path,changed)
            path.write_bytes(b'changed-wave-bytes')
            with self.assertRaisesRegex(ValueError,'changed'):
                self.m.validate_receipt(path,row)

if __name__=='__main__':
    unittest.main()
