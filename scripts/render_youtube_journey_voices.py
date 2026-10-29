#!/usr/bin/env python3
"""Synthesize the approved YouTube beginner-journey preview or full dialogue, once per voice.

This workflow uses CPU Chatterbox Multilingual V3, with the existing approved
English identities. It never creates fake audio or silently changes engines.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile

from build_youtube_journey_preview import PREVIEW_SECTIONS, validate_script
from chatterbox_voice_profile import DEFAULT_NARRATOR
from pix_voice_profile import DEFAULT_PIX
from check_chatterbox_v3 import require_v3_loader


def render(speaker: str, script: Path, destination: Path,
           scope: str = 'preview', shard_index: int = 0, shard_count: int = 1) -> dict:
    import torch
    import torchaudio
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS

    require_v3_loader(ChatterboxMultilingualTTS.from_pretrained)
    torch.set_num_threads(min(4, torch.get_num_threads()))
    profile = DEFAULT_PIX if speaker == "pix" else DEFAULT_NARRATOR
    dialogue = validate_script(json.loads(script.read_text(encoding="utf-8")))
    if scope not in ('preview', 'full') or shard_count < 1 or not 0 <= shard_index < shard_count:
        raise ValueError("Invalid scope or shard selection")
    if scope == 'preview':
        candidates = [ident for _, section_ids in PREVIEW_SECTIONS for ident in section_ids
                      if dialogue[ident]["speaker"] == speaker]
    else:
        candidates = [ident for ident, line in dialogue.items() if line["speaker"] == speaker]
    ids = [ident for i, ident in enumerate(candidates) if i % shard_count == shard_index]
    if not ids:
        raise ValueError(f"No {scope} lines for {speaker} shard {shard_index}")
    options = {
        "language_id": "en",
        "exaggeration": profile.exaggeration,
        "cfg_weight": profile.cfg_weight,
    }
    if speaker == "pix":
        from prepare_pix_reference import prepare
        reference = prepare(Path("input/pix-reference.wav"))
        options["audio_prompt_path"] = str(reference)
    print(f"Loading official Chatterbox V3 CPU model for {speaker}", flush=True)
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu", t3_model="v3")
    destination = destination / speaker
    destination.mkdir(parents=True, exist_ok=True)
    manifest = {
        "engine": "Chatterbox Multilingual V3", "speaker": speaker,
        "voice_profile": profile.identifier, "language": "en",
        "sample_rate": model.sr, "clips": [], "human_review_required": True,
        "scope": scope, "shard_index": shard_index, "shard_count": shard_count,
    }
    for ident in ids:
        speech = dialogue[ident]["text"]
        print(f"Synthesizing {ident} ({len(speech)} chars)", flush=True)
        audio = model.generate(speech, **options).detach().cpu()
        if audio.ndim == 1:
            audio = audio.unsqueeze(0)
        if (audio.ndim != 2 or audio.shape[0] != 1 or
                audio.shape[1] < model.sr // 3 or
                not bool(torch.isfinite(audio).all())):
            raise RuntimeError(f"Invalid or non-finite WAV generated: {ident}")
        final_path = destination / f"{ident}.wav"
        with tempfile.NamedTemporaryFile(prefix=".render-", suffix=".wav",
                                         dir=destination, delete=False) as tmp:
            temporary = Path(tmp.name)
        try:
            torchaudio.save(str(temporary), audio, model.sr,
                            encoding="PCM_S", bits_per_sample=16)
            if temporary.stat().st_size <= 44:
                raise RuntimeError(f"Empty output for {ident}")
            temporary.replace(final_path)
        finally:
            temporary.unlink(missing_ok=True)
        manifest["clips"].append({
            "id": ident, "file": final_path.name,
            "duration_seconds": round(audio.shape[1] / model.sr, 3),
            "sample_count": int(audio.shape[1]), "text": speech,
        })
    manifest_name = "manifest.json" if shard_count == 1 else f"manifest-{shard_index}.json"
    (destination / manifest_name).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--speaker", choices=("urfavxbf", "pix"), required=True)
    p.add_argument("--scope", choices=("preview", "full"), default="preview")
    p.add_argument("--shard-index", type=int, default=0)
    p.add_argument("--shard-count", type=int, default=1)
    p.add_argument("--script", type=Path, default=Path("productions/youtube-beginner-journey/dialogue.json"))
    p.add_argument("--out", type=Path, default=Path("out/youtube-journey-voices"))
    args = p.parse_args()
    try:
        report = render(args.speaker, args.script, args.out, args.scope,
                        args.shard_index, args.shard_count)
        print(f"Completed {len(report['clips'])} real WAV clips for {args.speaker}")
        return 0
    except (OSError, ValueError, RuntimeError, ImportError, KeyError) as exc:
        print(f"YouTube journey TTS failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
