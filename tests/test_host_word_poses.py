"""Guard the audio-derived word schedule against silent alignment errors."""
import importlib.util,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class WordPoses(unittest.TestCase):
    def adapter(self):
        path=ROOT/'scripts/prepare_host_word_poses.py'
        self.assertTrue(path.exists(),'missing word performance preparation')
        spec=importlib.util.spec_from_file_location('prepare_host_word_poses',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module
    def test_real_word_boundaries_are_preserved(self):
        m=self.adapter()
        words=m.align_words({'text':'Hello there!','poses':['waving','front']},[{'text':'Hello','start':.1,'end':.4},{'text':'there!','start':.5,'end':.8}],offset=.7)
        self.assertAlmostEqual(words[0]['startMs'],800)
        self.assertAlmostEqual(words[1]['endMs'],1500)
        self.assertEqual(words[0]['pose'],'waving')
    def test_omitted_or_wrong_words_are_rejected(self):
        m=self.adapter();row={'text':'Hello there!','poses':['waving','front']}
        for asr in ([],[{'text':'Wrong','start':.1,'end':.4},{'text':'there','start':.5,'end':.8}]):
            with self.assertRaises(ValueError):m.align_words(row,asr,0)
    def test_duplicate_pose_and_unrenderably_short_words_are_rejected(self):
        m=self.adapter()
        for poses in (['front','front'],['front','bogus']):
            with self.assertRaises(ValueError):m.align_words({'text':'Hello there','poses':poses},[{'text':'Hello','start':.1,'end':.4},{'text':'there','start':.5,'end':.8}],0)
        with self.assertRaises(ValueError):m.align_words({'text':'Hi','poses':['waving']},[{'text':'Hi','start':.1,'end':.11}],0)
    def test_art_source_and_nine_views_are_present(self):
        m=self.adapter();manifest=m.art_manifest()
        self.assertEqual(len(manifest['poses']),9)
        self.assertEqual(manifest['sourceSha256'],m.digest(ROOT/manifest['source']))
        for p in manifest['poses'].values():
            x,y,w,h=p['rect'];self.assertTrue(0<=x<x+w<=1280 and 0<=y<y+h<=960)
    def test_changed_script_cannot_reuse_stale_performance(self):
        m=self.adapter()
        with self.assertRaisesRegex(ValueError,'script'):
            m.check_current({'ready':True,'scriptSha256':'0'*64})
    def test_jasper_identity_is_enforced_even_if_showreel_config_changes(self):
        m=self.adapter();profile=json.loads((ROOT/'src/showcase/showreel-voices.json').read_text())
        profile['voices']['urfavxbf']='Bruno'
        with self.assertRaisesRegex(ValueError,'Jasper'):m.host_voice_request(profile)
    def test_quantized_word_starts_leave_one_stable_frame_after_glitch(self):
        m=self.adapter()
        with self.assertRaisesRegex(ValueError,'four frames'):
            m.validate_schedule([{'text':'Hello','pose':'waving','startMs':0,'endMs':34},{'text':'there','pose':'front','startMs':34,'endMs':68}],30,require_all=False)
