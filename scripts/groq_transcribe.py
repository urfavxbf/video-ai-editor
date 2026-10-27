#!/usr/bin/env python3
"""Groq Whisper transcription of Tagalog, Taglish and English videos to SRT/JSON/TXT.

Audio is sent to Groq only when user runs the command. GROQ_API_KEY is required.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

MODELS = ("whisper-large-v3-turbo", "whisper-large-v3")
MAX_FREE_BYTES = 25_000_000

def srt_time(seconds: float) -> str:
    ms = max(0, round(float(seconds) * 1000))
    hours, rem = divmod(ms, 3600_000)
    minutes, rem = divmod(rem, 60_000)
    sec, milli = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{sec:02},{milli:03}"

def caption_groups(words: list[dict]) -> list[tuple[float, float, str]]:
    result = []
    current = []
    for item in words:
        text = str(item.get("word", "")).strip()
        if not text:
            continue
        start, end = float(item["start"]), float(item["end"])
        if end < start:
            continue
        if current:
            candidate = " ".join([*(str(w["word"]) for w in current), text])
            if (len(current) >= 5 or end - current[0]["start"] > 2.2
                    or len(candidate) > 34 or start - current[-1]["end"] > .7):
                result.append((current[0]["start"], current[-1]["end"], " ".join(w["word"] for w in current)))
                current.clear()
        current.append({"word": text, "start": start, "end": end})
        if text.endswith((".", "!", "?")):
            result.append((current[0]["start"], current[-1]["end"], " ".join(w["word"] for w in current)))
            current.clear()
    if current:
        result.append((current[0]["start"], current[-1]["end"], " ".join(w["word"] for w in current)))
    return result

def render_srt(transcript: dict) -> str:
    if transcript.get("words"):
        captions = caption_groups(transcript["words"])
    else:
        captions = [(float(s["start"]), float(s["end"]), str(s["text"]).strip())
                    for s in transcript.get("segments", []) if str(s.get("text", "")).strip()]
    if not captions:
        raise ValueError("No word or segment timestamps were returned by Groq.")
    parts = []
    for i, (start, end, text) in enumerate(captions, 1):
        parts.append(f"{i}\n{srt_time(start)} --> {srt_time(max(start+.04, end))}\n{text}\n")
    return "\n".join(parts) + "\n"

def transcribe_video(source: Path, model: str, language: str | None) -> dict:
    if not source.is_file():
        raise FileNotFoundError(f"No media file: {source}")
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY missing: add a GitHub Codespaces secret and restart Codespaces.")
    from groq import Groq
    with tempfile.TemporaryDirectory(prefix="groq-audio-") as tmp:
        mp3 = Path(tmp) / "speech.mp3"
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(source), "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000",
                        "-c:a", "libmp3lame", "-b:a", "48k", str(mp3)], check=True)
        if mp3.stat().st_size > MAX_FREE_BYTES:
            raise ValueError("Audio exceeds the 25MB free-tier limit. Split into shorter clips.")
        kwargs = {"model": model, "response_format": "verbose_json", "temperature": 0,
                  "timestamp_granularities": ["word", "segment"]}
        if language:
            kwargs["language"] = language
        with mp3.open("rb") as audio_file:
            result = Groq().audio.transcriptions.create(file=audio_file, **kwargs)
        return result.model_dump() if hasattr(result, "model_dump") else dict(result)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, help="Input video or audio with speech")
    parser.add_argument("--output-dir", type=Path, default=Path("out/transcripts"))
    parser.add_argument("--model", choices=MODELS, default="whisper-large-v3-turbo")
    parser.add_argument("--language", help="Set tl for purely Tagalog, omit for Taglish")
    args = parser.parse_args()
    try:
        result = transcribe_video(args.video, args.model, args.language)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        stem = args.video.stem
        (args.output_dir / f"{stem}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        (args.output_dir / f"{stem}.txt").write_text(str(result.get("text", "")).strip()+"\n", encoding="utf-8")
        (args.output_dir / f"{stem}.srt").write_text(render_srt(result), encoding="utf-8")
        print(f"Subtitle saved: {args.output_dir / (stem + '.srt')}")
        return 0
    except (RuntimeError, ImportError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Transcription failed: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
