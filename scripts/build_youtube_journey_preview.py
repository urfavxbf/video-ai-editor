#!/usr/bin/env python3
"""Build a frame-accurate Remotion excerpt from REAL per-turn Chatterbox WAVs.

Only the preview is assembled. The generated caption blocks are approximate
and unreviewed; this command never claims word-aligned subtitles or a final MP4.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_voice_envelope import voice_event_from_wav

FPS = 30
# Deliberately edited excerpts, not a false continuous conversation.
PREVIEW_SECTIONS = (
    ("01", ("YT-001", "YT-002", "YT-003")),
    ("05", ("YT-029",)),
    ("06", ("YT-039", "YT-042")),
)
PROFILES = {"pix": "pix-cute-female-emily-v1", "urfavxbf": "natural-storyteller-v1"}
SAFE_ID = re.compile(r"^YT-[0-9]{3}$")


def validate_script(payload: dict) -> dict[str, dict]:
    if payload.get("language") != "en" or payload.get("format") != {
        "width": 1920, "height": 1080, "fps": FPS
    }:
        raise ValueError("Episode must use approved English 1920x1080 30fps format")
    result = {}
    for line in payload.get("lines", []):
        ident, speaker, text = line.get("id"), line.get("speaker"), line.get("text")
        if not isinstance(ident, str) or not SAFE_ID.fullmatch(ident) or ident in result:
            raise ValueError(f"Invalid or duplicate dialogue ID: {ident}")
        if speaker not in PROFILES or line.get("voice_profile") != PROFILES[speaker]:
            raise ValueError(f"Unexpected speaker or voice identity: {ident}")
        if not isinstance(text, str) or not text.strip() or len(text) > 700:
            raise ValueError(f"Invalid speech text: {ident}")
        result[ident] = line
    if len(result) != 68:
        raise ValueError(f"Expected 68 authored turns; found {len(result)}")
    for scene, ids in PREVIEW_SECTIONS:
        for ident in ids:
            if ident not in result or result[ident].get("scene") != scene:
                raise ValueError(f"Missing or mismatched preview line: {ident}")
    return result


def caption_blocks(text: str, start: int, end: int, limit: int = 74) -> list[dict]:
    """Editorially estimated chunk timing, NOT measured word alignment."""
    words = text.split()
    chunks = []
    current = []
    for word in words:
        candidate = " ".join(current + [word])
        if current and len(candidate) > limit:
            chunks.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        chunks.append(" ".join(current))
    weights = [max(1, len(chunk.split())) for chunk in chunks]
    total = sum(weights)
    elapsed = 0
    output = []
    for index, chunk in enumerate(chunks):
        s = start + round((end - start) * elapsed / total)
        elapsed += weights[index]
        e = end if index == len(chunks) - 1 else start + round((end - start) * elapsed / total)
        if e > s:
            output.append({"text": chunk, "startFrame": s, "endFrame": e})
    return output


def inspect_wav(path: Path) -> tuple[int, int]:
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Missing regular WAV: {path}")
    with wave.open(str(path), "rb") as wav:
        rate = wav.getframerate()
        samples = wav.getnframes()
        if wav.getcomptype() != "NONE" or wav.getsampwidth() != 2:
            raise ValueError(f"Expected uncompressed PCM16 WAV: {path}")
        if wav.getnchannels() not in (1, 2) or rate < 16000 or samples < rate // 3:
            raise ValueError(f"Missing, silent-length or malformed WAV: {path}")
    return samples, rate


def assemble(script: Path, audio_root: Path, public_root: Path,
             gap_frames: int = 7, transition_frames: int = 36) -> dict:
    if gap_frames < 0 or transition_frames < 10:
        raise ValueError("Invalid gap or editorial transition duration")
    dialogue = validate_script(json.loads(script.read_text(encoding="utf-8")))
    lines, sections, voice_events = [], [], []
    frame = 0
    for scene, ids in PREVIEW_SECTIONS:
        if sections:
            frame += transition_frames
        section_start = frame
        for n, ident in enumerate(ids):
            if n:
                frame += gap_frames
            line = dialogue[ident]
            speaker = line["speaker"]
            wav_path = audio_root / speaker / f"{ident}.wav"
            samples, rate = inspect_wav(wav_path)
            duration_frames = math.ceil(samples * FPS / rate)
            destination = (public_root / "voiceovers" / "youtube-beginner-journey" /
                           "preview" / speaker / wav_path.name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if wav_path.resolve() != destination.resolve():
                shutil.copy2(wav_path, destination)
            static_path = "/".join(destination.relative_to(public_root).parts)
            voice_events.append(voice_event_from_wav(wav_path, speaker, frame, FPS))
            lines.append({
                "id": ident, "scene": int(scene), "speaker": speaker,
                "text": line["text"], "file": static_path, "startFrame": frame,
                "endFrame": frame + duration_frames,
                "captions": caption_blocks(line["text"], frame, frame + duration_frames),
            })
            frame += duration_frames
        sections.append({"scene": int(scene), "startFrame": section_start, "endFrame": frame})
    if not lines:
        raise ValueError("No preview lines")
    duration_frames = frame + 12
    seconds = duration_frames / FPS
    return {
        "lines": lines, "sections": sections, "voiceEvents": voice_events,
        "totalFrames": duration_frames, "captionTiming": "estimated-unreviewed",
        "durationSeconds": round(seconds, 3), "targetDurationMet": 45 <= seconds <= 75,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--script", type=Path, default=Path("productions/youtube-beginner-journey/dialogue.json"))
    p.add_argument("--audio-root", type=Path, required=True, help="Contains pix/YT-xxx.wav and urfavxbf/YT-xxx.wav")
    p.add_argument("--public-root", type=Path, default=Path("public"))
    p.add_argument("--output", type=Path, default=Path("out/youtube-journey-preview.props.json"))
    p.add_argument("--strict-duration", action="store_true", help="Fail if measured excerpt is outside 45–75 s")
    args = p.parse_args(argv)
    try:
        props = assemble(args.script, args.audio_root, args.public_root)
        if args.strict_duration and not props["targetDurationMet"]:
            raise ValueError(f"Measured preview {props['durationSeconds']}s outside 45–75 s; edit excerpts")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(props, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {args.output}: {props['durationSeconds']} seconds; {len(props['lines'])} real WAVs")
        print("Caption blocks are estimated. Review/align before declaring synchronized subtitles.")
        if not props["targetDurationMet"]:
            print("WARNING: Measured excerpt is outside target 45–75 seconds", file=sys.stderr)
        return 0
    except (ValueError, OSError, KeyError, json.JSONDecodeError, wave.Error) as exc:
        print(f"Preview build failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
