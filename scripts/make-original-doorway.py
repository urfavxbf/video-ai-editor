#!/usr/bin/env python3
"""Build original Tagalog narration, timed subtitles and self-generated soundtrack.

Online Filipino speech uses edge-tts, an unofficial Edge service client. When it
is unavailable, gTTS is a best-effort fallback (not a commercial TTS SLA).
All visuals and music are produced locally; no stock or borrowed footage.
"""
from __future__ import annotations

from array import array
import argparse
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import sys
import wave

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "public" / "original" / "doorway"
DURATION_PATH = ROOT / "out" / "doorway-props.json"

# Original script; scientific wording avoids presenting doorway forgetting as inevitable.
SCRIPT = (
    "Pumasok ka sa kuwarto para kumuha ng isang bagay... "
    "pero pagdating mo, bigla kang nablangko. Bakit nga ba? "
    "May tawag diyan: doorway effect. "
    "Kapag lumilipat tayo ng lugar, puwedeng magbago ang konteksto ng iniisip natin. "
    "Para bang bagong eksena ang binubuksan ng utak. "
    "Minsan, mas mahirap tuloy balikan ang naunang pakay, lalo na kapag marami kang iniisip. "
    "Pero hindi ito palaging nangyayari. Magkakaiba ang resulta ng mga pag-aaral. "
    "Kaya kung makalimutan mo ang pakay mo, subukan mong bumalik sa pinanggalingan mo. "
    "Baka doon mo maalala kung ano talaga ang kukunin mo!"
)


def media_duration(path: Path) -> float:
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nokey=1:noprint_wrappers=1", str(path)],
        text=True, capture_output=True, check=True
    )
    return float(p.stdout.strip())


def generate_voice() -> bool:
    dest = DIR / "voiceover.mp3"
    srt = DIR / "voiceover.srt"
    cmd = [sys.executable, "-m", "edge_tts",
           "--voice", "fil-PH-AngeloNeural",
           "--rate=+8%", "--text", SCRIPT,
           "--write-media", str(dest), "--write-subtitles", str(srt)]
    try:
        subprocess.run(cmd, timeout=150, check=True, stdout=subprocess.DEVNULL)
        if dest.stat().st_size < 10000:
            raise ValueError("voiceover too short")
        print("Filipino voice synthesized via edge-tts.")
        return True
    except Exception as exc:
        print("edge-tts unavailable; trying Filipino gTTS fallback:", type(exc).__name__)
        srt.unlink(missing_ok=True)
        from gtts import gTTS
        gTTS(text=SCRIPT, lang="tl", slow=False).save(str(dest))
        if dest.stat().st_size < 10000:
            raise RuntimeError("Failed to produce actual voiceover")
        return False


def seconds(s: str) -> float:
    hh, mm, rest = s.replace(",", ".").split(":")
    return int(hh) * 3600 + int(mm) * 60 + float(rest)


def subtitle_words() -> list[tuple[float, float, str]]:
    path = DIR / "voiceover.srt"
    if not path.exists():
        return []
    contents = path.read_text(encoding="utf-8-sig")
    results = []
    for block in re.split(r"\n\s*\n", contents):
        match = re.search(
            r"(\d\d:\d\d:\d\d[,.]\d+)\s*-->\s*(\d\d:\d\d:\d\d[,.]\d+)",
            block)
        if match:
            phrase = block[match.end():].strip()
            phrase = re.sub(r"<[^>]*>", "", phrase)
            if phrase:
                results.append((seconds(match.group(1)), seconds(match.group(2)), phrase))
    return results


def captions_from_words(duration: float, words: list[tuple[float, float, str]]) -> list[dict]:
    if not words:
        # Approximate timings only if fallback synthesizer cannot provide word boundaries.
        parts = re.findall(r"\S+", SCRIPT)
        out = []
        width = 4
        for i in range(0, len(parts), width):
            start = duration * i / len(parts)
            end = duration * min(i + width, len(parts)) / len(parts)
            out.append({"startFrame": round(start * 30), "endFrame": round(end * 30),
                        "text": " ".join(parts[i:i+width])})
        return out

    # Combine word-boundary SRT entries into 3–5-word subtitle cards.
    cards = []
    group: list[tuple[float, float, str]] = []
    def flush():
        nonlocal group
        if not group:
            return
        start = group[0][0]
        end = max(group[-1][1], start + .13)
        txt = " ".join(x[2] for x in group)
        cards.append({"startFrame": max(0, round(start * 30)),
                      "endFrame": max(round(start * 30) + 1, round(end * 30)),
                      "text": txt})
        group = []

    for word in words:
        if group and (word[0] - group[-1][1] > .30 or
                      len(group) >= 5 or
                      word[0] - group[0][0] >= 1.9):
            flush()
        group.append(word)
        if re.search(r"[?!]$", word[2]) and len(group) >= 2:
            flush()
    flush()
    return cards


def soundtrack(duration: float) -> None:
    # Entirely synthesized composition. Atmospheric pads, alternating bass notes,
    # ticking pulses; no external music or samples.
    sr = 22050
    total = int(duration * sr)
    phase = [0.0, 0.0, 0.0]
    notes = [55, 65.406, 73.416, 49, 55, 82.407, 73.416, 65.406]
    out = DIR / "score.wav"
    with wave.open(str(out), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        # Chunked to keep RAM usage constant.
        for begin in range(0, total, 22050):
            end = min(total, begin + 22050)
            buff = array("h")
            for i in range(begin, end):
                t = i / sr
                idx = int(t / 4) % len(notes)
                root = notes[idx]
                swell = .45 + .55*(.5-.5*math.cos(2*math.pi*min(1,(t%4)/4)))
                pad = (math.sin(2*math.pi*root*t)*.44 +
                       math.sin(2*math.pi*root*1.5*t)*.16 +
                       math.sin(2*math.pi*root*2.0*t)*.11)
                pulse = math.exp(-20*(t%1.0)) * math.sin(2*math.pi*180*(t%1.0)) * .17
                spark = math.exp(-40*(t%2.0)) * math.sin(2*math.pi*630*(t%2.0)) * .04
                entrance = min(1.0,t/1.8)
                exit_ = min(1.0,(duration-t)/2)
                val = (.20*pad*swell + .025*pulse + .012*spark) * entrance * max(0.0,exit_)
                buff.append(int(max(-1,min(1,val))*32767))
            wf.writeframes(buff.tobytes())


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "out").mkdir(parents=True, exist_ok=True)
    edges = generate_voice()
    duration = media_duration(DIR / "voiceover.mp3")
    if not (17 < duration < 78):
        raise ValueError(f"Unexpected speech duration: {duration}")
    total_frames = math.ceil(duration * 30) + 12
    captions = captions_from_words(duration, subtitle_words() if edges else [])
    if not captions:
        raise ValueError("Speech caption alignment did not generate subtitles")
    soundtrack(total_frames / 30)
    data = {"totalFrames": total_frames, "captions": captions, "narrationAvailable": True}
    DURATION_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    print(f"Original video assets ready: {duration:.2f}s narration, "
          f"{total_frames} frames, {len(captions)} caption cards.")
    print(f"Built original score: {DIR / 'score.wav'}")
    print(f"Ready props: {DURATION_PATH}")


if __name__ == "__main__":
    main()
