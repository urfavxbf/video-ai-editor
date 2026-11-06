# GitHub Copilot — Video AI Editor agent routing

Start by reading **all five required files** in the checked-out branch:
- [AGENTS.md](../AGENTS.md) — canonical AI agent operating rules
- [docs/PRODUCTION_POLICY.md](../docs/PRODUCTION_POLICY.md)
- [characters/registry.json](../characters/registry.json)
- [characters/pixel-default-manifest.json](../characters/pixel-default-manifest.json)
- [.claude/skills/ai-video-editor/SKILL.md](../.claude/skills/ai-video-editor/SKILL.md)

Route specialized work through the [central video AI orchestrator](../.claude/skills/video-ai-orchestrator/SKILL.md)
and its [skill catalog](../.claude/skills/video-ai-orchestrator/references/skill-catalog.md).
Load only the relevant specialist skill and references after respecting the five
mandatory authoritative files. External integration skills cover local
HyperFrames/GSAP motion, approved Chatterbox voices, consented Groq captions,
and vetted Duik/Lottie/Bodymovin imports; none grants cloud processing rights. The generic senior skill is canonical under
`.agents/skills/senior-multidisciplinary-agent/`, not duplicated under `.github/skills/`.

Use [docs/AI_AGENT_PROMPTS.md](../docs/AI_AGENT_PROMPTS.md) for reusable prompt
templates. This file is a routing pointer, **not** an alternative policy.
Follow the latest explicit owner request and current registry values. No
unapproved paid APIs, GPUs, remote media processing, publishing or merges.
Never call an art proof, voice-only test, Lottie demo or timeline preview a
delivered video.
