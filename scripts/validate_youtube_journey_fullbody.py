#!/usr/bin/env python3
"""Check approved transparent full-body PNGs before making Remotion props renderable.

An ordinary full-body PNG can sway, step and bounce as one sprite. Independent
arms/head/legs require correctly aligned transparent full-canvas rig layers.
Never mark missing assets as ready or generate substituted characters.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path, PurePosixPath

DEFAULT_ASSETS = {
    "urfavxbf": {"assetPath": "characters/pixel-glitch/urfavxbf/base.png"},
    "pix": {"assetPath": "characters/pixel-glitch/pix/base.png"},
}
REQUIRED_LIMBS = ("body", "head", "leftArm", "rightArm", "leftLeg", "rightLeg")
# PIX is a seated cat: two visible forelegs and tail, but no separately visible
# hind limbs in the canonical 2D artwork. Never pretend nonexistent legs are rigged.
PIX_REQUIRED_LIMBS = ("body", "head", "leftArm", "rightArm", "tail")
# Mirrored with src/characters/OfficialV2Rig.ts and generated rig-assets.json.
# Default episode renders now require actual articulated layers, not a flat PNG.
def _rig_for(character: str) -> dict:
    suffix = f"characters/pixel-glitch/{character}/rig/"
    keys = ("body", "head", "leftArm", "rightArm", "leftLeg", "rightLeg") if character == "urfavxbf" else (
        "body", "head", "leftArm", "rightArm", "tail")
    pivots = ({"headPivotPercent": [54,43], "leftArmPivotPercent": [37,47],
               "rightArmPivotPercent": [72,48], "leftLegPivotPercent": [41,73],
               "rightLegPivotPercent": [63,73]} if character == "urfavxbf" else
              {"headPivotPercent": [44,69], "leftArmPivotPercent": [31,74],
               "rightArmPivotPercent": [50,75], "tailPivotPercent": [66,71]})
    return {
        "assetPath": DEFAULT_ASSETS[character]["assetPath"],
        "layeredRig": {"underlay": suffix+"underlay.png",
                       **{k:suffix+k+".png" for k in keys},
                       **pivots},
    }

DEFAULT_FULL_BODY_RIG_ASSETS = {key: _rig_for(key) for key in ("urfavxbf", "pix")}
OPTIONAL_LIMBS = ("underlay", "tail", "leftLeg", "rightLeg", "mouthClosed", "mouthOpen")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def safe_path(public_root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name.startswith("characters/"):
        raise ValueError(f"Asset path must be under characters/: {name!r}")
    posix = PurePosixPath(name)
    if posix.is_absolute() or ".." in posix.parts or "\\" in name:
        raise ValueError(f"Unsafe character asset path: {name}")
    result = public_root / Path(*posix.parts)
    if result.is_symlink() or any(p.is_symlink() for p in result.parents if p != public_root.parent):
        raise ValueError(f"Character asset must not pass through a symlink: {name}")
    return result


def check_png(public_root: Path, name: str) -> tuple[int, int]:
    path = safe_path(public_root, name)
    if not path.is_file() or path.stat().st_size < 100:
        raise ValueError(f"Missing or empty approved full-body PNG: {path}")
    data = path.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise ValueError(f"Not a PNG: {path}")
    width, height, depth, color, comp, filtr, inter = struct.unpack(">IIBBBBB", data[16:29])
    if not 128 <= width <= 8192 or not 128 <= height <= 8192:
        raise ValueError(f"Unusable character dimensions: {path} ({width}x{height})")
    if color not in (4, 6) and not (color == 3 and b"tRNS" in data):
        raise ValueError(f"Character must have transparency: {path}")
    if b"IDAT" not in data or b"IEND" not in data:
        raise ValueError(f"Truncated PNG: {path}")
    return width, height


OFFICIAL_V2_SHA256 = {
    "urfavxbf": "b11936a4ace7c6cba1ee391ff768fce93bee80b2adf81b3a44a89cbaa4cf01b4",
    "pix": "cc5ecccdbb74b8c90ea3af09a0c75ff2c72db05fcdf0006fdc19255641304c6f",
}


def validate_assets(public_root: Path, assets: dict) -> dict[str, str]:
    if set(assets) != {"urfavxbf", "pix"}:
        raise ValueError("Exactly urfavxbf and pix full-body assets are required")
    modes: dict[str, str] = {}
    for character, config in assets.items():
        if not isinstance(config, dict) or not isinstance(config.get("assetPath"), str):
            raise ValueError(f"Missing approved full-body sprite for {character}")
        check_png(public_root, config["assetPath"])
        # Pin the real V2 base sprites, not merely any valid transparent PNG.
        if config["assetPath"] == DEFAULT_ASSETS[character]["assetPath"]:
            actual = hashlib.sha256(safe_path(public_root, config["assetPath"]).read_bytes()).hexdigest()
            if actual != OFFICIAL_V2_SHA256[character]:
                raise ValueError(f"{character}: V2 full-body artwork SHA-256 mismatch")
        rig = config.get("layeredRig")
        if rig is None:
            modes[character] = "single-sprite-whole-body"
            continue
        required = PIX_REQUIRED_LIMBS if character == "pix" else REQUIRED_LIMBS
        if not isinstance(rig, dict) or any(not rig.get(k) for k in required):
            raise ValueError(f"{character} rig missing required aligned original body parts: {required}")
        dims = {check_png(public_root, rig[k]) for k in required}
        for k in OPTIONAL_LIMBS:
            if k not in required and rig.get(k):
                dims.add(check_png(public_root, rig[k]))
        if len(dims) != 1:
            raise ValueError(f"{character} rig PNG layers must have the same canvas size")
        if bool(rig.get("mouthClosed")) != bool(rig.get("mouthOpen")):
            raise ValueError(f"{character}: open and closed mouth layers must be paired")
        modes[character] = "independently-articulated-limbs"
    return modes


def authorize_props(public_root: Path, props: dict) -> dict:
    if not isinstance(props.get("lines"), list) or not props["lines"]:
        raise ValueError("Only a complete voiced props manifest may be authorized")
    assets = props.get("fullBodyAssets") or DEFAULT_FULL_BODY_RIG_ASSETS
    modes = validate_assets(public_root, assets)
    result = dict(props)
    result["fullBodyAssets"] = assets
    result["assetsReady"] = True
    result["bodyMotionModes"] = modes
    # Image validation must never mark unreviewed captions or audio as publish-ready.
    result["readyForPublishing"] = False
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-root", type=Path, default=Path("public"))
    parser.add_argument("--props", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--assets-json", type=Path, help="Optional approved character sprite and layer manifest")
    a = parser.parse_args(argv)
    try:
        props = json.loads(a.props.read_text(encoding="utf-8"))
        if a.assets_json:
            props["fullBodyAssets"] = json.loads(a.assets_json.read_text(encoding="utf-8"))
        authorized = authorize_props(a.public_root, props)
        if a.out.resolve() == a.props.resolve():
            raise ValueError("Write validated props separately; keep the draft untouched")
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(authorized, indent=2)+"\n", encoding="utf-8")
        print("Approved full-body assets validated:", authorized["bodyMotionModes"])
        print("Render authorized for review. CAPTIONS AND FINAL VIDEO STILL REQUIRE HUMAN QC.")
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error, json.JSONDecodeError) as e:
        print(f"Full-body staging rejected: {e}", file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
