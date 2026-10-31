#!/usr/bin/env python3
"""Build original animated UrFavXBF + PIX source for 12 advanced FX with matching mattes.
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
    # Five contrasting visual environments rather than the rejected dark grid template.
    palettes=[(245,222,200),(46,42,98),(252,169,133),(22,101,120),(190,154,220)]
    accents=[(241,89,90),(145,125,251),(255,220,111),(75,232,185),(246,130,189)]
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
            # Original animated shapes, color fields and independently moving layers.
            # No dark technical grid, fixed HUD, progress track or dashboard layout.
            accent=accents[(i//60)%len(accents)]
            wave=math.sin(t*1.65)
            d.ellipse((-250+int(30*wave),-210,540+int(40*wave),600),
                      fill=(*accent,46))
            d.ellipse((180+int(45*math.cos(t*.9)),400,820,1090),
                      fill=(255,255,255,29))
            d.polygon([(-180,720+int(t*28)),(120,340+int(45*wave)),
                       (450,100+int(30*math.cos(t))), (670,320),
                       (210,930),(-180,1050)],fill=(*accent,30))
            for k in range(14):
                xx=int((k*101 + i*(1.1+.09*k))%(W+140))-70
                yy=int((k*157+i*(.8+.06*k))%(H+120))-60
                rad=12+(k%6)*6
                d.ellipse((xx-rad,yy-rad,xx+rad,yy+rad),
                          fill=(255,255,255,18+(k%4)*6))
            # A small PIX cameo appears as a secondary graphic; the host matte stays correct.
            px=22+int(8*math.sin(t*1.4))
            py=665+int(9*math.sin(t*2.1))
            image.paste(sidekick,(px,py),sidekick)
            # Host animation is an actual sequence of pose changes and bobs.
            sway=int(24*math.sin(t*1.7)+6*math.sin(t*5.3))
            bob=int(18*math.sin(t*2.5))
            x=(W-host.width)//2+sway
            y=365+bob
            matte=Image.new("RGBA",(W,H),(0,0,0,0))
            matte.alpha_composite(host,(x,y))
            sticker=Image.new("RGBA",(W,H),(0,0,0,0))
            sticker.alpha_composite(outlined,(x,y))
            image.paste(matte,(0,0),matte)
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
