#!/usr/bin/env python3
"""Stage user-approved super-pixelated HEAD portrait atlas snapshots.

Two 128x64 RGBA/paletted PNGs contain [neutral | talking] frames. They were
reduced from the approved 2026-10-28 pixel/glitch sprite pack. No full bodies.
"""
from __future__ import annotations
import argparse
import base64
import json
import struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def stage(props:Path|None):
    dest=ROOT/"public"/"episodes"/"youtube-automation"
    dest.mkdir(parents=True,exist_ok=True)
    files=[]
    for who in ("urfavxbf","pix"):
        src=ROOT/"assets"/"automation"/f"{who}-atlas.base64"
        raw=base64.b64decode(src.read_text(encoding="ascii").strip(),validate=True)
        if raw[:8]!=b"\x89PNG\r\n\x1a\n" or struct.unpack(">II",raw[16:24])!=(128,64):
            raise ValueError(f"Invalid {who} portrait atlas PNG; expected 128x64.")
        target=dest/f"{who}-atlas.png"
        target.write_bytes(raw)
        files.append(str(target))
    if props:
        data=json.loads(props.read_text(encoding="utf-8"))
        if data.get("audioEngine")!="Chatterbox Multilingual V3" or len(data.get("voiceClips",[]))<20:
            raise ValueError("Never mark visual assets ready unless real Chatterbox audio is packaged")
        data["assetsReady"]=True
        props.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print("Staged approved neutral/talk pixel head portraits:",*files,sep="\n")
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--props",type=Path)
    args=parser.parse_args()
    stage(args.props)
if __name__=="__main__":main()
