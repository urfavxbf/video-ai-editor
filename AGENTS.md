# Video AI Editor — authoritative instructions for AI agents

> **Primary agent operating policy.** Applies to Codex, Claude Code, Copilot,
> and other agents working in this repository. Start here for every task.
> [Production defaults](docs/PRODUCTION_POLICY.md) and the character registry
> are authoritative for their respective domains. Prompt templates are examples,
> **not** permission to override this policy.

## 1. Required reading and precedence

**Before planning, editing code, generating assets, or rendering**, inspect these
five current files in the checked-out branch:

1. `AGENTS.md` (this agent entry point)
2. `docs/PRODUCTION_POLICY.md` (new-production policy)
3. `characters/registry.json` (machine-readable current defaults and voices)
4. `characters/pixel-default-manifest.json` (approved asset paths and hashes)
5. `.claude/skills/ai-video-editor/SKILL.md` (production workflow guidance)

For an interactive prompt, see [the ready-to-use prompt playbook](docs/AI_AGENT_PROMPTS.md).
Use the **latest explicit owner instruction** for the current request; otherwise
follow the active production policy and registry. Do not let old demos, sample
videos, imported Remotion skills, or historically named documents supersede current
defaults. A Tagalog-language message alone **does not** authorize Tagalog output.
If two currently authoritative sources actually conflict, report the exact
conflict before dependent production. Do not invent a compromise.

These instructions do not imply access to tools, credentials, payments, or an
actual media asset; inspect and verify each relevant input and result.

## 2. Default for a NEW original episode

- **English** for script, narration, captions, on-screen copy and metadata.
- **16:9, 1920×1080, 30 fps**; total duration comes from the approved script and
  chapters, not a generic fixed-length demo.
- **HeroCharacterStage**, with approved **UrFavXBF and PIX** full-body pixel poses
  (13 committed images: 6 UrFavXBF, 7 PIX), cinematic **2.5D** staging.
- UrFavXBF: Chatterbox Multilingual V3 `natural-storyteller-v1`, Natural Storyteller.
- PIX: Chatterbox Multilingual V3 `pix-cute-female-emily-v1`, Emily; never substitute
  another speaker or use UrFavXBF voice for PIX.
- Use the committed approved art. Before rendering, run:

```bash
python3 scripts/stage_pixel_default_pack.py --verify-workspace
```

- **Tagalog/VoxCPM2 is opt-in only.** No paid API, GPU spending, new third-party
  processing, or external sprite purchase is authorized by the default workflow.
- Speaker/listener **pose swaps**, RMS-driven movement, and 2.5D staging are
  **not** phoneme lip-sync or genuine 3D. Never claim otherwise.

An explicit request can select a different language/format for a particular
deliverable, but do not silently modify the registry or project-wide defaults.

## 3. Select the correct composition

| Task | Correct composition / rule |
| --- | --- |
| New original character episode | `HeroCharacterStage`, default character scene |
| Multi-chapter episode assembly | `EpisodeProduction`; assemble real media and captions |
| Verify chapter schedule only | `EpisodeTimelineProof`; **not** a finished episode |
| Verify approved art only | `PixelProductionProof`; **not** a finished voiced episode |
| Supplied footage / frame-based cut list | `ExampleEdit` using `src/edit/edit.json`; validate edit and physical media |
| Existing podcast footage | `DudutPremium` / `DudutV2`: specialized templates for source interval **00:42–01:24**, not generic defaults |
| One visual effect | `FxPreview`; supply a valid effect ID and necessary footage |
| All 21 effect previews | `FxShowcase`; run `npm run sample` first |
| Official Remotion feature demonstration | `OfficialFeaturesDemo`; captions/transitions/shapes demonstration only |
| Repo product reel | `RepoShowcase`; **not** an editing application |
| Lottie / Bodymovin graphics | `AfterEffectsLottieProof`; compatible local JSON only, not a full AE renderer |
| Baked Duik-style puppet motion | `DuikBakedCharacterProof`; original demo JSON, **not** proof of a real Duik export |
| Historical or prototype | `OriginalDoorway`, `ChallengerDeep`, `Y2038Teaser`, `CharacterAnimationLab`, `PixelPortraitHUD`, `CanonicalFullBodyReviewStage`, `TrueFrameReviewStage`, `ChibiV4ReviewStage`, `V4FacialReviewStage`, `ImportedSpriteAnimationReview`; require requested scope, actual assets and approval |

Do not use a proof, preview, historical workbench, or demo as evidence that a
production-grade MP4 has been created.

## 4. Choose an FX to reinforce what the narrator says

Effects are **optional**, not timeline filler. Verify source footage, copy,
matte/sticker frames, and face position where relevant. Check the actual effect
properties and source contract before rendering.

| Effect ID | Narrative role / layout and required assets |
| --- | --- |
| `orbit` | Tools/ecosystem; cut-out matte and face position |
| `chat-takeover` | Assistant prompt/workflow; replace demo UI and copy |
| `frame-escape` | Reveal / outside-the-box; matte and face position |
| `snap-zoom` | Punchline / strong keyword emphasis; sensible face framing |
| `checklist-pop` | 3–4 quick points; **four-item** layout |
| `headline-storm` | News/hype; matte and **seven** validated headline banners |
| `zoom-portal` | “Let me show you” transition; face position |
| `growth-curve` | Growth/results; matte; only **verified** figures and labels |
| `broll-overlay` | Explaining editing, footage inserts or B-roll |
| `paper-cutout` | Playful beat; matte **and** sticker-frame assets |
| `magazine-cover` | Profile/credibility; matte and verified, original copy |
| `liquid-glass` | Inspect a detail; face position |
| `zoom-through-cut` | Time/topic jump; real source video |
| `green-screen` | Change a visual set; matte |
| `frame-break` | Myth-busting/reveal; matte, can follow green-screen |
| `digital-zoom` | Scrutiny of a detail; face position |
| `phone-mockup` | Social-feed context; replace placeholder UI copy |
| `checklist-tally` | Closing summary card; no footage, put at the end |
| `glass-widgets` | Statistics/progress; matte, keep face visible |
| `checklist` | Five-stage process; **five-row** layout |
| `split` | Comparison/average; face position, **five-bar** layout |

For source/asset constraints, consult the scoped root
[`SKILL.md`](SKILL.md), `src/fx/index.tsx` and `src/fx/shared.tsx`.
Never fabricate chart numbers, captions, source positions, or source media.

## 5. Media, voice, captions and audio

- **Reuse approved real WAV audio** where available. When **explicitly
  authorized** to generate new English narration, use the existing
  `scripts/character_voiceover.py` CLI with `--language en --device cpu`,
  the right `--character`, an approved script, and a real `--output`.
  PIX **requires** `input/pix-reference.wav`; a named preset alone is not
  proof that a WAV was rendered.
- Derive speaker events, captions and word timing from **actual listened-to
  audio** and reviewed alignment. Do not infer phonemes or seconds from text
  length, RMS, a filename, or a fake waveform.
- `scripts/groq_transcribe.py` uploads audio to a third-party Groq service;
  obtain **explicit permission for external processing**, credentials and any
  financial implications **before** using it. Prefer verified local transcripts
  when third-party processing is not authorized.
- For `ExampleEdit`, run `node scripts/validate-edit.cjs src/edit/edit.json
  --media` after staging real source/derivative media. A schema-only check does
  not prove the referenced files exist or have the stated duration.
- Use the measured Python media-verification workflow for physical stream
  bounds and speaker timing; an `EpisodeManifest` structure check is **not**
  a media check. Preserve original footage dialogue; translation/redubbing needs
  explicit authorization.
- Licensed/original art, fonts, textures, score and sound effects only.

## 6. Existing Remotion packages and After Effects bridges

- Verified active demo usage: `@remotion/captions`,
  `@remotion/transitions`, `@remotion/shapes`.
- Also installed but require task-specific render QA:
  `@remotion/effects`, `@remotion/motion-blur`, `@remotion/sfx`.
- `@remotion/player` is a library dependency, **not** a shipped editor app.
  The 12 imported Remotion skills are **guidance**, not installed rendering
  capabilities, account permissions or an external service.
- Bodymovin/Lottie accepts supported local animation JSON; it does **not**
  execute arbitrary After Effects plugins, expressions or full 3D effects.
  See `docs/AFTER_EFFECTS_LOTTIE.md`.
- Duik Ángela needs a licensed After Effects workstation for authoring; only
  compatible **baked 2D vector Bodymovin exports** can be validated/imported
  via `scripts/import_duik_baked_lottie.py`. Its bundled demo was
  hand-authored, **not** tested with a real Duik-generated export.
  See `docs/DUIK_ANGELA_IMPORT.md`.

## 7. Development, acceptance and delivery gate

1. Use a dedicated Git branch and PR; leave `main` green. **Never push to
   `main` or merge without explicit authorization.**
2. Inspect actual user-supplied input before making factual visual/audio claims.
3. Keep code and data deterministic, validate inputs, avoid hardcoding media
   paths in shared components, and add appropriate automated tests.
4. Run relevant checks, including `npm ci`, `npm run typecheck`,
   `node --test tests/*.test.cjs`, Python regressions, approved-art verification,
   the actual composition render, and any needed physical media preflight.
5. Verify the **real** output using `ffprobe`/FFmpeg: dimensions, frame rate,
   codec, duration, presence of required audio/video streams, and decodability.
   Inspect representative and transition frames; **listen** for pacing, speech
   identity, clipping and mix; review exact subtitle text, readability and timing.
6. Never claim a proof frame, generated JSON, CI success, or presence of a profile
   equals a finished voiced video; label incomplete renders accurately.
7. No unapproved external uploads, paid API/GPU use, publishing, account
   connections, privileged or write-capable automated workflows. Creating a
   branch/PR or executing writes requires authorization for the requested work.
   No silent merge.

When editing the **source skill** `.claude/skills/ai-video-editor/SKILL.md`,
regenerate the compiled skill with
`python3 scripts/build-cineforge-master-skill.py` and run
`python3 -m unittest discover -s tests -p 'test_production_instructions.py' -v`.
Changing this agent entry point or the prompt playbook alone does not change
the generated skill's underlying source.

## 8. Prompt playbook

Use [`docs/AI_AGENT_PROMPTS.md`](docs/AI_AGENT_PROMPTS.md) for ready-to-copy,
task-specific instructions. Prompts **inherit**, and never replace, this file,
`docs/PRODUCTION_POLICY.md` and verified machine-readable defaults.
