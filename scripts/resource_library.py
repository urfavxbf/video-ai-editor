#!/usr/bin/env python3
"""Offline, rights-aware media resource library for Video AI Editor.

Actions never contact external services or accept remote media downloads.
Bundled resources remain tracked; imported raw stock is ignored by Git.
An intake receipt is owner's attestation, NOT independent legal clearance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BUILTIN_PUBLIC = ROOT / "public"  # Never overridden by isolated local intake tests
CATALOG = ROOT / "resources" / "catalog.json"
LOCAL_CATALOG = ROOT / "resources" / "local-catalog.json"
DEST_ROOT = PUBLIC / "library"

EXTENSIONS = {
    "video": {".mp4", ".mov", ".webm"},
    "image": {".png", ".jpg", ".jpeg", ".webp"},
    "music": {".wav", ".mp3", ".ogg", ".m4a"},
    "sfx": {".wav", ".mp3", ".ogg"},
    "font": {".ttf", ".otf"},
}
LICENSES = {
    "owner-original", "CC0-1.0", "CC-BY-4.0", "Pexels License",
    "Pixabay Content License", "Unsplash License", "Mixkit Free License",
    "OFL-1.1",
}
MAX_SIZE = 250 * 1024 * 1024
MAX_ITEMS = 2000


def fail(message: str) -> None:
    raise ValueError(message)


def read_json(path: Path, default: dict | None = None) -> dict:
    if not path.exists() and default is not None:
        return default
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 2_000_000:
        fail("catalog is missing, symlinked or oversized")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        fail("catalog is not valid JSON")
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        fail("unsupported catalog schema")
    return data


def ensure_file(path: Path, *, root: Path, extensions: set[str]) -> Path:
    if not path.is_relative_to(root):
        fail("media path is outside the approved directory")
    current = root
    for component in path.relative_to(root).parts:
        if component in (".", "..") or component.startswith("."):
            fail("hidden or traversal path rejected")
        current = current / component
        if current.is_symlink():
            fail("symlink media path rejected")
    if not path.is_file() or path.suffix.lower() not in extensions:
        fail("media file or extension invalid")
    if not 0 < path.stat().st_size <= MAX_SIZE:
        fail("media file size out of bounds")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1_048_576), b""):
            digest.update(block)
    return digest.hexdigest()


def probe(path: Path, kind: str) -> dict:
    if kind == "font":
        signature = path.open("rb").read(4)
        if signature not in (b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1"):
            fail("invalid font signature")
        return {"format": path.suffix.lower()[1:]}
    if kind == "image":
        from PIL import Image
        try:
            with Image.open(path) as pic:
                if pic.format not in {"PNG", "JPEG", "WEBP"} or pic.width > 10000 or pic.height > 10000:
                    fail("unsupported or oversized image")
                width, height = pic.size
                pic.verify()
        except (OSError, SyntaxError, ValueError):
            fail("image payload could not be verified")
        return {"width": width, "height": height}
    if kind == "vector":
        text = path.read_text(encoding="utf-8")
        if (len(text) > 60_000 or
            not text.startswith('<svg xmlns="http://www.w3.org/2000/svg"') or
            re.search(r"<script|<foreignObject|<image|https?://(?!www\.w3\.org/2000/svg)|<!DOCTYPE|onload=", text, re.I)):
            fail("unsafe original SVG source")
        return {"format": "svg"}
    if kind not in {"video", "music", "sfx"}:
        fail("unsupported kind")
    cmd = [
        "ffprobe", "-v", "error", "-protocol_whitelist", "file",
        "-format_whitelist", "mov,mp4,m4a,3gp,3g2,mj2,matroska,webm,wav,mp3,ogg",
        "-show_entries", "stream=codec_type,codec_name,width,height,channels,sample_rate:format=duration",
        "-of", "json", str(path),
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=20)
        if len(result.stdout) > 500_000:
            fail("excessive probe metadata")
        info = json.loads(result.stdout)
        duration = float(info["format"]["duration"])
        streams = info["streams"]
    except (subprocess.SubprocessError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        fail("media probe failed")
    if not 0 < duration <= 7200:
        fail("media duration out of bounds")
    expected = "video" if kind == "video" else "audio"
    active = [s for s in streams if s.get("codec_type") == expected]
    if not active:
        fail("required media stream missing")
    stream = active[0]
    if expected == "video":
        if not 0 < stream.get("width", 0) <= 7680 or not 0 < stream.get("height", 0) <= 4320:
            fail("unsupported video dimensions")
        return {"durationSeconds": round(duration, 3), "width": stream["width"], "height": stream["height"], "codec": stream.get("codec_name")}
    return {"durationSeconds": round(duration, 3), "codec": stream.get("codec_name")}


def audit() -> dict:
    built = read_json(CATALOG)
    entries = built.get("builtIn")
    if not isinstance(entries, list) or len(entries) < 18:
        fail("built-in resource inventory is incomplete")
    result = {"builtInVerified": 0, "rightsReviewNeeded": 0, "localVerified": 0}
    known = set()
    for item in entries:
        if not isinstance(item, dict) or item.get("kind") not in EXTENSIONS | {"image": set()}:
            fail("invalid built-in inventory item")
        identity, name, kind = item.get("id"), item.get("path"), item["kind"]
        if not isinstance(identity, str) or identity in known or not re.fullmatch(r"[a-z0-9-]{3,72}", identity):
            fail("duplicate or invalid resource id")
        known.add(identity)
        if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9/_\-.]{1,180}", name):
            fail("unsafe bundled resource path")
        item_path = BUILTIN_PUBLIC / name
        if item_path.suffix == ".svg" and name.startswith("resources/original/"):
            ensure_file(item_path, root=BUILTIN_PUBLIC, extensions={".svg"})
            probe(item_path, "vector")
        else:
            ensure_file(item_path, root=BUILTIN_PUBLIC, extensions=EXTENSIONS[kind])
            if kind == "font":
                if item.get("license") != "OFL-1.1" or not (BUILTIN_PUBLIC / "fonts/OFL.txt").is_file():
                    fail("bundled font license missing")
            elif item.get("rightsStatus") == "review-before-publication":
                result["rightsReviewNeeded"] += 1
            else:
                probe(item_path, kind)
        result["builtInVerified"] += 1
    local = read_json(LOCAL_CATALOG, {"schemaVersion": 1, "resources": []})
    items = local.get("resources")
    if not isinstance(items, list) or len(items) > MAX_ITEMS:
        fail("local asset registry is malformed")
    for item in items:
        if not isinstance(item, dict) or item.get("kind") not in EXTENSIONS:
            fail("invalid local asset registry record")
        path = item.get("path")
        if not isinstance(path, str) or not re.fullmatch(r"library/[a-z]+/[a-z0-9-]+[.][a-z0-9]+", path):
            fail("invalid local asset path")
        kind = item["kind"]
        resolved = ensure_file(PUBLIC / path, root=DEST_ROOT.parent, extensions=EXTENSIONS[kind])
        if item.get("sha256") != sha256(resolved):
            fail("local asset hash mismatch")
        probe(resolved, kind)
        if item.get("license") not in LICENSES or item.get("reviewed") is not True:
            fail("local rights receipt missing")
        result["localVerified"] += 1
    return result


def intake(args) -> dict:
    if not args.rights_confirmed:
        fail("owner rights confirmation is required")
    if args.license not in LICENSES or (args.kind == "font" and args.license not in {"OFL-1.1", "owner-original"}):
        fail("unapproved or non-commercial license")
    if args.license == "CC-BY-4.0" and not args.attribution.strip():
        fail("CC BY requires attribution")
    if not args.creator.strip() or len(args.creator) > 120:
        fail("creator attribution/provenance is required")
    if args.license != "owner-original":
        for url in (args.source_url, args.license_url):
            if not isinstance(url, str) or not re.fullmatch(r"https://[A-Za-z0-9._/-]+(?:[?][A-Za-z0-9_=&%.-]+)?", url):
                fail("third-party media requires a reviewed HTTPS item URL and exact license URL")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", args.slug):
        fail("use a safe lowercase slug (2–64 characters)")
    source = args.file.expanduser()
    if source.is_symlink() or not source.is_file() or source.suffix.lower() not in EXTENSIONS[args.kind]:
        fail("input is missing, symlinked or has an unsupported extension")
    if not 0 < source.stat().st_size <= MAX_SIZE:
        fail("input file too large")
    details = probe(source, args.kind)
    destination = DEST_ROOT / args.kind / f"{args.slug}{source.suffix.lower()}"
    if destination.exists() or destination.is_symlink():
        fail("asset already exists; refusing overwrite")
    local = read_json(LOCAL_CATALOG, {"schemaVersion": 1, "resources": []})
    assets = local.get("resources")
    if not isinstance(assets, list) or len(assets) >= MAX_ITEMS:
        fail("local registry is full")
    if any(isinstance(v, dict) and v.get("slug") == args.slug for v in assets):
        fail("slug already in use")
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".stage-", suffix=".tmp", delete=False) as f:
            tmp = Path(f.name)
            with source.open("rb") as stream:
                shutil.copyfileobj(stream, f, length=1_048_576)
        if sha256(tmp) != sha256(source):
            fail("copy digest differs")
        os.replace(tmp, destination)
        receipt = {
            "slug": args.slug, "kind": args.kind,
            "path": str(destination.relative_to(PUBLIC)),
            "sha256": sha256(destination), "license": args.license,
            "creator": args.creator, "sourceUrl": args.source_url or None,
            "licenseUrl": args.license_url or None,
            "attribution": args.attribution or None,
            "reviewed": True, "reviewNote": args.review_note or "",
            "details": details,
        }
        assets.append(receipt)
        LOCAL_CATALOG.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=LOCAL_CATALOG.parent, prefix=".resource-catalog-", suffix=".json", mode="w", encoding="utf-8", delete=False) as f:
            tmp = Path(f.name)
            json.dump(local, f, indent=2)
            f.write("\n")
        os.replace(tmp, LOCAL_CATALOG)
        return receipt
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        if tmp:
            tmp.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("audit", help="verify tracked library assets and all staged local resources")
    commands.add_parser("list", help="list bundled and user-staged resources without downloading")
    cmd = commands.add_parser("intake", help="stage owner-reviewed local media and write a SHA receipt")
    cmd.add_argument("file", type=Path)
    cmd.add_argument("--kind", required=True, choices=sorted(EXTENSIONS))
    cmd.add_argument("--slug", required=True)
    cmd.add_argument("--license", required=True, choices=sorted(LICENSES))
    cmd.add_argument("--creator", required=True)
    cmd.add_argument("--source-url", default="")
    cmd.add_argument("--license-url", default="")
    cmd.add_argument("--attribution", default="")
    cmd.add_argument("--review-note", default="")
    cmd.add_argument("--rights-confirmed", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "audit":
            result = audit()
        elif args.command == "list":
            result = {"bundled": read_json(CATALOG).get("builtIn", []),
                      "local": read_json(LOCAL_CATALOG, {"schemaVersion": 1, "resources": []}).get("resources", [])}
        else:
            result = intake(args)
    except (ValueError, OSError) as exc:
        print(f"Resource library check failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
