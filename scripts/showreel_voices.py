#!/usr/bin/env python3
"""Synthesize every showreel line with Chatterbox Multilingual V3 (CPU), loading the model once.

UrFavXBF -> approved built-in "Natural Storyteller" profile (no reference audio).
PIX      -> approved Emily-reference profile (input/pix-reference.wav from prepare_pix_reference.py).
Writes out/showreel/voice/NN.wav (PCM16) + voices.json with durations and per-frame RMS envelopes.
"""
from __future__ import annotations
import argparse, json, math, sys, tempfile, wave, audioop
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chatterbox_voice_profile import DEFAULT_NARRATOR  # noqa: E402
from pix_voice_profile import DEFAULT_PIX  # noqa: E402

FPS = 30

def envelope(path: Path) -> tuple[float, list[float]]:
    with wave.open(str(path), "rb") as w:
        rate, width, ch, n = w.getframerate(), w.getsampwidth(), w.getnchannels(), w.getnframes()
        data = w.readframes(n)
    if ch > 1:
        data = audioop.tomono(data, width, 0.5, 0.5)
    hop = rate // FPS
    vals = []
    for i in range(0, n, hop):
        chunk = data[i * width:(i + hop) * width]
        vals.append(audioop.rms(chunk, width) / 32768 if chunk else 0.0)
    peak = max(vals) or 1.0
    return n / rate, [round(v / peak, 4) for v in vals]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", type=Path, default=Path("showreel/script.json"))
    ap.add_argument("--out", type=Path, default=Path("out/showreel/voice"))
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()
    spec = json.loads(a.script.read_text())
    a.out.mkdir(parents=True, exist_ok=True)
    import torch, torchaudio
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    torch.manual_seed(7)
    model = ChatterboxMultilingualTTS.from_pretrained(device=a.device, t3_model=DEFAULT_NARRATOR.checkpoint)
    ref = Path(spec["voices"]["pix"]["reference"])
    if not ref.is_file():
        raise SystemExit("PIX reference missing; run scripts/prepare_pix_reference.py first")
    result = []
    for s in spec["scenes"]:
        dest = a.out / f"{s['n']:02d}.wav"
        if s["speaker"] == "pix":
            opts = dict(language_id="en", exaggeration=DEFAULT_PIX.exaggeration, cfg_weight=DEFAULT_PIX.cfg_weight,
                        audio_prompt_path=str(ref))
            profile = DEFAULT_PIX.identifier
        else:
            opts = dict(language_id="en", exaggeration=DEFAULT_NARRATOR.exaggeration, cfg_weight=DEFAULT_NARRATOR.cfg_weight)
            profile = DEFAULT_NARRATOR.identifier
        wav = model.generate(s["text"], **opts)
        torchaudio.save(str(dest), wav.detach().cpu(), model.sr, encoding="PCM_S", bits_per_sample=16)
        dur, env = envelope(dest)
        if dur < 0.8 or max(env) <= 0:
            raise SystemExit(f"line {s['n']} looks empty")
        print(f"[{s['n']:02d}] {s['speaker']:4s} {dur:5.2f}s  {s['text']}", flush=True)
        result.append({"n": s["n"], "speaker": s["speaker"], "profile": profile, "file": dest.name,
                       "seconds": round(dur, 3), "rms": env})
    (a.out / "voices.json").write_text(json.dumps({"engine": "Chatterbox Multilingual V3", "sampleRate": model.sr,
                                                   "lines": result}, indent=1))
    print("Synthesized", len(result), "Chatterbox lines")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
