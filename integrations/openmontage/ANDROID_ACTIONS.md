# OpenMontage video rendering from Android (without an existing Codespace)

The repository has the reviewed, pinned OpenMontage integration on `main`. **An old test Codespace is not required** for the supported GitHub Actions tasks. Do not restore or retrieve the old experimental project's checkpoints.

## Launch a test render

1. Open https://github.com/urfavxbf/video-ai-editor/actions/workflows/openmontage-manual-demo.yml on Android Chrome.
2. Select **Run workflow** on `main` (once this workflow has been reviewed and merged).
3. Choose one of `world-in-numbers`, `code-to-screen`, or `focusflow-pitch`.
4. Check the resulting Actions run for both successful tests and a successfully validated MP4.
5. Download the `openmontage-demo-<name>` Actions artifact to Android.

This workflow runs on a GitHub-hosted runner and does **not** connect to any user's Codespace. It uses the pinned upstream code, FFmpeg and free bundled demonstration compositions. It uses no AI API and no stored video project state. GitHub Actions compute minutes and storage may still count against the account's usage allowance.

**This is a test render, not a finished faceless YouTube episode.** A production pipeline still needs an agent or a deterministic, fully specified video brief, the approved English Chatterbox Natural Storyteller voice with usable compute, licensed media, and verification of captions/audio/video before upload. Nothing here publishes videos.

## Deleting the old test Codespace

Since its local experimental files are not being used, the old test Codespace may be deleted **if you don't want to keep any uncommitted work or generated media stored inside it**. The OpenMontage integration and verified sample CI artifact are tracked independently on GitHub.

From an Android browser, open https://github.com/codespaces. Locate the **old test Codespace** for `urfavxbf/video-ai-editor`, open its `...` menu, and choose **Delete**. Confirm the specific Codespace; do not delete the GitHub repository. Deletion permanently discards Codespace-only files and cannot be undone by this integration. This action must be completed by the account owner via the GitHub UI; the ChatGPT GitHub integration cannot delete Codespaces.
