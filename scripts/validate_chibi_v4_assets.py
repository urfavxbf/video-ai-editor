#!/usr/bin/env python3
"""Validate owner-reviewed future Chibi V4 ZIP or staged files against source art.

The new pack contains actual 171 distinct-pose source frame files and reference
mouth/face tiles, but is DRAFT. Never equate 3-5 source poses to a complete 8
frame walk cycle or exact phoneme lip-sync. No GPU dependencies needed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
from zipfile import ZipFile

PNG_HEADER=b"\x89PNG\r\n\x1a\n"
EXPECTED={"urfavxbf":(23,85),"pix":(24,86)}


def png_meta(raw:bytes)->tuple[int,int,int]:
    if raw[:8]!=PNG_HEADER or raw[12:16]!=b"IHDR" or len(raw)<26:
        raise ValueError("Not a valid PNG header")
    w,h=struct.unpack(">II",raw[16:24])
    color=raw[25]
    return w,h,color


def check_manifest(manifest:dict)->dict:
    if manifest.get("version")!="v4-concept-extracted-draft":
        raise ValueError("Not the V4 source-drawn draft")
    if manifest.get("renderFps")!=30 or manifest.get("transparent") is not True:
        raise ValueError("Wrong timebase or alpha policy")
    if manifest.get("frameDrawingStatus")!="sourced-from-generated-concept-sheet-needs-artist-QA":
        raise ValueError("Unverified claims of completed new animations")
    if set(manifest.get("characters",{}))!=set(EXPECTED):
        raise ValueError("Both protagonists required")
    out={}
    for name, (actions, frames) in EXPECTED.items():
        c=manifest["characters"][name]
        pose=c["motions"]
        total=sum(len(v["frames"]) for v in pose.values())
        if len(pose)!=actions or total!=frames:
            raise ValueError(f"{name}: inaccurate action or pose count")
        if len(c["facialRefs"])!=10 or len(c["mouthRefs"])!=15:
            raise ValueError(f"{name}: incomplete facial/mouth reference sheet")
        for key,v in pose.items():
            if v["sourceFrames"]!=len(v["frames"]) or v["sourceFrames"]<1:
                raise ValueError(f"{name}/{key}: made-up frame count")
            if v["qualityGate"]!="draft-contact-sheet-extraction":
                raise ValueError(f"{name}/{key}: cannot skip draft review")
        out[name]={"actions":len(pose),"sourceFrames":total,
                   "expressionReferences":len(c["facialRefs"]),
                   "mouthReferences":len(c["mouthRefs"])}
    return out


def verify_bundle(zippath:Path)->dict:
    with ZipFile(zippath) as z:
        members=set(z.namelist())
        manifest=json.loads(z.read("sprite-v4-manifest.json"))
        summary=check_manifest(manifest)
        original=z.read(manifest["sourceSheet"])
        if hashlib.sha256(original).hexdigest()!=manifest["sourceSha256"]:
            raise ValueError("Source concept artwork differs from manifest")
        for character,c in manifest["characters"].items():
            sprites=[f for v in c["motions"].values() for f in v["frames"]]
            sprites+=list(c["facialRefs"].values())+list(c["mouthRefs"].values())
            for frame in sprites:
                path=frame["path"]
                if path not in members:raise ValueError(f"Missing PNG: {path}")
                data=z.read(path)
                if hashlib.sha256(data).hexdigest()!=frame["sha256"]:
                    raise ValueError(f"Altered PNG: {path}")
                if png_meta(data)!= (frame["width"],frame["height"],6):
                    raise ValueError(f"Wrong RGBA source dimensions: {path}")
        return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pack",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(verify_bundle(args.pack),indent=2))


if __name__=="__main__":
    main()
