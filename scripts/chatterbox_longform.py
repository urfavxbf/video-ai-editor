#!/usr/bin/env python3
"""Synthesize long-form Chatterbox Multilingual V3 narration.

Loads the model once, splits source on speech-friendly sentence boundaries,
stitches watermarked clips with short pauses, and writes a timing manifest.
Output is NOT deemed publish-ready until listened to and QC checked.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

from chatterbox_voiceover import (
    LANGUAGES, MAX_TEXT_LENGTH, choose_device,
)

DEFAULT_CHUNK_LIMIT = 320


def split_script(text: str, max_chars: int = DEFAULT_CHUNK_LIMIT) -> list[str]:
    if not (40 <= max_chars <= MAX_TEXT_LENGTH):
        raise ValueError(f"max_chars must be between 40 and {MAX_TEXT_LENGTH}")
    cleaned = " ".join(text.split())
    if not cleaned:
        raise ValueError("Narration script is empty.")
    # End speech at sentence boundaries where possible. Retain punctuation.
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    result: list[str] = []
    current = ""
    for sentence in sentences:
        if len(sentence) > max_chars:
            # Fall back to word boundaries for unusually long sentences.
            words = sentence.split(" ")
            for word in words:
                if len(word) > max_chars:
                    raise ValueError(f"Word exceeds chunk limit: {word[:40]!r}")
                candidate = f"{current} {word}".strip()
                if len(candidate) > max_chars:
                    result.append(current)
                    current = word
                else:
                    current = candidate
            continue
        candidate = f"{current} {sentence}".strip()
        if len(candidate) > max_chars:
            if current:
                result.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        result.append(current)
    assert result and all(0 < len(part) <= max_chars for part in result)
    assert " ".join(result) == cleaned
    return result


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate long-form Chatterbox V3 voice-over.")
    p.add_argument("--text-file", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--language-id", default="en", choices=sorted(LANGUAGES))
    p.add_argument("--voice-reference", type=Path, default=None,
                   help="Optional reference audio with explicit speaker consent.")
    p.add_argument("--device", choices=("auto", "cpu", "cuda", "mps"), default="auto")
    p.add_argument("--max-chars", type=int, default=DEFAULT_CHUNK_LIMIT)
    p.add_argument("--pause-ms", type=int, default=280)
    p.add_argument("--exaggeration", type=float, default=0.5)
    p.add_argument("--cfg-weight", type=float, default=0.5)
    p.add_argument("--overwrite", action="store_true")
    return p


def validate(args: argparse.Namespace) -> list[str]:
    if not args.text_file.is_file():
        raise ValueError(f"Script not found: {args.text_file}")
    if args.output.suffix.lower() != ".wav":
        raise ValueError("Output must be .wav")
    if args.output.exists() and not args.overwrite:
        raise ValueError("Output exists. Pass --overwrite if intentional.")
    if args.voice_reference is not None and (
        not args.voice_reference.is_file()
        or args.voice_reference.suffix.lower() not in {".wav", ".flac", ".mp3"}
    ):
        raise ValueError("Voice reference must be an existing .wav/.flac/.mp3 file")
    if not 0 <= args.pause_ms <= 3000:
        raise ValueError("--pause-ms must be between 0 and 3000")
    for name in ("exaggeration", "cfg_weight"):
        if not 0 <= getattr(args, name) <= 1:
            raise ValueError(f"--{name.replace('_', '-')} must be between 0 and 1")
    return split_script(args.text_file.read_text(encoding="utf-8-sig"), args.max_chars)


def synthesize(args: argparse.Namespace) -> tuple[Path, Path]:
    parts = validate(args)
    import torch
    import torchaudio
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from check_chatterbox_v3 import require_v3_loader
    require_v3_loader(ChatterboxMultilingualTTS.from_pretrained)

    device = choose_device(torch, args.device)
    if device == "cpu":
        torch.set_num_threads(min(4, torch.get_num_threads()))
    print(f"Loading Chatterbox Multilingual V3 once on {device}", file=sys.stderr)
    model = ChatterboxMultilingualTTS.from_pretrained(device=device, t3_model="v3")
    pause_samples = round(args.pause_ms * model.sr / 1000)
    pause = torch.zeros((1, pause_samples), dtype=torch.float32)
    joined: list = []
    chapters = []
    samples = 0
    for index, sentence in enumerate(parts, 1):
        kwargs = {
            "language_id": args.language_id,
            "exaggeration": args.exaggeration,
            "cfg_weight": args.cfg_weight,
        }
        if args.voice_reference is not None:
            kwargs["audio_prompt_path"] = str(args.voice_reference)
        print(f"Synthesizing {index}/{len(parts)} ({len(sentence)} chars)", file=sys.stderr)
        waveform = model.generate(sentence, **kwargs).detach().cpu()
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        if waveform.ndim != 2 or waveform.shape[0] != 1 or waveform.shape[1] < model.sr // 5:
            raise RuntimeError(f"Invalid or empty speech at chunk {index}")
        if not bool(torch.isfinite(waveform).all()):
            raise RuntimeError(f"Non-finite audio at chunk {index}")
        start = samples / model.sr
        joined.append(waveform)
        samples += waveform.shape[1]
        chapters.append({
            "index": index, "text": sentence,
            "start_seconds": round(start, 3),
            "end_seconds": round(samples / model.sr, 3),
        })
        if index < len(parts) and pause_samples:
            joined.append(pause)
            samples += pause_samples

    data = torch.cat(joined, dim=-1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output.with_suffix(".json")
    with tempfile.NamedTemporaryFile(dir=args.output.parent, prefix=".narration-",
                                     suffix=".wav", delete=False) as handle:
        temp_wav = Path(handle.name)
    try:
        torchaudio.save(str(temp_wav), data, model.sr, encoding="PCM_S", bits_per_sample=16)
        if temp_wav.stat().st_size <= 44:
            raise RuntimeError("Empty WAV generated")
        temp_wav.replace(args.output)
    finally:
        temp_wav.unlink(missing_ok=True)

    manifest_path.write_text(json.dumps({
        "engine": "Chatterbox Multilingual V3", "language": args.language_id,
        "sample_rate": model.sr, "duration_seconds": round(samples / model.sr, 3),
        "chunks": chapters, "review_required": True,
    }, indent=2) + "\n", encoding="utf-8")
    return args.output, manifest_path


def main() -> int:
    try:
        output, manifest = synthesize(build_parser().parse_args())
        print(f"Created {output} and {manifest}")
        return 0
    except (ValueError, RuntimeError, OSError, ImportError) as exc:
        print(f"Chatterbox long-form error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
