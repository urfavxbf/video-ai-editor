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

The queued job file currently uses a temporary signed source-media download URL, **visible in this public repository while it remains tracked and in Git history**. It will eventually expire, but removing a tracked file does not erase historical Git commits. Only use this queue mode for footage whose temporary accessibility is acceptable; for confidential files, a private repo plus secure object storage or an authenticated file-transfer mechanism is needed. Never place permanent API credentials in job files.

Do not publish third-party podcast footage without the necessary license or permission. Credits and motion graphics do not automatically confer reuse rights.

## Current scope

This automation renders the existing Dudut composition. The workflow does not yet automatically select highlights, write new motion-design compositions, upload to YouTube or turn any arbitrary clip into a publish-ready edit unattended. Those features require a more general editing orchestrator and secure upload channel.
