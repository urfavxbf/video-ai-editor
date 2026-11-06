---
name: character-voice-production
description: Use for generating or validating approved UrFavXBF and PIX character narration with Kitten Mini Jasper/Kiki, checking voice identities and WAV receipts, or handling explicitly authorized optional VoxCPM2 voice experiments.
---

# Character Voice Production

**Scope:** approved character narration in this repository. Read
`AGENTS.md`, `docs/PRODUCTION_POLICY.md`, `characters/registry.json`,
`docs/ENGLISH_PRODUCTION_POLICY.md` and `docs/CHATTERBOX_TTS.md` first.
The registry is authoritative; the older optional Tagalog design is NOT the
default.

## English character identities

- **UrFavXBF:** Kitten Mini 0.8 / Jasper,
  `kitten-mini-jasper-en-v1`.
- **PIX:** Kitten Mini 0.8 / Kiki,
  `kitten-mini-kiki-en-v1`. Both are built-in synthetic speakers; no reference WAV is needed.
- Default language `en`; approved new videos are long-form 16:9 at 30fps.
- Model inference is optional and resource-intensive; **reuse reviewed WAVs**
  where they exist, and do not claim generated audio until it exists and is
  listened to. Do not infer a WAV from a profile name.

## Existing production command

Only synthesize new English audio with explicit authorization, approved text,
a properly installed optional Kitten ONNX runtime and real output paths:

```bash
python3 scripts/character_voiceover.py \
  --character urfavxbf --language en --device cpu \
  --text-file input/approved-english.txt \
  --output out/urfavxbf-approved.wav
```

Use `--character pix` with its approved text and output when PIX is the
speaker; the CLI selects Kiki. English `--dry-run` prints the voice request without inference. Do not use `--overwrite`
unless the user explicitly approves replacing an output.

## Verification and assembly

1. Validate script/speaker mapping, reference-audio rights and local model
   prerequisites; `requirements-kitten-onnx.txt` is separate from basic
   `requirements.txt`. Model installation or preflight is **not** speech proof.
2. Confirm each output is a non-empty, decodable real PCM WAV; listen for
   timbre, pronunciation, cadence, artifacts and speaker consistency.
3. Prepare measured clip receipts with the correct registry voiceProfile,
   local file hashes and reviewed timings via the existing
   `scripts/episode_media.py` pipeline. Word alignment is a separate,
   reviewed step; RMS-driven pose changes are not phoneme lip-sync.
4. Run model-free checks when relevant:
   ```bash
   python3 -m unittest discover -s tests -p 'test_character_voiceover.py' -v
   python3 -m unittest discover -s tests -p 'test_chatterbox_voice_profile.py' -v
   python3 -m unittest discover -s tests -p 'test_chatterbox_preflight.py' -v
   ```
5. Verify actual episode mix and media streams with the shared production
   QA gate before claiming a voiced MP4 exists.

## Optional Tagalog route

`VoxCPM2` remains **on hold**. Only a specific owner opt-in may authorize
`--language tl` or `scripts/voxcpm_voiceover.py` for that requested work;
do not change the global registry, replace English default audio, switch to
Malay, incur paid GPU/API charges or ship an experiment as approved narration.
See `docs/MULTILINGUAL_PRODUCTION_POLICY.md` only as scoped historical
background, not current production policy.

Legacy Chatterbox tools remain available only through explicit `--engine chatterbox`; they are not the production default. Model install instructions: `docs/CINEMATIC_SHOWREEL.md`.
