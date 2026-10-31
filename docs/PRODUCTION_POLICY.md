# Current production policy

> **Canonical production defaults.** AI agents must first follow
> [AGENTS.md](../AGENTS.md), verify the current
> [registry](../characters/registry.json) and
> [approved pixel manifest](../characters/pixel-default-manifest.json), and
> use the [AI agent prompt playbook](AI_AGENT_PROMPTS.md) only as an optional
> task template. Historical documents never supersede these active settings.

This is the current guide for new UrFavXBF × PIX productions, reflecting the
approved 2026-10-29 pixel-pose defaults and retained English voice setting.
Machine-readable values live in [the registry](../characters/registry.json)
and [the approved asset manifest](../characters/pixel-default-manifest.json).

## Precedence and scope

1. The latest explicit user instruction governs the current request. A message
   written in Tagalog does not itself change the production language.
2. Otherwise read the registry's `production_language`, `default_video` and
   `character_hero_system`. For English use each character's **`english_voice`**;
   the retained `voice` objects describe optional Tagalog designs. Persona prose
   describes characterization; `production_language` and `default_video` select
   the current language, not a historical language phrase in a persona.
3. This guide, the current character bible and quality standard explain those
   defaults. Historical policy bodies and generic imported skills apply only
   within their stated scope; their dates or words such as "latest" do not
   override the supersession notices.
4. If current sources conflict without a clear user-approved supersession,
   report the specific discrepancy before dependent production. Do not invent
   a combined identity or silently change the registry to match old prose.

## Approved defaults

| Area | Current setting |
| --- | --- |
| Language | English (en): script, narration, captions, graphics and metadata |
| Format | Long-form, 16:9, 1920×1080, 30 fps; script/chapter-driven runtime |
| UrFavXBF voice | Chatterbox V3 `natural-storyteller-v1`, Natural Storyteller |
| PIX voice | Chatterbox V3 `pix-cute-female-emily-v1`, synthetic Emily reference |
| Artwork | 13 committed approved RGBA pixel poses: UrFavXBF 6, PIX 7 |
| Layout/runtime | Full-body pixel-pose characters, cinematic 2.5D; `HeroCharacterStage` |
| Motion | Speaker/listener pose swaps; short glitches at transitions; no false lip-sync claims |
| Asset verification | `python3 scripts/stage_pixel_default_pack.py --verify-workspace` |
| Visual proof | `PixelProductionProof`; artwork proof, not a voiced episode |
| Budget | No paid API or GPU usage; maximum external sprite spend is zero |

UrFavXBF retains black/neon-green styling; PIX retains the approved
cyan/lavender feline styling. Use the existing PNGs and their hashes, not a
new interpretation, substitute pack, concept-sheet crop or rejected prototype.
Check actual files before rendering: the repository includes the approved art;
a missing local file is a concrete setup failure, not a reason to demand a new
Library upload or silently select historical assets. Voice synchronization and
word alignment remain episode-specific and must use actual audio.

Tagalog/VoxCPM2 is **on hold and opt-in only**. Keep its designs/runtime for an
explicitly requested experiment; opt-in does not authorize paid GPU/API use.
Reuse approved English audio when available. Authorized new English generation
uses the same profiles and existing CPU-capable Chatterbox path; never silently
substitute speakers or claim a new WAV was generated from a preset alone.

## Historical reproduction and delivery

Portrait-only/V2 layouts, canonical rig workbenches, old Tagalog defaults and
9:16 demos remain available for explicit historical reproduction. They are
not the default for a new original episode. Follow their exact asset staging
instructions only when that historical workflow is selected.

Preserve authentic dialogue in supplied media. Translation/redubbing needs
explicit authorization. Use the 21 existing effects selectively, keep captions
readable, and fact-check material claims. Verify real media and final audio/video
streams, timing, identity and playback before claiming delivery. Publish only
when explicitly requested; tests or artwork readiness do not prove a finished
episode, permanent skill installation or a working external connection.

## Agent routing and verification requirements

The primary agent instructions are [`AGENTS.md`](../AGENTS.md). Its composition
routing and 21-FX selection table apply to all work; a task-specific prompt
from [`docs/AI_AGENT_PROMPTS.md`](AI_AGENT_PROMPTS.md) cannot grant any missing
assets, processing permissions or production approvals.

- Use `HeroCharacterStage` for the default character scene and
  `EpisodeProduction` for actual multi-chapter assembly. `PixelProductionProof`
  and `EpisodeTimelineProof` are proof tools, not finished episodes.
- For supplied footage use `ExampleEdit`, validate `src/edit/edit.json`
  with `node scripts/validate-edit.cjs src/edit/edit.json --media` and confirm
  real video, mattes, stickers, face coordinates and audio streams.
- The Lottie/Bodymovin and Duik compositions are import **demonstrations** only,
  not a complete After Effects runtime nor proof of a genuine Duik export.
- New English speech requires express authorization, the approved
  `scripts/character_voiceover.py --language en --device cpu` route, a real
  reference WAV for PIX at `input/pix-reference.wav`, and listening QA.
  Using Groq uploads content externally and requires separate permission.
- RMS or pose-swap character motion does not establish phoneme lip-sync.
  Do not describe 2.5D images as physically modeled 3D.
- Before delivery, verify the **actual rendered media** with FFprobe,
  representative/transition frames, listened-to speech/mix and reviewed caption
  alignment. A schema validation, successful CI run or artwork proof alone
  never constitutes verified final delivery.
- Do not merge changes to `main`, publish, trigger write-capable workflows,
  or incur paid API/GPU costs without the owner's explicit authorization.

## HyperFrames first-class animation production

HyperFrames by HeyGen is **integrated into the local production toolchain** for
authoring motion graphics, using pinned CLI dependencies and a real tested
renderer. Use `npm run hyperframes:lint`, `npm run hyperframes:render`, and the
validated `EpisodeProduction.motionGraphics` chapter clips. The approved
narration, identity, artwork and character-stage defaults remain unchanged.
This is not an optional dependency installation or a replacement for Remotion;
graphics are applied selectively when they improve the story. See
[`docs/HYPERFRAMES_PRODUCTION.md`](HYPERFRAMES_PRODUCTION.md).

Run only offline local rendering with telemetry disabled; do not invoke cloud
services, external media pipelines, paid HeyGen features or publishing without
explicit owner authorization. Never infer a finished episode from a successful
motion-graphics test.
