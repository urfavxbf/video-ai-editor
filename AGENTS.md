# Repository instructions for Codex and other coding agents

This is a Remotion/TypeScript + FFmpeg/Python AI video-production workspace.

Before planning production, read [the current policy](docs/PRODUCTION_POLICY.md)
and `characters/registry.json` (`production_language`, `default_video`,
`character_hero_system`, and each character's `english_voice`). Verify artwork
against `characters/pixel-default-manifest.json`.

The latest explicit user instruction takes precedence for that request. Otherwise
use the current registry and production policy. Historical documents, example
videos, imported framework skills and archived voice designs do not redefine
new-production defaults. If current sources genuinely disagree and no explicit
supersession resolves it, report the exact conflict before dependent production.

Keep the approved English Chatterbox speakers, committed pixel poses,
HeroCharacterStage and 1920×1080/30 fps long-form settings. Preserve historical
work for explicit reproduction. A request written in Tagalog is not a request
to change the video's language. Tagalog/VoxCPM2 requires explicit opt-in and
does not authorize paid API or GPU use.

Use the custom `.claude/skills/ai-video-editor/SKILL.md` for production guidance.
`SKILL.md` at the root covers the legacy supplied-footage effects workflow.
OpenMontage remains an opt-in isolated integration; follow its own nested
guide when selected. Do not migrate frameworks, replace approved art, change
voice identities, mix integration dependencies or fabricate completed renders.

For changes, use a dedicated branch/PR and run relevant existing checks. Never
push to main, merge, publish videos or incur paid usage without authorization.
Keep the pending Zod security work separate from unrelated tasks.

When changing project instructions, update their source and regenerate
CineForge with `python3 scripts/build-cineforge-master-skill.py`. Run
`python3 -m unittest discover -s tests -p 'test_production_instructions.py' -v`
to check routing, registry consistency, regeneration and packaged guidance.
