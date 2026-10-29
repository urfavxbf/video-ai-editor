#!/usr/bin/env python3
"""Import existing GIF, transparent PNG frames or grid spritesheets into Remotion.

Based on the local-saving workflow in Spritesheets.ai's MIT-described
spritesheets-companion. No image generation, GPU, account access, credit
spending, watermark removal, or upscaling is performed.

Examples:
 python scripts/import_sprite_animation.py --source idle.gif --character urfavxbf --action idle_normal --loop
 python scripts/import_sprite_animation.py --source walk.png --columns 8 --rows 1 --character pix --action walk --fps 8 --loop
 python scripts/import_sprite_animation.py --source ./idle-frames --character urfavxbf --action idle_normal --fps 8 --loop
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
from PIL import Image

MAX_FRAMES=600
MAX_SIDE=4096
MAX_BYTES=96*1024*1024
SAFE_ID=re.compile(r'^[a-z][a-z0-9_-]{0,48}$')


def validate_id(value:str)->str:
    if not SAFE_ID.fullmatch(value):
        raise ValueError(f"Unsafe character/action identifier: {value!r}")
    return value


def load_frames(source:Path,columns:int|None,rows:int|None,
                count:int|None,fps:float|None)->tuple[list[Image.Image],list[int]]:
    if not source.exists() or source.is_symlink():
        raise ValueError(f"Source missing or symlink: {source}")
    sources=sorted(source.glob('*.png')) if source.is_dir() else [source]
    if not sources or len(sources)>MAX_FRAMES:
        raise ValueError("Source directory must have 1–600 PNG frames")
    if source.is_dir() and any(x is not None for x in (columns,rows,count)):
        raise ValueError("Grid layout requires one source PNG")
    if (columns is None)!=(rows is None):
        raise ValueError("Specify both --columns and --rows for a grid")
    frames=[]
    durations=[]
    for path in sources:
        if path.stat().st_size>MAX_BYTES:
            raise ValueError(f"Input file exceeds 96MB: {path}")
        with Image.open(path) as src:
            src.load()
            if max(src.size)>MAX_SIDE*max(1,columns or 1,rows or 1):
                raise ValueError("Source dimensions exceed safety limit")
            if getattr(src,'n_frames',1)>1:
                if columns is not None:
                    raise ValueError("Cannot use grid layout with animated GIF")
                for k in range(src.n_frames):
                    src.seek(k)
                    frames.append(src.convert('RGBA').copy())
                    durations.append(max(20,int(src.info.get('duration',100))))
            elif columns is not None:
                if src.format!='PNG':raise ValueError("Grid source must be PNG")
                assert rows is not None
                if columns<1 or rows<1 or src.width%columns or src.height%rows:
                    raise ValueError("Sprite grid must divide evenly")
                w,h=src.width//columns,src.height//rows
                if w>MAX_SIDE or h>MAX_SIDE:raise ValueError("Tile too large")
                total=columns*rows
                if count is not None and not 1<=count<=total:
                    raise ValueError("Frame count exceeds grid bounds")
                for i in range(count or total):
                    x,y=i%columns,i//columns
                    frames.append(src.crop((x*w,y*h,(x+1)*w,(y+1)*h)).convert('RGBA'))
                    durations.append(125)
            else:
                frames.append(src.convert('RGBA').copy())
                durations.append(125)
    if not frames or len(frames)>MAX_FRAMES:
        raise ValueError("Expected 1–600 frames")
    if fps is not None:
        if not .5<=fps<=60:raise ValueError("FPS must be 0.5–60")
        durations=[round(1000/fps)]*len(frames)
    return frames,durations


def inspect(frames:list[Image.Image],require_alpha:bool)->list[str]:
    w,h=frames[0].size
    if w<1 or h<1 or max(w,h)>MAX_SIDE:raise ValueError("Invalid frame size")
    seen=set()
    warnings=[]
    for i,im in enumerate(frames):
        if im.size!=(w,h):raise ValueError(f"Frame {i} canvas differs")
        a=im.getchannel('A')
        corners=(a.getpixel((0,0)),a.getpixel((w-1,0)),
                 a.getpixel((0,h-1)),a.getpixel((w-1,h-1)))
        if require_alpha and (a.getextrema()[0]==255 or max(corners)>8):
            raise ValueError(f"Frame {i} has opaque or visible background")
        if not a.getbbox():warnings.append(f"Frame {i} empty")
        digest=hashlib.sha256(im.tobytes()).hexdigest()
        if digest in seen:warnings.append(f"Frame {i} repeats a prior drawing")
        seen.add(digest)
    if w<256 or h<256:
        warnings.append(f"Only {w}x{h} native pixels; 1080p canvas cannot invent detail")
    return warnings


def write_import(source:Path,root:Path,character:str,action:str,
                 columns:int|None,rows:int|None,count:int|None,
                 fps:float|None,loop:bool,allow_opaque:bool=False)->dict:
    character=validate_id(character)
    action=validate_id(action)
    frames,durations=load_frames(source,columns,rows,count,fps)
    warnings=inspect(frames,not allow_opaque)
    target=root/character/action
    if target.exists():raise FileExistsError(f"Refusing to overwrite: {target}")
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.sprites-import-',dir=target.parent) as td:
        staging=Path(td)
        output=[]
        for i,(im,dur) in enumerate(zip(frames,durations)):
            filename=f'{i:03d}.png'
            path=staging/filename
            im.save(path,format='PNG',optimize=True)
            output.append({'file':filename,'durationMs':dur,
                           'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        manifest={
            'schema':'video-ai-editor/imported-animation-v1',
            'character':character,'action':action,'source':source.name,
            'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest()
                           if source.is_file() else None,
            'frameCount':len(frames),'nativeWidth':frames[0].width,
            'nativeHeight':frames[0].height,'loop':loop,
            'durationsMs':durations,'frames':output,
            'qualityStatus':'draft-requires-owner-visual-review',
            'realTransparencyVerified':not allow_opaque,
            'warnings':warnings,
        }
        (staging/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        staging.rename(target)
    return manifest


def main()->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--character',required=True)
    p.add_argument('--action',required=True)
    p.add_argument('--output-root',type=Path,default=Path('public/characters/imported'))
    p.add_argument('--columns',type=int)
    p.add_argument('--rows',type=int)
    p.add_argument('--frame-count',type=int)
    p.add_argument('--fps',type=float)
    p.add_argument('--loop',action='store_true')
    p.add_argument('--allow-opaque',action='store_true',
                   help='Use only for draft review; unverified background is retained')
    args=p.parse_args()
    try:
        m=write_import(args.source,args.output_root,args.character,args.action,
                       args.columns,args.rows,args.frame_count,args.fps,
                       args.loop,args.allow_opaque)
        print(json.dumps({'success':True,'frames':m['frameCount'],
                          'nativeSize':[m['nativeWidth'],m['nativeHeight']],
                          'status':m['qualityStatus'],'warnings':m['warnings']},indent=2))
        return 0
    except (ValueError,OSError) as exc:
        print(f'IMPORT BLOCKED: {exc}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
