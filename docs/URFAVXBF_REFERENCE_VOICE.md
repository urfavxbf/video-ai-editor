# UrFavXBF — reference-matched Filipino storyteller voice

**Status:** CPU-only reference-clone path implemented, awaiting model inference and listening QA. The supplied reference audio is deliberately **not committed** to GitHub. This opt-in Tagalog path does not change the approved English Chatterbox Natural Storyteller narrator or PIX's independently approved identity.

## Why VoxCPM2, not pitch-shifted Edge TTS?

VoxCPM2 supports Tagalog among 30 languages, local speaker-reference cloning via `reference_wav_path`, and `device="cpu", optimize=False`. A reference can guide the speaker timbre, unlike a generic Azure/Edge voice, but cloning is **not guaranteed to sound identical**. It is computationally heavy: the 2B model requires several GB of download/RAM and CPU inference may be slow. License for code/model: Apache-2.0. Source: https://voxcpm.readthedocs.io/en/latest/usage_guide.html

## Personal/local setup (no GPU and no paid API)

1. Obtain an authorized, clean, single-speaker reference recording. Do not publish it or put it in a public Git repo. Consent/rights to synthesize the speaker are required.
2. Create a **5–30 second, mono, 16 kHz, 16-bit PCM WAV**. For the owner's supplied ~46-second MP3, the locally reviewed candidate trim is 29.4–41.6 seconds (12.2 seconds). Adjust if an audition reveals noise/music:

   ```bash
   mkdir -p input
   ffmpeg -hide_banner -y -ss 29.4 -t 12.2 -i "lyca the breadwinner.mp3" -ac 1 -ar 16000 -c:a pcm_s16le input/urfavxbf-reference.wav
   ```

3. On Python 3.10–3.12 with adequate RAM, install the existing optional VoxCPM2 runtime (no GPU):

   ```bash
   python3.11 -m venv .venv-voxcpm
   .venv-voxcpm/bin/pip install -r requirements-voxcpm.txt
   ```

4. Dry-run before actual inference:

   ```bash
   .venv-voxcpm/bin/python scripts/character_voiceover.py \
     --character urfavxbf --language tl --device cpu \
     --reference-audio input/urfavxbf-reference.wav --confirm-voice-rights \
     --text "Siyam na taon pa lang. Breadwinner na si Laika. Pero bakit?" \
     --output out/urfavxbf-tagalog.wav --dry-run
   ```

5. Remove `--dry-run` to synthesize WAV locally. The original recording never leaves the machine in this workflow. The manifest beside the generated WAV records `voice_mode=reference-clone` and the reference's SHA-256, **not the reference audio or its local path**. Keep the same local reference for a stable character identity across episodes.

This code supports an **explicit Tagalog opt-in only**. It does not silently change all English videos to Tagalog or switch PIX to a male voice. Any future automatic pipeline should supply the private reference path explicitly and fail rather than silently substitute a generic voice.

## Quality gate

Before exporting a finished episode, compare generated and reference audio by listening: Filipino pronunciation, timbre, natural rests, intonation, consistency between chunks, clipping, and mouth/scene sync. Check the actual output with ffprobe; ensure captions are aligned to real narration. No live model generation or identical-sounding audio has yet been verified in this repository.

## Security and rights

Cloning is for speaker-authorized references only. The CLI requires `--confirm-voice-rights` whenever `--reference-audio` is passed. Keep original WAV and MP3 in `input/` (already gitignored); do not add voice samples to PRs or logs, do not send them to third-party services, and label publicly released synthetic narration appropriately.
