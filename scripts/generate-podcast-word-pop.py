#!/usr/bin/env python3
"""Build clean word-by-word ASS motion captions from reviewed speech timings.

The JSON is an *alignment manifest*, never AI-generated quotes. Each word start
must come from the actual source recording. No automatic or guessed timestamps
are introduced by this renderer.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

HEADER = """[Script Info]
Title: Editorial Word Reveal
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style:Speaker,Inter Display,74,&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,1,0,0,0,100,100,-1,0,1,3,1,5,40,40,40,1
Style:Paper,Inter Display,83,&H001D1D1D,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,1,0,0,0,100,100,-1,0,1,0,0,5,40,40,40,1
Style:Detail,Inter Display,25,&H00777777,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,0,0,5,40,40,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def timestamp(sec: float) -> str:
    if sec < 0 or not math.isfinite(sec):
        raise ValueError("Timestamp must be finite and nonnegative")
    hours = int(sec // 3600)
    minutes = int(sec // 60) % 60
    return f"{hours}:{minutes:02d}:{sec % 60:05.2f}"


def dialogue(layer: int, start: float, end: float, style: str, text: str) -> str:
    return f"Dialogue: {layer},{timestamp(start)},{timestamp(end)},{style},,0,0,0,,{text}"


def escape_ass(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "").replace("}", "").replace("\n", " ")


def validate(manifest: dict) -> None:
    if not isinstance(manifest.get("scenes"), list) or not manifest["scenes"]:
        raise ValueError("At least one scene is required")
    last = 0.0
    for scene in manifest["scenes"]:
        start = float(scene["start"])
        end = float(scene["end"])
        if not (math.isfinite(start) and math.isfinite(end) and last <= start < end):
            raise ValueError("Scenes must be ordered, nonoverlapping, and positive length")
        if scene["mode"] not in ("speaker", "paper"):
            raise ValueError("Scene mode must be speaker or paper")
        words = scene["words"]
        if not words:
            raise ValueError("Every scene needs explicitly aligned words")
        previous = start - 1
        for word in words:
            position = float(word["start"])
            if not (start <= position < end and position > previous):
                raise ValueError("Every word must have a unique, increasing start within its scene")
            if not isinstance(word["text"], str) or not word["text"].strip():
                raise ValueError("Word text cannot be empty")
            previous = position
        last = end


def compose(manifest: dict) -> str:
    validate(manifest)
    captions: list[str] = []
    for scene in manifest["scenes"]:
        start, end = float(scene["start"]), float(scene["end"])
        paper = scene["mode"] == "paper"
        style = "Paper" if paper else "Speaker"
        if paper:
            captions.append(dialogue(1, start, end, "Paper",
                r"{\an7\pos(0,0)\p1\c&HF6F5F2&}m 0 0 l 1080 0 l 1080 1920 l 0 1920{\p0}"))
            captions.append(dialogue(3, start, end, "Paper",
                r"{\an7\pos(0,0)\p1\c&H1B1D21&}m 0 0 l 190 0 l 118 33 l 158 89 l 78 85 l 96 175 l 44 118 l 0 190{\p0}"))
            captions.append(dialogue(3, start, end, "Paper",
                r"{\an7\pos(1080,1920)\p1\c&H1B1D21&}m 0 0 l -170 0 l -112 -35 l -141 -85 l -70 -80 l -80 -168 l -30 -116 l 0 -175{\p0}"))
        words = scene["words"]
        # Small rolling groups, precisely revealed; no giant static quote cards.
        groups = [words[i:i + 4] for i in range(0, len(words), 4)]
        for i, group in enumerate(groups):
            finish = float(groups[i + 1][0]["start"]) if i + 1 < len(groups) else end
            width = sum(max(38, len(w["text"]) * (38 if paper else 31)) for w in group)
            width += (len(group) - 1) * 18
            scale = min(1.0, 920 / max(1, width))
            x = (1080 - width * scale) / 2
            y = 980 if paper else 1440
            for w in group:
                size = max(43, round((83 if paper else 74) * scale))
                text = escape_ass(w["text"])
                estimate_width = max(38, len(text) * (38 if paper else 31)) * scale
                center = x + estimate_width / 2
                x += estimate_width + 18 * scale
                strong = bool(w.get("emphasis", False))
                color = r"&H00434CC9&" if paper and strong else r"&H00191919&" if paper else r"&H00FFFFFF&"
                at = float(w["start"])
                if finish - at <= 0.04:
                    continue
                motion = (r"{\an5\move(" + f"{center:.0f},{y + 24:.0f},{center:.0f},{y:.0f},0,200)"
                          + r"\fscx87\fscy87\t(0,190,\fscx100\fscy100)"
                          + r"\fad(95,95)\1c" + color + rf"\fs{size}" + "}")
                captions.append(dialogue(20, at, finish, style, motion + text))
        if paper:
            captions.append(dialogue(5, start, end, "Detail",
                r"{\an8\pos(540,275)\fsp2\c&H777777&}GLOC-9   /   i-LISTEN"))
    return HEADER + "\n".join(captions) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("alignment_json", type=Path)
    parser.add_argument("output_ass", type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.alignment_json.read_text(encoding="utf8"))
    result = compose(manifest)
    args.output_ass.parent.mkdir(parents=True, exist_ok=True)
    args.output_ass.write_text(result, encoding="utf8")
    print(f"Rendered {len(manifest['scenes'])} scenes: {args.output_ass}")


if __name__ == "__main__":
    main()
