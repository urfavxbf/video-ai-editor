"""Stage independently drawn UrFavXBF/PIX pixel poses from the review ZIP.

Run: python scripts/stage_pixel_pose_pack.py <path-to-zip>
Requires Pillow. Does not crop source sprite sheets or generate missing art.
"""
from __future__ import annotations
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile, BadZipFile
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "characters" / "pixel-pose-style-lock.json"
DST = ROOT / "public" / "characters" / "pixel-poses-v1"
ARCHIVE_FOLDER = "UrFavXBF_PIX_Pixel_Poses_v1"
MAX_PNG_BYTES = 4 * 1024 * 1024

def validated_assets(zip_path: Path, manifest_path: Path=SPEC_PATH):
    spec = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    items = []
    with ZipFile(zip_path) as z:
        for who, poses in spec["characterPoses"].items():
            for pose, item in poses.items():
                paths = [item["sourcePath"], item["exportPath"]]
                payloads = []
                for path in paths:
                    archive_path = ARCHIVE_FOLDER + "/" + path
                    obj = z.getinfo(archive_path)
                    if obj.file_size > MAX_PNG_BYTES:
                        raise ValueError(f"Oversized PNG: {archive_path}")
                    data = z.read(archive_path)
                    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                        raise ValueError(f"Not a PNG: {archive_path}")
                    payloads.append(data)
                from io import BytesIO
                native, upscaled = [Image.open(BytesIO(b)).convert("RGBA") for b in payloads]
                if native.size != (256, 256) or upscaled.size != (1024, 1024):
                    raise ValueError(f"Incorrect canvas size: {who}/{pose}")
                if native.getpixel((0,0))[3] != 0 or upscaled.getpixel((0,0))[3] != 0:
                    raise ValueError(f"Transparency missing: {who}/{pose}")
                expected_sha = item["sha256"]
                if hashlib.sha256(payloads[1]).hexdigest() != expected_sha:
                    raise ValueError(f"SHA256 mismatch: {who}/{pose}")
                upcheck = native.resize((1024, 1024), Image.Resampling.NEAREST)
                if ImageChops.difference(upcheck, upscaled).getbbox():
                    raise ValueError(f"Upscale is not nearest-neighbor pixel-perfect: {who}/{pose}")
                items.append((who, pose, payloads))
    if len(items) != 10:
        raise ValueError("Expected exactly ten pose assets")
    if len({hashlib.sha256(it[2][1]).hexdigest() for it in items}) != 10:
        raise ValueError("One or more individual poses are duplicate drawings")
    return items

def stage(zip_path: Path, out: Path=DST):
    items = validated_assets(zip_path)
    out=Path(out)
    if out.exists() and any(out.rglob("*.png")):
        raise FileExistsError(f"Asset directory already has poses: {out}")
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pixel-pose-",dir=out.parent) as td:
        tmp = Path(td) / "verified"
        for who, pose, payloads in items:
            dst = tmp / who
            dst.mkdir(parents=True,exist_ok=True)
            (dst / f"{pose}_native_256.png").write_bytes(payloads[0])
            (dst / f"{pose}.png").write_bytes(payloads[1])
        if out.exists() and any(out.iterdir()):
            raise FileExistsError(f"Output exists and is not empty: {out}")
        if out.exists():
            out.rmdir()
        shutil.move(str(tmp), str(out))
    return {"status":"STAGED_UNAPPROVED_FOR_REVIEW","exportedPoses":len(items),"output":str(out)}

def main(argv: list[str]):
    if len(argv) != 2:
        raise SystemExit("Usage: python scripts/stage_pixel_pose_pack.py /path/to/UrFavXBF_PIX_Individual_Pixel_Poses_v1.zip")
    report=stage(Path(argv[1]))
    print(json.dumps(report,indent=2))

if __name__ == "__main__":
    main(sys.argv)
