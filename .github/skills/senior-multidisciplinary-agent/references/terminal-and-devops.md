# Terminal, Linux, Git and DevOps — senior workflow

## Discovery before mutations
Determine working directory, operating system, active user, repository root, current branch, status, permissions and available tools. Read failures exactly; capture exit codes. Prefer bounded commands such as `git status --short --branch`, `git diff --check`, `df -h`, `free -h`, `command -v ffmpeg`, and `git log -5 --oneline`. Do not print secret-bearing environment variables. Diagnose using the minimum necessary privileges.

## Execution discipline
Use quoted paths, explicit working directories, `set -euo pipefail` for nontrivial Bash scripts when appropriate, verified exit codes, safe temp directories, and cleanup traps. Commands should be idempotent where possible. For bulk operations, dry-run or enumerate targets first. Never pipe opaque network scripts into a shell, use sudo blindly, overwrite credentials, or force-push without authorization. Keep CPU, disk, memory and network usage bounded.

## Git and pull requests
Fetch and inspect existing branches; preserve unrelated changes. Create short focused branches, avoid committing generated secrets and huge binaries, review diffs and staged files, run relevant tests, and give a rollback strategy. Avoid pushing to main or merging without authorization. Keep PR descriptions reproducible, including exact verification and failures.

## Containers and Codespaces
Read `.devcontainer/devcontainer.json`, installed tool versions, package lock files and repository scripts first. Favor pinned versions and least privilege. Check port exposure and secrets injection; make build dependencies reproducible. Avoid needless package installation or rebuilding Codespaces. For deployment: plan health checks, backups, rollbacks, cost controls and observability.

## Debugging
Reproduce the failure, isolate the earliest incorrect assumption, test one hypothesis at a time, collect minimal logs and redact secrets. Distinguish network, permissions, disk, CPU, process lifecycle, version mismatch, and configuration issues. Test fixes without turning off safety checks. For shell output include command, exit status, relevant stdout/stderr and next actionable step.

## Verification gate
Run appropriate lint/tests, verify file paths, monitor resource use, review diff and state what was *actually* executed. When commands cannot run, report the missing capability rather than asserting success.
