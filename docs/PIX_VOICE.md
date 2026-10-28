# PIX voice — Chatterbox Multilingual V3

**Character**: PIX, the speaking AI cat sidekick of UrFavXBF. PIX is an English-speaking female-voiced companion: cute, bright, inquisitive, playful and distinctly different from UrFavXBF's narration.

## Current status — voice candidate, not yet approved

The initial candidate is **Emily**, a synthetic female voice reference from the open-source [Chatterbox TTS Server](https://github.com/devnen/Chatterbox-TTS-Server). The upstream repository publishes its synthetic voice sample collection and source under [MIT](https://github.com/devnen/Chatterbox-TTS-Server/blob/915ae289340e10c6047f27f47e22eae9bf350c32/LICENSE). The voice reference is pinned to the immutable Git revision `915ae289340e10c6047f27f47e22eae9bf350c32`, with a verified Git blob SHA before synthesis. Keep the upstream license notice and provenance when distributing this reference.

This is a reference audio used by **Chatterbox Multilingual V3**, not a fictitious built-in Chatterbox voice selector. Chatterbox chooses a different speaker using `audio_prompt_path`. A generated recording must be listened to before it can be declared the final approved voice.

Configuration: `scripts/pix_voice_profile.py`

- PIX candidate profile: `pix-cute-female-emily-v1`
- Language: English (`en`)
- Model: Chatterbox Multilingual V3
- Style exploration: exaggeration `0.65`, CFG weight `0.35`
- Reference: [Emily.wav pinned source](https://github.com/devnen/Chatterbox-TTS-Server/blob/915ae289340e10c6047f27f47e22eae9bf350c32/voices/Emily.wav)
- Main narrator: **unchanged**, `natural-storyteller-v1` without a voice reference

## Hear the actual PIX sample

The [PIX Chatterbox cute female voice sample workflow](https://github.com/urfavxbf/video-ai-editor/actions/workflows/pix-chatterbox-voice-sample.yml) runs pinned Chatterbox V3 on a GitHub CPU runner, checks the generated speech, and uploads the `pix-cute-female-chatterbox-voice-sample` artifact containing `pix-cute-female-chatterbox.wav`. Open a successful workflow run and download the artifact; **the sample exists only once the run is successful**.

CPU inference may be slow; Actions minutes and storage are subject to GitHub quotas. The waveform is generated rather than mocked. The sample still needs listening review to assess whether Emily sounds cute enough for PIX.

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
