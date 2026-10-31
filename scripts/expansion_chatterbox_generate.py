#!/usr/bin/env python3
"""Produce scene-separated *real* UrFavXBF Chatterbox V3 speech, loading model once.

No substitute speaker, synthetic silence or generated test tone is permitted.
The output is for audiovisual QA; written voice profile != human listening review.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import tempfile
import wave

def extract_lines(path: Path) -> list[str]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schemaVersion") != 1 or not isinstance(obj.get("scenes"), list):
        raise ValueError("expected approved scene-plan.json schemaVersion 1")
    scenes = obj["scenes"]
    if len(scenes) != 25:
        raise ValueError("Expected exactly 25 scenes")
    out = []
    for i, scene in enumerate(scenes):
        if scene.get("index") != i:
            raise ValueError("Scene indices must be consecutive")
        s = scene.get("narration")
        if not isinstance(s, str) or not s.strip() or len(s) > 700:
            raise ValueError(f"Invalid scene {i} narration")
        out.append(" ".join(s.split()))
    return out

def synthesize(lines: list[str], out_dir: Path) -> dict:
    import torch
    import torchaudio
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from chatterbox_voice_profile import DEFAULT_NARRATOR
    from check_chatterbox_v3 import require_v3_loader
    require_v3_loader(ChatterboxMultilingualTTS.from_pretrained)
    if DEFAULT_NARRATOR.identifier != "natural-storyteller-v1":
        raise ValueError("UrFavXBF narrator profile changed unexpectedly")
    torch.set_num_threads(min(4, torch.get_num_threads()))
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu", t3_model=DEFAULT_NARRATOR.checkpoint)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = []
    all_wavs = []
    offset = 0
    sample_rate = model.sr
    for i, line in enumerate(lines):
        print(f"Chatterbox V3 scene {i+1}/{len(lines)}: {line}", flush=True)
        waveform = model.generate(
            line, language_id="en",
            exaggeration=DEFAULT_NARRATOR.exaggeration,
            cfg_weight=DEFAULT_NARRATOR.cfg_weight,
        ).detach().cpu()
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)
        if (waveform.ndim != 2 or waveform.shape[0] != 1 or
                waveform.shape[1] < sample_rate // 5 or
                not bool(torch.isfinite(waveform).all())):
            raise RuntimeError(f"Invalid voice audio at scene {i}")
        filename = f"{i:02}.wav"
        dest = out_dir / filename
        torchaudio.save(str(dest), waveform, sample_rate, encoding="PCM_S", bits_per_sample=16)
        frames = int(waveform.shape[1])
        result.append({
            "index": i, "text": line, "file": filename,
            "sampleRate": sample_rate,
            "samples": frames,
            "startSeconds": round(offset / sample_rate, 3),
            "endSeconds": round((offset + frames) / sample_rate, 3),
            "durationSeconds": round(frames / sample_rate, 3),
        })
        all_wavs.append(waveform)
        offset += frames
        if i != len(lines) - 1:
            gap = torch.zeros((1, round(.13 * sample_rate)), dtype=waveform.dtype)
            all_wavs.append(gap)
            offset += gap.shape[1]
    output = out_dir / "urfavxbf-chatterbox-v3-scene-narration.wav"
    joined = torch.cat(all_wavs, dim=1)
    torchaudio.save(str(output), joined, sample_rate, encoding="PCM_S", bits_per_sample=16)
    manifest = {
        "schemaVersion": 1,
        "engine": "Chatterbox Multilingual V3",
        "voiceProfile": DEFAULT_NARRATOR.identifier,
        "voiceSource": DEFAULT_NARRATOR.source,
        "language": "en",
        "sampleRate": sample_rate,
        "durationSeconds": round(joined.shape[1] / sample_rate, 3),
        "scenes": result,
        "manualListeningReviewRequired": True,
    }
    (out_dir / "voice-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scene-plan", type=Path, default=Path("productions/expansion-original/scene-plan.json"))
    p.add_argument("--output-dir", type=Path, default=Path("out/expansion-chatterbox"))
    p.add_argument("--validate-only", action="store_true")
    args = p.parse_args()
    lines = extract_lines(args.scene_plan)
    if args.validate_only:
        print(f"Validated {len(lines)} scene lines without generating audio.")
        return
    manifest = synthesize(lines, args.output_dir)
    print("Generated actual Chatterbox V3 WAV; duration:", manifest["durationSeconds"])

if __name__ == "__main__":
    main()
