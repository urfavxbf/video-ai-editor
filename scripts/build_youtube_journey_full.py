#!/usr/bin/env python3
"""Assemble all 68 approved English turns from *real* WAV files.

Editorial storyboard timecodes are targets, never a reason to time-stretch
speech or invent caption synchronization. This writes a draft Remotion props
manifest and loud drift warnings for an editor to address.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_youtube_journey_preview import (
    FPS, caption_blocks, inspect_wav, validate_script,
)
from extract_voice_envelope import voice_event_from_wav

EPISODE = "youtube-beginner-journey"
SCENE_BEAT = {**{i: i for i in range(1, 8)}, 8: 8, 9: 8}


def assemble_full(script: Path, storyboard: Path, audio_root: Path, public_root: Path,
                  gap_frames: int = 7) -> dict:
    if not 0 <= gap_frames <= FPS * 2:
        raise ValueError("gap_frames must be between 0 and 60")
    dialogue = json.loads(script.read_text(encoding="utf-8"))
    lookup = validate_script(dialogue)
    visual = json.loads(storyboard.read_text(encoding="utf-8"))
    beats = visual.get("beats", [])
    if (visual.get("episode") != EPISODE or len(beats) != 8 or
            visual.get("format") != dialogue["format"] or
            beats[-1]["endSeconds"] != visual["targetDurationSeconds"]):
        raise ValueError("Storyboard / episode format or ending does not match")
    covered = [n for b in beats for n in b["scenes"]]
    if covered != list(range(1, 10)):
        raise ValueError("Each scripted chapter must be represented exactly once")
    for i, b in enumerate(beats):
        if (b["index"] != i + 1 or b["startSeconds"] < 0 or
                b["endSeconds"] <= b["startSeconds"] or
                (i and b["startSeconds"] != beats[i-1]["endSeconds"])):
            raise ValueError("Invalid or overlapping storyboard timecodes")
    lines, envelopes, timeline = [], [], []
    frame = 0
    last_scene = 0
    for authored in dialogue["lines"]:
        line = lookup[authored["id"]]
        scene = int(line["scene"])
        if scene < last_scene or scene not in SCENE_BEAT:
            raise ValueError("Narration scenes must progress 01–09")
        if lines:
            frame += gap_frames
        speaker = line["speaker"]
        wav = audio_root / speaker / (line["id"] + ".wav")
        samples, rate = inspect_wav(wav)
        duration = math.ceil(samples * FPS / rate)
        asset = (public_root / "voiceovers" / EPISODE / "full" /
                 speaker / wav.name)
        asset.parent.mkdir(parents=True, exist_ok=True)
        if wav.resolve() != asset.resolve():
            shutil.copy2(wav, asset)
        envelopes.append(voice_event_from_wav(wav, speaker, frame, FPS))
        lines.append({
            "id": line["id"], "scene": scene, "speaker": speaker,
            "text": line["text"], "startFrame": frame,
            "endFrame": frame + duration,
            "file": "/".join(asset.relative_to(public_root).parts),
            "captions": caption_blocks(line["text"], frame, frame + duration),
        })
        if scene != last_scene:
            timeline.append({"scene": scene, "beat": SCENE_BEAT[scene],
                             "startFrame": frame})
        frame += duration
        last_scene = scene
    if len(lines) != 68 or len(timeline) != 9:
        raise ValueError("Incomplete 68-turn / nine-chapter timeline")
    total_frames = frame + FPS // 2
    for section in timeline:
        beat = beats[section["beat"] - 1]
        target = beat["startSeconds"]
        section["storyboardStartSeconds"] = target
        section["measuredStartSeconds"] = round(section["startFrame"] / FPS, 3)
        section["driftSeconds"] = round(section["startFrame"] / FPS - target, 3)
    return {
        "lines": lines, "voiceEvents": envelopes, "totalFrames": total_frames,
        "captionTiming": "estimated-unreviewed", "assetsReady": False,
        "durationSeconds": round(total_frames / FPS, 3),
        "storyboardDurationSeconds": visual["targetDurationSeconds"],
        "chapters": timeline, "readyForPublishing": False,
        "reviewRequired": ["speaker voices", "portrait assets", "caption alignment",
                           "graphic timing", "visual playback", "audio mix"],
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--script", type=Path, default=Path("productions/youtube-beginner-journey/dialogue.json"))
    p.add_argument("--visual-aid", type=Path, default=Path("productions/youtube-beginner-journey/visual-aid.json"))
    p.add_argument("--audio-root", type=Path, required=True)
    p.add_argument("--public-root", type=Path, default=Path("public"))
    p.add_argument("--output", type=Path, default=Path("out/youtube-journey-full.props.json"))
    p.add_argument("--gap-frames", type=int, default=7)
    a = p.parse_args(argv)
    try:
        result = assemble_full(a.script, a.visual_aid, a.audio_root, a.public_root, a.gap_frames)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"Measured episode: {result['durationSeconds']} seconds, 68 actual WAVs")
        print(f"Editorial target: {result['storyboardDurationSeconds']} seconds; never time-stretch speech")
        for section in result["chapters"]:
            print(f"Scene {section['scene']:02}: measured {section['measuredStartSeconds']}s "
                  f"vs beat target {section['storyboardStartSeconds']}s "
                  f"(drift {section['driftSeconds']:+.2f}s)")
        print("DRAFT ONLY: reviewed captions, exact graphical cue timing, portrait assets and playback pending")
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(f"Could not build full episode: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
