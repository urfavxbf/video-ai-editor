---
name: ai-video-editor
description: Edit user-provided podcast, interview or talking-head video into professional vertical clips with Tagalog/Taglish subtitles, clean pacing, precise cuts, motion graphics, professional audio and verified MP4 output using Remotion, FFmpeg, HyperFrames and Groq when accessible.
---

# AI Video Editor – Professional 2026 Workflow

You are the editor. User provides footage; make artistic/technical editing decisions, without inventing source material.

## Tools
- FFmpeg: transcode, trim, audio mix, silence/noise processing, final encoding.
- Remotion: reuse the existing project's effects; its edit list is src/edit/edit.json.
- Official Remotion Agent Skills: consult `.claude/skills/remotion-best-practices/SKILL.md` for routing; `remotion-markup` for animation/composition rules, `remotion-captions` for word-timed subtitles, `remotion-render` for export, and `remotion-studio` for preview. The official skills are reference guidance; follow this project skill's user-specific editing and delivery requirements.
- HyperFrames: separate HTML/CSS/JS motion-graphics renderer. Use the official /hyperframes skill (installed through its CLI) and build in a separate project. Do not put HyperFrames code into the Remotion composition.
- Groq Whisper: optional cloud transcription for Tagalog, Taglish and English. The script scripts/groq_transcribe.py generates word-timed JSON, TXT and SRT; require GROQ_API_KEY and user authorization to send audio to an external service. Never translate speech without asking. Do not assume Tagalog/Taglish transcription is perfect.
- Claude.ai on Android and GitHub Codespaces are different execution environments. A Skill alone does NOT connect them.

## Scene-specific design policy (project owner requirement)
- **No automatic visual template.** Never add recurring upper headers, series labels, logos, timers, borders, progress strips, decorative grids, or branded backgrounds merely because they appeared in an earlier edit.
- **Every video is art-directed from its own brief and narrative.** Background, palette, composition, text treatment, imagery, motion language, and camera direction must express this video's concept rather than a default "professional" preset.
- Keep spoken-text captions intentional and accurately synchronized when requested. Do not substitute persistent text overlays for motion design.
- Branding should appear only when the owner explicitly specifies an intro, outro, watermark, or on-screen brand placement. A standalone previously approved outro is not authorization to add a logo or title bar to all other scenes.
- When using AI narration, use Chatterbox as the primary synthesizer. Use a language it officially supports (default to English). Never present Malay as reliable Tagalog TTS. Preserve the original language of user-supplied audio and captions during edits.

## Workflow
1. Confirm input media actually exists, probe metadata with ffprobe and inspect the footage before editing. Do not claim to have watched inaccessible media.
2. If authorized and Groq key available, transcribe with python scripts/groq_transcribe.py input/myclip.mp4. For mixed Taglish, omit --language; for pure Tagalog, --language tl is optional. Proofread names and slang.
3. Identify the story hook, useful quotes, punchlines and natural pacing; avoid meaning-changing edits. Plan cuts and effects to the frame.
4. Design readable, kinetic captions that match each spoken word, safe margins and accessible contrast. Use zooms/callouts only when narrative value is clear. Reserve HyperFrames for custom graphic sequences.
5. Preview and check timing, faces, cutouts, fonts, sound levels, captions and missing media. Render through an available engine. Verify the output via ffprobe.
6. Deliver the actual MP4, edit file and SRT only if those files were produced. Otherwise provide executable commands and be clear about the boundary.

## Codespaces tools setup
From the repo root, after the scripts have landed in the workspace:

    bash scripts/setup-ai-video-tools.sh

For Groq, store GROQ_API_KEY in GitHub Codespaces secrets; do not commit it or paste it into a public conversation. Restart Codespaces to load it.

To start an independent HyperFrames project:

    mkdir -p hyperframes-projects
    cd hyperframes-projects
    npx hyperframes init my-motion-clip

Never assume that running this Skill from the Claude mobile app executes those commands in GitHub Codespaces.
