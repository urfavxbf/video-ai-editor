# UrFavXBF — 33 fast text effects (voiced English preview)

**Owner request, 2026-11-02:** Show all 33 retro motion ideas with the animation applied to **text rather than the character**. Keep the 8-bit UrFavXBF visible at left as a speaking presenter. Fast, discrete one-effect-at-a-time transitions.

- Composition: `Host33MotionShowcase`, 1920×1080 at 30fps.
- 33 named treatments × 36 frames = **1,188 frames / 39.6 seconds**.
- Character: original 116-frame SVG UrFavXBF host pack, animated independently. No mask or text effect transforms the host.
- Narration: approved **English Chatterbox V3 natural-storyteller-v1** on CPU, using `scripts/8bit-33-voiceover.txt`.
- Speech is narration, not phoneme-level lip-sync. A preset by itself is not a WAV.
- No paid cloud providers, GPU, third-party uploads, or merge to main.
- This is a 33-text-motion **showcase**; the project's original 21+12 video FX implementations remain available unchanged.

## Rendering with real audio

The pull-request GitHub Actions workflow `8bit-host-33-motion-preview.yml` generates actual Chatterbox speech from the committed script using the existing `scripts/character_voiceover.py` pathway, aligns measured WAV duration within a limited tempo envelope using `scripts/prepare_8bit_voiceover.py`, renders the Remotion composition with a local verified WAV, and checks actual H.264 + AAC streams and 1,188 fully decoded frames. Uploads MP4, WAV, and source script as one GitHub artifact.

Visual-only local preview (no voice claimed):

```bash
npm ci
npm run typecheck
npx remotion render Host33MotionShowcase out/text-only.mp4 --codec=h264
```

Audio-backed renders require a **real** file under `public/narration`, not a substituted silent file:

```bash
python scripts/character_voiceover.py --character urfavxbf --language en --device cpu --text-file scripts/8bit-33-voiceover.txt --output out/8bit-host-raw.wav
python scripts/prepare_8bit_voiceover.py out/8bit-host-raw.wav public/narration/8bit-host-39s.wav
npx remotion render Host33MotionShowcase out/8bit-host-voiced.mp4 --props='{"voiceoverFile":"narration/8bit-host-39s.wav"}' --audio-codec=aac
```

If CPU synthesis, alignment, stream validation, or full decode fails, the video is **not** verified as voiced. Review pacing and spoken accuracy by listening before any public release.

## Real Chatterbox failure and timing correction (2026-11-02)

The first real English voice-render job synthesized a **26.56s WAV** from the 96-word script; the alignment tool rejected a 0.68 tempo ratio as unnatural. This is a narration-length issue, not evidence that Chatterbox V3 is broken. The revised **154-word** script explicitly describes each text effect and targets the measured 39.6-second edit. The guard still rejects unsupported large speed changes. CI also saves the raw WAV as a diagnostic artifact even if alignment or final rendering fails. Only treat the video as successfully voiced after a completed workflow with H.264 + AAC verification.
