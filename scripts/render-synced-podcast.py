#!/usr/bin/env python3
"""Render speech-synchronized, word-reveal podcast clips.

The source of truth is Groq Whisper's per-word transcript timing. No invented
text, duration-weighted word spacing, or pseudo alignment is permitted.

Input: rights-cleared source media + GROQ_API_KEY (or existing validated Groq
verbose_json transcript). Output: 9:16 MP4, ASS captions, alignment JSON.

Usage:
  GROQ_API_KEY=... python3 scripts/render-synced-podcast.py clip.mp4 \
    --start 12 --duration 36.5 \
    --paper 21.6:30.25 --output out/podcast-aligned.mp4

The user-provided recording must remain outside public Git repositories.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

FPS = 30
W, H = 1080, 1920
# Latin words are measured with a real font, not by rough character count.
FONT_PATHS = (
    "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
)
FONT = "Inter Display"
INK = "&H00191B1F&"
RED = "&H00414ACC&"  # ASS BGR
WHITE = "&H00FFFFFF&"
EMPHASIZE = {"makakalimutan", "nakitungo", "kanta", "hindi", "tao", "tandaan"}

ASS_HEADER = """[Script Info]
Title: Original Voice / Verified Word-Timed Podcast Captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style:Speech,Inter Display,66,&H00FFFFFF,&H00FFFFFF,&H000C1017,&H60080C11,1,0,0,0,100,100,0,0,1,3,1,5,48,48,40,1
Style:Paper,Inter Display,82,&H00191B1F,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,1,0,0,0,100,100,0,0,1,0,0,5,48,48,40,1
Style:Small,Inter Display,25,&H00666666,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,0,0,5,48,48,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def get_audio_words(transcript: dict) -> list[dict]:
    """Do not silently fall back to segments or fabricate time stamps."""
    raw = transcript.get("words")
    if not isinstance(raw, list) or not raw:
        raise ValueError("ASR did not return word timestamps: aborting instead of guessing")
    words: list[dict] = []
    last_start = -1.0
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"Bad word object at index {i}")
        word = str(item.get("word", "")).strip()
        if not word:
            continue
        start, end = float(item["start"]), float(item["end"])
        if not all(math.isfinite(x) for x in (start, end)):
            raise ValueError("Nonfinite speech timestamp")
        if start < 0 or end <= start or start < last_start - 0.015:
            raise ValueError(f"Malformed or unordered word timing at {i}: {word}")
        last_start = start
        words.append({"word": word, "start": start, "end": end})
    if not words:
        raise ValueError("No nonempty speech words in transcript")
    return words


def ass_time(t: float) -> str:
    centi = max(0, round(t * 100))
    hour, centi = divmod(centi, 360000)
    minute, centi = divmod(centi, 6000)
    sec, centi = divmod(centi, 100)
    return f"{hour}:{minute:02d}:{sec:02d}.{centi:02d}"


def event(layer: int, start: float, end: float, style: str, txt: str) -> str:
    if end <= start:
        raise ValueError("Nonpositive subtitle duration")
    return f"Dialogue: {layer},{ass_time(start)},{ass_time(end)},{style},,0,0,0,,{txt}"


def esc(txt: str) -> str:
    return txt.replace("\\", "\\\\").replace("{", "").replace("}", "").replace("\n", " ")


def in_paper(t: float, windows: list[tuple[float, float]]) -> bool:
    return any(start <= t < end for start, end in windows)


def text_width(font, text: str) -> float:
    if font is not None:
        return float(font.getlength(text))
    # Conservative fallback if PIL is not available.
    return len(text) * 42


def get_font(size: int):
    try:
        from PIL import ImageFont
        for candidate in FONT_PATHS:
            if Path(candidate).is_file():
                return ImageFont.truetype(candidate, size=size)
    except ImportError:
        pass
    return None


def group_words(
    words: list[dict], clip_start: float, duration: float,
    paper_windows: list[tuple[float, float]],
) -> list[dict]:
    """Phrase groups, split exactly on gaps, card changes or overflow."""
    selected = []
    for w in words:
        st = w["start"] - clip_start
        if 0 <= st < duration and w["end"] - clip_start > 0:
            selected.append({**w, "start": max(0.0, st), "end": min(duration, w["end"] - clip_start)})
    if not selected:
        raise ValueError("No source words inside selected time range")
    groups = []
    current: list[dict] = []
    for word in selected:
        paper = in_paper(word["start"], paper_windows)
        size = 79 if paper else 64
        font = get_font(size)
        suggested = [*(item["word"] for item in current), word["word"]]
        width = sum(text_width(font, w) for w in suggested) + 23 * (len(suggested)-1)
        gap = word["start"] - current[-1]["end"] if current else 0
        change = current and paper != in_paper(current[0]["start"], paper_windows)
        if current and (gap > .42 or len(current) >= 5 or width > 915 or change):
            groups.append({"words": current, "paper": in_paper(current[0]["start"], paper_windows)})
            current = []
        current.append(word)
    if current:
        groups.append({"words": current, "paper": in_paper(current[0]["start"], paper_windows)})
    for i, group in enumerate(groups):
        # Group remains until the next group's first word, but never holds for > ~1 sec after speech.
        nxt = groups[i+1]["words"][0]["start"] if i+1 < len(groups) else duration
        group["end"] = min(nxt, duration, group["words"][-1]["end"] + .42)
        # A short hold is permitted so the complete phrase is actually readable.
        group["end"] = max(group["end"], group["words"][-1]["start"] + .12)
    return groups


def render_ass(
    words: list[dict], clip_start: float, duration: float,
    paper_windows: list[tuple[float, float]],
) -> tuple[str, list[dict]]:
    groups = group_words(words, clip_start, duration, paper_windows)
    lines: list[str] = []
    # Paper cards have no proprietary shapes: restrained original corner geometry.
    for st, en in paper_windows:
        st, en = max(0.0, st), min(duration, en)
        if en <= st: continue
        lines.extend([
            event(0, st, en, "Paper", r"{\an7\pos(0,0)\p1\c&HF7F6F2&}m 0 0 l 1080 0 l 1080 1920 l 0 1920{\p0}"),
            event(1, st, en, "Paper", r"{\an7\pos(0,0)\p1\c&H1E2228&}m 0 0 l 120 0 l 0 120{\p0}"),
            event(1, st, en, "Paper", r"{\an7\pos(1080,1920)\p1\c&H1E2228&}m 0 0 l -122 0 l 0 -122{\p0}"),
            event(5, st, en, "Small", r"{\an8\pos(540,267)\fsp2}GLOC-9  /  i-LISTEN"),
        ])
    for group in groups:
        items, paper = group["words"], group["paper"]
        style = "Paper" if paper else "Speech"
        fontsize = 79 if paper else 64
        font = get_font(fontsize)
        widths = [text_width(font, w["word"]) for w in items]
        spacing = 23
        total = sum(widths) + spacing * (len(widths)-1)
        # Words are absolutely positioned for a stable line; no shifting on entrance.
        if total > 930:
            scale = 930 / total
        else:
            scale = 1.0
        x = (W - scale * total) / 2
        y = 1020 if paper else 1470
        for idx, w in enumerate(items):
            mid_x = x + widths[idx] * scale / 2
            x += (widths[idx] + spacing) * scale
            onset = w["start"]
            end = min(duration, group["end"])
            if end - onset < .05:
                continue
            normalized = re.sub(r"[^a-z0-9]", "", w["word"].lower())
            color = RED if paper and normalized in EMPHASIZE else INK if paper else WHITE
            # <= 110ms fade at exact ASR word start. No pre-roll / fake word times.
            # Scale + Y movement lasts 150ms; earlier words remain on screen.
            animation = (
                r"{\an5\move(" + f"{mid_x:.0f},{y+24:.0f},{mid_x:.0f},{y:.0f},0,165)"
                + r"\fscx86\fscy86\t(0,165,\fscx100\fscy100)"
                + r"\fad(90,65)\1c" + color
                + (r"\3c&H001019&\bord3" if not paper else r"\bord0")
                + rf"\fs{round(fontsize * scale)}" + "}"
            )
            lines.append(event(20, onset, end, style, animation + esc(w["word"])))
    return ASS_HEADER + "\n".join(lines) + "\n", groups


def parse_windows(values: list[str], clip_start: float, duration: float) -> list[tuple[float, float]]:
    out = []
    for window in values:
        match = re.fullmatch(r"(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)", window)
        if not match:
            raise ValueError(f"Bad --paper window {window!r}, use SOURCE_START:SOURCE_END")
        begin, end = (float(match[1]) - clip_start, float(match[2]) - clip_start)
        if not (0 <= begin < end <= duration):
            raise ValueError(f"Paper window outside requested clip: {window!r}")
        out.append((begin, end))
    out.sort()
    if any(a[1] > b[0] for a,b in zip(out, out[1:])):
        raise ValueError("Overlapping card windows")
    return out


def parse_crop_switches(values: list[str], clip_start: float, duration: float, first_x: int) -> str:
    """Crop x expression evaluated per 30fps output frame, never at source fps."""
    result = str(first_x)
    previous = -1.0
    for val in values:
        match = re.fullmatch(r"(\d+(?:\.\d+)?):(\d+)", val)
        if match is None:
            raise ValueError(f"Invalid crop switch {val!r}; expected SOURCE_SECONDS:X")
        at = float(match[1]) - clip_start
        x = int(match[2])
        if not (0 <= at <= duration and at >= previous and 0 <= x <= 2390):
            raise ValueError(f"Invalid crop position/time: {val!r}")
        previous = at
        result = f"if(gte(n\\,{round(at*FPS)})\\,{x}\\,{result})"
    return result


def render_video(source: Path, output: Path, ass_path: Path,
                 start: float, duration: float, crop_x: int,
                 crop_switches: list[str]) -> None:
    if not 0 <= crop_x <= 2390:
        raise ValueError("crop-x outside 3200-wide source")
    # Filter uses a fixed, centered speaker crop; manual QA required for speaker switches.
    # ASS paper cards obscure video only when intended; native source audio remains continuous.
    escaped = str(ass_path.resolve()).replace("\\", "\\\\").replace(":", "\\:").replace(",", "\\,").replace("'", "\\'")
    vf = (
        f"fps={FPS},crop=810:1440:x='{parse_crop_switches(crop_switches, start, duration, crop_x)}':y=0,"
        f"scale={W}:{H}:flags=lanczos,"
        f"ass='{escaped}'"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    run("ffmpeg", "-hide_banner", "-nostdin", "-y", "-loglevel", "error",
        "-ss", str(start), "-i", str(source), "-t", str(duration),
        "-vf", vf, "-af",
        "highpass=f=80,acompressor=threshold=-21dB:ratio=2.1:attack=15:release=160,"
        "loudnorm=I=-16:TP=-1.5:LRA=10",
        "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(output))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path)
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--duration", type=float, default=35)
    ap.add_argument("--paper", action="append", default=[], metavar="SOURCE_START:SOURCE_END")
    ap.add_argument("--crop-x", type=int, default=800, help="for 3200x1440 source; 800=Gloc-9")
    ap.add_argument("--crop-switch", action="append", default=[], metavar="SOURCE_SECONDS:X",
                    help="Switch portrait crop on verified camera changes; repeat as needed")
    ap.add_argument("--transcript", type=Path, help="Groq verbose_json with word timestamps; skips API")
    ap.add_argument("--output", type=Path, default=Path("out/synced-quote.mp4"))
    ap.add_argument("--no-render", action="store_true", help="Validate and create ASS/JSON, no MP4")
    args = ap.parse_args()
    try:
        if not args.source.is_file():
            raise FileNotFoundError(args.source)
        if args.start < 0 or args.duration <= 0:
            raise ValueError("Invalid time range")
        if args.transcript is not None:
            data = json.loads(args.transcript.read_text(encoding="utf8"))
        else:
            # Uses the existing repo's Groq helper and requires GROQ_API_KEY.
            # The source stays local; only extracted compressed audio goes to Groq.
            from groq_transcribe import transcribe_video
            data = transcribe_video(args.source, "whisper-large-v3", None)
        words = get_audio_words(data)
        paper = parse_windows(args.paper, args.start, args.duration)
        captions, groups = render_ass(words, args.start, args.duration, paper)
        base = args.output.with_suffix("")
        base.parent.mkdir(parents=True, exist_ok=True)
        ass = base.with_suffix(".ass")
        metadata = base.with_name(base.name + "-timing.json")
        ass.write_text(captions, encoding="utf8")
        metadata.write_text(json.dumps({
            "origin": "groq-word-timestamps", "sourceStart": args.start,
            "duration": args.duration, "groups": groups,
            "reviewRequired": True,
        }, ensure_ascii=False, indent=2), encoding="utf8")
        print(f"From {len(words)} ASR words: {len(groups)} subtitle groups")
        print(f"ASS: {ass}; word timestamps: {metadata}")
        if not args.no_render:
            render_video(args.source, args.output, ass, args.start, args.duration,
                         args.crop_x, args.crop_switch)
            print(f"Rendered: {args.output}")
        print("REVIEW REQUIRED: Whisper timestamps/text may contain errors. Verify against original audio.")
        return 0
    except (OSError, ImportError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Cannot produce verified word subtitles: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
