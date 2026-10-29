#!/usr/bin/env python3
"""Verify and stage a 2026-10-29 canonical full-body draft review pack.

This never grants production approval. A staged draft can be reviewed with
CanonicalFullBodyReviewStage, but cannot bypass the production art gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
from zipfile import ZipFile
from PIL import Image

CHARS = ("urfavxbf", "pix")
ACTIONS = ("idle", "explain", "wave", "point", "walk", "celebrate", "listen")
MAX_PACK_BYTES = 256 * 1024 * 1024
MAX_TOTAL_BYTES = 480 * 1024 * 1024


def _allowed(path: str) -> bool:
    p = PurePosixPath(path)
    if p.is_absolute() or ".." in p.parts or "\\" in path:
        return False
    parts = p.parts
    if len(parts) >= 5 and parts[:3] == ("public", "characters", "canonical"):
        return parts[3] in CHARS
    if len(parts) == 4 and parts[0] == "animation-frames":
        return parts[1] in CHARS and parts[2] in ACTIONS and (
            parts[3] == "manifest.json" or parts[3] in {f"{i:03d}.png" for i in range(8)}
        )
    return False


def validate_pack(pack: Path) -> dict:
    if not pack.is_file() or pack.is_symlink() or pack.stat().st_size > MAX_PACK_BYTES:
        raise ValueError("Missing, linked, or oversized character pack")
    with ZipFile(pack) as z:
        names = z.namelist()
        if len(set(names)) != len(names):
            raise ValueError("Duplicate ZIP members")
        if sum(item.file_size for item in z.infolist()) > MAX_TOTAL_BYTES:
            raise ValueError("Decompressed assets exceed safety limit")
        data = json.loads(z.read("asset-package-manifest.json"))
        if data.get("schema") != "video-ai-editor/2.5d-review-pack/v1":
            raise ValueError("Invalid canonical animation pack schema")
        if data.get("designVersion") != "canonical-2026-10-29":
            raise ValueError("Incorrect character reference generation")
        if data.get("ownerApprovedArt") is not False:
            raise ValueError("A draft pack cannot declare owner approval")
        if data.get("framesPerCharacter") != 56 or set(data.get("actions", [])) != set(ACTIONS):
            raise ValueError("Missing or falsified animation coverage")
        entries = data["files"]
        if len({entry["path"] for entry in entries}) != len(entries):
            raise ValueError("Duplicate digest records")
        expected = {entry["path"]: entry for entry in entries}
        for who in CHARS:
            required = [f"public/characters/canonical/{who}/full-body.png"]
            required += [f"animation-frames/{who}/{action}/{i:03d}.png" for action in ACTIONS for i in range(8)]
            for rel in required:
                if rel not in expected or rel not in names:
                    raise ValueError(f"Required canonical sprite missing: {rel}")
        for rel, meta in expected.items():
            if not _allowed(rel) and not rel.startswith("references/"):
                raise ValueError(f"Unexpected asset path: {rel}")
            if rel not in names:
                raise ValueError(f"Manifest entry missing from ZIP: {rel}")
            zi = z.getinfo(rel)
            if zi.file_size != meta["size"] or zi.file_size > 48 * 1024 * 1024:
                raise ValueError(f"Invalid asset size: {rel}")
            raw = z.read(rel)
            if hashlib.sha256(raw).hexdigest() != meta["sha256"]:
                raise ValueError(f"SHA256 mismatch: {rel}")
            if rel.endswith(".png") and _allowed(rel):
                from io import BytesIO
                with Image.open(BytesIO(raw)) as im:
                    if im.format != "PNG" or im.mode != "RGBA":
                        raise ValueError(f"Sprite must be transparent RGBA: {rel}")
                    if im.width < 256 or im.height < 256:
                        raise ValueError(f"Sprite master too small: {rel}")
                    if im.getchannel("A").getextrema()[0] >= 255:
                        raise ValueError(f"Sprite has opaque background: {rel}")
        return {"status": "DRAFT_VERIFIED_NOT_APPROVED", "characters": list(CHARS),
                "frames": len(CHARS) * len(ACTIONS) * 8, "files": len(expected)}


def stage(pack: Path, public_root: Path) -> dict:
    report = validate_pack(pack)
    target = public_root / "characters" / "canonical"
    if target.exists():
        raise FileExistsError("Refusing to overwrite staged canonical character artwork")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".canonical-stage-", dir=target.parent) as temp:
        stage_root = Path(temp) / "canonical"
        stage_root.mkdir()
        with ZipFile(pack) as z:
            for who in CHARS:
                prefix = f"public/characters/canonical/{who}/"
                for meta in z.namelist():
                    if meta.startswith(prefix) and _allowed(meta) and not meta.endswith("/"):
                        dest = stage_root / meta.removeprefix("public/characters/canonical/")
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(z.read(meta))
                for action in ACTIONS:
                    for i in range(8):
                        name = f"animation-frames/{who}/{action}/{i:03d}.png"
                        dest = stage_root / who / "actions" / action / f"{i:03d}.png"
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes(z.read(name))
        (stage_root / "review-status.json").write_text(json.dumps({
            **report, "ownerApprovedArt": False, "phonemeAligned": False
        }, indent=2) + "\n")
        stage_root.rename(target)
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pack", type=Path, required=True)
    p.add_argument("--public-root", type=Path, default=Path("public"))
    p.add_argument("--validate-only", action="store_true")
    args = p.parse_args()
    try:
        result = validate_pack(args.pack) if args.validate_only else stage(args.pack, args.public_root)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, KeyError, OSError, RuntimeError) as exc:
        p.exit(2, f"CANONICAL REVIEW PACK BLOCKED: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
