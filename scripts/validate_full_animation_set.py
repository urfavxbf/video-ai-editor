#!/usr/bin/env python3
"""Validate the COMPLETE creative animation spec without claiming missing artwork.

By default checks the repository manifest and exact sprite-path contract.
With --sprite-pack, additionally inspects actual original 48 head sprite PNGs
and exact expressions. No GPU, ffmpeg, or heavy vision model needed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"characters"/"full-animation-set.json"
IDS={"urfavxbf","pix"}
STATUSES={"available-closeup","available-composite","needs-new-animation-art","production-approved"}
CLASSES={"existing-head-loop","existing-expression","composite-vfx",
         "full-body-cycle","pose-sequence","viseme","facial-cycle",
         "hair-cycle","paired-staging"}
SOURCE_SPEC={
    "urfavxbf":{"loopActions":{"idle_normal":"idle","idle_talking":"talk"},
                "expressions":{"surprised":"surprised","laugh":"excited"}},
    "pix":{"loopActions":{"idle_sitting":"idle","meow_talk":"talk"},
           "expressions":{"happy_excited":"happy","curious":"curious",
                          "surprised":"surprised","head_tilt":"curious"}}
}
CANONICAL={
 "urfavxbf":"b11936a4ace7c6cba1ee391ff768fce93bee80b2adf81b3a44a89cbaa4cf01b4",
 "pix":"cc5ecccdbb74b8c90ea3af09a0c75ff2c72db05fcdf0006fdc19255641304c6f",
}


def validate_manifest(manifest:dict, animation_assets:Path|None=None)->dict:
    if manifest.get("fps")!=30 or manifest.get("version")!="1.0.0":
        raise ValueError("Invalid animation catalog version or frame rate")
    if set(manifest.get("characters",{}))!=IDS:
        raise ValueError("Precisely two official recurring protagonists required")
    if manifest.get("policy",{}).get("sourceV2Sha256")!=CANONICAL:
        raise ValueError("Approved source art changed")
    existing=manifest.get("existingSprites",{})
    if existing.get("headLoopDimension")!=[384,384] or existing.get("loopFrames")!=8:
        raise ValueError("Sprite pack is head-only, 8 frames at 384x384")
    stats={}
    for character,entries in manifest["characters"].items():
        names=[x.get("id") for x in entries]
        if len(names)!=len(set(names)) or len(names)<30:
            raise ValueError(f"{character} animation ID repeated or missing")
        for item in entries:
            if item["status"] not in STATUSES or item["assetClass"] not in CLASSES:
                raise ValueError("Unknown status or asset type")
            if item["minimumFrames"]<1 or item["proposedFps"]!=30:
                raise ValueError("Invalid frame contract")
            if item["status"]=="production-approved":
                approval=item.get("approval",{})
                if approval.get("ownerApproved") is not True or not approval.get("reviewedFrameRange"):
                    raise ValueError(f"{character}/{item['id']}: owner visual approval required")
                hashes=approval.get("frameSha256",[])
                if not isinstance(hashes,list) or len(hashes)!=item["minimumFrames"]:
                    raise ValueError(f"{character}/{item['id']}: every original frame must be SHA pinned")
                if animation_assets is None:
                    raise ValueError(f"{character}/{item['id']}: approved art must be verified locally")
                for i,sha in enumerate(hashes):
                    frame=(animation_assets/character/item["id"]/f"{i:03d}.png")
                    if not frame.is_file() or frame.is_symlink() or len(sha)!=64 or hashlib.sha256(frame.read_bytes()).hexdigest()!=sha:
                        raise ValueError(f"{character}/{item['id']}: frame {i} missing or altered")
                    if png_dimensions(frame.read_bytes())!=(560,768):
                        raise ValueError(f"{character}/{item['id']}: frame {i} must be 560x768")
            elif item["assetClass"] in {"viseme","hair-cycle","full-body-cycle",
                                      "pose-sequence","paired-staging","facial-cycle"}:
                if item["status"]!="needs-new-animation-art":
                    raise ValueError(f"{character}/{item['id']} falsely marked ready")
            if item["status"]=="available-closeup" and item["assetClass"] not in {
                "existing-head-loop","existing-expression"}:
                raise ValueError(f"{character}/{item['id']}: non-sprite marked ready")
            if item["status"]=="available-composite" and item["assetClass"]!="composite-vfx":
                raise ValueError("Compositing is not full-body animation")
        for viseme in ("A","E","I","O","U","M","F"):
            if f"mouth_{viseme}" not in names:
                raise ValueError(f"{character}: required viseme missing")
        for action in SOURCE_SPEC[character]["loopActions"]:
            entry=next(x for x in entries if x["id"]==action)
            if entry["status"]!="available-closeup":
                raise ValueError("Existing real sprite loop not acknowledged")
        stats[character]={
            "total":len(entries),
            "existing":sum(x["status"].startswith("available") for x in entries),
            "needs_new_art":sum(x["status"]=="needs-new-animation-art" for x in entries),
        }
    return stats


def png_dimensions(data:bytes)->tuple[int,int]:
    if data[:8]!=b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG")
    if data[12:16]!=b"IHDR" or len(data)<26:
        raise ValueError("Corrupted PNG header")
    return struct.unpack(">II",data[16:24])


def verify_sprite_zip(path:Path)->dict:
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    with zipfile.ZipFile(path) as archive:
        root="PixelGlitch_SpritePack/"
        expected=[]
        for char in IDS:
            expected.append((f"{root}{char}/base.png",(560,768),CANONICAL[char]))
            for name in manifest["existingSprites"][char]["expressions"]:
                expected.append((f"{root}{char}/{name}.png",(384,384),None))
            for mode in ("idle","talk","react"):
                for i in range(8):
                    expected.append((f"{root}{char}/loops/{mode}/{i:02d}.png",(384,384),None))
        missing=[name for name,_,_ in expected if name not in archive.namelist()]
        if missing:
            raise ValueError(f"Missing canonical sprite files: {missing[:5]}")
        for name,size,hash_ in expected:
            raw=archive.read(name)
            if png_dimensions(raw)!=size:
                raise ValueError(f"Wrong sprite size: {name}")
            if hash_ and hashlib.sha256(raw).hexdigest()!=hash_:
                raise ValueError(f"Unapproved canonical artwork: {name}")
        return {"verified_png_files":len(expected),
                "head_loop_frames":2*3*8,
                "true_viseme_frames":0,
                "new_full_body_cycles":0}


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sprite-pack",type=Path)
    p.add_argument("--animation-assets",type=Path,help="Private public/characters/animation-v4 root used to verify all future approved frame hashes")
    args=p.parse_args()
    try:
        s=validate_manifest(json.loads(MANIFEST.read_text(encoding="utf-8")),args.animation_assets)
        print(json.dumps({"catalog":s,
             "art_verified":verify_sprite_zip(args.sprite_pack) if args.sprite_pack else
               "not supplied (use --sprite-pack to check 48 real frames)"},indent=2))
        return 0
    except (ValueError, OSError, zipfile.BadZipFile) as e:
        print("ANIMATION VALIDATION FAILED:",e,file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
