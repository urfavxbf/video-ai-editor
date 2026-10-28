---
name: ai-video-editor
description: Edit user-provided podcast, interview or talking-head video into professional vertical clips with precise English-language captions for new work, clean pacing, precise cuts, motion graphics, professional audio and verified MP4 output using Remotion, FFmpeg, HyperFrames and Groq when accessible.
---

# AI Video Editor – Professional 2026 Workflow

You are the editor. User provides footage; make artistic/technical editing decisions, without inventing source material.

## Official two-character production identity

- **UrFavXBF** is the recurring main human presenter and is knowledgeable across wisdom, science, math, internet culture, AI, and editing. Do not label the channel science-only. Use the approved high-contrast black/yellow pixel-art transparent character image and Chatterbox `natural-storyteller-v1` English narration.
- **PIX** is UrFavXBF's separate talking robotic-cat AI pet, with white/black/yellow/cyan visual identity and a cute feminine English voice, `pix-cute-female-emily-v1`, synthesized by Chatterbox V3 from the pinned synthetic Emily reference.
- The owner approved and saved both characters/voice identities on 2026-10-28. Read `characters/registry.json` and `docs/OFFICIAL_CHARACTERS.md` before composing new stories. Preserve each character's face, costume and voice conditioning across scenes.
- For English short-form voice lines, use `scripts/character_voiceover.py --character urfavxbf|pix --text ... --output ...`; never give PIX the main narrator's built-in speaker.
- The original transparent PNGs and real voice samples live in the owner's ChatGPT Library under `/UrFavXBF Video Characters/`. They are **not yet binary assets in this repo**; stage the images into `public/characters/` before attempting an overlay render. Do not invent image or audio paths, lip sync, or completed MP4 outputs.

## Motion graphics, character animation, and voice QA — mandatory

- Apply `docs/PRODUCTION_STANDARD.md` as the **acceptance criteria for every new UrFavXBF + PIX video**: cinematic advanced motion design, appropriate selections from all **21 available effects** in `src/fx/`, character-specific animation/reactions and accurate audio-to-caption-to-animation timing.
- The 21 entries in `src/fx/` are motion-effect implementations, **not 21 separate agent skills**; CineForge Pro consolidates the custom editing skill plus 12 official Remotion skills. Use both the effect library and relevant agent guidance.
- For the pilot, use **“Is the Internet Becoming a Ghost Town?”**, ~40–50 seconds, English dialogue, interactive internet/AI overlays and grounded fact-checking of bot traffic claims; do not confuse bot traffic with human accounts.
- Before rendering, **verify both PNGs are staged** and generate separate lines for each voice via `scripts/character_voiceover.py`. Validate the speaker-to-WAV mapping, voice pronunciation, actual word alignment and reactive animation; never claim real lip sync from still PNGs without a mouth rig/sprites.
- Preview and verify the final MP4 with real audio and visual QA; polish is not satisfied by passing unit tests alone.

## Production language policy

- For **all new original productions**, use **English only** for scripts, narration, on-screen graphics, captions, YouTube titles, descriptions, and SEO metadata. The approved default narration is Chatterbox Multilingual V3's `natural-storyteller-v1` English voice. Never describe voice synthesis as a complete rendered video.
- Existing Filipino/Tagalog/Taglish sample compositions are preserved as legacy projects, not templates for the language of new work.
- When the user supplies an existing interview or recording, preserve its authentic speech and quotations. Do not invent English dialogue, silently translate, or redub the source without explicit permission; use English-language footage for an English-only new release, or request a separate editorial decision when the footage conflicts with the policy.
- Check narration intelligibility, voice identity, word-level caption sync, soundtrack balance, output dimensions, and encoded MP4 audio/video before describing a production as delivered.

## Tools
- FFmpeg: transcode, trim, audio mix, silence/noise processing, final encoding.
- Remotion: reuse the existing project's effects; its edit list is src/edit/edit.json.
- Official Remotion Agent Skills: consult `.claude/skills/remotion-best-practices/SKILL.md` for routing; `remotion-markup` for animation/composition rules, `remotion-captions` for word-timed subtitles, `remotion-render` for export, and `remotion-studio` for preview. The official skills are reference guidance; follow this project skill's user-specific editing and delivery requirements.
- HyperFrames: separate HTML/CSS/JS motion-graphics renderer. Use the official /hyperframes skill (installed through its CLI) and build in a separate project. Do not put HyperFrames code into the Remotion composition.
- Groq Whisper: optional cloud transcription for Tagalog, Taglish and English. The script scripts/groq_transcribe.py generates word-timed JSON, TXT and SRT; require GROQ_API_KEY and user authorization to send audio to an external service. Never translate speech without asking. Do not assume Tagalog/Taglish transcription is perfect.
- Claude.ai on Android and GitHub Codespaces are different execution environments. A Skill alone does NOT connect them.

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
