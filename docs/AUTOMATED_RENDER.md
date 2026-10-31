# Automated podcast rendering (GitHub Actions)

Workflow: [Render Premium Podcast Short](../.github/workflows/render-podcast.yml)

## What is automated

For the Dudut Lang podcast template, a GitHub Actions runner downloads authorized input media, verifies it, builds the Remotion project, renders the 42-second vertical composition, checks the output file, then uploads it as an Actions artifact.

- Composition: `DudutPremium`
- Original segment: 00:42–01:24 of the 93.7-second supplied source
- Output: `dudut-premium-1080x1920.mp4`
- Export target: 1080×1920, 30 fps, H.264 CRF 16, AAC 256 kbit/s
- Output retention: 14 days in GitHub Actions artifacts, subject to repository plan settings
- Script: `bash scripts/render-dudut.sh input/50812.mp4`

The first queued request is `render-queue/dudut-20261027-premium.json`. The runner stages the supplied footage under the ignored `input/` directory; the original media and rendered MP4 are not committed to the Git repository.

## Download a completed render

Open the successful workflow run in the Actions tab and download the **dudut-premium-1080p** artifact from the Artifacts section. The artifact is a ZIP containing the actual MP4. A successful CI smoke-test frame alone is not a finished video.

## Privacy and intellectual property

The historical queue contains a signed source-media download URL in reachable
Git history. The 2026-10-31 audit found none in current tracked files; token
validity and active deployments remain unverified. See
[the redacted security audit](EDIT_INPUT_SECURITY.md). Removing a tracked file
does not erase historical commits. Keep future URLs in a secret manager and use
authenticated private storage for confidential media. Never commit API credentials.

Do not publish third-party podcast footage without the necessary license or permission. Credits and motion graphics do not automatically confer reuse rights.

## Current scope

This automation renders the existing Dudut composition. The workflow does not yet automatically select highlights, write new motion-design compositions, upload to YouTube or turn any arbitrary clip into a publish-ready edit unattended. Those features require a more general editing orchestrator and secure upload channel.
