# Official Remotion Agent Skills

We have **12 official Remotion skills** under [`.claude/skills/`](../.claude/skills/) alongside the independent [`ai-video-editor`](../.claude/skills/ai-video-editor/SKILL.md) project-specific skill.

## Source and reproduction

- Official publisher: [remotion-dev/skills](https://github.com/remotion-dev/skills).
- Also included in the [Remotion monorepo](https://github.com/remotion-dev/remotion/tree/main/packages/skills).
- Pin: `docs/REMOTION_SKILLS_SOURCE_COMMIT.txt` after synchronization.
- To re-download exactly the pinned source version from this repo: `bash scripts/sync-remotion-skills.sh`.
- The sync script updates only the 12 official `remotion-*` skill folders. It never modifies `ai-video-editor`.

The full skill directories (including supporting `REFERENCE.md`, technique documents, scripts, and assets) are committed. Do not copy just `SKILL.md` because some skills link to other files.

## Skills available

| Skill | Application |
| --- | --- |
| remotion-best-practices | Router and general guidance |
| remotion-create | Create projects and compositions |
| remotion-markup | React markup, animation, typography, layout |
| remotion-captions | Transcription and timed on-screen captions |
| remotion-render | Still and MP4 render guidance |
| remotion-studio | Interactive Studio preview |
| remotion-interactivity | Editable objects and timeline |
| remotion-multimedia | Audio/video handling and metadata |
| remotion-maps | Maps and geographic visualizations |
| remotion-docs | Documentation navigation |
| remotion-upgrade | Upgrade framework and compatible dependencies |
| remotion-saas | App and SaaS integration architecture |

## Which skill controls this project?

Use the local `ai-video-editor` skill for practical editing rules—Tagalog/Taglish dialogue, source timing, motion design, creative pacing, rights and final MP4 verification. Consult the appropriate official Remotion skills for implementation best practices.

These are **agent instructions**, not installed React video effects or new npm packages. Importing skills alone does not upgrade Remotion or guarantee automatic video editing. Our Remotion npm dependencies remain pinned separately in `package.json`.

## Licensing

The official skills are maintained by Remotion and are **not relabeled as MIT licensed**. Refer to [Remotion's license](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md) and our [third-party notices](../THIRD_PARTY_NOTICES.md). Keep attribution to the official publisher.
