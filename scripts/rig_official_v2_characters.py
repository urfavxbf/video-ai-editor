#!/usr/bin/env python3
"""Extract real articulated pixel-art layers from approved Super Pixel V2 bases.

Requires Pillow and numpy (see requirements-character-rig.txt). Polygon
boundaries are hand-traced on the exact 560x768 original art, and must never be
applied to stock/generated substitutes. Regenerated neutral poses reproduce
the original pixels exactly; painted joint underlay is hidden at rest.
This produces 2D cutout motion, NOT 3D, unverified visemes, or a 4-legged PIX.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

OFFICIAL = {
    "urfavxbf": {
        "hash": "b11936a4ace7c6cba1ee391ff768fce93bee80b2adf81b3a44a89cbaa4cf01b4",
        "headPivotPercent": [54,43], "leftArmPivotPercent": [37,47],
        "rightArmPivotPercent": [72,48], "leftLegPivotPercent": [41,73],
        "rightLegPivotPercent": [63,73],
    },
    "pix": {
        "hash": "cc5ecccdbb74b8c90ea3af09a0c75ff2c72db05fcdf0006fdc19255641304c6f",
        "headPivotPercent": [44,69], "leftArmPivotPercent": [31,74],
        "rightArmPivotPercent": [50,75], "tailPivotPercent": [66,71],
    },
}

# Exactly the original 560x768 source coordinates, hand traced. PIX's arms are
# the two visible front legs; her hind legs are not isolated in the reference.
MASKS = {
  "urfavxbf": {
     "head": [(0,0),(560,0),(560,287),(492,286),(472,298),(436,311),
              (412,311),(400,324),(372,337),(353,346),(324,363),
              (305,358),(274,337),(249,328),(219,304),(191,293),
              (125,311),(80,310),(0,307)],
     "leftArm": [(187,330),(221,342),(250,366),(269,401),
                 (263,442),(253,481),(237,518),(220,556),(176,564),
                 (137,556),(108,543),(70,501),(62,466),(80,428),
                 (115,397),(145,364)],
     "rightArm": [(366,338),(405,329),(446,351),(463,406),
                  (486,449),(500,483),(493,519),(473,555),(498,581),
                  (479,600),(452,616),(422,607),(392,586),
                  (389,551),(379,520),(366,474),(361,423)],
     "leftLeg": [(160,544),(269,539),(283,566),(282,608),(280,653),
                 (260,701),(272,759),(76,759),(96,716),(115,671),
                 (144,619)],
     "rightLeg": [(277,537),(370,527),(414,559),(429,609),
                  (434,646),(476,677),(511,758),(276,758),
                  (278,707),(286,678),(286,633)],
  },
  "pix": {
     "tail": [(342,446),(389,458),(425,467),(498,469),
              (556,490),(560,765),(360,765),(360,725),(375,691),
              (357,650),(347,615),(337,567)],
     "head": [(0,150),(560,150),(560,358),(468,357),(465,461),
              (443,488),(416,506),(375,521),(338,535),(306,545),
              (262,548),(208,549),(166,542),(124,525),(85,513),
              (25,503),(0,493)],
     "leftArm": [(155,552),(204,542),(230,558),(224,614),
                 (221,664),(218,723),(217,759),(58,759),(66,714),
                 (87,679),(101,640),(124,606)],
     "rightArm": [(244,543),(302,546),(332,563),(352,605),
                  (359,665),(373,759),(190,759),(199,709),
                  (216,663),(218,601)],
  },
}

Z_ORDER = ("tail","leftLeg","rightLeg","body","leftArm","rightArm","head")


def polygon(shape: tuple[int,int], points: list[tuple[int,int]]) -> np.ndarray:
    mask = Image.new("L",shape,0)
    ImageDraw.Draw(mask).polygon(points,fill=255)
    return np.asarray(mask,dtype=np.uint8)>0


def joint_underlay(character: str, source: Image.Image) -> Image.Image:
    back = Image.new("RGBA",source.size,(0,0,0,0))
    draw = ImageDraw.Draw(back)
    if character=="urfavxbf":
        draw.ellipse((211,286,392,410),fill=(20,17,27,255))
        draw.polygon([(176,350),(270,350),(291,434),(278,568),
                      (197,577),(170,512)],fill=(29,25,42,255))
        draw.polygon([(360,345),(438,344),(455,500),
                      (436,594),(366,572)],fill=(30,25,43,255))
        draw.rounded_rectangle((180,539,415,662),radius=30,fill=(31,27,45,255))
        draw.polygon([(257,407),(282,400),(290,550),(260,556)],fill=(231,165,4,255))
    else:
        draw.ellipse((122,490,365,643),fill=(38,31,63,255))
        draw.rounded_rectangle((122,540,349,746),radius=65,fill=(132,111,186,255))
        draw.ellipse((118,555,247,741),fill=(153,125,206,255))
        draw.ellipse((219,560,355,745),fill=(157,127,211,255))
        draw.ellipse((329,480,432,680),fill=(36,47,77,255))
    # No new silhouette at rest: restrict subsurface fill to opaque original art.
    pixels=np.array(back)
    original=np.asarray(source)
    pixels[:,:,3]=np.where(original[:,:,3]>253,pixels[:,:,3],0).astype(np.uint8)
    return Image.fromarray(pixels,"RGBA")


def extract(character:str, source:Path, public_characters_dir:Path) -> dict:
    if character not in OFFICIAL:
        raise ValueError("Unknown approved protagonist")
    if not source.is_file() or source.is_symlink():
        raise ValueError(f"Original PNG absent: {source}")
    official=OFFICIAL[character]
    if hashlib.sha256(source.read_bytes()).hexdigest()!=official["hash"]:
        raise ValueError(f"{character}: official V2 source SHA-256 mismatch")
    image=Image.open(source).convert("RGBA")
    if image.size!=(560,768):
        raise ValueError("Expected source art at exact 560x768")
    original=np.array(image)
    alpha=original[:,:,3]
    masks={key:polygon(image.size,points) for key,points in MASKS[character].items()}
    masks["body"]=~np.logical_or.reduce(list(masks.values()))
    layers={}
    assigned=np.zeros(alpha.shape,bool)
    for key in reversed(Z_ORDER):
        if key not in masks:continue
        region=masks[key]&~assigned
        pixels=original.copy()
        pixels[:,:,3]=np.where(region,alpha,0).astype(np.uint8)
        layers[key]=Image.fromarray(pixels,"RGBA")
        assigned|=region
    if not np.all(assigned):
        raise ValueError("Rig artwork is incomplete")
    layers["underlay"]=joint_underlay(character,image)
    root=public_characters_dir/character
    rig_dir=root/"rig"
    rig_dir.mkdir(parents=True,exist_ok=True)
    if source.resolve() != (root/"base.png").resolve():
        shutil.copy2(source,root/"base.png")  # Preserve byte-exact canonical PNG SHA-256
    for key,layer in layers.items():
        layer.save(rig_dir/f"{key}.png",compress_level=9)
    neutral=Image.new("RGBA",image.size)
    for key in ("underlay",*Z_ORDER):
        if key in layers:neutral.alpha_composite(layers[key])
    reproduced=np.array(neutral)
    mismatch_rate=float(np.mean(np.any(reproduced!=original,axis=2)))
    if mismatch_rate>0.00001:
        raise ValueError(f"{character}: neutral frame changed {mismatch_rate:.4%} of pixels")
    neutral.save(rig_dir/"neutral-reconstruction.png")
    paths={
        "underlay":f"characters/pixel-glitch/{character}/rig/underlay.png",
        **{key:f"characters/pixel-glitch/{character}/rig/{key}.png"
           for key in Z_ORDER if key!="body" and key in layers},
        "body":f"characters/pixel-glitch/{character}/rig/body.png",
        **{key:value for key,value in official.items() if key.endswith("PivotPercent")},
    }
    return {
        "assetPath":f"characters/pixel-glitch/{character}/base.png",
        "layeredRig":paths,
        "sourceSHA256":official["hash"],
        "canvas":[560,768],
        "neutralPixelMismatchRate":mismatch_rate,
        "riggingMethod":"manually traced original cutout polygons, source-accurate neutral",
    }


def generate(urfavxbf:Path,pix:Path,public_characters_dir:Path)->dict:
    output={}
    for character,path in (("urfavxbf",urfavxbf),("pix",pix)):
        output[character]=extract(character,path,public_characters_dir)
    render_manifest={key:{
        "assetPath":value["assetPath"],"layeredRig":value["layeredRig"]
    } for key,value in output.items()}
    public_characters_dir.mkdir(parents=True,exist_ok=True)
    (public_characters_dir/"rig-assets.json").write_text(
        json.dumps(render_manifest,indent=2)+"\n",encoding="utf-8")
    (public_characters_dir/"rig-provenance.json").write_text(
        json.dumps(output,indent=2)+"\n",encoding="utf-8")
    return output


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--urfavxbf",required=True,type=Path)
    parser.add_argument("--pix",required=True,type=Path)
    parser.add_argument("--out",type=Path,default=Path("public/characters/pixel-glitch"))
    args=parser.parse_args()
    try:
        result=generate(args.urfavxbf,args.pix,args.out)
        print(json.dumps(result,indent=2))
        return 0
    except (OSError,ValueError) as exc:
        print("Rig extraction blocked:",exc,file=__import__("sys").stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
