# Senior Multidisciplinary AI Agent

This repository includes a workspace custom agent and reusable skill for professional engineering assistance.

## Locations
- VS Code / Copilot custom agent: `.github/agents/senior-multidisciplinary.agent.md`
- Copilot project skill: `.github/skills/senior-multidisciplinary-agent/SKILL.md`
- Codex project skill: `.agents/skills/senior-multidisciplinary-agent/SKILL.md`

The two skill copies have matching content for compatibility; update both when maintaining the skill. The agent may be selected from the VS Code Chat agent picker; skill discovery depends on the active harness.

## Scope
Senior-level procedures for terminal and DevOps, AI engineering, motion graphics, sourced research, and production software engineering. This skill is instructions and supporting scripts, not a separately hosted model or autonomous service.

## Precedence and preservation
Follow the existing root `AGENTS.md`, `docs/PRODUCTION_POLICY.md`, character registry, and existing `.claude/skills/ai-video-editor/SKILL.md` for actual video production. The new skill does not replace or weaken those requirements.

## Verification
Run `python3 .agents/skills/senior-multidisciplinary-agent/scripts/validate_skill.py`, or the equivalent command at `.github/skills/`. The read-only diagnostic is `scripts/doctor.py` in either skill directory.

Agent definition and skill files are configuration/instructions. They do not grant model access, terminal execution rights, file-edit permission or paid API access. Review resulting actions and tests.
