#!/usr/bin/env python3
"""Extract distinct whole-character pose tiles from a CHROMA background grid.

This is not animation synthesis. A grid of separate drawings yields separate
pose studies. Never claim motion-loop coverage or manufacture inbetweens.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image

def magenta(pixel:tuple[int,int,int])->bool:
    r,g,b=pixel
    return r>155 and b>150 and g<135 and abs(r-b)<90

def extract(source:Path,columns:int,rows:int,out:Path,character:str)->dict:
    if character not in ("urfavxbf","pix"):
        raise ValueError("Unknown canonical character")
    if not source.is_file() or source.is_symlink():
        raise ValueError("Source image missing or symlinked")
    if not 1<=columns<=16 or not 1<=rows<=16 or columns*rows>64:
        raise ValueError("Invalid pose sheet grid")
    if out.exists():
        raise FileExistsError("Output already exists; do not overwrite artist work")
    with Image.open(source) as img:
        if img.format!="PNG":
            raise ValueError("A lossless PNG source sheet is required")
        raw=img.convert("RGB")
    w,h=raw.size
    if w%columns or h%rows or w//columns<128 or h//rows<128:
        raise ValueError("Invalid sheet grid dimensions; do not resample")
    bw,bh=w//columns,h//rows
    records=[]
    out.mkdir(parents=True)
    try:
        for i in range(columns*rows):
            x=(i%columns)*bw;y=(i//columns)*bh
            tile=raw.crop((x,y,x+bw,y+bh))
            rgb=list(tile.getdata())
            if sum(magenta(v) for v in (tile.getpixel((0,0)),tile.getpixel((bw-1,0)),
                          tile.getpixel((0,bh-1)),tile.getpixel((bw-1,bh-1))))<4:
                raise ValueError(f"Tile {i} does not have four chroma corners")
            alpha=Image.new("L",(bw,bh))
            alpha.putdata([0 if magenta(pixel) else 255 for pixel in rgb])
            bbox=alpha.getbbox()
            if bbox is None:
                raise ValueError(f"Empty pose tile {i}")
            if bbox[2]-bbox[0]<bw//5 or bbox[3]-bbox[1]<bh//5:
                raise ValueError(f"Pose tile {i} suspiciously empty")
            rgba=tile.convert("RGBA");rgba.putalpha(alpha)
            filename=f"{i:03d}.png"
            target=out/filename
            rgba.save(target,optimize=True)
            records.append({
                "file":filename,"sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
                "canvas":[bw,bh],"alphaBounds":list(bbox),
                "clippedAtEdge":any((bbox[0]<=1,bbox[1]<=1,bbox[2]>=bw-1,bbox[3]>=bh-1)),
                "needsVisualReview":True,
            })
        data={
            "schema":"video-ai-editor/pose-study-extraction/v1",
            "character":character,"sourceReference":"canonical-2026-10-29",
            "sourceSha256":hashlib.sha256(source.read_bytes()).hexdigest(),
            "method":"independent-pose-cells-chroma-key-NOT-cutout-puppetry",
            "frames":records,"artApproved":False,"motionReviewed":False,
            "isAnimationLoop":False,
            "note":"Pose studies are not timed coherent motions. Never mark as complete actions.",
        }
        (out/"manifest.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
        return data
    except BaseException:
        import shutil
        shutil.rmtree(out)
        raise

def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--columns",required=True,type=int)
    p.add_argument("--rows",required=True,type=int)
    p.add_argument("--character",required=True)
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    try:
        result=extract(args.source,args.columns,args.rows,args.out,args.character)
        print(json.dumps({"status":"POSE_STUDY_UNREVIEWED","frames":len(result["frames"]),
                          "clipsDetected":sum(x["clippedAtEdge"] for x in result["frames"])},indent=2))
        return 0
    except (OSError,ValueError,KeyError) as exc:
        print(f"POSE EXTRACTION BLOCKED: {exc}",file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
