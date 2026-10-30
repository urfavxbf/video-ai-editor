# Software Engineering — senior workflow

## Discovery and design
Map the actual repository stack, architectural boundaries, dependency versions, test conventions, deployment path, observability, bottlenecks and security constraints. Prefer official practices and present repository style to default frameworks. Evaluate simplicity, failure modes, change risk and long-term ownership. Do not impose Android patterns on React/TypeScript/Remotion projects.

## Implementation
Define acceptance criteria and contract/interface changes. Prefer small cohesive units, explicit types, predictable errors, backpressure, cancellation, testable boundaries, safe concurrency and data migration plans. Separate domain logic from I/O and UI, avoiding needless abstraction. Never break working behavior to perform unrelated refactors.

## Testing
Start with a reproducible failing case for defects. Add focused unit and integration tests; inspect error, empty, loading and cancellation paths. Run the existing project tests, static checks and targeted builds, and use mocks only for genuine external boundaries. State tests that were not run and why. Do not claim coverage that was not measured.

## Review and security
Review changes for correctness, injection risks, auth/authz, data exposure, dependency vulnerabilities, configuration drift, performance regressions, accessibility, logging, licensing and privacy. Ensure API surface and database contracts remain compatible, or include migration/rollback. Be explicit about security-sensitive changes and minimize permissions.

## Repository-specific video-ai-editor
The repo is a Remotion + React + TypeScript + Python + FFmpeg workspace. Start with root `AGENTS.md`, current production policy and registry. Useful checks include `npm run typecheck` and relevant Python unittest suites. Only run commands supported by available environment and required inputs. Follow regeneration requirements when modifying current production-instruction sources.

## Handoff
Summarize changed files, reason for each architectural decision, verification outcomes, open risks, and how to revert. Use a feature branch/PR where authorized; never merge or release automatically.
