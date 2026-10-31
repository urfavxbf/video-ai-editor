"""Contract tests for Duik-authored *baked Bodymovin* assets; no AE required."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "import_duik_baked_lottie.py"
SPEC = importlib.util.spec_from_file_location("duik_import", SCRIPT)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

FIXTURE = ROOT / "src" / "after-effects" / "duik-imported.json"


class DuikImportTests(unittest.TestCase):
    def base(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_original_rig_style_vector_fixture_is_valid_and_animated(self):
        result = mod.validate_lottie(self.base())
        self.assertEqual(result["fps"], 30)
        self.assertEqual(result["width"], 900)
        self.assertGreater(result["animatedProperties"], 2)

    def test_rejects_unbaked_expression_property(self):
        obj = self.base()
        obj["layers"][0]["ks"]["r"]["x"] = "$bm_rt = effect('IK')('Angle')"
        with self.assertRaisesRegex(ValueError, "Unbaked expression"):
            mod.validate_lottie(obj)

    def test_rejects_remote_and_embedded_media(self):
        for value in ("https://example.org/x", "data:image/png;base64,abcd", "file:///etc/passwd"):
            with self.subTest(value=value):
                obj = self.base()
                obj["nm"] = value
                with self.assertRaisesRegex(ValueError, "External URLs"):
                    mod.validate_lottie(obj)
        obj = self.base()
        obj["assets"].append({"id":"img", "p":"file.png", "u":"assets/"})
        with self.assertRaisesRegex(ValueError, "images, media"):
            mod.validate_lottie(obj)

    def test_rejects_unsupported_rig_layers(self):
        for replacement in ({"ty":5}, {"ty":2}, {"ty":13}):
            with self.subTest(replacement=replacement):
                obj=self.base()
                obj["layers"][0].update(replacement)
                with self.assertRaisesRegex(ValueError, "only 2D"):
                    mod.validate_lottie(obj)

    def test_rejects_3d_masks_blend_and_bad_precomp(self):
        for key, value in (("ddd",1),("hasMask",True),("bm",2),("ef",[{"ty":5}])):
            with self.subTest(key=key):
                obj=self.base()
                obj["layers"][0][key]=value
                with self.assertRaises(ValueError):
                    mod.validate_lottie(obj)
        obj=self.base()
        obj["layers"][0]["ty"]=0
        obj["layers"][0]["refId"]="missing"
        with self.assertRaisesRegex(ValueError, "precomp"):
            mod.validate_lottie(obj)

    def test_accepts_vector_precompositions_only(self):
        obj=self.base()
        child=copy.deepcopy(obj["layers"][0])
        obj["assets"]=[{"id":"nested","layers":[child]}]
        obj["layers"][0]={"ind":50,"ty":0,"ddd":0,"bm":0,"refId":"nested",
                          "ks":copy.deepcopy(child["ks"])}
        result=mod.validate_lottie(obj)
        self.assertGreater(result["animatedProperties"],2)

    def test_rejects_wrong_fps_and_empty_animation(self):
        obj=self.base()
        obj["fr"]=60
        with self.assertRaisesRegex(ValueError, "frame rate"):
            mod.validate_lottie(obj)
        obj=self.base()
        for layer in obj["layers"]:
            for prop in layer["ks"].values():
                if isinstance(prop,dict) and prop.get("a")==1:
                    prop.update(a=0,k=0)
        with self.assertRaisesRegex(ValueError,"No animated"):
            mod.validate_lottie(obj)

    def test_import_is_atomic_and_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            source=root/"input.json"
            target=root/"nested"/"safe.json"
            source.write_text(json.dumps(self.base()),encoding="utf-8")
            outcome=mod.import_file(source,target)
            self.assertEqual(outcome["fps"],30)
            self.assertEqual(json.loads(target.read_text())["w"],900)
            source.write_text('{"v":""}',encoding="utf-8")
            with self.assertRaises(ValueError):
                mod.import_file(source,target)
            self.assertEqual(json.loads(target.read_text())["w"],900)
            link=root/"linked.json"
            link.symlink_to(target)
            with self.assertRaisesRegex(ValueError,"symlink"):
                mod.import_file(link,root/"else.json")
            source.write_text(json.dumps(self.base()),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"symlink"):
                mod.import_file(source,link)

    def test_rejects_nonfinite_limits_and_deep_objects(self):
        for key,value in (("w",0),("h",6000),("op",18001),("ip",-1),("fr",12)):
            obj=self.base()
            obj[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                mod.validate_lottie(obj)


if __name__=="__main__":
    unittest.main()
