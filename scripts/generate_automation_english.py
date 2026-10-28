#!/usr/bin/env python3
"""Generate real English UrFavXBF/PIX WAV dialogue with approved Chatterbox V3.

No alternate TTS voices and no paid GPU are used. Loads one V3 checkpoint for
the selected batch, retains the exact Natural Storyteller and PIX Emily settings.
"""
from __future__ import annotations

import argparse
import inspect
import json
import math
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCRIPT = ROOT / "episodes/youtube-automation-en.json"


def load_cues(path: Path) -> list[dict]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("language") != "en" or doc.get("voiceEngine") != "Chatterbox Multilingual V3":
        raise ValueError("This episode requires the English Chatterbox V3 voice engine.")
    if doc.get("voices") != {
        "urfavxbf": "natural-storyteller-v1",
        "pix": "pix-cute-female-emily-v1",
    }:
        raise ValueError("Unexpected voice identities. Do not silently replace approved voices.")
    cues = doc.get("cues", [])
    if len(cues) < 20:
        raise ValueError("This long-form episode needs at least 20 dialogue lines.")
    for i, cue in enumerate(cues):
        if cue.get("speaker") not in ("urfavxbf", "pix"):
            raise ValueError(f"Invalid speaker at line {i}")
        if not (1 <= len(cue.get("text", "")) <= 700):
            raise ValueError(f"Dialogue at line {i} is empty or too long for Chatterbox.")
    return cues


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        if wav.getsampwidth() != 2 or wav.getcomptype() != "NONE":
            raise ValueError(f"Expected PCM16 WAV: {path}")
        if wav.getframerate() < 16000 or wav.getnframes() < wav.getframerate() // 3:
            raise ValueError(f"Empty or too-short WAV: {path}")
        return wav.getnframes() / wav.getframerate()


def generate_clips(cues: list[dict], output: Path, device: str, limit: int, start: int, overwrite: bool) -> None:
    if start < 0 or start >= len(cues) or limit < 0:
        raise ValueError("Invalid start/limit; limit 0 means all remaining cues.")
    selected = list(enumerate(cues))[start:(start + limit if limit else None)]
    pending = [(i, cue) for i, cue in selected if overwrite or not (output / f"{i:02d}.wav").exists()]
    if not pending:
        print("All selected Chatterbox English WAVs already exist.", flush=True)
        return
    import torch
    import torchaudio
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from chatterbox_voice_profile import DEFAULT_NARRATOR
    from pix_voice_profile import DEFAULT_PIX
    from prepare_pix_reference import prepare

    if "t3_model" not in inspect.signature(ChatterboxMultilingualTTS.from_pretrained).parameters:
        raise RuntimeError("This package does not expose Chatterbox Multilingual V3.")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("Requested CUDA but no GPU is available")
    if device == "cpu":
        torch.set_num_threads(min(4, torch.get_num_threads()))
    # The pinned, MIT-licensed Emily reference is fetched and SHA-1 verified.
    ref = prepare(ROOT / "input/pix-reference.wav") if any(x["speaker"] == "pix" for _, x in pending) else None
    model = ChatterboxMultilingualTTS.from_pretrained(device=device, t3_model="v3")
    output.mkdir(parents=True, exist_ok=True)
    for i, cue in pending:
        speaker = cue["speaker"]
        voice = DEFAULT_PIX if speaker == "pix" else DEFAULT_NARRATOR
        options = dict(language_id="en", exaggeration=voice.exaggeration, cfg_weight=voice.cfg_weight)
        if speaker == "pix":
            options["audio_prompt_path"] = str(ref)
        torch.manual_seed(9100 + i)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(9100 + i)
        result = model.generate(" ".join(cue["text"].split()), **options)
        dst = output / f"{i:02d}.wav"
        with tempfile.NamedTemporaryFile(dir=output, prefix=".voice-", suffix=".wav", delete=False) as file:
            temp = Path(file.name)
        try:
            torchaudio.save(str(temp), result.detach().cpu(), model.sr, encoding="PCM_S", bits_per_sample=16)
            secs = wav_duration(temp)
            # Validate that the waveform is not effectively silent.
            amplitude = result.detach().float().abs().mean().item()
            if not math.isfinite(amplitude) or amplitude < 0.00005:
                raise ValueError(f"Silent or malformed generated WAV for cue {i}")
            temp.replace(dst)
            print(f"Voice cue {i+1}/{len(cues)}: {speaker} {secs:.1f}s; mean_abs={amplitude:.5f}", flush=True)
        finally:
            temp.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, default=DEFAULT_SCRIPT)
    parser.add_argument("--output", type=Path, default=ROOT / "out/youtube-automation/voices")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--max-cues", type=int, default=0)
    parser.add_argument("--start-cue", type=int, default=0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    cues = load_cues(args.episode)
    print(f"Validated {len(cues)} English cues; voices: Natural Storyteller + PIX Emily.", flush=True)
    if not args.validate_only:
        generate_clips(cues, args.output, args.device, args.max_cues, args.start_cue, args.overwrite)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
