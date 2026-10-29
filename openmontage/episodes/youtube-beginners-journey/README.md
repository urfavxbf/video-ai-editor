# YouTube Beginner's Journey — fresh OpenMontage production

**Status (2026-10-29): OpenMontage research completed; proposal awaiting approval. No rendered video yet.**

This is an isolated **brand-new production** using the upstream [OpenMontage](https://github.com/calesthio/OpenMontage) `animated-explainer` pipeline. We do not import or reference earlier graphics, characters, sprite sheets, recordings, captions, scripts, intro sequences, thumbnails or B-roll. This project is scoped under `openmontage/episodes/youtube-beginners-journey/`; no old `public/characters`, `src/episodes`, or recording paths should be read or linked by production scripts. Existing legacy assets in other repository directories are preserved but **excluded from this episode**.

## Goal

Build an original, 16:9 English-language 1920x1080 long-form YouTube explainer **YouTube Beginner's Journey: The First Upload Nobody Watched**. This is about beginning on YouTube, learning from the first underperforming upload, developing an original content process and understanding the monetization journey without suggesting guaranteed income.

- **Budget:** USD 0 paid API/generation spending; do not invoke premium TTS, image/video providers or GPU runners.
- **Assets:** 100% new art and audio created for this episode; no legacy asset references. Any future presenter/sidekick character designs must be freshly generated, separately reviewed and never copied from the old pack.
- **Publishing:** never upload or post automatically.
- **Production method:** read upstream `AGENT_GUIDE.md`, `pipeline_defs/animated-explainer.yaml`, and the relevant director skill before each stage; use upstream schemas and checkpoints.
- **Renderer:** Remotion is the **proposed**, unapproved runtime; actual availability and the Remotion-vs-HyperFrames alternatives must be reviewed before lock-in. `composition_mode=atelier` is the draft direction to avoid reusing old creative assets or templates.

## Pre-production artifacts

- [Research brief](./research_brief.json): six source-backed evidence anchors, three angles, audience questions and independent references.
- [Proposal packet](./proposal_packet.json): three original choices and an explicit **pending** approval gate.
- [Fresh-asset contract](./FRESH_ASSETS_POLICY.md): strict isolation and quality gates.
- `scripts/openmontage_youtube_journey_preflight.py` validates both artifacts against the **actual pinned OpenMontage schemas**, initializes a brand-new OpenMontage project and writes upstream research and awaiting-human proposal checkpoints.
- [GitHub Actions preflight](../../../.github/workflows/openmontage-youtube-journey.yml) checks out the official pinned upstream source, rather than copying AGPL source into this repository, and uploads the checkpoint workspace.

## Resume

Once the proposal and renderer are approved, continue in **OpenMontage order**: `script → scene_plan → assets → edit → compose → publish`. Every scene requires original assets, voice auditioning, quality review and source-aware fact checks. No script/asset/render stage is represented as completed until real, verifiable outputs exist.

This is an OpenMontage **preproduction integration**, not an already-installed, one-click automatic editor and not a completed MP4. Upstream OpenMontage is AGPLv3; this repository merely checks out the external project as a build-time tool. Review license obligations before redistributing combined software.
