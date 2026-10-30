---
name: ai-video-editor
description: Use when planning or producing UrFavXBF and PIX episodes, editing supplied footage, or checking production identity, narration, captions and video delivery in this Remotion workspace.
---

# AI Video Editor

Read `docs/PRODUCTION_POLICY.md` and `characters/registry.json` before production.
The latest explicit user instruction wins for that request; otherwise use the
registry's `production_language`, `default_video`, `character_hero_system` and
each character's `english_voice`. Historical policies and generic examples do
not replace these defaults. Report unresolved current-source conflicts before
dependent production. A Tagalog user message does not change video language.

## Current approved defaults

- **English (en)** for scripts, narration, captions, graphics and metadata.
- Long-form **1920×1080, 16:9, 30 fps**; runtime follows script and chapters.
- UrFavXBF: Chatterbox V3 **Natural Storyteller**, `natural-storyteller-v1`.
- PIX: Chatterbox V3 **Emily**, `pix-cute-female-emily-v1`; keep independent speakers.
- **13 committed** approved pixel PNG poses (UrFavXBF 6, PIX 7), under
  `public/characters/pixel-default/`; verify against `characters/pixel-default-manifest.json`.
- Full-body pixel-pose characters on a cinematic 2.5D stage:
  **HeroCharacterStage** with approved assets enabled; **PixelProductionProof**
  is the existing model-free artwork proof. No substitute/rejected art.
- Preserve black/neon-green UrFavXBF and cyan/lavender PIX identities. Use
  speaker/listener pose swaps and short scene-transition glitches; no claim of
  phoneme lip-sync or volumetric 3D from PNG transforms.
- Tagalog/VoxCPM2 stays on hold, **opt-in only**. **No paid API or GPU** usage.
  Its retained `voice` profiles are not the English production defaults.

Verify files with `python3 scripts/stage_pixel_default_pack.py --verify-workspace`.
The approved art is in the repository; if a local file is absent, report that
path and repair the authorized checkout/staging, not the approved identity.
Do not demand the old V2 Library pack for the default workflow.

## Production and verification

1. Verify the requested output and actual media. Preserve authentic supplied
   dialogue; translate/redub only with explicit authorization.
2. Plan the story, chapter lengths, speaker turns and restrained FX. UrFavXBF
   covers wisdom, science, math, internet culture, AI and editing; never science-only.
3. Reuse approved English WAVs when available. If new narration is authorized,
   use the existing Chatterbox profiles via `scripts/character_voiceover.py`
   with `--language en --device cpu`. Actual WAVs, word alignment and listening
   QA determine captions and speaker events, not guessed text duration.
4. Apply `docs/PRODUCTION_STANDARD.md`. Use the 21 existing FX selectively,
   clear captions and verified facts; inspect representative/transition frames.
5. Verify final MP4 dimensions, duration, video/audio streams and playback with
   FFprobe and audiovisual QA. Deliver only real files; publish only if requested.

Groq transcription (`scripts/groq_transcribe.py`) is optional and requires an
available key and authorization to send audio externally. A skill does not
connect a chatbot to Codespaces, install models or grant credentials/budget.
Historical portrait/V2 and 9:16 workflows remain explicit reproduction options.
OpenMontage remains isolated and opt-in: read `integrations/openmontage/README.md`
and its nested agent guide when selected. Do not mix its runtime into Remotion.
Official Remotion skills supply framework techniques, not project defaults.
