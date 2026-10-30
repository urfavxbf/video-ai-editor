# Senior Multidisciplinary Agent Skill

Reusable senior-level operating procedures for terminal/Linux/Codespaces, AI engineering, motion graphics/video, factual research/information systems, and production software engineering.

## Quick start

- **Use with an agent that supports Agent Skills:** Install or upload the entire `senior-multidisciplinary-agent/` folder or ZIP according to your agent environment. Its entry file is `SKILL.md`.
- **Codespaces / Codex-style environments:** Keep the folder intact in your environment's supported skills directory. Ask your coding agent to use the `senior-multidisciplinary-agent` skill. Placement/discovery depends on the product and its version.
- **Ordinary ChatGPT chat:** Upload the ZIP or `SKILL.md` and request: "Use the senior-multidisciplinary-agent skill for this task." Uploading a file does **not** necessarily install a persistent skill or provide missing tools.
- **Optional repository instructions:** You may adapt `assets/AGENTS-template.md` as `AGENTS.md` in a repo after reviewing it. The specialized skill is **not** Android-only.

### What this bundle does **not** do

It is not an AI model, actual 15-year employment experience, persistent agent service, guaranteed install in every ChatGPT plan, GitHub authentication token, terminal permission, automatic video rendering, or external cloud deployment. It supplies reusable expert workflows and checklists. The runtime must provide the model and tools.

### Files

- `SKILL.md` — scope, routing, orchestration, safeguards.
- `references/` — detailed domain-specific playbooks.
- `assets/` — report template and optional repository instruction template.
- `scripts/doctor.py` — read-only tool/environment probe.
- `scripts/validate_skill.py` — bundle integrity checks.

### Check locally

```bash
python3 senior-multidisciplinary-agent/scripts/validate_skill.py
python3 senior-multidisciplinary-agent/scripts/doctor.py
```

No network access is needed for these two checks. The doctor reports availability only and does not install software.

### Examples of requests

- "Diagnose this failing Codespaces terminal build and fix it safely."
- "Architect a production AI agent with real tools, permission gates, and evaluation tests."
- "Build an animated title intro with a reproducible FFmpeg/Remotion workflow."
- "Fact-check this topic, cite current primary sources, and make an executive briefing."
- "Create a scalable full-stack application with CI, tests, security, and documentation."

## Design notes

The manifest uses the `name` and `description` YAML frontmatter pattern, with specialist references loaded only when pertinent. It's intentionally vendor-neutral and can be adapted to the installed agent runtime.