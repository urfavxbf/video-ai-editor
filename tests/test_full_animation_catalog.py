"""Creative completeness is a contract, not a fake cutout-rig claim."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/"scripts"/"validate_full_animation_set.py"
spec=importlib.util.spec_from_file_location("animation_gate",path)
gate=importlib.util.module_from_spec(spec)
sys.modules["animation_gate"]=gate
spec.loader.exec_module(gate)
DATA=json.loads((ROOT/"characters"/"full-animation-set.json").read_text())


class FullHeroAnimationCatalogTests(unittest.TestCase):
    def test_spec_includes_all_seventy_two_requested_actions(self):
        stats=gate.validate_manifest(DATA)
        self.assertEqual({x:v["total"] for x,v in stats.items()},
                         {"urfavxbf":36,"pix":36})
        self.assertGreater(stats["urfavxbf"]["needs_new_art"],20)
        self.assertGreater(stats["pix"]["needs_new_art"],20)
        self.assertIn("hair_run",[x["id"] for x in DATA["characters"]["urfavxbf"]])
        self.assertIn("ride_shoulder",[x["id"] for x in DATA["characters"]["pix"]])
        self.assertTrue(DATA["policy"]["neverClaimFullBodyFromHeadOnly"])

    def test_no_fake_visemes_or_walk_cycles_claimed(self):
        for char,entries in DATA["characters"].items():
            for slot in entries:
                if slot["assetClass"] in {"viseme","full-body-cycle","hair-cycle",
                    "pose-sequence","facial-cycle","paired-staging"}:
                    self.assertEqual(slot["status"],"needs-new-animation-art",
                                     (char,slot["id"]))

    def test_fake_status_is_rejected(self):
        clone=copy.deepcopy(DATA)
        target=next(x for x in clone["characters"]["pix"] if x["id"]=="run_trot")
        target["status"]="available-closeup"
        with self.assertRaisesRegex(ValueError,"falsely marked ready"):
            gate.validate_manifest(clone)

    def test_incompatible_art_versions_rejected(self):
        clone=copy.deepcopy(DATA)
        clone["policy"]["sourceV2Sha256"]["pix"]="0"*64
        with self.assertRaisesRegex(ValueError,"Approved source art changed"):
            gate.validate_manifest(clone)

    def test_head_only_sprite_path_counts(self):
        self.assertEqual(DATA["existingSprites"]["loopFrames"],8)
        self.assertEqual(DATA["existingSprites"]["headLoopDimension"],[384,384])
        self.assertEqual(DATA["existingSprites"]["loopFps"],
                         {"idle":5,"talk":8,"react":8})


if __name__=="__main__":unittest.main()
