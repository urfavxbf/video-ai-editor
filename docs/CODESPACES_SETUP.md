# GitHub Codespaces setup — Video AI Editor

This repository has a checked-in [dev container](../.devcontainer/devcontainer.json) that prepares the video-editing tools for a browser-based Codespace. A ChatGPT-connected GitHub repository integration can edit the configuration, but **the account owner must create and authorize a Codespace using the GitHub UI**.

## Create a new Codespace (Android browser)

1. Open https://github.com/urfavxbf/video-ai-editor while signed into your GitHub account.
2. Choose **Code** → **Codespaces** → **Create codespace on main**. If you see **New with options**, select branch `main` and the **Video AI Editor** dev container.
3. Open in the browser's VS Code editor. If the UI is cramped on a phone, use the browser's **Desktop site** option.
4. The dev container runs `bash scripts/setup-ai-video-tools.sh` at first creation. This installs Node/Remotion, FFmpeg, Python/Groq SDK, HyperFrames skills, and the Remotion browser.

Initial setup downloads several dependencies. If it stops or an installation fails, reopen the terminal in the repository and retry:

```bash
bash scripts/setup-ai-video-tools.sh
```

## Safely enable the Groq API key

The secret **name** is `GROQ_API_KEY`. Never paste its value in chat, an issue, a repository file or a terminal command that would end up in history.

If the secret was already saved for `video-effects-mobile`, keep the existing secret and update its **Repository access** to also include `urfavxbf/video-ai-editor`.

1. Open https://github.com/settings/codespaces
2. Under **Codespaces secrets**, locate `GROQ_API_KEY`, choose **Update**.
3. Under **Repository access**, tick `urfavxbf/video-ai-editor` and save.
4. **Restart** any Codespace that was already running before the change (or create the Codespace after updating access).

Don't confuse Codespaces secrets with GitHub Actions repository secrets. The editor's Groq transcription needs a **Codespaces** secret.

## Verify installation

Run in the Codespaces terminal:

```bash
bash scripts/check-codespace.sh
```

The check verifies Node.js, FFmpeg/FFprobe, Groq SDK, NumPy, Pillow, Remotion CLI and TypeScript. It only reports whether a Groq key is present — it never prints the key or makes a paid API request.

For a preview, from the project root:

```bash
npm run studio
```

Then open the forwarded Remotion Studio port (normally port 3000). For a working sample motion-effects output:

```bash
npm run render:showcase
```

The output should be generated in `out/showcase.mp4`. Renders use your Codespace's available compute resources and might use billable Codespaces quota; monitor your usage.

## Working with your own footage

Upload authorized footage to `input/` inside the Codespace, then transcribe when needed:

```bash
mkdir -p input
.venv/bin/python scripts/groq_transcribe.py input/myclip.mp4 --output-dir out/transcripts
```

The `input/`, `out/`, and `.venv/` folders are ignored by Git. Avoid making input files publicly available, and ensure you have permission to edit and publish third-party footage.

## Notes and limitations

- The 21 original effect components are included. Some cutout effects depend on macOS Apple Vision tools; Linux Codespaces cannot run those native Swift helpers directly. Other effects and renders work without those helpers.
- The dev container installs the editing toolkit; it does not automatically control or upload to YouTube, build a finished edit from arbitrary source footage, or give this chat direct terminal access to the new Codespace.
- If you get a missing-secret message, check the secret's Repository access and restart the Codespace.
- If the Codespace is missing the devcontainer configuration, create it from the current `main` branch or rebuild the container.
