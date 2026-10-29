#!/usr/bin/env python3
"""Zero-paid-credit true frame-by-frame action import for canonical characters.

Takes INDEPENDENTLY DRAWN/GENERATED WHOLE-BODY frames. Never invents poses,
interpolates sprites, or applies cutout/piecewise transforms. This tool validates
file hygiene only; artistic quality and independent art provenance need review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "characters" / "zero-budget-sprite-policy.json"
CONTRACT_PATH = ROOT / "characters" / "true-action-contract.json"
MIN_CANVAS = (256, 256)
MAX_PIXELS = 4096 * 4096

def load_contracts() -> tuple[dict, dict]:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    spec = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if policy["maximumExternalSpendUsd"] != 0 or policy["allowPaidApis"] or policy["allowGpuRental"] or policy["autoGenerateSprites"]:
        raise ValueError("Zero-budget policy was weakened")
    if not policy["forbidProductionCutoutFallback"] or policy["animationMode"] != "independent-whole-character-frames":
        raise ValueError("Cutout fallback is forbidden")
    if spec["referenceIdentity"] != policy["sourceIdentity"]:
        raise ValueError("Character reference policy mismatch")
    return policy, spec

def validate_frames(directory: Path, who: str, action: str, spec: dict) -> list[dict]:
    if who not in spec["characters"] or action not in spec["characters"][who]:
        raise ValueError("Unknown canonical character or action")
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("Frame source folder missing or symlinked")
    expected = spec["characters"][who][action]["frames"]
    found = sorted(directory.glob("*.png"))
    if len(found) != expected:
        raise ValueError(f"Expected {expected} DISTINCT whole-character drawings, found {len(found)}")
    if any(p.name != f"{i:03d}.png" for i, p in enumerate(found)):
        raise ValueError("Frames must be sequentially named 000.png, 001.png, ...")
    seen_pixels: set[str] = set()
    result = []
    canvas = None
    for i, path in enumerate(found):
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 32 * 1024 * 1024:
            raise ValueError(f"Unsafe or oversized frame: {path.name}")
        with Image.open(path) as source:
            source.load()
            if source.format != "PNG" or source.mode != "RGBA":
                raise ValueError(f"True RGBA PNG required: {path.name}")
            if source.width < MIN_CANVAS[0] or source.height < MIN_CANVAS[1]:
                raise ValueError(f"Native sprite too small: {path.name}")
            if source.width * source.height > MAX_PIXELS:
                raise ValueError(f"Sprite dimensions exceed limit: {path.name}")
            if canvas is None:
                canvas = source.size
            if source.size != canvas:
                raise ValueError(f"Canvas sizes not aligned: {path.name}")
            alpha = source.getchannel("A")
            if alpha.getbbox() is None or alpha.getextrema()[0] == 255:
                raise ValueError(f"Not transparent full-body artwork: {path.name}")
            corners = [(0,0), (0,source.height-1), (source.width-1,0), (source.width-1,source.height-1)]
            if any(alpha.getpixel(p) > 8 for p in corners):
                raise ValueError(f"Transparent corner margin missing: {path.name}")
            if alpha.getbbox() is None:
                raise ValueError(f"Frame has no character: {path.name}")
            # Decoded-pixel equality, not PNG file-byte equality.
            pixel_hash = hashlib.sha256(source.tobytes()).hexdigest()
            if pixel_hash in seen_pixels:
                raise ValueError(f"Duplicate image frame (not a new drawing): {path.name}")
            seen_pixels.add(pixel_hash)
            # Not an automated proof of truly repainted art or of a smooth loop.
            result.append({"index":i,"filename":path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                           "pixelSha256":pixel_hash,"width":source.width,"height":source.height,
                           "alphaBounds":list(alpha.getbbox())})
    return result

def stage(directory: Path, out: Path, who: str, action: str, spec: dict, fps: int) -> dict:
    if fps < 1 or fps > 30:
        raise ValueError("Invalid animation FPS")
    frames = validate_frames(directory, who, action, spec)
    target = out / who / action
    if target.exists():
        raise FileExistsError("Target action exists; never overwrite approved/pending art")
    target.mkdir(parents=True)
    try:
        for row in frames:
            shutil.copyfile(directory / row["filename"], target / row["filename"])
        manifest = {
            "schema":"video-ai-editor/independently-drawn-action/v1",
            "character":who,"action":action,"sourceReference":"canonical-2026-10-29",
            "frameCount":len(frames),"fps":fps,
            "loop":spec["characters"][who][action]["loop"],
            "artProvenance":"user-supplied-full-body-png-frames-unverified",
            "technique":"independent-whole-character-frames",
            "artApproved":False,"motionReviewed":False,"phonemeAligned":False,
            "notes":"Technically staged, not proof of artistic consistency or non-transformed frame provenance.",
            "frames":frames
        }
        (target/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
        return manifest
    except BaseException:
        shutil.rmtree(target)
        raise

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan",action="store_true",help="Print the complete free action production contract")
    parser.add_argument("--character",choices=("urfavxbf","pix"))
    parser.add_argument("--action")
    parser.add_argument("--frames-dir",type=Path)
    parser.add_argument("--out-dir",type=Path)
    parser.add_argument("--fps",type=int,default=12)
    args=parser.parse_args()
    try:
        policy,spec=load_contracts()
        if args.plan:
            print(json.dumps({"policy":policy,"contract":spec},indent=2))
            return 0
        if not args.character or not args.action or args.frames_dir is None:
            raise ValueError("Choose --character, --action, --frames-dir, and optionally --out-dir")
        if args.out_dir is None:
            result=validate_frames(args.frames_dir,args.character,args.action,spec)
            print(json.dumps({"status":"SOURCE_FRAMES_TECHNICALLY_VALID","frames":len(result),
                              "artApproved":False,"motionReviewed":False},indent=2))
        else:
            result=stage(args.frames_dir,args.out_dir,args.character,args.action,spec,args.fps)
            print(json.dumps({"status":"STAGED_FOR_VISUAL_REVIEW","manifest":result},indent=2))
        return 0
    except (OSError,ValueError,KeyError,FileExistsError) as exc:
        print(f"TRUE FRAME IMPORT BLOCKED: {exc}",file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())
