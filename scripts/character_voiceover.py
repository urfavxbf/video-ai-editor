#!/usr/bin/env python3
"""Route UrFavXBF/PIX dialogue to Tagalog VoxCPM2 by default or legacy English Chatterbox.

Default voice identities are stored in characters/registry.json. Importing this
module does not download model weights; Tagalog is never routed as Malay.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from chatterbox_voice_profile import DEFAULT_NARRATOR
from pix_voice_profile import DEFAULT_PIX

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "characters" / "registry.json"


def default_language() -> str:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))["production_language"]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Synthesize UrFavXBF or PIX dialogue (Tagalog by default).")
    p.add_argument("--character", required=True, choices=("urfavxbf", "pix"))
    p.add_argument("--language", choices=("tl", "en"), default=default_language(),
                   help="Tagalog/Taglish (tl, default) or legacy English (en).")
    t = p.add_mutually_exclusive_group(required=True)
    t.add_argument("--text")
    t.add_argument("--text-file", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--device", choices=("auto", "cpu", "cuda", "mps"), default="auto")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="Validate Tagalog voice plan without inference.")
    return p


def synth_args(args: argparse.Namespace, pix_reference: Path | None = None) -> list[str]:
    """Legacy English Chatterbox arguments; never use for Tagalog."""
    if args.language != "en":
        raise ValueError("Chatterbox V3 is not approved for Tagalog; use VoxCPM2")
    profile = DEFAULT_PIX if args.character == "pix" else DEFAULT_NARRATOR
    options = ["--output", str(args.output), "--device", args.device,
               "--language-id", profile.language,
               "--exaggeration", str(profile.exaggeration),
               "--cfg-weight", str(profile.cfg_weight)]
    if args.text_file is not None:
        options.extend(["--text-file", str(args.text_file)])
    else:
        options.extend(["--text", args.text])
    if args.character == "pix":
        if pix_reference is None:
            raise ValueError("PIX requires a verified English speaker reference.")
        options.extend(["--voice-reference", str(pix_reference)])
    if args.overwrite:
        options.append("--overwrite")
    return options


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.language == "tl":
        from voxcpm_voiceover import main as voxcpm_main
        options = ["--character", args.character, "--device", args.device,
                   "--output", str(args.output)]
        if args.text_file is not None:
            options.extend(["--text-file", str(args.text_file)])
        else:
            options.extend(["--text", args.text])
        if args.overwrite:
            options.append("--overwrite")
        if args.dry_run:
            options.append("--dry-run")
        return voxcpm_main(options)

    if args.dry_run:
        print("English Chatterbox dry-run is unavailable; use --language tl for a design preview.")
        return 2
    reference = None
    if args.character == "pix":
        from prepare_pix_reference import prepare
        reference = prepare(Path("input/pix-reference.wav"))
    from chatterbox_voiceover import main as chatterbox_main
    return chatterbox_main(synth_args(args, reference))


if __name__ == "__main__":
    raise SystemExit(main())
