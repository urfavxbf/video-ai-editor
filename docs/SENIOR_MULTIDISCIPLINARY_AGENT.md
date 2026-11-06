# Senior Multidisciplinary AI Agent

This repository keeps **one canonical copy** of the general senior skill:

- Skill source: `.agents/skills/senior-multidisciplinary-agent/SKILL.md`
- Copilot custom agent: `.github/agents/senior-multidisciplinary.agent.md`
- Central selector: `.claude/skills/video-ai-orchestrator/SKILL.md`

The older `.github/skills/senior-multidisciplinary-agent/` mirror was
byte-for-byte identical and is intentionally removed. Copilot's custom agent
continues to link to the canonical `.agents/skills/` version. Skill automatic
discovery varies by host; use the explicit agent/profile or repository instructions
where auto-discovery of that directory is unavailable.

## Scope and precedence

The reusable skill covers terminal/DevOps, AI engineering, motion graphics,
sourced research, software engineering and quality review. Load only the
relevant reference files for each task. It does not override `AGENTS.md`,
`docs/PRODUCTION_POLICY.md`, the registry, or the project production skill.

## Verification

Run:

```bash
python3 .agents/skills/senior-multidisciplinary-agent/scripts/validate_skill.py
python3 -m unittest discover -s tests -p 'test_skill_orchestrator.py' -v
```

The skill/profile cannot grant model access, terminal permissions, paid API
access or any autonomous service.
