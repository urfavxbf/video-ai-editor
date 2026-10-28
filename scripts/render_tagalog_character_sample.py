#!/usr/bin/env python3
"""One-off real VoxCPM2 voice audition for the two approved Filipino characters.

Loads the model ONCE, renders two short lines with their distinct, approved
text-based voice descriptions, saves individual WAVs and a joined conversation.
No external or unauthorized reference recordings are used.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import soundfile as sf

from voxcpm_voiceover import profile_for

DIALOGUE = [
    ("urfavxbf", "Uy, PIX! Alam mo ba? Minsan, kayang lokohin ng utak ang ating mga mata."),
    ("pix", "Hala, seryoso?! Paano nangyayari iyon? Kuwento mo sa akin!"),
]

OUT = Path("out/tagalog-character-voice-sample")


def main() -> None:
    from voxcpm import VoxCPM

    OUT.mkdir(parents=True, exist_ok=True)
    print("Loading VoxCPM2 once for the approved Filipino character designs...", flush=True)
    model = VoxCPM.from_pretrained(
        "openbmb/VoxCPM2", device="cpu", optimize=False, load_denoiser=False
    )
    rate = int(model.tts_model.sample_rate)
    if rate < 16000:
        raise RuntimeError("Unexpected synthesis sample rate")

    timeline = []
    combined = []
    cursor = 0
    for i, (speaker, script) in enumerate(DIALOGUE):
        profile = profile_for(speaker)
        print(f"Generating {speaker} with {profile['identifier']}", flush=True)
        designed = f"({profile['voice_design_prompt']}) {script}"
        audio = np.asarray(
            model.generate(
                text=designed, cfg_value=2.0, inference_timesteps=10, seed=42 + i,
            ),
            dtype=np.float32,
        ).reshape(-1)
        if len(audio) < rate // 2 or not np.isfinite(audio).all():
            raise RuntimeError(f"Invalid synthesized output for {speaker}")
        # Avoid hard clipping. Preserve relative expressiveness across utterances.
        max_amp = float(np.abs(audio).max())
        if max_amp > 0.98:
            audio *= 0.98 / max_amp
        sf.write(OUT / f"{speaker}.wav", audio, rate, subtype="PCM_16")
        start = cursor / rate
        combined.append(audio)
        cursor += len(audio)
        timeline.append({
            "speaker": speaker,
            "profile_id": profile["identifier"],
            "language": "tl",
            "text": script,
            "start_seconds": round(start, 3),
            "end_seconds": round(cursor / rate, 3),
            "filename": f"{speaker}.wav",
        })
        if i < len(DIALOGUE) - 1:
            silence = np.zeros(int(0.5 * rate), dtype=np.float32)
            combined.append(silence)
            cursor += len(silence)

    sf.write(OUT / "UrFavXBF-and-PIX-Tagalog-voice-test.wav",
             np.concatenate(combined), rate, subtype="PCM_16")
    (OUT / "sample-dialogue.json").write_text(
        json.dumps({
            "purpose": "Tagalog speaker audition only, not a final video",
            "engine": "VoxCPM2",
            "model_id": "openbmb/VoxCPM2",
            "sample_rate": rate,
            "voice_design_note": "Text-only voice design; timbre not guaranteed across future renders",
            "lines": timeline,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    print(f"REAL AUDITION WAV GENERATED: {OUT / 'UrFavXBF-and-PIX-Tagalog-voice-test.wav'}", flush=True)


if __name__ == "__main__":
    main()
