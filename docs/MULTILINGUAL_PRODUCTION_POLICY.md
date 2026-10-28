# Production language and character voices (2026-10-28)

New original UrFavXBF + PIX videos default to **Tagalog/Taglish (tl)**, not
English-only. Write the narration, character dialogue, captions, on-screen
motion-graphic labels and publishing metadata in natural Filipino. Retain
English terms where familiar (AI, glitch, internet, etc.). Keep Tagalog and
Taglish spelling, pronunciation and caption timing under human review.
**English (en) remains supported by explicit opt-in.**

## Character voices — approved design, not yet an auditioned WAV

| Character | Preferred identity | Default engine | Language |
|---|---|---|---|
| UrFavXBF | Neon Storyteller: warm, medium-low, slightly textured, intelligent Filipino adult male; charismatic natural Tagalog/Taglish storytelling | VoxCPM2 | tl |
| PIX | Pixel Spark: youthful-adult-sounding expressive Filipino female; soft bright mid-high voice, curious, playful, never shrill or childlike | VoxCPM2 | tl |

The definitive English-language voice design prompts and IDs are stored in
[`characters/registry.json`](../characters/registry.json). The prompts are
**textual voice design settings**; they are not voice IDs from a hosted TTS
provider, a trained speaker embedding or validated audio samples.
VoxCPM2's voice design can vary between calls despite fixed seeds.
For consistently identical timbre across long-form episodes, audition audio,
then use consented reference audio/fine-tuning under properly cleared rights.
Do not clone any third-party person's voice without authorization.

## Default command (Tagalog) — optional GPU-dependent TTS

```bash
python3.11 -m venv .venv-voxcpm
.venv-voxcpm/bin/pip install -r requirements-voxcpm.txt
.venv-voxcpm/bin/python scripts/character_voiceover.py \
  --character urfavxbf \
  --text "Alam mo ba, PIX? May misteryo sa likod ng internet!" \
  --output out/urfavxbf-tl.wav
.venv-voxcpm/bin/python scripts/character_voiceover.py \
  --character pix \
  --text "Hala, seryoso?! Tara, alamin natin!" \
  --output out/pix-tl.wav
```

For **free model-free verification**, add `--dry-run` to the Tagalog command:
the result previews the resolved prompt and chunks, not generated audio.
`scripts/voxcpm_voiceover.py` splits long scripts, loads the model once,
writes a WAV and JSON chunk manifest. Manifest timestamps are **not**
verified word-level caption alignment; perform an alignment/QC pass later.
VoxCPM2 requires downloading large model weights and real compute.
No synthetic WAV, video or model weights are committed by this change.

## English/legacy option remains available

English remains an **explicit** alternate for new productions:

```bash
python scripts/character_voiceover.py --character urfavxbf --language en \
  --text "Welcome to the next episode!" --output out/urfavxbf-en.wav
python scripts/character_voiceover.py --character pix --language en \
  --text "I've got three questions!" --output out/pix-en.wav
```

Those commands continue to use the pinned **Chatterbox Multilingual V3**
Natural Storyteller / Emily-reference English voices (from prior approved
samples). They need `requirements-chatterbox.txt` and appropriate compute.
Do not map Tagalog to Chatterbox's Malay language tag; Tagalog is not on its
official language list.

## Production requirements

New videos retain **16:9, 1920×1080, 30 fps, long-form** and the two enlarged
animated pixel-glitch **head portraits only** (no full-body overlays). Preserve
the 21 Remotion FX and speaker-aware motion/caption timing standards.
All scripts, on-screen text, captions, titles and descriptions use the chosen
production language consistently. Do not silently translate licensed source
footage, or auto-publish without authorization. Validate actual speech,
pronunciation, captions, voices and WAV/MP4 tracks before release.
The old English Ghost Town pilot and existing assets/workflows remain historical
and can still be reproduced explicitly; this new policy does not rewrite them.

VoxCPM2 documentation: https://openbmb.cn/docs/en/guides/voxcpm/voxcpm-2
License: https://huggingface.co/openbmb/VoxCPM2
