#!/usr/bin/env python3
"""Stage the two SHA-verified V2 hero sprites and actual WAV samples for Remotion.

Outputs usable HeroCharacterStage props. Does not synthesize, alter, or fake audio.
Never commits private binary assets to Git. No claim of lip or limb rigging.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import sys
import wave

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_voice_envelope import voice_event_from_wav
from validate_youtube_journey_fullbody import DEFAULT_ASSETS, DEFAULT_FULL_BODY_RIG_ASSETS, OFFICIAL_V2_SHA256, validate_assets

FPS = 30


def prepare(host_png: Path, pix_png: Path, host_wav: Path, pix_wav: Path,
            public: Path, host_start: int = 30, pix_start: int = 190,
            require_rig: bool = True) -> dict:
    if host_start < 0 or pix_start <= host_start:
        raise ValueError("PIX voice must begin after host voice")
    sources = {"urfavxbf": host_png, "pix": pix_png}
    for name, source in sources.items():
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"Missing approved V2 PNG for {name}: {source}")
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        if actual != OFFICIAL_V2_SHA256[name]:
            raise ValueError(f"Unapproved V2 source image for {name}: SHA-256 mismatch")
    for name, source in sources.items():
        path = public / DEFAULT_ASSETS[name]["assetPath"]
        path.parent.mkdir(parents=True,exist_ok=True)
        if source.resolve() != path.resolve():
            shutil.copy2(source,path)
    active_assets = DEFAULT_FULL_BODY_RIG_ASSETS if require_rig else DEFAULT_ASSETS
    modes=validate_assets(public,active_assets)
    events,clips=[],[]
    for name, wav, start in [
        ("urfavxbf",host_wav,host_start),("pix",pix_wav,pix_start)
    ]:
        if not wav.is_file() or wav.is_symlink():
            raise ValueError(f"Missing real sample WAV for {name}")
        with wave.open(str(wav),"rb") as w:
            if w.getsampwidth()!=2 or w.getcomptype()!="NONE" or w.getframerate()<8000:
                raise ValueError(f"Unsupported WAV format for {name}")
            duration=math.ceil(w.getnframes()*FPS/w.getframerate())
        if duration <= 0: raise ValueError("Empty sample WAV")
        dest=public/"voiceovers"/"hero-stage"/(name+".wav")
        dest.parent.mkdir(parents=True,exist_ok=True)
        if wav.resolve()!=dest.resolve():shutil.copy2(wav,dest)
        event=voice_event_from_wav(dest,name,start,FPS)
        events.append(event)
        clips.append({
            "file":dest.relative_to(public).as_posix(),
            "startFrame":start,"endFrame":start+duration
        })
    if clips[0]["endFrame"]>clips[1]["startFrame"]:
        raise ValueError("Voices overlap; re-time the sample explicitly")
    return {
        "assetsReady":True,
        "voiceEvents":events,
        "chapter":1,
        "audio":clips,
        "durationFrames":max(c["endFrame"] for c in clips)+40,
        "assetValidation":modes,
        "assets":active_assets,
        "projectStatus":"character-motion-review-only",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for field in ("host-png","pix-png","host-wav","pix-wav"):
        p.add_argument("--"+field,type=Path,required=True)
    p.add_argument("--public",type=Path,default=Path("public"))
    p.add_argument("--out",type=Path,default=Path("out/hero-stage.props.json"))
    p.add_argument("--host-start-frame",type=int,default=30)
    p.add_argument("--pix-start-frame",type=int,default=190)
    p.add_argument("--flat-review",action="store_true",
        help="Opt out of independently rigged assets for an explicitly flat preview only")
    args=p.parse_args()
    try:
        props=prepare(args.host_png,args.pix_png,args.host_wav,args.pix_wav,
            args.public,args.host_start_frame,args.pix_start_frame,
            require_rig=not args.flat_review)
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(props,indent=2)+"\n",encoding="utf-8")
        print(f"Validated two official V2 characters and real audio: {props['durationFrames']/FPS:.2f}s draft")
        print(f"Staged assets under {args.public}; draft props at {args.out}; NOT publish-ready")
        return 0
    except (ValueError, OSError, wave.Error) as error:
        print(f"Character stage blocked: {error}",file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
