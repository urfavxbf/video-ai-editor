"""Rights-aware resource library checks: no paid API, network or downloads."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
import wave

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("resource_library",ROOT/"scripts/resource_library.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ResourceLibraryTests(unittest.TestCase):
    def make_image(self, path):
        from PIL import Image
        Image.new("RGB",(48,32),(15,72,120)).save(path,format="PNG")

    def args(self,path,**more):
        opts=dict(file=path,kind="image",slug="test-photo",license="owner-original",
                  creator="Original author",source_url="",license_url="",attribution="",
                  review_note="",rights_confirmed=True)
        opts.update(more)
        return SimpleNamespace(**opts)

    def test_existing_bundled_resources_and_license_review_flags(self):
        inventory=mod.read_json(mod.CATALOG)["builtIn"]
        self.assertEqual(len(inventory),18)
        self.assertEqual(sum(x["kind"]=="font" for x in inventory),3)
        self.assertEqual(sum(x["kind"]=="sfx" for x in inventory),13)
        self.assertEqual(sum(x["kind"]=="image" for x in inventory),2)
        self.assertTrue(all(x["rightsStatus"]=="review-before-publication" for x in inventory if x["kind"]=="sfx"))
        report=mod.audit()
        self.assertEqual(report["builtInVerified"],18)
        self.assertEqual(report["rightsReviewNeeded"],13)

    def test_source_index_covers_all_kinds_and_provides_licenses(self):
        entries=mod.read_json(ROOT/"resources/sources.json")["sources"]
        self.assertTrue({"video","image","font","music","sfx"} <= {k for e in entries for k in e["categories"]})
        self.assertTrue(all(e["url"].startswith("https://") and e["licenseUrl"].startswith("https://") for e in entries))

    def test_intake_atomic_receipt_and_hash_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp=Path(tmp)
            image=temp/"fresh.png";self.make_image(image)
            saved=(mod.PUBLIC,mod.DEST_ROOT,mod.LOCAL_CATALOG)
            mod.PUBLIC,mod.DEST_ROOT,mod.LOCAL_CATALOG=temp/"public",temp/"public/library",temp/"resources/local-catalog.json"
            try:
                outcome=mod.intake(self.args(image))
                self.assertEqual(outcome["path"],"library/image/test-photo.png")
                self.assertEqual(outcome["details"]["width"],48)
                self.assertEqual(mod.audit()["localVerified"],1)
                with self.assertRaisesRegex(ValueError,"already exists"):
                    mod.intake(self.args(image))
                (mod.PUBLIC/outcome["path"]).write_bytes(b"tampered")
                with self.assertRaisesRegex(ValueError,"hash mismatch"):
                    mod.audit()
            finally:
                mod.PUBLIC,mod.DEST_ROOT,mod.LOCAL_CATALOG=saved

    def test_rejects_noncommercial_unreviewed_and_bad_attribution(self):
        with tempfile.TemporaryDirectory() as tmp:
            image=Path(tmp)/"image.png";self.make_image(image)
            bad=[
                self.args(image,rights_confirmed=False),
                self.args(image,license="CC-BY-NC-4.0"),
                self.args(image,license="CC-BY-4.0",source_url="https://example.org/item",license_url="https://example.org/license"),
                self.args(image,license="Pexels License",source_url="http://example.org/item",license_url="https://example.org/license"),
                self.args(image,slug="../../escape"),
                self.args(image,creator=""),
            ]
            for case in bad:
                with self.subTest(case=case),self.assertRaises(ValueError):
                    mod.intake(case)

    def test_rejects_bad_image_and_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);good=root/"good.png";self.make_image(good)
            link=root/"link.png";link.symlink_to(good)
            with self.assertRaisesRegex(ValueError,"symlink"):
                mod.intake(self.args(link))
            bad=root/"bad.png";bad.write_text("invalid image")
            with self.assertRaisesRegex(ValueError,"image payload"):
                mod.intake(self.args(bad))

    def test_original_svgs_are_local_and_safe(self):
        for fn in ("neon-grid.svg","orbit-lines.svg"):
            self.assertEqual(mod.probe(ROOT/"public/resources/original"/fn,"vector")["format"],"svg")
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bad.svg"
            p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>bad()</script></svg>')
            with self.assertRaisesRegex(ValueError,"unsafe"):
                mod.probe(p,"vector")

    def test_original_audio_generator_produces_pcm16_stereo(self):
        spec2=importlib.util.spec_from_file_location("ambient_gen",ROOT/"scripts/generate_original_ambient.py")
        a=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(a)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"ambient.wav";a.generate(p)
            with wave.open(str(p)) as w:
                self.assertEqual((w.getframerate(),w.getnframes(),w.getnchannels()),(48000,384000,2))
            self.assertGreater(p.stat().st_size,1_500_000)
            with self.assertRaises(FileExistsError):a.generate(p)

    def test_original_broll_composition_is_registered(self):
        root=(ROOT/"src/Root.tsx").read_text()
        self.assertIn('id="ResourceLibraryProof"',root)
        code=(ROOT/"src/resources/ResourceLibraryProof.tsx").read_text()
        self.assertIn("resources/original/neon-grid.svg",code)
        self.assertIn("resources/original/orbit-lines.svg",code)
if __name__=="__main__":
    unittest.main()
