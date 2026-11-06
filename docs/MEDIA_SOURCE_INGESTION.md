# yt-dlp media-source ingestion

A focused, opt-in **authorized URL → local source footage → FFprobe → Remotion**
path. This is not a hosted editor, DRM bypass, video piracy tool, permanent
ChatGPT plugin, or one-click story-to-MP4 generator.

## Install in Codespaces or a local environment

The stable upstream release `yt-dlp==2026.10.26` is pinned in
[`requirements-media-ingestion.txt`](../requirements-media-ingestion.txt).
The devcontainer automatically runs `scripts/setup-ai-video-tools.sh`, which
installs yt-dlp into the project-local `.venv`. Install independently when
needed (Python 3.11+, FFmpeg and FFprobe):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-media-ingestion.txt
.venv/bin/python -m yt_dlp --version
```

Some website extractors require optional JavaScript support (Node.js 22+
is part of this project's Codespaces setup). A pinned stable version is
reproducible but sites may change unexpectedly.

## Only source material you are allowed to use

Obtain footage that you own or have explicit permission and site rights to
download and edit. Public YouTube/Vimeo availability does **not** confer
reuse rights. Respect copyright and terms of service; no DRM, private
account, paywall, login or geo-restriction bypass.

Metadata-only inspection contacts the source website:

```bash
.venv/bin/python scripts/media_ingest.py inspect 'https://vimeo.com/123'
```

Download one specifically approved public source:

```bash
.venv/bin/python scripts/media_ingest.py download \\
  'https://vimeo.com/123' --confirm-rights

# Request existing subtitle tracks when available.
.venv/bin/python scripts/media_ingest.py download \\
  'https://vimeo.com/123' --confirm-rights --subtitles
```

The wrapper accepts only HTTPS sources from YouTube, Vimeo, Internet
Archive or Wikimedia Commons. No playlists, arbitrary URLs, cookie
extraction, credentials or custom yt-dlp flags. It ignores user config,
puts files under **gitignored** `input/ingested/`, requests at most one
media item, has timeouts and a best-effort 500 MiB file-size filter, and
checks the final file path and size. This allowlist reduces risk but is
**not a complete SSRF sandbox**: run on trusted URLs and nonprivileged hosts.

The format selector prefers up-to-1080p MP4 video. Unsupported formats
may fail rather than silently transcode; some sites require updated
extractors. Neither metadata success nor a source download is a
completed, edited, publishable video.

## Hand off to FFmpeg / Remotion

1. Verify actual footage identity, licensing and audible/visual content.
2. Use FFprobe against the real file (replace the path with your output):

   ```bash
   ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height -of json input/ingested/EXAMPLE.mp4
   ```

3. Set the approved source path and cuts in `src/edit/edit.json`.
   Run `node scripts/validate-edit.cjs src/edit/edit.json --media`.
   Ingestion never silently changes your edit configuration.
4. Render with Remotion, inspect frame integrity, captions and actual output,
   and follow the project's existing delivery QA gate.

## Validation and scope

```bash
python3 -m unittest discover -s tests -p 'test_media_ingest.py' -v
```

The tests run without downloading media. GitHub Actions also verifies
that the pinned Python CLI installs and displays a version. A skill ZIP
is instructions only: installing the CLI in Codespaces does not permanently
install it in ChatGPT's toolset.

Upstream: [yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
and [installation instructions](https://github.com/yt-dlp/yt-dlp/wiki/Installation).
