---
name: video-ai-orchestrator
description: Central task router for this Video AI Editor repository. Use to coordinate original UrFavXBF and PIX episodes, supplied-footage editing, Remotion/FFmpeg workflows, motion graphics, audio/captions, software maintenance, and verified delivery without loading unrelated skills.
---

# Video AI Editor — Central Skill Orchestrator

This is the **single coordination entrypoint**, not a replacement for the
specialist skills. Read `references/skill-catalog.md` to select only the
instructions needed for the task; never merge all modules into one long prompt.

## Authority: read before choosing a workflow

1. `AGENTS.md` — repository operating rules and authorization gates.
2. `docs/PRODUCTION_POLICY.md` — active video-production policy.
3. `characters/registry.json` — format, identity, and English voice defaults.
4. `characters/pixel-default-manifest.json` — approved art and hashes.
5. `.claude/skills/ai-video-editor/SKILL.md` — project-specific production instructions.

The **latest explicit owner request** defines the deliverable. Otherwise,
current registry/policy take precedence over generic Remotion examples or
historical workflows. A Tagalog chat message is not authorization to switch
the English production default. Never overwrite a newer user change.

## Routing procedure

1. Identify the outcome: finished MP4, footage edit, composition, still,
   interactive preview, captions, tooling feature, skills maintenance, or QA.
2. Verify inputs and environment, including media/voice assets, local tools,
   GitHub access, hardware, licensing, and approved external-provider usage.
3. Consult the catalog and load only the relevant specialist `SKILL.md` and
   linked references. Begin with the smallest applicable set; expand as needed.
4. Produce a concrete acceptance checklist before editing.
5. Work in a dedicated branch/PR for repository changes; keep `main` green.
6. Execute the necessary script/tests/render, and inspect evidence rather than
   inferring success from a prompt, composition name, or JSON manifest.
7. Report what was changed, which checks **actually ran**, results, and any
   work that remains unverified. Never invent video files or download links.

## Critical routes

- **New original character episode:** `ai-video-editor`, approved art/voices,
  `HeroCharacterStage`; use `EpisodeProduction` for assembled chapters.
- **Supplied portrait 9:16 footage:** root `video-effects` skill and actual
  media, cut list, matte and face-location checks. This is NOT the default for
  original episodes.
- **Remotion implementation:** `remotion-best-practices` plus a targeted
  `remotion-*` skill from the catalog; keep original upstream supporting files.
- **Original local HTML/GSAP motion or episode graphic:** `hyperframes-motion-graphics`;
  use the pinned offline renderer, then verify the Remotion chapter bridge.
- **Character narration or voice integrity:** `character-voice-production`;
  keep approved English Chatterbox V3 identities, with VoxCPM2 opt-in only.
- **Transcripts, SRT or word alignment:** `transcription-captions`; prefer
  verified local input, and never transmit audio to Groq without consent.
- **After Effects, Bodymovin, Lottie or Duik imports:** `animation-import`;
  inspect the actual export and enforce the baked-vector compatibility limits.
- **Engineering, AI, research, security, or terminal issues:** canonical
  `senior-multidisciplinary-agent`, opening only relevant references.
- **Final media:** apply shared QA from `scripts/episode_qa.py` and
  `docs/PRODUCTION_STANDARD.md`: inspect actual frame timing, dimensions,
  encoding, captions, stream integrity, audio and visual content.
  FFmpeg/FFprobe are tools rather than a separate redundant skill.
  Artwork/timeline proofs and editor previews are not finished voiced episodes.

## Safeguards

No unapproved paid APIs/GPU, third-party uploads/transcription, publication,
credential exposure, unverified copyrighted assets, or silent merge to `main`.
Skill documents provide instructions, **not** installed models, rendering
software, hardware, permissions, or proof of execution.

## Maintenance and proof

- Add a new specialist only for an independently reusable workflow.
- Avoid duplicating a specialist's entire content in this router.
- Change the catalog when adding, relocating, or retiring a specialist.
- Keep vendor Remotion modules intact; run their pinned sync intentionally.
- Run `python3 -m unittest discover -s tests -p 'test_skill_orchestrator.py' -v`
  and `python3 -m unittest discover -s tests -p 'test_production_instructions.py' -v`.
- For source changes also run `npm run typecheck` and relevant integration QA.
