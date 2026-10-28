#!/usr/bin/env python3
"""Safely stage ONLY approved head-portrait PNGs from the user's V2 ZIP.

This does not download or invent character art. It extracts the reviewed
expression sprites from a caller-supplied local ZIP into Remotion public/.
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/characters/pixel-glitch"
EXPRESSIONS = {
    "urfavxbf": ("neutral", "talk", "excited", "thinking", "surprised", "glitch"),
    "pix": ("neutral", "talk", "happy", "curious", "surprised", "glitch"),
}
PACK_ROOT = "PixelGlitch_SpritePack"


def stage(zip_path: Path, dest: Path = OUT) -> int:
    if not zip_path.is_file():
        raise FileNotFoundError(f"Approved V2 sprite ZIP does not exist: {zip_path}")
    total = 0
    with zipfile.ZipFile(zip_path) as archive:
        for character, expressions in EXPRESSIONS.items():
            for expression in expressions:
                member = f"{PACK_ROOT}/{character}/{expression}.png"
                try:
                    blob = archive.read(member)
                except KeyError as exc:
                    raise ValueError(f"Missing approved expression sprite: {member}") from exc
                if not blob.startswith(b"\x89PNG\r\n\x1a\n"):
                    raise ValueError(f"Invalid PNG: {member}")
                output = dest / character / f"{expression}.png"
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(blob)
                total += 1
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", dest="zip_path", type=Path, required=True,
                        help="Local path to PixelGlitch_Complete_Pack.zip from character Library")
    parser.add_argument("--dest", type=Path, default=OUT)
    args = parser.parse_args()
    staged = stage(args.zip_path, args.dest)
    print(f"Staged {staged} approved portrait PNGs in {args.dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
