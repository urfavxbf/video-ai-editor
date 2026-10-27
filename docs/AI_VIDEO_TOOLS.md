# AI Video Editing Tools for Claude (Codespaces + Android)

This extends the existing Remotion-based effects project without modifying its effect components. It provides guidance and optional tooling, **not** a one-tap connection from Claude's mobile chat to GitHub.

## Install in Codespaces

After this PR is merged and pulled into the Codespace:

    git pull
    bash scripts/setup-ai-video-tools.sh

The script checks FFmpeg, requires Node.js 22+, installs a Python environment and Groq SDK, then installs HyperFrames official **core skills** for compatible coding agents. It does not install Claude Code, create a Groq account, render a video, or connect Claude.ai to the Codespace.

For **Claude Code** users, HyperFrames' official plugin install is alternatively:

    claude plugin marketplace add heygen-com/hyperframes
    claude plugin install hyperframes@hyperframes

Use either the official plugin or standalone skills; you don't need both.

To make motion graphics in a separate directory (do not mix project formats):

    mkdir -p hyperframes-projects
    cd hyperframes-projects
    npx hyperframes init my-motion-clip

## Transcribe Tagalog or Taglish speech

1. Obtain your own API key from https://console.groq.com/keys.
2. Under GitHub user Settings > Codespaces > Secrets, add GROQ_API_KEY and grant access to this repository. Restart the Codespace.
3. Upload an audio/video file that you have the right to process to a local untracked input directory, e.g. input/myclip.mp4.
4. From the repo root run:

    source .venv/bin/activate
    python scripts/groq_transcribe.py input/myclip.mp4 --output-dir out/transcripts

Output: out/transcripts/myclip.json, .txt and .srt. The script compresses audio and uploads it to Groq. For Taglish, let Whisper auto-detect language. Review transcription: code-switching, slang and names can be inaccurate. Groq has usage limits and potential charges.

## Claude Skill

Project-local .claude/skills/ai-video-editor/SKILL.md is for Claude Code. For the separate Claude.ai app upload, import the accompanying ZIP through Customize > Skills > Create skill > Upload a skill. Enable code execution. The ZIP describes workflows; it cannot access files in Codespaces without an actual connection.

Links:
- https://github.com/heygen-com/hyperframes
- https://console.groq.com/docs/speech-to-text
- https://support.claude.com/en/articles/12512180-use-skills-in-claude
