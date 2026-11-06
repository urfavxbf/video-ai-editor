---
name: transcription-captions
description: Use when transcribing authorized user footage, preparing Groq Whisper JSON TXT SRT outputs, reviewing word timing, or integrating verified captions with actual WAV and Remotion episode timelines.
---

# Transcription and Captions

**Scope:** truthful speech recognition, reviewed captions and media-timed
subtitles. Follow `AGENTS.md`, `docs/PRODUCTION_POLICY.md`,
`docs/AI_VIDEO_TOOLS.md` and `docs/PRODUCTION_STANDARD.md`.
Load official `remotion-captions` when implementing visual subtitles; it
owns Remotion-specific caption structures and animation, not provider consent.

## Choose the source safely

1. Inspect actual authorized input audio/video, language and required output.
   Prefer existing verified local transcripts and approved caption timing when
   available; avoid unnecessary external transmission.
2. Groq Whisper transcription through `scripts/groq_transcribe.py` is a
   **third-party upload**. Request explicit owner permission to transmit that
   particular recording and to accept any service cost. A `GROQ_API_KEY` is
   required via an environment secret; never print, commit or paste it.
3. If permission/key is absent, do not call the remote script, fabricate a
   transcript, or assert that an uninstalled local speech recognizer is
   available. Report the blocked step and continue only with authorized
   local input.

## Authorized Groq workflow

With FFmpeg, the Groq Python dependency and a permitted input file:

```bash
python3 scripts/groq_transcribe.py input/myclip.mp4 \
  --output-dir out/transcripts
```

The script extracts/compresses audio and **uploads speech** to Groq. It
writes `<stem>.json`, `<stem>.txt`, and `<stem>.srt` when successful.
Its default model is `whisper-large-v3-turbo`. Omit `--language` for
mixed-language/Taglish speech; use `--language tl` only for purely Tagalog
source audio when appropriate. User chat language does not change the
approved English language for new original productions.

## Timing and QA

- Review names, code-switching, punctuation, missed words, segment boundaries,
  readability, safe areas, and audible start/end times against **real audio**.
- Groq-produced word estimates are **not automatically** approved production
  alignment. For voiceover assembly, `scripts/episode_media.py` requires
  reviewed alignment bound to the exact WAV SHA-256, checked durations and
  speaker identity; do not synthesize timings from text length or clip names.
- Preserve original language and dialogue unless redubbing/translation was
  explicitly requested. Do not confuse RMS volume cues with visemes.
- Run relevant model-free checks:
  ```bash
  python3 -m unittest discover -s tests -p 'test_groq_transcribe.py' -v
  python3 -m unittest discover -s tests -p 'test_episode_media.py' -v
  node --test tests/episode-captions.test.cjs
  ```
- Inspect representative caption frames and final decoded audio/video output.
  SRT/JSON success alone is not proof of final subtitled MP4 delivery.
