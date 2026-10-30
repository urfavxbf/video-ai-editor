# Security, Operational Safety and Quality — senior workflow

## Authorization
Differentiate analysis from mutation. Read-only inspection can proceed within granted tool scope; external publishing, destructive operations, spending money/GPU resources, access-control changes, credential rotation and merges need explicit authorization. Use feature branches and reviewed PRs for repository changes. Do not bypass project policies or owner approval by declaring an action 'autonomous'.

## Threat modeling
List protected assets, entry points, data flows, attackers and trust boundaries. For AI tools, guard against prompt injection, hostile retrieved documents, tool-output laundering, server-side request forgery, command injection, path traversal and unsafe code execution. For media, verify rights, personal-data consent and disclosure obligations. Secure secrets through a supported secret manager and never hardcode or echo them.

## Reliability
Use timeouts, bounded retries, idempotency, fallbacks, safe rollback, alerts and health checks. For code require tests and measurable acceptance criteria. For AI require evaluations and traceable tool outputs. For motion require playable artifacts, frame/audio checks, license audit and reproducible renders. For research require credible, dated citations and methodological transparency.

## Independent review
Before delivery, inspect the actual diff or artifact for correctness, maintainability, readability, compatibility, error handling, resource use, accessibility and unfinished work. Distinguish no-issues-observed from proof of safety. Do not claim a check passed unless executed. Report command, exit status, evidence, known limitations and rollback.

## High-impact stop conditions
Stop before destructive commands affecting personal data, uncontrolled scripts from external sources, credential disclosure, secret commits, public release, paid GPU/API calls, force pushes and irreversible account changes unless specifically authorized. Seek approval only for the blocked high-impact action, not routine engineering decisions.
