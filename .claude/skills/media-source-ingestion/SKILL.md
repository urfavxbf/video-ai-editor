---
name: media-source-ingestion
description: Use for inspecting approved video URLs, rights-cleared single-source yt-dlp downloads, optional subtitle files, and FFprobe preparation before Remotion editing.
---

# Media Source Ingestion (yt-dlp)

Use only on authorized online video sources. Read `AGENTS.md`,
`docs/PRODUCTION_POLICY.md`, `characters/registry.json`, and
`docs/MEDIA_SOURCE_INGESTION.md` before a media-import task.
Use the root `video-effects` or appropriate Remotion specialist **after**
retrieving and checking an approved source.

- Runtime: `requirements-media-ingestion.txt` pins yt-dlp 2026.10.26.
- Existing local entrypoint: `scripts/media_ingest.py` (no shell, single video,
  explicit HTTPS host allowlist, no cookies/playlists, local ignored output).
- Codespaces installation: `scripts/setup-ai-video-tools.sh`.
- Read-only version check: `.venv/bin/python -m yt_dlp --version`.

## Task workflow

1. Confirm rights to download/edit the **specific** source and the source
   website's terms. Public availability and extractor metadata do not
   establish copyright permission.
2. Only for a user-approved URL, inspect metadata:

   ```bash
   .venv/bin/python scripts/media_ingest.py inspect 'https://vimeo.com/123'
   ```

3. Download only when the user has authorized the specific source:

   ```bash
   .venv/bin/python scripts/media_ingest.py download \\
     'https://vimeo.com/123' --confirm-rights
   ```

   Add `--subtitles` to request available English/Tagalog tracks.
4. Check the actual file under ignored `input/ingested/` using FFprobe,
   validate legal use, media duration/codecs/orientation and create a real
   local edit manifest. Use `node scripts/validate-edit.cjs
   src/edit/edit.json --media` for a supplied-source edit.
5. Run `python3 -m unittest discover -s tests -p 'test_media_ingest.py' -v`.
   CI uses mocks and **never downloads** video from remote sites.

## Non-negotiable boundaries

Do not automatically run a pasted URL; metadata inspection itself calls a
remote server. Never evade DRM, paywalls, sign-in, geo/access restrictions,
or acquire prohibited/uncleared copyrighted footage. No batch downloads,
cookies, third-party login, unreviewed uploads, hidden media publishing,
or privileged arbitrary URL execution. Host allowlisting is a first gate,
not a complete SSRF sandbox. yt-dlp's 500 MiB transfer filter is only
best-effort; the final file is checked for size as well.

This `SKILL.md` supplies agent guidance, not a permanently installed
ChatGPT application or direct internet-downloading power. Running the
Codespaces setup installs the CLI **inside that Codespace**, not ChatGPT.
