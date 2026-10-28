# English-only production policy — new videos

As of October 28, 2026, the owner has chosen **English-only** as the production language for **new original videos** created by AI agents using Video AI Editor. The intent is to reach potential viewers beyond one local-language audience; broader reach is an opportunity, not a guaranteed outcome.

## Official on-screen speakers

New original video productions center on **UrFavXBF** and his talking AI cat **PIX**. Wisdom, science, math, internet culture, AI, and editing are possible areas of expertise, not separate mascot identities or a science-only channel. UrFavXBF uses the approved Chatterbox `natural-storyteller-v1` English narrator; PIX uses the independently configured Chatterbox V3 female-voiced `pix-cute-female-emily-v1` preset. See [character registry](../characters/registry.json).

## Defaults for every new production

- Write English scripts, English spoken narration, English animated captions and graphics, and English YouTube titles, descriptions, and discoverability metadata.
- Default to the approved **Natural Storyteller** voice preset `natural-storyteller-v1` in `scripts/chatterbox_voice_profile.py`, using Chatterbox Multilingual V3 with `language_id=en`. An explicitly authorized alternate English voice can be used for the individual project.
- Treat the repository as an **AI-operated video editing toolchain**, not a consumer editing app requirement. The agent is responsible for choosing original story structure, visual treatment, sound and timing, while requiring suitable production inputs and truthful source handling.
- Verify narration language, actual audible output, speech-caption alignment, export resolution, duration and audio/video tracks. Passing unit tests or a WAV-only job does **not** prove that a complete video has been delivered.
- Do not publish automatically without owner authorization.

## Existing media and historical projects

- Preserve the current Tagalog/Taglish compositions and examples. They are legacy work and regression material, not a default for new content.
- Existing footage must be edited faithfully. Never invent translated quotations or silently replace someone's real speech; only translate/redub with explicit permission and a suitable rights-cleared source.
- Transcription tools may detect a source's original language. Do not force an English recognition language on non-English source footage, because that can corrupt transcripts.

## Current capability versus the next engineering milestone

The repository already implements an English voice generator and a separate Remotion narration track. The next engineering milestone is an **agent-driven end-to-end pipeline** that connects an English script, completed English narration, reviewed timed captions, planned scenes, final Remotion composition, audio mix, render and file validation. This policy is a production default; it is **not** a claim that those steps are already fully automated.
