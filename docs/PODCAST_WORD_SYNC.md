# Speech-accurate kinetic captions — mandatory standard

## Why the Gloc-9 V6 captions were rejected

The V6 renderer assigned word start positions in proportion to word length inside a manually estimated phrase window. That method **cannot synchronize** each word to the actual spoken audio. Even when the transcript text is correct, it can produce captions that appear far too early or late.

**Do not publish another podcast video using approximated word timing.** Source-based transcription with actual per-word timestamps is now mandatory.

## Correct editorial pipeline

1. Start with authorized podcast footage, locally.
2. Extract mono audio and transcribe it with **Groq Whisper** using `response_format=verbose_json` and `timestamp_granularities=["word", "segment"]`, via the repository's existing `scripts/groq_transcribe.py`.
3. Confirm the recognized words exactly match the **real spoken audio**, particularly Tagalog/English code-switches, proper names and fillers. ASR still makes mistakes.
4. For each word, retain the ASR **start** and **end**. The renderer must not estimate a word's position from its length, redistribute words uniformly, or substitute a paraphrase.
5. Render each word with its own 90ms fade-in and 165ms upward-motion/scale entrance, beginning at that **word's actual timestamp**. Previously spoken words stay visible until the phrase group ends.
6. Group at most five words without shifting their visual positions after a new one appears. Switch to a fresh group on a 0.42s pause, card boundary, max length, or text-width limit.
7. Use a minimalist black/white editorial layout; show source speaker shots plus short off-white type cards **while original source audio continues**. Cropping changes must follow the speaker and each shot.
8. **Review** the generated subtitles at normal speed and by stepping through high-impact words. Shift per-word timing if ASR onsets are wrong. Only then declare the MP4 publish-ready.

## One-command workflow

The editor can generate the aligned JSON and final MP4 in Codespaces when `GROQ_API_KEY` is available:

```bash
python3 scripts/render-synced-podcast.py /path/to/50866.mp4 \
  --start 12 --duration 36.5 \
  --paper 21.6:25.8 --paper 25.8:30.25 \
  --crop-x 800 \
  --crop-switch 15.83:1770 \
  --crop-switch 16.83:800 \
  --crop-switch 19.77:1770 \
  --crop-switch 21.6:800 \
  --crop-switch 30.6:1770 \
  --crop-switch 34.9:1250 \
  --crop-switch 37.77:1770 \
  --crop-switch 39:800 \
  --output out/gloc9-word-synced.mp4
```

Every source time above is in **seconds of the original 50.3s source clip**. The paper scene and crop switch values are a visual starting point and must be rechecked against source footage and the transcript; unlike the caption onsets, those values do not claim to be automatically recognized.

The script uses the local recording for the finished video, generates the transcript via a temporary 16kHz 48kbps audio upload, and writes:

- `out/gloc9-word-synced.mp4` — rendered portrait clip, if successful.
- `out/gloc9-word-synced.ass` — independently synchronized words.
- `out/gloc9-word-synced-timing.json` — timestamped source-word groups for QA.

**No artificial transcript fallback.** If the Groq key is missing, no word timestamps are returned, or the requested clip has no transcribed words, the renderer exits nonzero rather than generating false synchronized captions.

If Groq already produced a reviewed verbose JSON transcript, pass `--transcript path/to/output.json` to avoid paying for a second transcription.

## Rights and release checklist

The public repository never includes user-uploaded third-party source footage or derived exports. Confirm permissions to redistribute the original GMA interview and review content context, actual transcript wording, word-level A/V sync and platform safe zones before publishing.

## Development tests

```bash
python3 -m unittest discover -s tests -p test_podcast_audio_sync.py -v
```

Regression tests exercise preserved source word onsets, absence of fake timestamps, caption grouping and camera crop switches without external API access.
