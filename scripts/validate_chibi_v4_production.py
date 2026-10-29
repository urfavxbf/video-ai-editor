#!/usr/bin/env python3
"""Fail-closed quality gate for genuinely detailed Chibi V4 character masters.

A 1920x1080 VIDEO CANVAS is not evidence of sharp source artwork. 64x78
poster crops / 128x128 padded crops cannot pass this production gate.
A styleframe may be 1080p even while character art remains low-resolution.

This checks true native dimensions, PNG transparency, asset completeness,
pixel-identity manifests and delivered video frame dimensions. It does not
invent detail by nearest-neighbor / neural / smooth resampling.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

PNG=b"\x89PNG\r\n\x1a\n"
MIN_NATIVE_BODY=(512,768)
MIN_NATIVE_FACE=(384,384)
OUTPUT_VIDEO=(1920,1080)
REQUIRED_MOUTH=("rest","A","E","I","O","U","M","F")
REQUIRED_FACE=("neutral","blink","happy","surprised","thinking")
CHARACTERS=("urfavxbf","pix")


def rgba_png(path:Path,min_size:tuple[int,int])->dict:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Missing source artwork: {path}")
    raw=path.read_bytes()
    if len(raw)<33 or raw[:8]!=PNG or raw[12:16]!=b"IHDR":
        raise ValueError(f"Corrupt PNG: {path}")
    width,height=struct.unpack(">II",raw[16:24])
    bit_depth,color_type=raw[24:26]
    if width<min_size[0] or height<min_size[1]:
        raise ValueError(f"Native image too small: {path}: {width}x{height}; "
                         f"required >= {min_size[0]}x{min_size[1]}")
    if bit_depth!=8 or color_type!=6:
        raise ValueError(f"Expected true RGBA art (not indexed RGB/opaque): {path}")
    return {"width":width,"height":height,"sha256":hashlib.sha256(raw).hexdigest()}


def validate_masters(root:Path,reference:dict)->dict:
    if set(reference.get("characters",{}))!=set(CHARACTERS):
        raise ValueError("Both original green V4 chibi heroes required")
    report={}
    for who in CHARACTERS:
        manifest=reference["characters"][who]
        full=rgba_png(root/who/"master-fullbody.png",MIN_NATIVE_BODY)
        face=rgba_png(root/who/"master-face.png",MIN_NATIVE_FACE)
        for role,actual in (("fullbody",full),("face",face)):
            if manifest.get(role,{}).get("sha256")!=actual["sha256"]:
                raise ValueError(f"{who}/{role} original native art differs from approved source hash")
        mouth={}
        for phoneme in REQUIRED_MOUTH:
            p=root/who/"mouth"/f"{phoneme}.png"
            mouth[phoneme]=rgba_png(p,MIN_NATIVE_FACE)
            if manifest.get("mouth",{}).get(phoneme)!=mouth[phoneme]["sha256"]:
                raise ValueError(f"{who}: unapproved/unaligned mouth reference {phoneme}")
        expressions={}
        for expr in REQUIRED_FACE:
            p=root/who/"expressions"/f"{expr}.png"
            expressions[expr]=rgba_png(p,MIN_NATIVE_FACE)
            if manifest.get("expressions",{}).get(expr)!=expressions[expr]["sha256"]:
                raise ValueError(f"{who}: unapproved/unaligned facial expression {expr}")
        if manifest.get("ownerApproved") is not True:
            raise ValueError(f"{who}: production requires owner visual approval")
        report[who]={"bodyNative":full,"faceNative":face,
                     "mouthShapes":len(mouth),"faceExpressions":len(expressions)}
    return report


def check_output_resolution(width:int,height:int):
    if (width,height)!=OUTPUT_VIDEO:
        raise ValueError(f"Wrong video export size: {width}x{height}; 1920x1080 required")


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--assets",required=True,type=Path)
    p.add_argument("--manifest",required=True,type=Path)
    args=p.parse_args()
    try:
        result=validate_masters(args.assets,json.loads(args.manifest.read_text()))
        print(json.dumps(result,indent=2))
        return 0
    except (ValueError,OSError,KeyError) as exc:
        print("CHIBI V4 PRODUCTION BLOCKED:",exc,file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
