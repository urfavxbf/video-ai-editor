"""Validate original procedural glTF assets without third-party dependencies."""
import base64
import json
from pathlib import Path
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"public/characters/3d"

class Rigged3DModelsTests(unittest.TestCase):
    def test_models_are_real_animated_gltf(self):
        expected={
            "urfavxbf":{"idle","walk","run","point_camera","point_object","talk","laugh","jump","explain","wave"},
            "pix":{"idle","walk","talk","laugh","jump","pounce","tail_wag","curious","assist_point","wave"}
        }
        for character,actions in expected.items():
            with self.subTest(character=character):
                data=json.loads((OUT/(character+".gltf")).read_text(encoding="utf-8"))
                self.assertEqual(data["asset"]["version"],"2.0")
                self.assertEqual(data["extras"]["character"], character)
                self.assertFalse(data["extras"]["productionArtApproved"])
                self.assertGreater(len(data["meshes"]),10)
                names={n["name"] for n in data["nodes"]}
                self.assertIn("motion_root",names)
                self.assertIn("head_joint",names)
                self.assertIn("mouth_joint",names)
                self.assertEqual({a["name"] for a in data["animations"]},actions)
                raw=base64.b64decode(data["buffers"][0]["uri"].split(",",1)[1],validate=True)
                self.assertEqual(len(raw),data["buffers"][0]["byteLength"])
                for v in data["bufferViews"]:
                    self.assertEqual(v["byteOffset"]%4,0)
                    self.assertLessEqual(v["byteOffset"]+v["byteLength"],len(raw))
                for m in data["meshes"]:
                    for prim in m["primitives"]:
                        self.assertIn("POSITION",prim["attributes"])
                        self.assertIn("indices",prim)
                for a in data["animations"]:
                    self.assertTrue(a["channels"])
                    for c in a["channels"]:
                        self.assertLess(c["target"]["node"],len(data["nodes"]))
                        self.assertIn(c["target"]["path"],("rotation","translation","scale"))

    def test_generator_is_deterministic_and_registry_no_old_model_path(self):
        before={x.name:x.read_bytes() for x in OUT.glob("*.gltf")}
        self.assertEqual(set(before),{"urfavxbf.gltf","pix.gltf"})
        subprocess.run(["node","scripts/build-3d-models.mjs"],cwd=ROOT,check=True,capture_output=True)
        after={x.name:x.read_bytes() for x in OUT.glob("*.gltf")}
        self.assertEqual(before,after)
        registry=json.loads((ROOT/"characters/registry.json").read_text())
        self.assertEqual(registry["character_hero_system"]["version"],"procedural-3d-v1")
        for id in ("urfavxbf","pix"):
            v=registry["characters"][id]["visual"]
            self.assertEqual(v["model_path"],f"public/characters/3d/{id}.gltf")
            self.assertNotIn("public_path",v)
            self.assertIn("reference_source_sha256",v)
        self.assertEqual(registry["production_language"],"en")

if __name__=="__main__":
    unittest.main()
