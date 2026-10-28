#!/usr/bin/env python3
"""Non-destructive V4 pixel-art source pose normalization + auditable QA.

All 171 source-drawn poses retain their exact RGBA pixels (no new art is
invented). Output uses 128x128 canvas and common ground baseline y=112.
The source remains a DRAFT and is not a production-ready 72-action set.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from statistics import median
from PIL import Image

SIZE=(128,128)
GROUND=112

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def convert_action(files:list[Path],folder:Path)->dict:
    images=[Image.open(p).convert("RGBA") for p in files]
    if not images or any(im.size!=(64,78) for im in images):
        raise ValueError("Expected one or more unmodified 64x78 RGBA source poses")
    boxes=[im.getchannel("A").getbbox() for im in images]
    if any(b is None for b in boxes):
        raise ValueError("Empty original sprite")
    mid=median([(b[0]+b[2])/2 for b in boxes])
    folder.mkdir(parents=True,exist_ok=True)
    rows=[]
    for i,(path,image,box) in enumerate(zip(files,images,boxes)):
        correction=max(-5,min(5,round(mid-(box[0]+box[2])/2)))
        dst=Image.new("RGBA",SIZE,(0,0,0,0))
        dst.alpha_composite(image,(32+correction,GROUND-78))
        target=folder/f"{i:03d}.png"
        dst.save(target,optimize=True)
        visible=sum(image.getchannel("A").histogram()[1:])
        converted=sum(dst.getchannel("A").histogram()[1:])
        if visible!=converted:
            raise ValueError(f"Alpha pixel count changed: {path}")
        rows.append({"source":path.name,"sourceSha256":sha(path),
                     "normalizedSha256":sha(target),"visiblePixels":visible,
                     "xCorrection":correction,"sourceBounds":list(box),
                     "targetBounds":list(dst.getchannel("A").getbbox()),
                     "alphaPreserved":True})
    ratios=[rows[i]["visiblePixels"]/max(1,rows[i-1]["visiblePixels"])
            for i in range(1,len(rows))]
    warnings=[]
    if len(rows)<6:warnings.append("Fewer than 6 original drawings; not an 8-frame cycle")
    for i,ratio in enumerate(ratios,1):
        if ratio>1.5 or ratio<0.67:
            warnings.append(f"Frame {i}: unexpected occupied-area ratio {ratio:.3f}")
    return {"sourceFrames":len(rows),"canvas":list(SIZE),
            "groundBaseline":GROUND,"warnings":warnings,"frames":rows}

def normalize(source:Path,out:Path)->dict:
    info={"format":"chibi-v4-normalization-v1","status":"draft-art-review-required",
          "newInbetweens":0,"phonemeAlignedMouthShapes":0,
          "hairRigApproved":False,"characters":{},"canvas":list(SIZE)}
    n=0
    for character in ("urfavxbf","pix"):
        origin=source/character
        if not origin.is_dir():raise ValueError(f"Missing source for {character}")
        info["characters"][character]={}
        for folder in sorted(origin.iterdir()):
            if not folder.is_dir() or folder.name in ("mouth-refs","face-refs"):
                continue
            files=sorted(folder.glob("[0-9][0-9][0-9].png"))
            if not files:continue
            result=convert_action(files,out/character/folder.name)
            info["characters"][character][folder.name]=result
            n+=len(files)
    if n!=171:raise ValueError(f"Expected 171 original motion poses; got {n}")
    (out/"quality-report.json").write_text(json.dumps(info,indent=2)+"\n",encoding="utf-8")
    return info

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True,type=Path,
        help="private original public/characters/animation-v4 directory")
    parser.add_argument("--out",required=True,type=Path,
        help="private public/characters/animation-v4-normalized directory")
    args=parser.parse_args()
    output=normalize(args.source,args.out)
    print(json.dumps({name:sum(x["sourceFrames"] for x in items.values())
                      for name,items in output["characters"].items()}))
