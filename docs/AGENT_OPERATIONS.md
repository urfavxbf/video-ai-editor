# ChatGPT-led production operations

## Role and boundaries

The owner assigns ChatGPT the **lead coordination role** for `urfavxbf/video-ai-editor`. In the ChatGPT conversation, the assistant makes technical and implementation decisions, reviews code and logs, opens issues/branches/PRs, and configures **testable** GitHub Actions tasks. The owner supplies topics and approves only business decisions, material costs, publication, or production gates that must have explicit human approval.

This does not grant direct shell access to the owner's Codespace. A GitHub connector can inspect committed files, branch states, pull requests, workflow results, and artifacts; it cannot see uncommitted workspace files or ignored OpenMontage checkpoints. The assistant also cannot continue working after a chat turn ends unless a separate scheduled or event-based automation has been configured.

## Existing systems

- **Mainline:** Remotion/FFmpeg `video-ai-editor`, with 16:9 long-form video as default.
- **Approved English narrator:** `natural-storyteller-v1` Chatterbox Multilingual V3: `scripts/chatterbox_voice_profile.py`, `scripts/chatterbox_longform.py`, `docs/CHATTERBOX_TTS.md`. Existing configured voice is NOT evidence of an audio file in the checkout.
- **OpenMontage:** isolated, pinned integration was merged via [PR #49](https://github.com/urfavxbf/video-ai-editor/pull/49). Its demos run on GitHub-hosted CI without an existing Codespace.
- **Discarded test projects:** do not recover, inspect, migrate, or rely on previous Codespaces test projects. Start new production requests with new, explicit artifacts; the owner may delete unused test Codespaces.

## Production workflow

1. **Request:** capture topic, target platform, duration, language/voice, budget and hard constraints from the conversation. Reuse known requirements; ask only for indispensable product choices.
2. **Locate:** inspect GitHub for reviewed production code, PRs, workflows, and artifacts relevant to the new requested production. Do not inspect or retrieve abandoned Codespaces experiments.
3. **Plan:** create a short, versioned production brief plus the appropriate pipeline manifest/artifacts. For OpenMontage, obey its upstream review stages and human approval gates. Do not invent that a generic prompt alone creates MP4 output.
4. **Build:** branch off green `main`; isolate OpenMontage changes, voices and dependencies. Implement reusable automation with a narrow attack surface and secrets only through approved secret stores.
5. **Run:** use a suitable triggered GitHub Actions job for deterministic code/testing/render tasks. Heavy TTS or video generation must have bounded runtime and resource preflight. If the agent-driven creative stages lack a running compatible agent, report the blocker and do not label the system “one click.”
6. **Validate:** inspect tests, real media artifacts, codecs and duration (`ffprobe`), audio, script/subtitle timing, copyright license metadata and visual samples. Report any checks that could not be performed.
7. **Deliver:** link the verified GitHub workflow/PR and real artifact; leave all proposed branch changes unmerged until approved. Do not publish videos automatically.

## New-project-first automation

All new video work begins with a clean production brief, a new project identifier, and a reviewable pipeline. GitHub Actions operates on checked-in inputs or approved artifacts, never on invisible or abandoned Codespaces-local files. Implement deterministic rendering and bounded agent orchestration on isolated branches, with proper approvals, provider limitations, and license checks.

Do not require the owner to keep an old Codespace, recover test checkpoints, or run interactive Copilot sessions. When a new production does require a human approval gate, present it clearly and wait for authorization rather than silently skipping it.

## No silent spending or unattended claims

Zero paid AI API use is a current constraint. GitHub hosted compute is **not** necessarily free or unlimited. Never promise an overnight live Copilot replacement merely by adding a workflow, and never imply ChatGPT runs while the conversation is closed. Automated runs must be clearly configured, bounded and visible in GitHub.
