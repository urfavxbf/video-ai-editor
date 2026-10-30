# Codex-native isolated OpenMontage

The current Codex environment is the coding/orchestration agent. Do not ask the
owner to install Copilot, Claude, Cursor or another AI assistant. Actions executes
bounded commands, not AI creative reasoning.

Read the root AGENTS.md/current production policy first, then README.md and
`docs/OPENMONTAGE_CODEX_GAP_AUDIT.md` in the host. Upstream is reference material;
provider promotions, budget defaults, 24 fps recommendations or generic voices
cannot override approved English Chatterbox, 1920×1080/30 fps and zero-paid-API/GPU.

From the host root use `setup.sh --skip-tts` and
`python3 integrations/openmontage/scripts/production.py preflight`.
In the verified nested checkout read CODEX.md → AGENT_GUIDE.md → PROJECT_CONTEXT.md,
pipeline_defs/documentary-montage.yaml and each selected director/meta/tool skill.
Preserve schema validation and all four human approval gates. Missing media/models
are blockers rather than permission to substitute providers or an execution agent.

Codex authors/reviews brief, original narration script, scene slots, footage
selection/provenance, timings and edits. Python does not invent creative artifacts.
Use the adapter for checkpoints/execution, with projects in the ignored runtime.
`--approve` records a real owner decision reference; never infer or fabricate it.
Automated gate simulation is confined to the labeled fixture test, rejected by
production mode. Stage approvals do not grant budget or publishing permission.

First route: approved local motion inputs, one approved English WAV and WAV-bound
reviewed captions, hard cuts and explicit music/end-tag opt-outs. Other choices
need real upstream stages/follow-up adapters; never silently drop them. Technical
QA is not listening, perceptual review or legal clearance. No secrets, paid calls,
publishing, direct main pushes or merges.
