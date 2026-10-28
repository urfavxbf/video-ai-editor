# Y2038 — Tagalog long-form production pack

## Episode identity

**Title:** The 2038 Problem: Bakit Puwedeng Bumalik sa 1901 ang Orasan ng Computer?  
**Hosts:** UrFavXBF (Neon Storyteller) and PIX (Pixel Spark)  
**Language:** Tagalog/Taglish (tl) by default; approved VoxCPM2 voice designs only  
**Visual:** two enlarged 414 × 468 pixel-glitch HEAD portraits; no full-body overlays  
**Master:** 1920 × 1080, 16:9, 30 fps, H.264 + AAC  
**Script:** 40 speaker turns, 8 chapters, 882 whitespace-delimited words; ~7m45s *estimated workprint*.

## Story

1. Ang Oras na Bumalik: the precise 2038 timestamp boundary.
2. Bakit Binibilang ang Segundo: the 1970 Unix epoch.
3. Isang Number na may Hangganan: signed 32-bit range and conditional wrap.
4. Ano ang Posibleng Masira: bounded, implementation-dependent risks.
5. Bakit may Ligtas na Systems: 64-bit time and dependency audits.
6. Ang Bug na Maagang Dumating: future-date calculations.
7. Paano Ito Inaayos: boundary tests, migration and compatibility.
8. Hindi Katapusan ng Mundo: evidence-based conclusion.

## Fact-check guardrails

- Largest signed 32-bit Unix seconds value: 2,147,483,647, or 2038-01-19 03:14:07 UTC.
- The first out-of-range timestamp is 2038-01-19 03:14:08 UTC.
- 1901-12-13 20:45:52 UTC is a wraparound *example*, not guaranteed behavior.
- Outcomes vary by platform, calling convention, kernel, library and application logic.
- Many contemporary platforms have 64-bit timestamp support, but long-lived legacy paths still need testing.

Primary technical references:
- https://manpages.debian.org/unstable/manpages-dev/time.2.en.html
- https://www.gnu.org/software/gnulib/manual/html_node/Avoiding-the-year-2038-problem.html
- https://www.sourceware.org/glibc/manual/2.40/html_node/64_002dbit-time-symbol-handling.html

## Material currently ready

- `src/episodes/y2038Dialogues.ts`: entire character dialogue and initial timing model.
- `src/episodes/Y2038LongForm.tsx`: Remotion composition registered as `Y2038LongForm`.
- `scripts/y2038_export_voice_cues.py`: prepares Tagalog voice text files and JSON manifest.
- `scripts/stage_y2038_sprites.py`: safely stages approved PNG expression assets from the owner's Library ZIP.
- Original ambient score generator available at `scripts/y2038_generate_ambient.py` (no third-party music).\n- The existing V2 sprite ZIP remains in Library; no generated character art or model weights are added to GitHub.

## Rendering in Codespaces / Linux

```bash
npm ci
python3 scripts/stage_y2038_sprites.py --zip /path/to/PixelGlitch_Complete_Pack.zip
python3 scripts/y2038_export_voice_cues.py
python3 scripts/y2038_generate_ambient.py --seconds 480
npm run typecheck
npx remotion render Y2038LongForm out/y2038-visual-workprint.mp4 \
  --codec=h264 --crf=20 --pixel-format=yuv420p \
  --props='{"assetsReady":true,"backgroundMusicPath":"audio/y2038-ambient.wav"}'
```

To synthesize candidate voice tracks on a compatible GPU-enabled runtime:

```bash
python3 scripts/y2038_export_voice_cues.py --generate --device cuda
python3 scripts/y2038_audio_props.py
npx remotion render Y2038LongForm out/y2038-voiced.mp4 --props=out/y2038/remotion-voice-props.json
```

This command uses the existing approved Tagalog VoxCPM2 router; it is not a cloud TTS service. Generation may require sizable downloads, memory and compute. Do not substitute unapproved English samples.

## Final production gates

1. Listen to and verify both Tagalog voice identities and pronunciations. Reject unnatural or inconsistent voices.
2. Derive actual cue boundaries and word-level captions from synthesized WAVs. Initial frame intervals in script are estimates only.
3. Use real WAV RMS envelopes for speaking state; never fabricate waveform/lip-sync measurements.
4. Render character portraits with source assets, chapter-specific motion graphics and time-aligned captions.
5. Review captions, audio levels, safe title margins, source credits, factual claims, and exported MP4 with ffprobe.
6. Keep the video **offline** for review; do not automatically upload to YouTube.

### Status

**Episode source ready for review and rendering.** The example visual preview is NOT a completed voiceover documentary. A final voiced MP4 cannot be asserted until the approved Tagalog WAVs are rendered and verified.


## Bilingual voices and Actions execution (2026-10-28)

The two original English Chatterbox V3 profiles remain unchanged and available by explicit `--language en`. `characters/registry.json` selects VoxCPM2 Tagalog (`tl`) by default. The VoxCPM2 2.0.3 API does not take a `seed` parameter: the generator now seeds PyTorch, and the episode batch **loads the model only once**.

For an *individual* synthetic speech sample:

```bash
python scripts/character_voiceover.py --character urfavxbf \
  --text "Alam mo ba, PIX? May misteryo sa computer." --output out/urfavxbf-tl.wav
python scripts/character_voiceover.py --character pix \
  --text "Hala, seryoso? Tara, alamin natin!" --output out/pix-tl.wav
```

Use Python 3.11 with `pip install -r requirements-voxcpm.txt`, plus a suitable GPU for efficient inference. Optional CPU inference may be extremely slow and memory-intensive with the 2B-parameter checkpoint.

A dedicated `.github/workflows/voxcpm-tagalog.yml` workflow:
- **sample:** Standard GitHub-hosted CPU runner, first two dialogue WAVs (one PIX, one UrFavXBF), 180-minute cutoff; uploads real outputs as artifacts only if successful.
- **full:** Requires a preconfigured trusted self-hosted Linux runner labeled `gpu`; creates all 40 dialogue WAVs and a measured Remotion props JSON.
- No external TTS account, fees or voice rights for the English profiles are silently altered.
- Never claim the WAVs or MP4 have been generated until the workflow shows success. A successful artifact still requires listening/QC before being approved as final character voices.

Run model-free CI at any time: `python3 -m unittest discover -s scripts -p 'test_y2038_*.py' -v`.
