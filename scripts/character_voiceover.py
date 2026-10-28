#!/usr/bin/env python3
"""Generate a voice line as UrFavXBF or PIX with the project's pinned Chatterbox V3.

The main host uses approved built-in voice conditioning. PIX uses the verified
synthetic female Emily reference; profiles remain independent.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from chatterbox_voice_profile import DEFAULT_NARRATOR
from pix_voice_profile import DEFAULT_PIX


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Synthesize UrFavXBF or PIX English dialogue.")
    p.add_argument("--character", required=True, choices=("urfavxbf", "pix"))
    t = p.add_mutually_exclusive_group(required=True)
    t.add_argument("--text")
    t.add_argument("--text-file", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--device", choices=("auto", "cpu", "cuda", "mps"), default="auto")
    p.add_argument("--overwrite", action="store_true")
    return p


def synth_args(args: argparse.Namespace, pix_reference: Path | None = None) -> list[str]:
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
            raise ValueError("PIX requires a verified speaker reference.")
        options.extend(["--voice-reference", str(pix_reference)])
    if args.overwrite:
        options.append("--overwrite")
    return options


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    reference = None
    if args.character == "pix":
        from prepare_pix_reference import prepare
        reference = prepare(Path("input/pix-reference.wav"))
    from chatterbox_voiceover import main as chatterbox_main
    return chatterbox_main(synth_args(args, reference))


if __name__ == "__main__":
    raise SystemExit(main())
