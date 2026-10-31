#!/usr/bin/env python3
"""Validate and import a baked, offline 2D Bodymovin export from a Duik-authored rig.

This script never starts After Effects or Duik; it validates a *renderable
export*, not provenance or licensing. The source artwork and After Effects
workstation remain the owner's responsibility.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile

MAX_BYTES = 5_000_000
MAX_LAYERS = 120
MAX_NODES = 60_000
MAX_DEPTH = 48
ALLOWED_LAYER_TYPES = {0, 3, 4}  # precomposition, null/controller, 2D vector
ALLOWED_SHAPES = {"gr", "tr", "fl", "st", "el", "rc", "sh"}
BLOCKED_URI = re.compile(r"(?i)(?:https?://|file://|data:|javascript:|ftp://|\\\\\\\\)")
OUTPUT_DEFAULT = Path("src/after-effects/duik-imported.json")


def positive_number(value, field: str, low: float, high: float) -> float:
    if type(value) not in (int, float) or not math.isfinite(value) or not (low <= value <= high):
        raise ValueError(f"{field} must be finite, between {low} and {high}")
    return float(value)


def walk_tree(value):
    """Bound processing work and reject embedded URIs / expression properties."""
    stack = [(value, 0)]
    seen = 0
    animated_properties = 0
    while stack:
        item, depth = stack.pop()
        seen += 1
        if seen > MAX_NODES or depth > MAX_DEPTH:
            raise ValueError("Lottie exceeds safe size/depth limits")
        if isinstance(item, str):
            if BLOCKED_URI.search(item):
                raise ValueError("External URLs / data URIs are not allowed in offline Lottie")
            if len(item) > 12_000:
                raise ValueError("Unexpectedly long embedded text")
        elif isinstance(item, list):
            stack.extend((v, depth + 1) for v in item)
        elif isinstance(item, dict):
            if item.get("a") == 1 and "k" in item and isinstance(item["k"], list):
                animated_properties += 1
            if "a" in item and "k" in item and "x" in item:
                raise ValueError("Unbaked expression detected; bake Duik expressions to keyframes first")
            stack.extend((key, depth + 1) for key in item.keys())
            stack.extend((v, depth + 1) for v in item.values())
    if animated_properties < 1:
        raise ValueError("No animated keyframes detected")
    return animated_properties


def validate_shapes(items, where: str):
    if not isinstance(items, list) or not items:
        raise ValueError(f"{where}: expected nonempty vector shapes")
    for i, item in enumerate(items):
        if not isinstance(item, dict) or item.get("ty") not in ALLOWED_SHAPES:
            raise ValueError(f"{where}[{i}]: unsupported shape/effect; use vector paths")
        if item["ty"] == "gr":
            validate_shapes(item.get("it"), f"{where}[{i}].it")


def validate_layers(layers, where: str, reference_ids: set[str]):
    if not isinstance(layers, list) or not layers or len(layers) > MAX_LAYERS:
        raise ValueError(f"{where}: expected 1–{MAX_LAYERS} layers")
    for i, layer in enumerate(layers):
        location = f"{where}[{i}]"
        if not isinstance(layer, dict) or layer.get("ty") not in ALLOWED_LAYER_TYPES:
            raise ValueError(f"{location}: only 2D vector, null and precomp layers are supported")
        if layer.get("ddd", 0) != 0:
            raise ValueError(f"{location}: 3D layers cannot be imported")
        if layer.get("bm", 0) != 0:
            raise ValueError(f"{location}: blend modes require separate compatibility review")
        if (layer.get("tt", 0) or layer.get("td", 0) or layer.get("hasMask") or
                layer.get("masksProperties") or layer.get("ef") or layer.get("tm")):
            raise ValueError(f"{location}: mattes, masks, effects and time remapping are unsupported")
        if not isinstance(layer.get("ks"), dict):
            raise ValueError(f"{location}: transforms missing")
        kind = layer["ty"]
        if kind == 4:
            validate_shapes(layer.get("shapes"), location + ".shapes")
        if kind == 0:
            ref = layer.get("refId")
            if not isinstance(ref, str) or ref not in reference_ids:
                raise ValueError(f"{location}: unresolved precomp reference")


def validate_lottie(data: object) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Lottie root must be an object")
    version = data.get("v")
    if not isinstance(version, str) or not re.fullmatch(r"[0-9]+[.][0-9]+[.][0-9]+", version):
        raise ValueError("Missing valid Bodymovin/Lottie version")
    w = int(positive_number(data.get("w"), "width", 16, 4096))
    h = int(positive_number(data.get("h"), "height", 16, 4096))
    if w != data["w"] or h != data["h"]:
        raise ValueError("Width/height must be integers")
    fps = positive_number(data.get("fr"), "frame rate", 30, 30)
    ip = positive_number(data.get("ip"), "in point", 0, 1_000_000)
    op = positive_number(data.get("op"), "out point", ip + 1, ip + 18_000)
    assets = data.get("assets", [])
    if not isinstance(assets, list) or len(assets) > 60:
        raise ValueError("Invalid precomposition assets")
    refs = set()
    for i, asset in enumerate(assets):
        if not isinstance(asset, dict) or set(asset) - {"id", "layers"}:
            raise ValueError(f"assets[{i}]: images, media and external dependencies not supported")
        ref = asset.get("id")
        if not isinstance(ref, str) or not ref or ref in refs:
            raise ValueError(f"assets[{i}]: invalid or duplicate precomp ID")
        refs.add(ref)
    validate_layers(data.get("layers"), "layers", refs)
    for i, asset in enumerate(assets):
        validate_layers(asset.get("layers"), f"assets[{i}].layers", refs)
    animated = walk_tree(data)
    return {"width": w, "height": h, "fps": int(fps), "frames": int(op - ip),
            "animatedProperties": animated, "layers": len(data["layers"])}


def import_file(source: Path, target: Path | None):
    if source.is_symlink() or not source.is_file():
        raise ValueError("Source must be an existing regular file, not a symlink")
    if source.stat().st_size > MAX_BYTES:
        raise ValueError("Lottie file exceeds the 5 MB import limit")
    payload = source.read_bytes()
    try:
        data = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid UTF-8 JSON file") from exc
    information = validate_lottie(data)
    information["sha256"] = hashlib.sha256(payload).hexdigest()
    if target is not None:
        if target.is_symlink():
            raise ValueError("Refusing to replace a symlink target")
        if source.resolve() == target.resolve():
            raise ValueError("Input and output paths must differ")
        target.parent.mkdir(parents=True, exist_ok=True)
        # Normalize JSON and use atomic replacement to avoid leaving partial imports.
        sanitized = (json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".duik-", suffix=".tmp",
                                            delete=False) as handle:
                tmp_path = Path(handle.name)
                handle.write(sanitized)
            os.replace(tmp_path, target)
        finally:
            if tmp_path is not None:
                tmp_path.unlink(missing_ok=True)
    return information


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path, help="Local Bodymovin JSON with baked rig keyframes")
    p.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    p.add_argument("--check", action="store_true", help="Validate only; do not modify files")
    args = p.parse_args()
    try:
        details = import_file(args.input, None if args.check else args.output)
    except (ValueError, OSError) as exc:
        print(f"Duik import rejected: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"validated": True, "imported": not args.check, **details}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
