# Video AI Editor — Skill Catalog

A **routing index**, not a second copy of any skill. Paths below are relative
to the repository root. In the portable skills bundle, modules are placed
side by side under `skills/<name>/`, including `video-effects` and
`senior-multidisciplinary-agent`. Workflows requiring the repository's source,
art or scripts still require a real checkout.

## Project-owned specialists

| Trigger / job | Skill | Repository path |
| --- | --- | --- |
| New character episode, approved narration, production QA, supplied-media decisions | `ai-video-editor` | `.claude/skills/ai-video-editor/SKILL.md` |
| Explicit legacy 9:16 talking-head effects, source cuts and matte preparation | `video-effects` | `SKILL.md` |
| Cross-domain terminal, DevOps, AI systems, research, software or quality procedures | `senior-multidisciplinary-agent` | `.agents/skills/senior-multidisciplinary-agent/SKILL.md` |

## Official Remotion specialists (pinned upstream)

| Trigger / job | Skill | Repository path |
| --- | --- | --- |
| Remotion task discovery / generic router | `remotion-best-practices` | `.claude/skills/remotion-best-practices/SKILL.md` |
| New project or composition | `remotion-create` | `.claude/skills/remotion-create/SKILL.md` |
| React markup, animation and effects | `remotion-markup` | `.claude/skills/remotion-markup/SKILL.md` |
| Transcription or subtitle rendering | `remotion-captions` | `.claude/skills/remotion-captions/SKILL.md` |
| Video output / still rendering | `remotion-render` | `.claude/skills/remotion-render/SKILL.md` |
| Interactive Studio preview | `remotion-studio` | `.claude/skills/remotion-studio/SKILL.md` |
| Editable compositions and timelines | `remotion-interactivity` | `.claude/skills/remotion-interactivity/SKILL.md` |
| Video/audio metadata and decoding | `remotion-multimedia` | `.claude/skills/remotion-multimedia/SKILL.md` |
| Animated maps / geospatial scenes | `remotion-maps` | `.claude/skills/remotion-maps/SKILL.md` |
| Current Remotion documentation lookup | `remotion-docs` | `.claude/skills/remotion-docs/SKILL.md` |
| Framework or dependency version migration | `remotion-upgrade` | `.claude/skills/remotion-upgrade/SKILL.md` |
| Productizing a renderer or building an editor app | `remotion-saas` | `.claude/skills/remotion-saas/SKILL.md` |

## Selection rules

- Read `AGENTS.md`, production policy, registry, asset manifest, and
  `ai-video-editor` before video-production work.
- For a new episode, prefer `ai-video-editor` plus `remotion-create` or
  `remotion-markup`, then add `remotion-captions` and `remotion-render`
  when those stages are reached.
- For provided 9:16 footage, use `video-effects`; do not apply that aspect
  ratio or the sample footage workflow to new original episodes.
- Use `remotion-best-practices` as the official framework router. The 12
  official skill directories contain nontrivial reference and asset material;
  do **not** remove them merely because sections overlap.
- The general senior skill is stored only once under `.agents/skills/`.
  Copilot's `.github/agents/senior-multidisciplinary.agent.md` links to it.
- For this project, `package.json` and the checked-in lockfile determine the
  installed Remotion version; vendor skill versions are guidance, not runtime.
- A specialization is active only when required for the user's actual task.
