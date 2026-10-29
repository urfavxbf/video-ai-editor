"""Stage and independently verify all 13 exact full-res RGBA PNGs.

Usage:
  python scripts/stage_pixel_default_pack.py /path/to/UrFavXBF_PIX_13_Pose_Production_Pack.zip
  python scripts/stage_pixel_default_pack.py --verify-workspace

No drawing/sheet cropping, no resampling, no paid services.
"""
from __future__ import annotations
import hashlib
import json
import sys
import zipfile
from io import BytesIO
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
COUNTS={"urfavxbf":6,"pix":7}

def manifest(root=ROOT):
    m=json.loads((Path(root)/"characters/pixel-default-manifest.json").read_text())
    if set(m["characters"])!=set(COUNTS):
        raise ValueError("Unexpected character identities")
    for who,count in COUNTS.items():
        if len(m["characters"][who]["poses"])!=count:
            raise ValueError("Incomplete pose manifest for "+who)
    return m

def check(path,raw,item):
    if path!=item["path"] or not path.startswith("public/characters/pixel-default/"):
        raise ValueError("Unsafe image path")
    if len(raw)!=item["bytes"] or hashlib.sha256(raw).hexdigest()!=item["sha256"]:
        raise ValueError("SHA-256 mismatch for "+path)
    if len(raw)>4_000_000 or not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Invalid PNG payload for "+path)
    im=Image.open(BytesIO(raw))
    im.load()
    if im.mode!="RGBA" or im.size!=(1254,1254):
        raise ValueError("Expected original 1254px RGBA: "+path)
    if im.getchannel("A").getextrema()!=(0,255) or im.getpixel((0,0))[3]!=0:
        raise ValueError("Expected transparent PNG: "+path)

def verified_archive(zip_path,root=ROOT):
    m=manifest(root)
    verified={}
    with zipfile.ZipFile(zip_path) as z:
        for who,desc in m["characters"].items():
            for pose,item in desc["poses"].items():
                path=f"public/characters/pixel-default/{who}/{pose}.png"
                info=z.getinfo(path)
                if info.file_size>4_000_000:
                    raise ValueError("Oversized image "+path)
                raw=z.read(info)
                check(path,raw,item)
                verified[path]=raw
    if len(verified)!=13:
        raise ValueError("Expected exactly 13 individual images")
    return verified

def stage(zip_path,root=ROOT):
    verified=verified_archive(zip_path,root)
    for path in verified:
        if (Path(root)/path).exists():raise FileExistsError(path)
    for path,raw in verified.items():
        p=Path(root)/path
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(raw)
    return len(verified)

def verify_workspace(root=ROOT):
    m=manifest(root)
    count=0
    for who,desc in m["characters"].items():
        for pose,item in desc["poses"].items():
            rel=f"public/characters/pixel-default/{who}/{pose}.png"
            p=Path(root)/rel
            if not p.is_file(): raise FileNotFoundError(rel)
            check(rel,p.read_bytes(),item)
            count+=1
    if count!=13:raise ValueError("Expected exactly 13 images")
    return count

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit(__doc__)
    if sys.argv[1]=="--verify-workspace":
        print("Verified workspace PNGs:",verify_workspace())
    else: print("Staged verified pose PNGs:",stage(Path(sys.argv[1])))
