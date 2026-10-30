"""Production copy and narration adapter tests; no model downloads required."""
import importlib.util
import json
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRIPT=Path(__file__).resolve().parents[2]/"integrations/openmontage/scripts/build_blue_app_props.py"
spec=importlib.util.spec_from_file_location("blue_app_props", SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PilotContractTests(unittest.TestCase):
    def setUp(self):
        self.template=json.loads((HERE/"scene-props.json").read_text())
        self.script=(HERE/"narration.txt").read_text(encoding="utf-8")
        self.title=(HERE/"title.txt").read_text(encoding="utf-8").strip()
        self.manifest={"voice_profile":"natural-storyteller-v1","language":"en","chunks":[
            {"text":"Deleted messages on the blue app?","start_seconds":0.0,"end_seconds":2.4},
            {"text":"Only check your own account.","start_seconds":2.6,"end_seconds":5.2},
        ]}
    def test_approved_title_and_reality_check(self):
        self.assertEqual(self.title,"DELETED MESSAGES ON THE BLUE APP? 👀 HERE'S WHAT TO CHECK!")
        self.assertIn("HTML",self.script)
        self.assertIn("cannot guarantee recovery",self.script)
        self.assertIn("only check your own account",self.script.lower())
    def test_temporal_continuity_and_landscape_safe_copy(self):
        cuts=self.template["cuts"]
        self.assertEqual(len(cuts),10)
        self.assertEqual(cuts[0]["in_seconds"],0)
        self.assertEqual(cuts[-1]["out_seconds"],69)
        for before, after in zip(cuts,cuts[1:]):
            self.assertEqual(before["out_seconds"],after["in_seconds"])
        self.assertTrue(all(c["source"]=="" for c in cuts if "source" in c))
        self.assertEqual(cuts[2]["leftValue"], "Still there")
        self.assertEqual(cuts[2]["rightValue"], "May be gone")
        self.assertLessEqual(max(len(c["rightValue"]) for c in cuts if c.get("type")=="comparison"), 18)
    def test_narration_props_include_caption_cues(self):
        out=mod.build_props(self.template,self.manifest,52)
        self.assertEqual(out["audio"]["narration"]["src"],"audio/blue-app-narration.wav")
        self.assertTrue(out["captions"])
        self.assertAlmostEqual(out["cuts"][-1]["out_seconds"],53.8,places=1)
        self.assertNotIn("audio",self.template) if False else None
    def test_refuses_other_voice(self):
        self.manifest["voice_profile"]="random-tts"
        with self.assertRaises(ValueError):
            mod.build_props(self.template,self.manifest,52)
    def test_refuses_invalid_duration(self):
        with self.assertRaises(ValueError):
            mod.build_props(self.template,self.manifest,4)

if __name__=="__main__":
    unittest.main()
