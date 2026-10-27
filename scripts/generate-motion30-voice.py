#!/usr/bin/env python3
"""Produce 30s English narration with Chatterbox Nano (no other TTS)."""
from pathlib import Path
import os
import subprocess
import tempfile
import wave

LINES = [
    "Your next chapter doesn't start when everything is perfect. It starts when you move.",
    "One idea. One decision. One small action can change your direction.",
    "Stop waiting for motivation to show up. Create momentum instead.",
    "You don't need to see the whole path. Just take the first step.",
    "Start now. Your future is watching.",
]
DEST = Path("public/voiceovers/motion30.wav")


def seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def main() -> None:
    import torch
    import torchaudio
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    torch.set_num_threads(min(4, os.cpu_count() or 2))
    print("Loading official Chatterbox Nano (English, CPU)", flush=True)
    model = ChatterboxTurboTTS.from_pretrained(device="cpu", nano=True)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cb-motion30-") as tmp:
        root = Path(tmp)
        paths = []
        for index, phrase in enumerate(LINES):
            print("Generating scene", index+1, "of 5:", phrase, flush=True)
            raw = root / ("raw-"+str(index)+".wav")
            padded = root / ("scene-"+str(index)+".wav")
            audio = model.generate(phrase)
            torchaudio.save(str(raw), audio, model.sr)
            length = seconds(raw)
            speed = max(1.0, length / 5.3)
            print("  seconds:", round(length, 2), "tempo:", round(speed, 2), flush=True)
            if speed > 1.7:
                raise RuntimeError("Scene voice too long to preserve speech. Shorten the script.")
            fx = "atempo="+str(round(speed,5))+",adelay=300:all=1,apad,atrim=0:6,asetpts=N/SR/TB"
            ffmpeg("-i", str(raw), "-af", fx, "-ar", "48000", "-ac", "2",
                   "-c:a", "pcm_s16le", str(padded))
            paths.append(padded)
        manifest = root/"concat.txt"
        manifest.write_text("".join("file '"+str(p)+"'\n" for p in paths))
        ffmpeg("-f", "concat", "-safe", "0", "-i", str(manifest),
               "-c:a", "pcm_s16le", str(DEST))
    print("Narration:", DEST, seconds(DEST), "seconds", flush=True)
    if not (29.95 <= seconds(DEST) <= 30.05):
        raise RuntimeError("The generated voice track is not 30 seconds.")


if __name__ == "__main__":
    main()
