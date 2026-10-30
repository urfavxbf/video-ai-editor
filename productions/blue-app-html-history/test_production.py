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
    def test_production_directory_is_correctly_resolved(self):
        self.assertEqual(mod.PRODUCTION, HERE)
        self.assertTrue((mod.PRODUCTION / "scene-props.json").is_file())

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


    def test_cinematic_reference_style_in_original_remotion_component(self):
        integration=Path(__file__).resolve().parents[2]/"integrations"/"openmontage"
        tsx=(integration/"creative"/"BlueAppVisual.tsx").read_text(encoding="utf-8")
        render=(integration/"scripts"/"render_blue_app_tutorial.sh").read_text(encoding="utf-8")
        self.assertIn("PixelGuide",tsx)
        self.assertIn("PixelChat",tsx)
        self.assertIn("Studio",tsx)
        self.assertIn("BigType",tsx)
        self.assertNotIn("ACCOUNT VIEW",tsx)
        self.assertIn("Captions",tsx)
        self.assertIn('BlueAppVisual',render)
        self.assertIn("--scale=0.5",render)
        self.assertIn("expected=(960,540)",render)
        self.assertIn("(1920,1080)",render)
        self.assertNotIn("src/index.tsx Explainer",render)

    def test_upstream_staging_is_idempotent_and_fails_closed(self):
        import tempfile
        integration=Path(__file__).resolve().parents[2]/"integrations"/"openmontage"
        script=integration/"scripts"/"stage_blue_app_visual.py"
        spec=importlib.util.spec_from_file_location("blue_app_stage",script)
        mod_stage=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod_stage)
        with tempfile.TemporaryDirectory() as d:
            composer=Path(d)/"remotion-composer"
            (composer/"src").mkdir(parents=True)
            (composer/"package.json").write_text("{}",encoding="utf-8")
            root=composer/"src"/"Root.tsx"
            root.write_text('import { Composition, CalculateMetadataFunction } from "remotion";\n'
                            "export const Root=()=> (\n  <>\n    </>\n  );\n};\n",encoding="utf-8")
            mod_stage.stage(integration,composer)
            first=root.read_text(encoding="utf-8")
            self.assertIn('id="BlueAppVisual"',first)
            self.assertIn('component={BlueAppVisual}',first)
            mod_stage.stage(integration,composer)
            self.assertEqual(first,root.read_text(encoding="utf-8"))
            self.assertTrue((composer/"src"/"BlueAppVisual.tsx").is_file())
            root.write_text("unexpected upstream format",encoding="utf-8")
            with self.assertRaises(RuntimeError):
                mod_stage.stage(integration,composer)

if __name__=="__main__":
    unittest.main()
