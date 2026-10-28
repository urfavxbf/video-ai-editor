#!/usr/bin/env python3
"""Render one short-form WAV narration using Resemble AI Chatterbox Multilingual V3.

Optional dependency: pip install -r requirements-chatterbox.txt
No model packages are imported until an actual generation is requested.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile

LANGUAGES = frozenset(
    "ar da de el en es fi fr he hi it ja ko ms nl no pl pt ru sv sw tr zh".split()
)
MAX_TEXT_LENGTH = 700


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a WAV voice-over with Chatterbox Multilingual V3."
    )
    text = parser.add_mutually_exclusive_group(required=True)
    text.add_argument("--text", help="Short text to narrate.")
    text.add_argument("--text-file", type=Path, help="UTF-8 script file.")
    parser.add_argument(
        "--output", required=True, type=Path, help="Destination .wav path."
    )
    parser.add_argument(
        "--language-id", default="en", choices=sorted(LANGUAGES),
        help="Official Chatterbox language code (Tagalog/tl is not supported).",
    )
    parser.add_argument(
        "--voice-reference", type=Path,
        help="Optional reference recording you own or have permission to use.",
    )
    parser.add_argument(
        "--device", choices=("auto", "cpu", "cuda", "mps"), default="auto",
        help="Inference device. Auto prefers CUDA, then Apple MPS, then CPU.",
    )
    parser.add_argument(
        "--exaggeration", type=float, default=0.5, help="Expressiveness 0 to 1."
    )
    parser.add_argument(
        "--cfg-weight", type=float, default=0.5, help="CFG weight 0 to 1."
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Replace an existing WAV."
    )
    return parser


def validate_request(args: argparse.Namespace) -> tuple[str, Path]:
    raw = args.text
    if args.text_file is not None:
        if not args.text_file.is_file():
            raise ValueError(f"Script not found: {args.text_file}")
        raw = args.text_file.read_text(encoding="utf-8-sig")
    narration = " ".join((raw or "").split())
    if not narration:
        raise ValueError("Narration must contain text.")
    if len(narration) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Narration is {len(narration)} characters; maximum is "
            f"{MAX_TEXT_LENGTH}. Split longer scripts into smaller clips."
        )
    for name in ("exaggeration", "cfg_weight"):
        value = getattr(args, name)
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"--{name.replace('_', '-')} must be from 0 to 1.")
    if args.voice_reference is not None:
        if not args.voice_reference.is_file():
            raise ValueError(f"Reference audio not found: {args.voice_reference}")
        if args.voice_reference.suffix.lower() not in {".wav", ".mp3", ".flac"}:
            raise ValueError("Reference audio must be .wav, .mp3, or .flac.")
    if args.output.suffix.lower() != ".wav":
        raise ValueError("Output must be a .wav file.")
    if args.output.exists() and not args.overwrite:
        raise ValueError(
            f"Output already exists: {args.output}. Use --overwrite to replace."
        )
    return narration, args.output


def choose_device(torch_module, requested: str) -> str:
    if requested != "auto":
        if requested == "cuda" and not torch_module.cuda.is_available():
            raise ValueError("CUDA requested but no CUDA GPU is available.")
        if requested == "mps" and not torch_module.backends.mps.is_available():
            raise ValueError("MPS requested but unavailable.")
        return requested
    if torch_module.cuda.is_available():
        return "cuda"
    if torch_module.backends.mps.is_available():
        return "mps"
    return "cpu"


def generate(args: argparse.Namespace) -> Path:
    narration, destination = validate_request(args)
    try:
        import torch
        import torchaudio
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    except ImportError as exc:
        raise RuntimeError(
            "Chatterbox dependencies are missing. Create an isolated Python "
            "environment and install requirements-chatterbox.txt."
        ) from exc

    # PyPI 0.1.7 predates the V3 selector even though upstream's source
    # pyproject continues to report 0.1.7. Fail clearly before model download.
    from inspect import signature
    if "t3_model" not in signature(ChatterboxMultilingualTTS.from_pretrained).parameters:
        raise RuntimeError(
            "The installed Chatterbox package does not support Multilingual V3. "
            "Reinstall the pinned GitHub source in requirements-chatterbox.txt."
        )

    device = choose_device(torch, args.device)
    print(f"Loading Chatterbox Multilingual V3 on {device}...", file=sys.stderr)
    model = ChatterboxMultilingualTTS.from_pretrained(
        device=device, t3_model="v3"
    )
    options = {
        "language_id": args.language_id,
        "exaggeration": args.exaggeration,
        "cfg_weight": args.cfg_weight,
    }
    if args.voice_reference is not None:
        options["audio_prompt_path"] = str(args.voice_reference)
    waveform = model.generate(narration, **options)
    destination.parent.mkdir(parents=True, exist_ok=True)

    # Write atomically so failed generations cannot leave a partial final WAV.
    with tempfile.NamedTemporaryFile(
        prefix=".chatterbox-", suffix=".wav",
        dir=destination.parent, delete=False,
    ) as handle:
        temporary = Path(handle.name)
    try:
        torchaudio.save(str(temporary), waveform.detach().cpu(), model.sr, encoding="PCM_S", bits_per_sample=16)
        if temporary.stat().st_size <= 44:
            raise RuntimeError("Chatterbox produced an empty WAV file.")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = generate(args)
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"Chatterbox error: {exc}", file=sys.stderr)
        return 2
    print(f"WAV generated: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
