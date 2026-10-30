# OpenMontage: Codespaces recovery and one-click sample rendering

This is an **incremental engineering step**, not a claim that an unattended OpenMontage creative agent has been installed. The full agent-directed research/script/assets/edit/compose process still needs a compatible execution agent, usable media sources, and required approvals.

## 1. Preserve your existing Outer Space Mysteries production

**Do not recreate or delete your original Codespace.** The production files and checkpoints live only in the Codespace's ignored `integrations/openmontage/.runtime/openmontage/projects/` directory unless separately exported.

To inspect those checkpoints **without printing narration, URLs, API keys, or media contents**, open the existing Codespace terminal at the repository root and run:

```bash
python3 integrations/openmontage/scripts/report_progress.py
```

To narrow it to one project, first take the `project_id` from the inventory and then run:

```bash
python3 integrations/openmontage/scripts/report_progress.py --project outer-space-mysteries
```

The command does not write, upload or delete anything; it prints project IDs, checkpoint **statuses only**, and whether a verified final MP4 exists. It calls `ffprobe` on an existing final MP4 when available. Share the **read-only output** with ChatGPT to plan the next safe recovery step. Before sharing, review project names as those too may be personal. This inventory cannot itself transfer the actual checkpoint payload or large media files to GitHub.

**If the command does not exist in the old Codespace checkout:** this tool was added after the existing Codespace branch was created. Instead of risky merges or a forced reset, open the latest reviewed branch on GitHub, select the file `integrations/openmontage/scripts/report_progress.py` and copy it into your existing Codespace, or wait for guided recovery. Do not clone over the running project.

## 2. One-click free video render (without Copilot)

On Android Chrome, open the repository's **Actions** tab and select **OpenMontage — manual zero-key MP4**. Select **Run workflow** on `main`, choose one of the three official demo fixtures and confirm.

The workflow runs isolated pinned OpenMontage on a clean GitHub-hosted runner, validates the MP4 using `ffprobe`, and uploads it as an Actions artifact. This is a **demo composition**, not a narration-led personal faceless episode. It uses no paid media or AI API, but GitHub Actions compute minutes may count against your account quota.

Manual workflow: https://github.com/urfavxbf/video-ai-editor/actions/workflows/openmontage-manual-demo.yml

## 3. Needed before full faceless-video automation

- Provide a secure, intentional transfer path for the Codespace's actual approved checkpoint artifacts and media; the GitHub connector cannot read ignored Codespace files.
- Implement an agent executor or explicit deterministic production specification for agent-dependent OpenMontage stages; do not silently skip required human gates.
- Generate English narration using **the existing approved Chatterbox V3 Natural Storyteller** profile, with practical CPU/GPU feasibility checks. The demo renderer does **not** silently replace this voice.
- Perform per-video licensing and audio/subtitle/video QC, publish only on explicit authorization, and link a verified final MP4 artifact.

The operating rules in [agent-policy draft PR #50](https://github.com/urfavxbf/video-ai-editor/pull/50) are separate from this integration.
