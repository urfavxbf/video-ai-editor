#!/usr/bin/env python3
"""Character-specific Tagalog/Taglish WAV generation with VoxCPM2.

Optional runtime: pip install -r requirements-voxcpm.txt
This module is safe to import and test without heavyweight TTS dependencies.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "characters" / "registry.json"
MAX_CHUNK = 320


def profile_for(character: str) -> dict:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if character not in ("urfavxbf", "pix"):
        raise ValueError(f"Unknown character: {character}")
    profile = registry["characters"][character]["voice"]
    if profile["engine"] != "voxcpm2" or profile["language"] != "tl":
        raise ValueError("Tagalog character profile must use VoxCPM2 with language tl")
    if not profile.get("voice_design_prompt") or not profile.get("model_id"):
        raise ValueError("Incomplete VoxCPM2 voice design profile")
    return profile


def split_text(text: str, max_chars: int = MAX_CHUNK) -> list[str]:
    """Split on sentence/word boundaries to avoid unstable long TTS inputs."""
    if max_chars < 40:
        raise ValueError("max_chars must be at least 40")
    normalized = " ".join(text.split())
    if not normalized:
        raise ValueError("Narration cannot be empty")
    sentences = re.split(r"(?<=[.!?。！？])\s+", normalized)
    result: list[str] = []
    current = ""
    for sentence in sentences:
        for word in sentence.split():
            if len(word) > max_chars:
                raise ValueError("Single token longer than max_chars")
            candidate = (current + " " + word).strip()
            if len(candidate) > max_chars:
                result.append(current)
                current = word
            else:
                current = candidate
        if current and current[-1:] in ".!?。！？":
            result.append(current)
            current = ""
    if current:
        result.append(current)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Filipino character voiceover with VoxCPM2.")
    parser.add_argument("--character", choices=("urfavxbf", "pix"), required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--text-file", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda", "mps"), default="auto")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-chars", type=int, default=MAX_CHUNK)
    parser.add_argument("--pause-ms", type=int, default=250)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Validate and preview; do not load model or write audio.")
    return parser


def validate(args: argparse.Namespace) -> tuple[dict, list[str]]:
    profile = profile_for(args.character)
    if args.text_file:
        if not args.text_file.is_file():
            raise ValueError(f"Script file not found: {args.text_file}")
        text = args.text_file.read_text(encoding="utf-8-sig")
    else:
        text = args.text or ""
    chunks = split_text(text, args.max_chars)
    if args.output.suffix.lower() != ".wav":
        raise ValueError("Output must have a .wav extension")
    if args.output.exists() and not args.overwrite:
        raise ValueError("WAV already exists; use --overwrite")
    if not 0 <= args.pause_ms <= 3000:
        raise ValueError("pause-ms must be between 0 and 3000")
    return profile, chunks


def synthesize(args: argparse.Namespace, profile: dict, chunks: list[str]) -> Path:
    try:
        import numpy as np
        import soundfile as sf
        from voxcpm import VoxCPM
    except ImportError as exc:
        raise RuntimeError("Install optional VoxCPM2 dependencies: pip install -r requirements-voxcpm.txt") from exc

    device_options = {"device": args.device, "load_denoiser": False}
    if args.device == "cpu":
        device_options["optimize"] = False
    model = VoxCPM.from_pretrained(profile["model_id"], **device_options)
    rate = int(model.tts_model.sample_rate)
    if rate < 16000:
        raise RuntimeError("Unexpected model sample rate")
    parts = []
    manifest_chunks = []
    offset = 0
    for i, chunk in enumerate(chunks):
        # Official VoxCPM2 voice-design syntax: parenthesized description before text.
        designed_text = f"({profile['voice_design_prompt']}) {chunk}"
        audio = np.asarray(model.generate(
            text=designed_text, cfg_value=2.0, inference_timesteps=10, seed=args.seed + i
        ), dtype=np.float32).reshape(-1)
        if audio.size < rate // 5 or not np.isfinite(audio).all():
            raise RuntimeError(f"Invalid audio returned for chunk {i + 1}")
        start = offset / rate
        parts.append(audio)
        offset += audio.size
        manifest_chunks.append({
            "index": i, "text": chunk, "start_seconds": round(start, 3),
            "end_seconds": round(offset / rate, 3),
        })
        if i != len(chunks) - 1 and args.pause_ms:
            pause = np.zeros(round(rate * args.pause_ms / 1000), dtype=np.float32)
            parts.append(pause)
            offset += pause.size

    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "character": args.character, "profile_id": profile["identifier"],
        "language": profile["language"], "engine": profile["engine"],
        "model_id": profile["model_id"], "sample_rate": rate,
        "seed": args.seed, "chunks": manifest_chunks,
        "timing_note": "Chunk boundaries only. Obtain word timing from alignment."
    }
    # Write WAV first to a temporary file, then replace the target atomically.
    with tempfile.NamedTemporaryFile(prefix=".voxcpm-", suffix=".wav", dir=output.parent, delete=False) as f:
        temp = Path(f.name)
    try:
        joined = np.concatenate(parts)
        if not np.isfinite(joined).all():
            raise RuntimeError("Non-finite WAV values")
        sf.write(str(temp), joined, rate, subtype="PCM_16")
        if temp.stat().st_size <= 44:
            raise RuntimeError("Empty output WAV")
        temp.replace(output)
        output.with_suffix(".json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    finally:
        temp.unlink(missing_ok=True)
    return output


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        profile, chunks = validate(args)
        if args.dry_run:
            print(json.dumps({
                "character": args.character, "engine": profile["engine"],
                "language": profile["language"], "profile_id": profile["identifier"],
                "voice_design_prompt": profile["voice_design_prompt"],
                "chunks": chunks, "output": str(args.output),
                "audio_generated": False,
            }, ensure_ascii=False, indent=2))
            return 0
        output = synthesize(args, profile, chunks)
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"VoxCPM2 error: {exc}", file=sys.stderr)
        return 2
    print(f"Generated Tagalog voiceover: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
