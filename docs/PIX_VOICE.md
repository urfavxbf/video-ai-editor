# PIX voice — Chatterbox Multilingual V3

**Character**: PIX, the speaking AI cat sidekick of UrFavXBF. PIX is an English-speaking female-voiced companion: cute, bright, inquisitive, playful and distinctly different from UrFavXBF's narration.

## Current status — saved PIX default voice

The approved default uses **Emily**, a synthetic female voice reference from the open-source [Chatterbox TTS Server](https://github.com/devnen/Chatterbox-TTS-Server). The upstream repository publishes its synthetic voice sample collection and source under [MIT](https://github.com/devnen/Chatterbox-TTS-Server/blob/915ae289340e10c6047f27f47e22eae9bf350c32/LICENSE). The voice reference is pinned to the immutable Git revision `915ae289340e10c6047f27f47e22eae9bf350c32`, with a verified Git blob SHA before synthesis. Keep the upstream license notice and provenance when distributing this reference.

This is a reference audio used by **Chatterbox Multilingual V3**, not a fictitious built-in Chatterbox voice selector. Chatterbox chooses a different speaker using `audio_prompt_path`. A real voice sample was generated successfully in GitHub Actions run 40614959831 on October 28, 2026. The owner subsequently requested saving both character voices as defaults. Each new WAV still requires listening QC.

Configuration: `scripts/pix_voice_profile.py`

- PIX default profile: `pix-cute-female-emily-v1`
- Language: English (`en`)
- Model: Chatterbox Multilingual V3
- Default expressive settings: exaggeration `0.65`, CFG weight `0.35`
- Reference: [Emily.wav pinned source](https://github.com/devnen/Chatterbox-TTS-Server/blob/915ae289340e10c6047f27f47e22eae9bf350c32/voices/Emily.wav)
- Main narrator: **unchanged**, `natural-storyteller-v1` without a voice reference

## Hear the actual PIX sample

The [PIX Chatterbox cute female voice sample workflow](https://github.com/urfavxbf/video-ai-editor/actions/workflows/pix-chatterbox-voice-sample.yml) runs pinned Chatterbox V3 on a GitHub CPU runner, checks the generated speech, and uploads the `pix-cute-female-chatterbox-voice-sample` artifact containing `pix-cute-female-chatterbox.wav`. Open a successful workflow run and download the artifact; the [successful October 28 run](https://github.com/urfavxbf/video-ai-editor/actions/runs/40614959831) contains the real sample.

CPU inference may be slow; Actions minutes and storage are subject to GitHub quotas. The output is a real generated WAV, not a mocked test. Check every new production's voice quality by listening.

## Reproduce in a compatible Python 3.11 environment

```bash
python scripts/prepare_pix_reference.py
python -m pip install -r requirements-chatterbox.txt
python scripts/chatterbox_voiceover.py \
  --text "Hey, UrFavXBF! I'm PIX, your tiny AI sidekick! Got a big question? Let's figure it out together! Ooh, I love this part!" \
  --language-id en --voice-reference input/pix-reference.wav \
  --exaggeration 0.65 --cfg-weight 0.35 \
  --output out/pix-cute-female-chatterbox.wav
```

The checked reference is used only for this secondary character. Other video narration continues to use the unchanged default narrator. Never describe this configuration or a source reference audio clip as proof that an actual synthesized PIX WAV has been produced.

## Using character voice IDs

New English dialogue may be rendered by the character-aware CLI:

```bash
python scripts/character_voiceover.py --character pix --text "Hey, UrFavXBF!" --output out/pix-line.wav
python scripts/character_voiceover.py --character urfavxbf --text "Welcome back." --output out/urfavxbf-line.wav
```

The PIX command verifies and fetches the pinned synthetic Emily reference and passes it to the existing Chatterbox V3 synthesizer. The UrFavXBF command uses the approved built-in Natural Storyteller; the two defaults cannot accidentally share speaker conditioning. Actual generation needs the optional Chatterbox requirements and model weights.
