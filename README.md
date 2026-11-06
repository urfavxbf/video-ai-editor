# Video AI Editor

**AI-assisted video production toolkit powered by Remotion, FFmpeg, HyperFrames, and specialized AI agent skills.**

Build and verify original character-led videos, footage edits, cinematic motion
graphics, narration, captions, and compatible vector animation imports in one
version-controlled workspace.

> **Project status:** This is a **Remotion/TypeScript + FFmpeg/Python production
> toolkit**, not a hosted one-click AI video generator, a finished GUI video
> editor, or a native Android app. Features below are existing tools and
> workflows; a complete episode still needs actual media, approved audio,
> storyboarding, rendering, and audiovisual review.

## What this repository can do

| Capability | Existing implementation | Where to start |
| --- | --- | --- |
| Original character videos | UrFavXBF + PIX, `HeroCharacterStage` (2.5D), chapter-based `EpisodeProduction` | [Production policy](docs/PRODUCTION_POLICY.md) |
| Source-footage edits | Frame-accurate edit lists, talking-head effects and Remotion `ExampleEdit` | [Video effects skill](SKILL.md) |
| Authorized online source intake | Pinned yt-dlp inspection, single-video downloads, and available subtitle files | [Media ingestion guide](docs/MEDIA_SOURCE_INGESTION.md) |
| Cinematic effects | **33 effects:** 21 original talking-head effects plus 12 advanced full-frame effects | [Effects guide](docs/CINEMATIC_FX_12.md) |
| Offline motion graphics | HyperFrames + GSAP, locally encoded H.264 clips, chapter-timed Remotion integration | [HyperFrames guide](docs/HYPERFRAMES_PRODUCTION.md) |
| Character narration | Optional Chatterbox V3 voice synthesis with distinct approved UrFavXBF and PIX profiles | [Voice guide](docs/CHATTERBOX_TTS.md) |
| Transcription and captions | Optional Groq Whisper JSON/TXT/SRT transcription; reviewed WAV-bound alignment for production | [AI video tools](docs/AI_VIDEO_TOOLS.md) |
| Animation imports | Compatible Bodymovin/Lottie JSON and baked 2D Duik Ángela exports | [Lottie](docs/AFTER_EFFECTS_LOTTIE.md) / [Duik](docs/DUIK_ANGELA_IMPORT.md) |
| AI-assisted workflows | **21 modular agent skills**, selected through one central orchestrator | [Skill catalog](.claude/skills/video-ai-orchestrator/references/skill-catalog.md) |
| Local AI assistant tools (MCP) | Official Python MCP v2 stdio server for current policy, skills, validation, FFprobe and bounded renders | [MCP server guide](docs/MCP_SERVER.md) |
| Production verification | Python/Node tests, TypeScript checks, GitHub Actions, FFprobe and encoded video fixtures | [Agent policy](AGENTS.md) |

These capabilities are scoped: a checked-in demo, proof composition, or
generated manifest does **not** prove that a complete voiced episode was delivered.

## Quick start

**Prerequisites:** Node.js 22+, npm, Python 3.11, FFmpeg and FFprobe.
Some audio/graphics tools have optional runtime dependencies; see the guides
before installing model weights or invoking external providers.

```bash
git clone https://github.com/urfavxbf/video-ai-editor.git
cd video-ai-editor
npm ci
npm run typecheck
npm run studio
```

Open **Remotion Studio** to inspect the registered compositions.

Useful local commands:

```bash
# Verify the 13 approved character images and their manifest.
python3 scripts/stage_pixel_default_pack.py --verify-workspace

# Preview the original 21-effect library after generating sample media.
npm run sample
npm run render:showcase

# Render your own source edit after configuring src/edit/edit.json.
npm run render:edit

# Offline HyperFrames graphics: validate first, then render.
npm run hyperframes:lint
npm run hyperframes:render

# Preview the 12 advanced full-frame effects on generated sample media.
npm run advanced-fx:sample
npm run advanced-fx:showcase

# Optional, after Codespaces setup: inspect metadata for an approved source.
.venv/bin/python scripts/media_ingest.py inspect 'https://vimeo.com/123'
```

Actual edits require valid footage and supporting assets. The default
`render:edit` command uses `src/edit/edit.json`; verify its referenced files
and timing before expecting a production result. HyperFrames local rendering
does not require HeyGen Cloud or its paid APIs.

### GitHub Codespaces (browser or Android)

Create a Codespace from **Code → Codespaces** using the desired branch, and run:

```bash
bash scripts/check-codespace.sh
```

The committed [devcontainer](.devcontainer/devcontainer.json) and
[setup guide](docs/CODESPACES_SETUP.md) describe the environment.
Codespaces may consume account quota. Creating a Codespace does not
automatically give this chat access to its terminal or files.

## Connect an AI assistant (MCP server)

A **local, opt-in MCP server** exposes real project tools to MCP-compatible
clients such as coding agents and desktop IDEs. It uses the official Python
MCP SDK v2 and starts over `stdio`, with no public endpoint or cloud
credentials required. It is separate from the 21 instructional skills.

```bash
# In a project-local Python 3.11+ virtual environment:
.venv/bin/python -m pip install -r requirements-mcp.txt
.venv/bin/python scripts/run-mcp-server.py
```

The last command intentionally **waits for an MCP host**; it is not a
human-facing CLI. Configure the host using the copy-ready instructions in
[docs/MCP_SERVER.md](docs/MCP_SERVER.md). It can inspect project metadata,
list skills, validate art and edits, probe local media, and, only with explicit
approval, run a restricted proof render or request yt-dlp metadata.
No finished video, remote ChatGPT connection, or plugin installation is
implied simply by running the server.

## Current approved production defaults

For **new original UrFavXBF × PIX episodes**, the authoritative settings are
in [`docs/PRODUCTION_POLICY.md`](docs/PRODUCTION_POLICY.md),
[`characters/registry.json`](characters/registry.json), and the
[approved pixel asset manifest](characters/pixel-default-manifest.json).

| Setting | Current default |
| --- | --- |
| Script, narration, captions, graphics and metadata | **English** |
| Format | **16:9, 1920 × 1080, 30 fps**; duration follows the story and chapters |
| Characters | UrFavXBF and PIX using **13 approved pixel poses** |
| Scene system | `HeroCharacterStage`, full-body 2.5D presentation |
| UrFavXBF voice | Chatterbox V3 **Natural Storyteller** (`natural-storyteller-v1`) |
| PIX voice | Chatterbox V3 **Emily** (`pix-cute-female-emily-v1`) |
| Optional Tagalog / VoxCPM2 | **On hold**, explicit opt-in only |
| External services and spending | No paid API/GPU use or external media upload without explicit authorization |

Speaker pose swaps and audio-driven motion are **not** genuine phoneme
lip-sync or native 3D. A specific new request can authorize an alternate
format, but archived portrait workflows do not silently replace the active
defaults. See [character identities](docs/OFFICIAL_CHARACTERS.md) and
[production quality](docs/PRODUCTION_STANDARD.md).

## Central AI skills architecture

The [central orchestrator](.claude/skills/video-ai-orchestrator/SKILL.md)
routes a task to the **relevant** instructions, rather than loading a huge
merged `SKILL.md` on every request.

```text
AGENTS.md                          # Authoritative project-wide rules
.claude/skills/
  video-ai-orchestrator/           # Central task router + skill catalog
  ai-video-editor/                 # Project production standards
  hyperframes-motion-graphics/     # Offline motion design
  character-voice-production/      # Chatterbox V3; VoxCPM2 opt-in
  transcription-captions/         # Groq consent and timing QA
  animation-import/               # Lottie + baked Duik imports
  media-source-ingestion/         # Authorized yt-dlp URL intake
  remotion-*/                      # 12 pinned official Remotion skills
.agents/skills/
  senior-multidisciplinary-agent/  # Engineering and quality workflows
SKILL.md                          # Supplied 9:16 footage/effects
```

**21 modular skills total:** 1 orchestrator + 12 official Remotion skills
+ 5 project-specific external integration skills + 3 other project
specialists (production, footage effects, senior engineering).
See the full [skill catalog](.claude/skills/video-ai-orchestrator/references/skill-catalog.md),
[`AGENTS.md`](AGENTS.md) and [AI agent prompt playbook](docs/AI_AGENT_PROMPTS.md).

Portable skill archives can be generated with:

```bash
python3 scripts/package-chatgpt-skills.py
```

This creates a **skills-only** bundle under `out/chatgpt-skills/`; it does
not install dependencies, connect the AI assistant to GitHub/Codespaces, grant
credentials, or authorize cloud processing. Specialized skills are loaded
only when their workflow is relevant.

## Media, voice, and import safety

- **yt-dlp:** Use the [source-ingestion guide](docs/MEDIA_SOURCE_INGESTION.md)
  to inspect/download specific rights-cleared videos, then independently
  validate streams before editing. No cookies, DRM bypass, playlist scraping,
  untrusted sites or automatic publishing. Sources remain gitignored.
- **Chatterbox V3:** Reuse approved WAVs when available. New synthesis uses
  `scripts/character_voiceover.py` only with authorized text, suitable
  optional model dependencies and an approved speaker. PIX needs its real,
  permitted reference recording; a voice preset alone is not a WAV.
- **Groq Whisper:** `scripts/groq_transcribe.py` sends audio to an external
  provider. Use only with explicit authorization, a securely configured
  `GROQ_API_KEY`, and acceptance of any usage costs. Locally available
  reviewed transcripts take priority when suitable.
- **HyperFrames:** Use the pinned local CLI. Cloud rendering, publication
  and external asset processing are out of scope without authorization.
- **Lottie / Duik:** Import approved, compatible vector animation. Duik
  requires a separate licensed After Effects workstation for authoring;
  the checked-in sample is not a real Duik-export proof.
- **Rights:** Only use footage, character art, audio, fonts and other
  assets that are owned or licensed for the intended use.

## Verification and delivery

```bash
npm run typecheck
node --test tests/*.test.cjs
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/stage_pixel_default_pack.py --verify-workspace
```

For rendered output, verify the actual encoded dimensions, frame rate,
duration, audio/video streams, decoded frames, captions and listening
quality. The [GitHub Actions PR safety gate](.github/workflows/pr-safety-gate.yml)
also builds and renders deterministic fixtures. Tests, preflight checks and
fixtures are evidence of those specific checks—not proof of an unseen
finished episode. Repository updates belong on a branch with a reviewed PR;
keep `main` working.

## Documentation and repository About

- [Project operating rules](AGENTS.md)
- [Current production policy](docs/PRODUCTION_POLICY.md)
- [Production quality standard](docs/PRODUCTION_STANDARD.md)
- [AI agent prompts](docs/AI_AGENT_PROMPTS.md)
- [Skills catalog](.claude/skills/video-ai-orchestrator/references/skill-catalog.md)
- [GitHub About description and topics](docs/GITHUB_ABOUT.md)

## Provenance and licenses

**Video AI Editor is not published under a repository-wide MIT license.** Its custom application and newer video compositions are distinct from the Remotion framework and from the effects source that was imported earlier.

The initial 21-effect library was imported from [urfavxbf/video-effects-mobile](https://github.com/urfavxbf/video-effects-mobile), originally derived from [JesseEisenbart/video-effects-skill](https://github.com/JesseEisenbart/video-effects-skill). The required MIT notice for the applicable imported source code is preserved **only as a third-party notice** in [licenses/video-effects-skill-MIT.txt](licenses/video-effects-skill-MIT.txt). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the license scope, separate font and audio asset notes, and the archived [upstream README](docs/UPSTREAM_README.md).

[Remotion](https://github.com/remotion-dev/remotion) is the independent video framework used as an npm dependency. It has its **own license** ([official Remotion license](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)); it is **not** relicensed by this project.

This repository is not a GitHub fork of either upstream repository. Refer to Git history and the links above for provenance.
