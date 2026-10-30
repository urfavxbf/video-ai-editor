# OpenMontage — isolated faceless YouTube production

This is an **opt-in** OpenMontage integration for the existing `video-ai-editor` repository. It deliberately does **not** change the default `.devcontainer/devcontainer.json`, root `package.json`, Remotion compositions, existing voice/character policies, or the `main` branch.

## Android phone only: Codespaces walkthrough

1. In Android Chrome, sign in to GitHub. Open the `urfavxbf/video-ai-editor` repository and enable **Desktop site** if the buttons are hidden.
2. Open **Code → Codespaces → Create codespace**. Select the branch `feature/openmontage-codespaces` and the **OpenMontage (isolated) — Faceless YouTube** devcontainer configuration (`.devcontainer/openmontage/devcontainer.json`). GitHub can show the configuration selector under advanced options.
3. Let the profile's `postCreateCommand` finish. It installs a pinned checkout, separate Python virtual environment and separate Remotion dependencies inside `integrations/openmontage/.runtime/openmontage/`. Cloud compute may count against your Codespaces/Actions allowances.
4. In Codespaces, open **Terminal → New Terminal** and run:

   ```bash
   bash integrations/openmontage/scripts/doctor.sh
   bash integrations/openmontage/scripts/demo.sh world-in-numbers
   ```

5. From the VS Code file explorer, find `integrations/openmontage/.runtime/openmontage/projects/demos/renders/world-in-numbers.mp4`. Right-click and **Download** to your Android phone. This first MP4 is a technical test, **not** yet your faceless episode.

If you chose the **default** devcontainer instead, install in its terminal with:

```bash
bash integrations/openmontage/scripts/codespace-setup.sh
```

No Termux, Android root access, or local laptop is needed. **Codespaces and any paid AI service may have usage costs.** A GitHub account's quota varies; check your billing before a large render.

## Start a faceless production

Open the nested upstream folder `integrations/openmontage/.runtime/openmontage/` in an AI coding assistant that can **read repository files and execute commands in the Codespace** (not just a plain text chatbot). Have it read `AGENT_GUIDE.md`, `PROJECT_CONTEXT.md` and the selected `pipeline_defs/` manifest before attempting production.

Starter prompt for a 16:9 YouTube episode:

> Read AGENT_GUIDE.md and PROJECT_CONTEXT.md first and follow the OpenMontage pipeline. Create an original 3-minute faceless YouTube documentary about why satellites don't fall straight to Earth. Use 16:9 1920x1080, clear English narration, captions, real licensed stock/archival footage where feasible, and copyright-safe background music. Choose the documentary-montage pipeline or explain why animated-explainer fits better. Use **zero paid API calls**. Research and propose an outline, storyboard, media sources/licenses and costs first; **stop for my approval** before producing assets or rendering. If free narration is not available, report the blocker instead of silently replacing it.

OpenMontage is an agent-driven production system, **not** an unattended one-command topic-to-video CLI. The agent must drive its documented pipeline and approval gates. It is separate from the original video's UrFavXBF/PIX characters and narration defaults.

## Manual commands

From the parent repository root:

```bash
bash integrations/openmontage/scripts/setup.sh           # pinned checkout + dependencies + optional Piper TTS
bash integrations/openmontage/scripts/setup.sh --skip-tts # installation without optional Piper TTS
bash integrations/openmontage/scripts/doctor.sh           # verify install; no secrets printed
bash integrations/openmontage/scripts/demo.sh             # free sample render
```

To upgrade the upstream snapshot, **review** the new OpenMontage commit and update `UPSTREAM_COMMIT` via a separate PR; re-run CI. The installer refuses to overwrite tracked changes in the nested checkout.

## Design and safety

- **Upstream pinned:** `calesthio/OpenMontage` at commit `195eab24478dc9363326aec437aefc3701635ddf` (third-party source, under its upstream AGPLv3 license). The code is fetched only when the optional installer runs; it is not copied or committed into this repository.
- **Isolation:** all checkout files, NPM installs, Python packages, local `.env`, downloaded media and MP4 renders live under ignored `integrations/openmontage/.runtime/`. It never changes root dependencies or project compositions.
- **Approval/billing:** no OpenMontage provider keys are required for demo rendering. Optional provider keys should be set through GitHub Codespaces secrets or kept exclusively in the ignored nested `.env`; never commit credentials. A separate AI coding assistant connection is still required to execute real production pipelines.
- **CI:** the new pull-request-only workflow runs contract tests and a zero-paid-API demo render, uploading a short-lived MP4 artifact when it succeeds. CI runs consume GitHub Actions minutes and are **not** a complete end-to-end faceless-episode test.
- **Licensing:** confirm media license and attribution terms before public YouTube uploads. Stock availability and copyright safety must not be assumed automatically.
- **Preservation:** the existing `video-ai-editor` mainline, UrFavXBF/PIX presets, default 16:9 pipeline, and historic videos stay unchanged. No merge is performed by this setup.

Upstream documentation: https://github.com/calesthio/OpenMontage/blob/main/README.md
