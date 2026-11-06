import importlib.util,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
class KittenShowreelTests(unittest.TestCase):
 def test_selected_voices_and_pinned_model_are_part_of_receipt(self):
  from prepare_showreel import voice_request
  for character,voice in [('urfavxbf','Jasper'),('pix','Kiki')]:
   request=voice_request({'character':character,'text':'A real line.'})
   self.assertEqual(request.get('engine'),'kitten-onnx')
   self.assertEqual(request.get('voice'),voice)
   self.assertEqual(request.get('model'),'KittenML/kitten-tts-mini-0.8')
   self.assertEqual(len(request.get('modelRevision','')),40)
   self.assertEqual(request.get('speed'),1.0)
 def test_model_integrity_rejects_changed_weights(self):
  path=ROOT/'scripts/kitten_showreel_voice.py'
  self.assertTrue(path.exists(),'missing Kitten adapter')
  spec=importlib.util.spec_from_file_location('kitten_voice',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'kitten_tts_mini_v0_8.onnx').write_bytes(b'wrong')
   (p/'voices.npz').write_bytes(b'wrong')
   with self.assertRaisesRegex(ValueError,'hash'):m.verify_model(p)
 def test_sdk_integrity_rejects_unpinned_code(self):
  path=ROOT/'scripts/kitten_showreel_voice.py'
  spec=importlib.util.spec_from_file_location('kitten_voice',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  self.assertTrue(hasattr(m,'verify_sdk'),'missing pinned SDK verification')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'__init__.py').write_text('unrelated SDK')
   with self.assertRaisesRegex(ValueError,'SDK hash'):m.verify_sdk(p)
 def test_interpreter_selection_preserves_virtual_environment_identity(self):
  path=ROOT/'scripts/render_showreel_voices.py'
  spec=importlib.util.spec_from_file_location('render_voices',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  self.assertTrue(hasattr(m,'same_python_environment'),'missing venv-aware interpreter comparison')
  with tempfile.TemporaryDirectory() as d:
   a=Path(d)/'venv-a';b=Path(d)/'venv-b';a.mkdir();b.mkdir()
   (a/'python').symlink_to(sys.executable);(b/'python').symlink_to(sys.executable)
   self.assertFalse(m.same_python_environment(str(a/'python'),str(b/'python')))
   self.assertTrue(m.same_python_environment(str(a/'python'),str(a/'python')))
if __name__=='__main__':unittest.main()
