import hashlib,importlib.util,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class StageAudio(unittest.TestCase):
 def module(self):
  path=ROOT/'scripts/stage_delivery_audio.py';self.assertTrue(path.exists(),'missing Drive-only audio staging')
  spec=importlib.util.spec_from_file_location('stage_delivery_audio',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
 def test_stages_only_hash_verified_whitelisted_files(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);archive=root/'audio.zip';raw=b'actual approved bytes';name='public/voiceovers/example.wav'
   with zipfile.ZipFile(archive,'w') as z:z.writestr(name,raw);z.writestr('../unexpected.wav',b'not allowed');z.writestr('src/Root.tsx',b'not allowed')
   self.assertEqual(m.stage_archive(archive,{name:hashlib.sha256(raw).hexdigest()},root),1)
   self.assertEqual((root/name).read_bytes(),raw);self.assertFalse((root/'src/Root.tsx').exists())
 def test_corrupt_audio_is_rejected_before_install(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);archive=root/'audio.zip';name='public/voiceovers/example.wav'
   with zipfile.ZipFile(archive,'w') as z:z.writestr(name,b'wrong bytes')
   with self.assertRaisesRegex(ValueError,'hash'):m.stage_archive(archive,{name:'0'*64},root)
   self.assertFalse((root/name).exists())
 def test_changed_existing_audio_is_not_silently_overwritten(self):
  m=self.module()
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);archive=root/'audio.zip';name='public/voiceovers/example.wav';p=root/name;p.parent.mkdir(parents=True);p.write_bytes(b'existing')
   with zipfile.ZipFile(archive,'w') as z:z.writestr(name,b'approved')
   with self.assertRaisesRegex(ValueError,'exists'):m.stage_archive(archive,{name:hashlib.sha256(b'approved').hexdigest()},root)
   self.assertEqual(p.read_bytes(),b'existing')
