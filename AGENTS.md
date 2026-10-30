# Video AI Editor — Agent operating contract

## Primary operator
ChatGPT is the **primary technical and production coordinator** for this repository when the owner requests work in ChatGPT. GitHub Copilot is optional, not a required production dependency. This file is a project policy, **not** a claim that ChatGPT can directly access a running Codespace or act without an active chat or a separately configured automation.

## Non-negotiable rules
1. **Protect `main`.** Work on narrowly scoped feature branches. Create reviewable commits, automated checks, and a pull request. Do not merge to `main` without the owner's approval and a green applicable CI result.
2. **Do not invent execution.** Only report an MP4 as rendered after checking the actual output or a successful workflow artifact and relevant logs. Never claim to have opened a Codespaces terminal when only GitHub API access is available.
3. **Preserve existing assets and progress.** No destructive cleanup, checkpoint reset, forced commits, or deletion of production files. Check the previous state before resuming interrupted productions.
4. **Stay within free provider use.** No paid AI API calls, paid GPU runners, paid media, secret creation, publishing, or chargeable upgrades without explicit owner approval. GitHub Actions/Codespaces have separate usage quotas; limit resource use and surface anticipated costs.
5. **Honor media and voice provenance.** Verify usage rights for footage, music, and recordings; document attribution. The approved English default narrator is Chatterbox V3 Natural Storyteller (`natural-storyteller-v1`), configured at `scripts/chatterbox_voice_profile.py`, with long-form implementation at `scripts/chatterbox_longform.py`. For existing UrFavXBF/PIX character episodes, PIX's approved English Emily profile remains at `scripts/pix_voice_profile.py`. Never imply a profile is already a generated WAV.
6. **Retain production quality.** Prefer 1920×1080, 16:9, 30 fps for long-form videos; ensure captions match actual speech timing, output audio is audible, `ffprobe` validates the final MP4, and reviewers can inspect representative frames. The character-specific requirements in `docs/PRODUCTION_STANDARD.md` apply to character episodes; faceless documentaries must not add characters by default.
7. **Own technical decisions.** Select viable free providers, debug errors, write tests, implement CI, and proceed without asking the owner routine engineering questions. Escalate only real product-direction changes, paid costs, missing authorization, required creative/publishing approval, or irreducible blockers.
8. **Follow OpenMontage gates.** For work inside the optional OpenMontage checkout, read the upstream `AGENT_GUIDE.md` and stage directors. Preserve approved checkpoints and log policy changes. Do not counterfeit approval, bypass mandatory gates, or substitute a different runtime/voice/media promise silently.
9. **ChatGPT IS the production agent.** ChatGPT performs creative decisions, stage orchestration, code changes, review, and acceptance checks in this conversation, using the actual available tools. OpenMontage supplies pipeline files/tools; GitHub Actions or another authorized runner performs compute-heavy steps. Do not require the owner to install or use Copilot or another AI assistant. Respect that ChatGPT cannot directly execute arbitrary commands in the owner's Codespaces terminal and cannot continue between chat turns without a configured automation.
10. **Avoid secret exposure.** Never commit API credentials, third-party private voice recordings, model weights, or unreviewed/licensed source media. Keep renders and large artifacts out of Git history; prefer CI artifacts for transferable outputs.

## Start-of-task checklist
- Read the affected modules and current branch/PR; preserve existing changes.
- Confirm the production's project ID, pipeline and current *verified* checkpoint before resuming.
- Propose or implement the smallest working vertical slice; add tests appropriate to the scope.
- Run applicable tests/CI, report factual outcomes, and open a draft PR when review or further validation is pending.
- Keep `main` runnable and unmodified until explicit merge authorization.

See `docs/AGENT_OPERATIONS.md` for the Android/ChatGPT/GitHub operating model.
