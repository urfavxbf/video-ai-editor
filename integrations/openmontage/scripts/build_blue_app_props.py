#!/usr/bin/env python3
"""Prepare OpenMontage Explainer props for the narrated TikTok video.

This is a small adapter to the EXISTING OpenMontage Remotion renderer, not
a new video editor or agent. Word timing is estimated from Chatterbox chunk
boundaries; it requires visual/audio review before publication.
"""
from __future__ import annotations
import argparse
import json
import re
import wave
from copy import deepcopy
from pathlib import Path

PRODUCTION = Path(__file__).resolve().parents[3] / "productions" / "blue-app-html-history"
PLANNED_SECONDS = 69.0
APPROVED_VOICE = "natural-storyteller-v1"

def build_props(template: dict, manifest: dict, audio_seconds: float) -> dict:
    if manifest.get("voice_profile") != APPROVED_VOICE or manifest.get("language") != "en":
        raise ValueError("Unapproved narrator or language in TTS manifest")
    if not (20 <= audio_seconds <= 110):
        raise ValueError("Narration must be 20–110 seconds for the pilot")
    if not isinstance(template.get("cuts"), list) or len(template["cuts"]) < 7:
        raise ValueError("Insufficient tutorial scenes")
    cuts = template["cuts"]
    if cuts[0]["in_seconds"] != 0 or cuts[-1]["out_seconds"] != PLANNED_SECONDS:
        raise ValueError("Unexpected tutorial template duration")
    target = audio_seconds + 1.8
    multiplier = target / PLANNED_SECONDS
    output = deepcopy(template)
    for item in output["cuts"] + output.get("overlays", []):
        item["in_seconds"] = round(item["in_seconds"] * multiplier, 3)
        item["out_seconds"] = round(item["out_seconds"] * multiplier, 3)
    chapters = manifest.get("chunks", [])
    if not isinstance(chapters, list) or not chapters:
        raise ValueError("Missing Chatterbox timing chunks")
    captions = []
    for chapter in chapters:
        words = re.findall(r"\S+", chapter.get("text", ""))
        start = float(chapter["start_seconds"])
        end = float(chapter["end_seconds"])
        if not words or not 0 <= start < end <= audio_seconds + 0.5:
            raise ValueError("Invalid narration chunk timestamps")
        weights = [max(2, len(re.sub(r"[^A-Za-z0-9]", "", word))) for word in words]
        total = sum(weights)
        position = start
        for idx, word in enumerate(words):
            nxt = position + (end-start) * weights[idx] / total
            captions.append({
                "word": word,
                "startMs": round(position * 1000),
                "endMs": round(nxt * 1000),
                "pageBreakAfter": idx == len(words)-1,
            })
            position = nxt
    output["captions"] = captions
    output["audio"] = {"narration": {"src": "audio/blue-app-narration.wav", "volume": 1}}
    return output

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wav", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with wave.open(str(args.wav), "rb") as voice:
        if voice.getnchannels() not in (1, 2) or voice.getframerate() < 16000:
            raise ValueError("Invalid speech WAV format")
        seconds = voice.getnframes() / voice.getframerate()
    template = json.loads((PRODUCTION / "scene-props.json").read_text(encoding="utf-8"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    props = build_props(template, manifest, seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(props, indent=2)+"\n", encoding="utf-8")
    print(f"Prepared {len(props['cuts'])} scenes, {len(props['captions'])} estimated word cues, {seconds:.1f}s narration")

if __name__ == "__main__":
    main()
