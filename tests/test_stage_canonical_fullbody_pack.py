"""The privately delivered body pack can be staged only as a verified draft."""
from __future__ import annotations
import hashlib
from io import BytesIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import stage_canonical_fullbody_pack as stage


def png(seed: int, opaque: bool = False) -> bytes:
    im=Image.new("RGBA", (320, 384), (0,0,0,255) if opaque else (0,0,0,0))
    ImageDraw.Draw(im).ellipse((60+seed%8,20,280,350), fill=(90,235,230,255))
    buf=BytesIO();im.save(buf,format="PNG")
    return buf.getvalue()


def make_pack(path: Path, corrupt=False, opaque=False):
    manifest={"schema":"video-ai-editor/2.5d-review-pack/v1",
              "designVersion":"canonical-2026-10-29","ownerApprovedArt":False,
              "framesPerCharacter":56,"actions":list(stage.ACTIONS),"files":[]}
    with zipfile.ZipFile(path,"w",compression=zipfile.ZIP_DEFLATED) as archive:
        for who in stage.CHARS:
            paths=[f"public/characters/canonical/{who}/full-body.png"]
            paths += [f"animation-frames/{who}/{action}/{i:03d}.png"
                      for action in stage.ACTIONS for i in range(8)]
            for i,rel in enumerate(paths):
                b=png(i,opaque=opaque and rel.endswith("full-body.png"))
                archive.writestr(rel,b)
                manifest["files"].append({"path":rel,"size":len(b),
                     "sha256":hashlib.sha256(b).hexdigest()})
        if corrupt:
            manifest["files"][1]["sha256"]="f"*64
        archive.writestr("asset-package-manifest.json",json.dumps(manifest))


class CanonicalStageTests(unittest.TestCase):
    def test_verifies_every_frame_and_stages_reusable_paths_without_approval(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);pack=root/"sprites.zip";make_pack(pack)
            result=stage.validate_pack(pack)
            self.assertEqual(result["frames"],112)
            self.assertEqual(result["status"],"DRAFT_VERIFIED_NOT_APPROVED")
            status=stage.stage(pack,root/"public")
            self.assertEqual(status["frames"],112)
            target=root/"public/characters/canonical/pix/actions/celebrate/007.png"
            self.assertTrue(target.is_file())
            state=json.loads((root/"public/characters/canonical/review-status.json").read_text())
            self.assertFalse(state["ownerApprovedArt"])
            with self.assertRaises(FileExistsError):
                stage.stage(pack,root/"public")

    def test_digest_corruption_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            pack=Path(td)/"bad.zip";make_pack(pack,corrupt=True)
            with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
                stage.validate_pack(pack)

    def test_opaque_fake_art_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            pack=Path(td)/"opaque.zip";make_pack(pack,opaque=True)
            with self.assertRaisesRegex(ValueError,"opaque"):
                stage.validate_pack(pack)

    def test_path_traversal_denied(self):
        self.assertFalse(stage._allowed("../secrets.txt"))
        self.assertFalse(stage._allowed("public/characters/canonical/../escape.png"))
        self.assertFalse(stage._allowed("public/characters/pixel-glitch/urfavxbf/base.png"))
        self.assertTrue(stage._allowed("animation-frames/pix/wave/003.png"))


if __name__ == "__main__":
    unittest.main()
