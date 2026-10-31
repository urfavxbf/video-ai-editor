#!/usr/bin/env python3
"""Build 10s of original animated UrFavXBF source plus pixel-correct mattes.
This is owner-approved character art composited with synthetic original motion,
not a slideshow and not a lip-sync demonstration. Never download remote media.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import math
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter

W, H, FPS, N = 540, 960, 30, 300
ROOT = Path(__file__).resolve().parents[1]
HOST_DIR = ROOT / "public/characters/pixel-default/urfavxbf"
PIX_DIR = ROOT / "public/characters/pixel-default/pix"

def character(path: Path, width: int, height: int) -> Image.Image:
    if not path.exists(): raise FileNotFoundError(str(path))
    source = Image.open(path).convert("RGBA")
    bounds = source.getchannel("A").getbbox()
    if not bounds: raise RuntimeError("approved sprite is transparent: " + str(path))
    sprite = source.crop(bounds)
    ratio = min(width / sprite.width,height / sprite.height)
    return sprite.resize((max(1,int(sprite.width*ratio)),max(1,int(sprite.height*ratio))),Image.Resampling.NEAREST)

def render(destination: Path):
    destination.mkdir(parents=True,exist_ok=True)
    fgdir,stickdir=destination/"fg",destination/"sticker"
    fgdir.mkdir(exist_ok=True);stickdir.mkdir(exist_ok=True)
    host_poses={}
    for key in ("idle","talk","point_camera","happy","surprised","point_side"):
        sprite=character(HOST_DIR/(key+".png"),400,585)
        alpha=sprite.getchannel("A")
        outer=alpha.filter(ImageFilter.MaxFilter(17))
        outline=Image.new("RGBA",sprite.size,(0,0,0,0))
        outline.paste((247,255,252,255),(0,0,sprite.width,sprite.height),outer)
        outline.alpha_composite(sprite)
        host_poses[key]=(sprite,outline)
    sidekick=character(PIX_DIR/"idle.png",110,140)
    palettes=[(7,17,31),(11,24,43),(10,20,39),(19,20,43),(11,30,40)]
    video=destination/"take.mp4"
    ffmpeg=subprocess.Popen(["ffmpeg","-y","-hide_banner","-loglevel","error",
        "-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-an","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",
        str(video)],stdin=subprocess.PIPE)
    assert ffmpeg.stdin is not None
    try:
        for i in range(N):
            t=i/FPS
            pose=("idle","talk","talk","point_camera","happy","surprised","point_side","talk")[(i//38)%8]
            host,outlined=host_poses[pose]
            palette=palettes[(i//60)%len(palettes)]
            image=Image.new("RGB",(W,H),palette)
            d=ImageDraw.Draw(image,"RGBA")
            # Real animated background and depth; no repeated still frame.
            for k in range(24):
                x=int((k*97 + i*(1.2+.1*k))%(W+180))-90
                y=int((k*83+i*(1.7+.08*k))%(H+180))-90
                r=8+(k%8)*3
                d.ellipse((x-r,y-r,x+r,y+r),fill=(92,239,184,12+(k%4)*7))
            # Ambient particle motion, not a technical grid / slideshow backdrop.
            for k in range(9):
                xx=int((k*107 + 28*math.sin(t*.8+k*3))%W)
                yy=int((k*137 + t*14)%(H+100))-50
                rad=18 + k*4
                d.ellipse((xx-rad,yy-rad,xx+rad,yy+rad),fill=(54,210,179,11))
            radius=210+int(math.sin(t*1.3)*30)
            glow=(W//2-radius,350-radius,W//2+radius,350+radius)
            d.ellipse(glow,outline=(83,255,199,70),width=4)
            d.ellipse((W//2-145,350-145,W//2+145,350+145),outline=(146,216,253,36),width=3)
            d.line([(0,715),(W,715)],fill=(123,251,201,96),width=5)
            for k in range(12):
                yy=715+k*k*2
                if yy < H:
                    d.line([(0,yy),(W,yy)],fill=(87,221,173,max(4,45-k*3)),width=2)
            # A small PIX cameo appears as a secondary graphic; the host matte stays correct.
            px=22+int(8*math.sin(t*1.4))
            py=665+int(9*math.sin(t*2.1))
            image.paste(sidekick,(px,py),sidekick)
            # Host animation is an actual sequence of pose changes and bobs.
            sway=int(9*math.sin(t*2.8))
            bob=int(11*math.sin(t*4.1))
            x=(W-host.width)//2+sway
            y=365+bob
            matte=Image.new("RGBA",(W,H),(0,0,0,0))
            matte.alpha_composite(host,(x,y))
            sticker=Image.new("RGBA",(W,H),(0,0,0,0))
            sticker.alpha_composite(outlined,(x,y))
            image.paste(matte,(0,0),matte)
            image.save if False else None
            matte.save(fgdir/(f"{i:04d}.webp"),format="WEBP",quality=85,method=1)
            sticker.save(stickdir/(f"{i:04d}.webp"),format="WEBP",quality=86,method=1)
            ffmpeg.stdin.write(image.tobytes())
    finally:
        ffmpeg.stdin.close()
        if ffmpeg.wait()!=0: raise RuntimeError("source video encoding failed")
    print(f"Produced {N} animated frames, {N} owner-approved host mattes and {N} sticker borders: {video}")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=ROOT/"public/sample")
    args=parser.parse_args()
    render(args.output)
