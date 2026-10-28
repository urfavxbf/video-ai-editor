"""Guard against confusing 1080p canvas with native character artwork quality."""
import importlib.util
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("v4production",ROOT/"scripts"/"validate_chibi_v4_production.py")
gate=importlib.util.module_from_spec(spec)
sys.modules["v4production"]=gate
spec.loader.exec_module(gate)


def png(path:Path,w:int,h:int)->None:
    def chunk(t:bytes,p:bytes)->bytes:
        return struct.pack(">I",len(p))+t+p+struct.pack(">I",zlib.crc32(t+p)&0xffffffff)
    path.parent.mkdir(parents=True,exist_ok=True)
    scanlines=b"".join(b"\x00"+b"\0\xdd\x66\xff"*w for _ in range(h))
    raw=gate.PNG+chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))
    raw+=chunk(b"IDAT",zlib.compress(scanlines,1))+chunk(b"IEND",b"")
    path.write_bytes(raw)


class NativeV4QualityTests(unittest.TestCase):
    def test_64px_pose_cannot_pass_even_with_1080p_container(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"draft.png"
            png(path,64,78)
            with self.assertRaisesRegex(ValueError,"Native image too small"):
                gate.rgba_png(path,gate.MIN_NATIVE_BODY)
            gate.check_output_resolution(1920,1080)

    def test_padding_or_128x128_does_not_create_true_master(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"padded.png"
            png(p,128,128)
            with self.assertRaisesRegex(ValueError,"Native image too small"):
                gate.rgba_png(p,gate.MIN_NATIVE_BODY)

    def test_720p_is_not_1080p(self):
        with self.assertRaisesRegex(ValueError,"1920x1080 required"):
            gate.check_output_resolution(1280,720)
        gate.check_output_resolution(1920,1080)

    def test_full_native_source_is_readable_and_sha_pinned(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"body.png"
            png(path,512,768)
            result=gate.rgba_png(path,gate.MIN_NATIVE_BODY)
            self.assertEqual((result["width"],result["height"]),(512,768))
            self.assertEqual(len(result["sha256"]),64)

    def test_owner_approval_is_explicit_not_implied_by_1080p(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name in gate.CHARACTERS:
                png(root/name/"master-fullbody.png",512,768)
                png(root/name/"master-face.png",384,384)
                for key in gate.REQUIRED_MOUTH:
                    png(root/name/"mouth"/(key+".png"),384,384)
                for key in gate.REQUIRED_FACE:
                    png(root/name/"expressions"/(key+".png"),384,384)
            import hashlib
            manifest={"characters":{}}
            for name in gate.CHARACTERS:
                base=root/name
                digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
                manifest["characters"][name]={
                    "fullbody":{"sha256":digest(base/"master-fullbody.png")},
                    "face":{"sha256":digest(base/"master-face.png")},
                    "mouth":{k:digest(base/"mouth"/(k+".png")) for k in gate.REQUIRED_MOUTH},
                    "expressions":{k:digest(base/"expressions"/(k+".png")) for k in gate.REQUIRED_FACE},
                    "ownerApproved":False,
                }
            with self.assertRaisesRegex(ValueError,"owner visual approval"):
                gate.validate_masters(root,manifest)


if __name__=="__main__":unittest.main()
