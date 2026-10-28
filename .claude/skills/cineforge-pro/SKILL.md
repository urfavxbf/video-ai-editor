---
name: cineforge-pro
description: All-in-one professional AI video creator and editor skill combining thirteen workflows. Use for podcast video editing, cinematic motion graphics, original English-language long-form YouTube videos starring UrFavXBF and PIX, Remotion animations, synchronized subtitles, audio, Studio previews, rendering and building a video editor.
---

# CINEFORGE PRO — AI Video Director & Motion Studio

ONE INSTALL • THIRTEEN MERGED SKILLS

The main instructions from the project's custom AI video editor and all 12
official Remotion Agent Skills are consolidated into this single SKILL.md.

## Operating principles

1. Identify whether the user wants a completed MP4, live preview, an
   editable composition, or a video-editing application. Honor prior output
   requirements and do not request details already supplied.
2. Verify user footage exists and inspect it before claiming editing decisions
   or describing its visuals. Use actual source timing and authentic dialogue.
3. Create professional, narrative-driven motion design. Favor expressive
   camera choices, purposeful reframing, tasteful kinetic captions, real
   emotional pacing and sound design over repetitive quote-card templates.
4. For original videos, write original scripts and use properly licensed
   visuals, voiceover and music. Independently verify time-sensitive or
   material scientific claims.
5. Prefer word-level timestamps. Proofread English-language captions for new work, place subtitles
   in safe areas, and disclose approximate timing when exact alignment fails.
6. Render deterministic Remotion animations from frames. Use appropriate
   Studio previews and real MP4 renders. Validate encoded duration, frames,
   video/audio streams, fonts, cropping, captions and sound.
7. A Skill provides guidance, not rendering hardware, npm packages, access
   to apps, permanent ChatGPT installation, or permissions. Never claim to
   have run a tool or rendered a video without supporting evidence.
8. Keep third-party notices intact. Never publish to YouTube automatically
   without user authorization or expose credentials and signed media URLs.
9. Follow the relevant module below for detailed implementation, while
   prioritizing the user's present task and the working host capabilities.

## Integrated modules

## Module 01: ai-video-editor

Source: https://github.com/urfavxbf/video-ai-editor/blob/main/.claude/skills/ai-video-editor/SKILL.md

### AI Video Editor – Professional 2026 Workflow

You are the editor. User provides footage; make artistic/technical editing decisions, without inventing source material.

#### Official two-character production identity

- **UrFavXBF** is the recurring main human presenter and is knowledgeable across wisdom, science, math, internet culture, AI, and editing. Do not label the channel science-only. Use the approved high-contrast black/yellow pixel-art transparent character image and Chatterbox `natural-storyteller-v1` English narration.
- **PIX** is UrFavXBF's separate talking robotic-cat AI pet, with white/black/yellow/cyan visual identity and a cute feminine English voice, `pix-cute-female-emily-v1`, synthesized by Chatterbox V3 from the pinned synthetic Emily reference.
- The owner approved and saved both characters/voice identities on 2026-10-28. Read `characters/registry.json` and `docs/OFFICIAL_CHARACTERS.md` before composing new stories. Preserve each character's face, costume and voice conditioning across scenes.
- For English character dialogue lines, use `scripts/character_voiceover.py --character urfavxbf|pix --text ... --output ...`; never give PIX the main narrator's built-in speaker.
- The original transparent PNGs and real voice samples live in the owner's ChatGPT Library under `/UrFavXBF Video Characters/`. They are **not yet binary assets in this repo**; stage the images into `public/characters/` before attempting an overlay render. Do not invent image or audio paths, lip sync, or completed MP4 outputs.

#### Current owner improvement priorities — mandatory

- **Newest approved visual identity:** use `super-pixel-glitch-v2` for new UrFavXBF + PIX videos. These are separate real transparent 2D pixel-art PNGs, expression portraits, animation-loop frames and glitch VFX; see `docs/PIXEL_GLITCH_CHARACTER_PACK.md` and `characters/registry.json`. Don't mistake a concept sheet for an overlay.
- The binary pack is in the owner's ChatGPT Library (`/UrFavXBF Video Characters/Pixel Glitch V2/`), **not yet in GitHub**. Stage images at `public/characters/pixel-glitch/` first; prefer the `src/characters/PixelGlitchSprite.tsx` frame-driven talk/idle/react loops when using this asset set.
- Keep Chatterbox `natural-storyteller-v1` for UrFavXBF and `pix-cute-female-emily-v1` for PIX. Glitch effects should decorate/react, not overwhelm character readability or captions.


- After watching the Ghost Town pilot, the owner requested **more expressive character animation first**: independent reactions, idle/head/ear/tail/body movement where real rig layers exist, speaker-aware cues and accurate voice attribution.
- Next implement **animated data/caption fusion**, tying verified stats and emphasized captions to the same final WAV word timestamps. Avoid disconnected subtitles and floating fact cards.
- Consult `docs/CHARACTER_ANIMATION_V2.md` and use `src/characters/CharacterPuppet.tsx` plus `scripts/extract_voice_envelope.py` when the matching approved assets are available.
- The existing repo has Remotion and FX, but no genuine rigged 3D character assets nor installed `@remotion/three` engine. Do not describe 2.5D transforms as volumetric 3D or claim phoneme-accurate mouth animation from a single transparent PNG.

#### Format, motion graphics, character animation, and voice QA — mandatory

- **Default output for new original episodes is long-form 16:9 widescreen (1920 × 1080 at 30 fps), not 9:16.** Runtime comes from a complete script/chapters and is confirmed for each video; preserve existing portrait demos but don't copy their framing for new work.
- Outline a sustained narrative with chapter boundaries, multi-scene character exchanges, visual breathing room and long-form audio continuity; do not stretch a Shorts template.

- Apply `docs/PRODUCTION_STANDARD.md` as the **acceptance criteria for every new UrFavXBF + PIX video**: cinematic advanced motion design, appropriate selections from all **21 available effects** in `src/fx/`, character-specific animation/reactions and accurate audio-to-caption-to-animation timing.
- The 21 entries in `src/fx/` are motion-effect implementations, **not 21 separate agent skills**; CineForge Pro consolidates the custom editing skill plus 12 official Remotion skills. Use both the effect library and relevant agent guidance.
- For the first **long-form 16:9 episode**, use **“Is the Internet Becoming a Ghost Town?”**, English dialogue, chaptered storytelling, detailed interactive internet/AI graphics and grounded fact-checking of bot traffic claims; do not confuse bot traffic with human accounts. **Do not use the obsolete 40–50-second Short duration.**
- Before rendering, **verify both PNGs are staged** and generate separate lines for each voice via `scripts/character_voiceover.py`. Validate the speaker-to-WAV mapping, voice pronunciation, actual word alignment and reactive animation; never claim real lip sync from still PNGs without a mouth rig/sprites.
- Preview and verify the final MP4 with real audio and visual QA; polish is not satisfied by passing unit tests alone.

#### Production language policy

- For **all new original productions**, use **English only** for scripts, narration, on-screen graphics, captions, YouTube titles, descriptions, and SEO metadata. The approved default narration is Chatterbox Multilingual V3's `natural-storyteller-v1` English voice. Never describe voice synthesis as a complete rendered video.
- Existing Filipino/Tagalog/Taglish sample compositions are preserved as legacy projects, not templates for the language of new work.
- When the user supplies an existing interview or recording, preserve its authentic speech and quotations. Do not invent English dialogue, silently translate, or redub the source without explicit permission; use English-language footage for an English-only new release, or request a separate editorial decision when the footage conflicts with the policy.
- Check narration intelligibility, voice identity, word-level caption sync, soundtrack balance, output dimensions, and encoded MP4 audio/video before describing a production as delivered.

#### Tools
- FFmpeg: transcode, trim, audio mix, silence/noise processing, final encoding.
- Remotion: reuse the existing project's effects; its edit list is src/edit/edit.json.
- Official Remotion Agent Skills: consult `.claude/skills/remotion-best-practices/SKILL.md` for routing; `remotion-markup` for animation/composition rules, `remotion-captions` for word-timed subtitles, `remotion-render` for export, and `remotion-studio` for preview. The official skills are reference guidance; follow this project skill's user-specific editing and delivery requirements.
- HyperFrames: separate HTML/CSS/JS motion-graphics renderer. Use the official /hyperframes skill (installed through its CLI) and build in a separate project. Do not put HyperFrames code into the Remotion composition.
- Groq Whisper: optional cloud transcription for Tagalog, Taglish and English. The script scripts/groq_transcribe.py generates word-timed JSON, TXT and SRT; require GROQ_API_KEY and user authorization to send audio to an external service. Never translate speech without asking. Do not assume Tagalog/Taglish transcription is perfect.
- Claude.ai on Android and GitHub Codespaces are different execution environments. A Skill alone does NOT connect them.

#### Workflow
1. Confirm input media actually exists, probe metadata with ffprobe and inspect the footage before editing. Do not claim to have watched inaccessible media.
2. If authorized and Groq key available, transcribe with python scripts/groq_transcribe.py input/myclip.mp4. For mixed Taglish, omit --language; for pure Tagalog, --language tl is optional. Proofread names and slang.
3. Identify the story hook, useful quotes, punchlines and natural pacing; avoid meaning-changing edits. Plan cuts and effects to the frame.
4. Design readable, kinetic captions that match each spoken word, safe margins and accessible contrast. Use zooms/callouts only when narrative value is clear. Reserve HyperFrames for custom graphic sequences.
5. Preview and check timing, faces, cutouts, fonts, sound levels, captions and missing media. Render through an available engine. Verify the output via ffprobe.
6. Deliver the actual MP4, edit file and SRT only if those files were produced. Otherwise provide executable commands and be clear about the boundary.

#### Codespaces tools setup
From the repo root, after the scripts have landed in the workspace:

    bash scripts/setup-ai-video-tools.sh

For Groq, store GROQ_API_KEY in GitHub Codespaces secrets; do not commit it or paste it into a public conversation. Restart Codespaces to load it.

To start an independent HyperFrames project:

    mkdir -p hyperframes-projects
    cd hyperframes-projects
    npx hyperframes init my-motion-clip

Never assume that running this Skill from the Claude mobile app executes those commands in GitHub Codespaces.

---

## Module 02: remotion-best-practices

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/SKILL.md

#### Preserve user changes

Users may make edits in the code outside of the conversation.

If you detect a surprising change made in the meanwhile, don't overwrite it, assume it was intentional or ask for confirmation.

#### Creating a video

If the user asks to make, create, or build a new video or composition, load [Create a new Remotion video](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-create/REFERENCE.md), whether or not a Remotion project already exists.

#### New project setup

If no Remotion project currently exists, load [Create a new Remotion project](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-create/REFERENCE.md)

#### React Markup Best Practices

If you are writing Remotion React Markup, load [Remotion Markup Best Practices](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-markup/REFERENCE.md)

#### Maps

For static maps, animated routes and markers, geographic explainers, Mapbox, MapLibre, MapTiler, GeoJSON, or 3D geographic flyovers, load [Remotion Maps](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-maps/REFERENCE.md).

#### Multimedia

For achieving multimedia tasks in the browser, such as trimming, cropping videos, or getting metadata from them, load [Remotion Multimedia](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-multimedia/REFERENCE.md)

#### Improving Interactivity

By structuring the Remotion markup well, we can allow users to interactively change things in the Studio and write back to code. If relevant: [Interactivity Best Practices](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-interactivity/REFERENCE.md)

#### Open the preview

If the user asks to "make" a video, "create" a video, etc.
Don't render the video by default unless they are very explicit. They want to instead see an interactive preview.
As soon as the project can run, start Studio and open the preview in the browser before building or editing the composition. Keep it open while you work so the user can watch progress and steer.

##### If you are using Cursor

Run Studio without `--no-open` so it opens the browser automatically:

```bash
npx remotion studio
```

##### If you are using another agent client with an in-app browser

You can use the command above to let Studio open the browser, or run:

```bash
npx remotion studio --no-open
```

This will start a long-running process and print the server URL for the preview.  
If the server is already started, it will print the URL.
If you use `--no-open`, open the exact printed URL in the in-app browser and verify that Studio loads. Once a composition exists, verify that its video preview loads. If you cannot open it there, run Studio without `--no-open`.
You can visit a specific composition by navigating to `/[composition-id]`, for example `http://localhost:3000/MapAnimation`.

:::note
The Studio supports WebMCP tools.
:::

##### If you do not have an in-app browser

This will open the Studio in the browser or refocus it if it is already open.

```bash
npx remotion studio
```

##### More options

To launch a project in Remotion Studio, open its exact local URL, or configure Studio CLI flags, load [Remotion Studio](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-studio/REFERENCE.md).

#### Render the video

Only render if the user is very explicit in asking for it.  
E.g. "Render the video", "Export", "Give me the MP4".

The preview also has a more intuitive rendering interface, so consider using it instead of the command line for rendering.

```
npx remotion render
```

For more options, see [Rendering](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-render/REFERENCE.md).

For advanced rendering beyond simple `npx remotion render`, see: [Rendering Best Practices](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-render/REFERENCE.md)

#### Captions

When working with Captions, load [Remotion Captions](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-captions/REFERENCE.md).

#### Creating a SaaS, automation or application

Use the [Remotion SaaS skill](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-saas/REFERENCE.md) for knowledge about Remotion-powered SaaS apps, such as `<Player>`, rendering on Lambda, Vercel, Cloudflare, via Express.js, client-side rendering, or for finding the right SaaS template.

#### Looking up Remotion APIs and documentation

To find and read current Remotion documentation, load [Remotion Docs](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-docs/REFERENCE.md).

#### Upgrading

To upgrade Remotion, related packages, compatible Mediabunny packages, and installed Remotion Agent Skills, load [Remotion Upgrade](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-best-practices/remotion-upgrade/REFERENCE.md).

---

## Module 03: remotion-create

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-create/SKILL.md

These are instructions for making a new Remotion project and composition.  
If this is not the next task, see Remotion Best Practices

#### Scaffold a project

If a project already exists, skip this.
Ensure Node.js and Git is installed, and the current folder is appropriate for starting a new project.

Inspect the current folder, including hidden files, before choosing where to scaffold.

##### Empty folder

If it is empty, or contains only disposable operating-system metadata such as `.DS_Store`, create the project directly in the current folder.
Remove only those disposable metadata files first, since `create-video` rejects non-empty folders.
Do not treat all hidden files as disposable: files such as `.env` and directories such as `.git` are meaningful contents.

Scaffold in existing folder:

```bash
npx create-video@latest --yes --blank --no-tailwind .
npm i
```

##### Non-empty folder

If the current folder contains meaningful contents and no project already exists, scaffold into a new subfolder.
Replace `my-video` with a suitable project name.

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
cd my-video
npm i
```

#### Open the preview before building the video

As soon as the project can run, open Remotion Studio in the browser before writing or changing the composition. For a new project, do this immediately after scaffolding and installing dependencies. For an existing project, do it before editing the video. Keep Studio running while you work so the user can see changes as they appear and steer the result.

#### Designing a video

Keep the scaffold and add React Markup.
Follow Remotion React Markup Best Practices and [Video Layout Rules](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-create/video-layout.md) for video-first layout and text sizing guidance.

Before writing the root that registers `<Composition>` or `<Still>` elements,
follow Compositions and stills.

#### Is this a timeline of clips?

If the video arranges multiple video or audio clips on a timeline, follow
Video editing before writing the
timeline. Give every clip that should be edited independently its own authored
JSX node.

#### Is this a multi-scene video?

If this is a video with multiple subsequent scenes, follow guidance at Multi-scene videos.

#### Interactivity Best Practices

By structuring the React Markup following Remotion Interactivity Best Practices, you allow the user to make edits in the Studio which write back to code.

#### TailwindCSS

If Tailwind is requested, see [tailwind.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-create/tailwind.md) for using TailwindCSS in Remotion.

#### Follow-up

The video creation process has finished.
For follow-up prompts, use Remotion Best Practices

---

## Module 04: remotion-markup

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/SKILL.md

This is guidance for writing Remotion React Markup.
If this is not relevant, load Remotion Best Practices instead.

#### Preserve user changes

Users may make edits in the code outside of the conversation.

If you detect a surprising change made in the meanwhile, don't overwrite it, assume it was intentional or ask for confirmation.

#### General rules

Keep `useCurrentFrame()` in the smallest component that needs it. Extract
frame-dependent audio volume, titles, and overlays into their own components
instead of subscribing the whole composition or scene; otherwise unrelated
descendants re-render on every frame. Preserve the existing frame coordinates
when extracting across timing boundaries, and keep editable interpolations
inline on the item's props.

Inside a composition or scene component, get `fps` from `useVideoConfig()` for
all seconds-to-frames calculations, including timing props such as `from`,
`trimBefore` and `durationInFrames`. Keeping the expression on
the JSX node, such as `trimBefore={4 * fps}`, lets Studio edit the timing and
keeps it correct if the composition frame rate changes.

Drive animations using `useCurrentFrame()` and `interpolate()`.  
CSS `transition` or `animation` will not render correctly, they need to refactored.  
Tailwind animation class will not render correctly, they need to be refactored.

Use `Easing.bezier()` and `Easing.spring()` to customize timing.

Before choosing the markup hierarchy, read
editable timeline structure.
Choose editing units first, then the tracks or shared timing boundaries they
need. It includes a complete example with interactive components and their
registrations. For source-editable styles, schemas, and keyframes, see
Remotion Interactivity.

```tsx
import { useCurrentFrame, useVideoConfig, Easing, interpolate, Interactive } from "remotion";

export const FadeIn = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <Interactive.Div
      name="Title"
      style={{
        opacity: interpolate(frame, [0, 2 * fps], [0, 1], {
          extrapolateRight: "clamp",
          extrapolateLeft: "clamp",
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        }),
      }}
    >
      Hello World!
    </Interactive.Div>
  );
};
```

Keep the `interpolate()` call inline in the `style` prop.
Use `scale`, `translate`, `rotate` CSS properties over `transform`.

```tsx
// 👍 Inline editable keyframes and transform shorthands
style={{
  scale: interpolate(frame, [0, 100], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
    output: 'perceptual-scale' // For `scale` animations, use "output: 'perceptual-scale'"
  }),
  translate: interpolate(frame, [0, 100], ["0px 0px", "100px 100px"], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
  }),
  rotate: interpolate(frame, [0, 100], ["20deg", "90deg"], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.spring({damping: 200}),
  }),
}}

// 👎 Non-inline values and transform strings become harder to edit in Studio
const scale = interpolate(frame, [0, 100], [0, 1]);

style={{
  transform: `scale(${scale})`,
}}
```

#### Assets

Place assets in the `public/` folder at your project root.
Use `staticFile()` to reference files from the `public/` folder.

#### Media components

Add video and audio using `<Video>` and `<Audio>` from `@remotion/media`.  
Add images using the `<CanvasImage>` component.
Add animated GIFs, APNG, WebP or AVIF images using `<AnimatedImage>`, use `@remotion/gif` if not using Chrome.
Use `staticFile()` for files in `public/` or pass a remote URL directly:

```tsx
import { Audio, Video } from "@remotion/media";
import { staticFile, CanvasImage, AnimatedImage } from "remotion";

export const MyComposition = () => {
  return (
    <>
      <Video src={staticFile("video.mp4")} style={{ opacity: 0.5 }} />
      <Audio src={staticFile("audio.mp3")} />
      <CanvasImage
        src={staticFile("logo.png")}
        style={{ width: 100, height: 100 }}
      />
      <Video src="https://remotion.media/video.mp4" />
      <AnimatedImage src={staticFile('nyancat.gif')} />
    </>
  );
};
```

If the composition is primarily a timeline of video or audio clips, read
[video-editing.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/video-editing.md) before choosing its source structure.

#### Delaying, trimming

Use [sequencing](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/sequencing.md) to choose the timing boundary and
[timing props](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/timing-props.md) for the supported props and order of operations.

#### Maps

See [Remotion Maps](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/remotion-maps/REFERENCE.md) if wanting to include maps in the video.

#### Text highlights and annotations

See [text-highlights.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/text-highlights.md) for text highlights (highlight markers), circles, underlines, strike-throughs, crossed-off text, boxes.

#### Multi-scene videos

See [multi-scene-video.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/multi-scene-video.md) if planning to make a video with multiple subsequent scenes.

#### Connected compositions

Read [connected compositions](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/connected-compositions.md) when a scene or group
needs its own editable timeline, or when handling a Studio pre-compose request.
It covers extraction, registration, inherited styles, and verification in both
the parent and standalone views.

#### Voiceover

See [voiceover.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/voiceover.md) for adding an AI-generated voiceover to Remotion compositions using ElevenLabs TTS.

#### Embedding Videos

See [embedding-videos.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/embedding-videos.md) for advanced knowledge about embedding videos - trimming, volume, speed, looping, pitch.

#### Embedding Audio

See [audio.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/audio.md) for advanced audio features like trimming, volume, speed, pitch.

#### Cropping

See [cropping.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/cropping.md) if needing to crop the visible rectangle of a component.

#### Transitions

See [transitions.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/transitions.md) for scene transition patterns.

#### Motion blur

When adding motion blur or a movement trail, read [motion-blur.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/motion-blur.md) for the preferred HTML-in-canvas approach, preview requirements, and alternatives.

#### Visual and pixel effects

When adding a visual effect, first identify the element or group it should affect.
If the target component supports `effects` and a built-in effect below matches the
request, prefer that effect over a CSS approximation. For example, apply
`vignette()` directly to a `<Video>`'s `effects` prop when the vignette should
affect that video.

These components accept `effects` directly:

| Import from        | Components                                                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `remotion`         | `<Img>`, `<CanvasImage>`, `<AnimatedImage>`, `<Solid>`, `<HtmlInCanvas>`                                                      |
| `@remotion/media`  | `<Video>`                                                                                                                     |
| `@remotion/gif`    | `<Gif>`                                                                                                                       |
| `@remotion/rive`   | `<RemotionRiveCanvas>`                                                                                                        |
| `@remotion/shapes` | `<Arrow>`, `<Callout>`, `<Circle>`, `<Ellipse>`, `<Heart>`, `<Pie>`, `<Polygon>`, `<Rect>`, `<Spark>`, `<Star>`, `<Triangle>` |

Ordinary HTML elements, `<Interactive.*>` DOM wrappers, `<AbsoluteFill>`, and
`<Sequence>` do not accept `effects` directly. To apply effects to their content,
wrap them in `<HtmlInCanvas>` and put the `effects` prop on the wrapper.

For other elements, prefer regular HTML and CSS where suitable. Consider wrapping
a group in [`<HtmlInCanvas>`](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/html-in-canvas.md) when post-processing the whole
group is appropriate and the environment supports it.

Read [effects.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/effects.md) before applying an effect for imports, parameters,
and setup. It also covers reusable custom effects with `createEffect()` when no
built-in effect matches.

##### Available effects

Built-in effects from `@remotion/effects`:

- Color and tone: `brightness()`, `colorCorrection()`, `colorKey()`, `contrast()`, `curves()`, `duotone()`, `exposure()`, `grayscale()`, `hue()`, `invert()`, `levels()`, `linearGradient()`, `linearGradientTint()`, `lut()`, `saturation()`, `shadowsHighlights()`, `thermalVision()`, `tint()`, `vibrance()`, `whiteBalance()`.
- Blur and trails: `blur()`, `lightTrail()`, `linearProgressiveBlur()`, `radialProgressiveBlur()`, `regionBlur()`, `zoomBlur()`.
- Lighting: `dropShadow()`, `longShadows()`, `glow()`, `lightLeak()`, `shine()`, `starburst()`, `vignette()`.
- Distortion and transforms: `barrelDistortion()`, `chromaticAberration()`, `cornerPin()`, `fisheye()`, `mirror()`, `noiseDisplacement()`, `scale()`, `skew()`, `tile()`, `uvTranslate()`, `wave()`, `xyTranslate()`.
- Textures and patterns: `burlap()`, `checkerboard()`, `contourLines()`, `dotGrid()`, `emboss()`, `flannel()`, `gridlines()`, `halftone()`, `halftoneLinearGradient()`, `lines()`, `liquidContours()`, `noise()`, `paper()`, `pattern()`, `rings()`, `scanlines()`, `speckle()`, `tvSignalOff()`, `waves()`, `whiteNoise()`, `zigzag()`.
- Edges: `outline()`, `roughenEdges()`, `shrinkwrap()`, `tear()`.
- Pixelation and transitions: `evolve()`, `linearProgressivePixelate()`, `pixelate()`, `pixelDissolve()`, `radialProgressivePixelate()`, `venetianBlinds()`.

#### Color correction

Read [color-correction.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/color-correction.md) for primary adjustments with
`colorCorrection()`, tonal mapping with `levels()` or `curves()`, their Studio
editors, and 3D `.cube` color grades with `lut()`.

#### 3D content

See [./3d.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/3d.md) for 3D content in Remotion using Three.js and React Three Fiber.

#### Sound effects

When needing to use sound effects, load the [./sfx.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/sfx.md) file for more information.

#### Audio visualization

When needing to visualize audio (spectrum bars, waveforms, bass-reactive effects), load the [./audio-visualization.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/audio-visualization.md) file for more information.

#### Maps

For static maps, animated routes and markers, geographic explainers, Mapbox, MapLibre, MapTiler, GeoJSON, or 3D geographic flyovers, load [Remotion Maps](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/remotion-maps/REFERENCE.md).

#### Captions

When dealing with captions or subtitles, load the Remotion Captions skill for more information.

#### Arabic and right-to-left text

For Arabic, Persian, Urdu or Hebrew text, read [arabic-text.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/arabic-text.md): set the base direction, animate by word, and split letters only in a way that keeps them joined.

#### Google Fonts

Is the recommended way to load fonts in Remotion. See [google-fonts.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/google-fonts.md) for how to load Google Fonts.

#### Local fonts

See [local-fonts.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/local-fonts.md) for how to load local fonts.

#### GIFs

See [gifs.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/gifs.md) for how to display GIFs synchronized with Remotion's timeline.

#### Advanced Images

See [images.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/images.md) for sizing and positioning images, dynamic image paths, and getting image dimensions.

#### Lottie animations

See [lottie.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/lottie.md) for embedding Lottie animations in Remotion.

#### Timing

See [timing.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/timing.md) for more timing techniques for `interpolate()`.

#### Parameterized videos

See [parameters.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/parameters.md) for making a composition parametrizable by adding a Zod schema.

#### Measuring DOM nodes

See [measuring-dom-nodes.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/measuring-dom-nodes.md) for measuring DOM element dimensions in Remotion.

#### Measuring text

See [measuring-text.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/measuring-text.md) for measuring text dimensions, fitting text to containers, and checking overflow.

#### Using FFmpeg

For some video operations, such as trimming videos or detecting silence, FFmpeg should be used. Load the [./ffmpeg.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/ffmpeg.md) file for more information.

#### Silence detection

When needing to detect and trim silent segments from video or audio files, load the [./silence-detection.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/silence-detection.md) file.

#### Dynamic duration, dimensions and data

See [calculate-metadata.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/calculate-metadata.md) for dynamically set composition duration, dimensions, and props.

#### Compositions and stills

Before registering `<Composition>` or `<Still>` elements, read [compositions.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/compositions.md) for source-editable registrations, folders, default props and nesting. For Studio navigation into a scene's own timeline, use [connected compositions](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/connected-compositions.md).

#### Advanced sequencing

See [sequencing.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-markup/sequencing.md) for more sequencing patterns - delay, trim, limit duration of items.

#### Install modules

Use `npx remotion add` to add new packages with the right version:

```
npx remotion add @remotion/media
```

This goes for `@remotion/*` packages, `mediabunny`, `@mediabunny/*`, `zod`, and `@huggingface/transformers`.

#### Visual checks

Open the Remotion Studio to check visual changes.
When changing timeline structure, inspect the full composition as well as any
connected components; verify the visible layers, cut timing, and synchronized
content.

You can also use Rendering to inspect one or several frames as images.

---

## Module 05: remotion-captions

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-captions/SKILL.md

All captions must be processed in JSON. The captions must use the [`Caption`](https://www.remotion.dev/docs/captions/caption.md) type which is the following:

```ts
import type { Caption } from "@remotion/captions";
```

This is the definition:

```ts
type Caption = {
  text: string;
  startMs: number;
  endMs: number;
  timestampMs: number | null;
  confidence: number | null;
  pageBreakAfter?: boolean;
};
```

#### Generating captions

To transcribe video and audio files to generate captions, load the [transcribe-captions.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-captions/transcribe-captions.md) file for more instructions.

#### Displaying captions

To display captions in your video, load the [display-captions.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-captions/display-captions.md) file for more instructions.

#### Importing captions

To import captions from a .srt file, load the [import-srt-captions.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-captions/import-srt-captions.md) file for more instructions.

#### Post-creation

After you're done, load this skill: Remotion Best Practices

If not alreay done, open the Remotion Studio, unless instructed otherwise.

---

## Module 06: remotion-studio

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-studio/SKILL.md

When creating or editing a video, start Studio and open its preview as soon as the project can run, before building the composition. Keep it open while you work so the user can see changes and steer.

In Cursor, run Studio without `--no-open` so the browser opens automatically:

```bash
npx remotion studio
```

In other agent clients, you can also let Studio open the browser automatically with the command above. If you have an in-app browser and intend to use it, run:

```bash
npx remotion studio --no-open
```

If the Studio is already opened, the URL will be printed and the command will exit.
Otherwise, a long-running process will start, and the URL will be printed.

When using `--no-open`, open the exact printed URL in the in-app browser and verify that Studio loads. Once a composition exists, verify that its video preview loads. Do not use `--no-open` if you cannot open the URL in the in-app browser.

#### Useful flags

| Argument          | Purpose                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------- |
| `--log=<level>`   | Set `error`, `warn`, `info` (default), or `verbose` logging.                                  |
| `--port=<number>` | Request a Studio server port; otherwise Remotion finds a free port.                           |
| `--force-new`     | Start another Studio instance even when one is already running for the same project and port. |

---

## Module 07: remotion-render

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-render/SKILL.md

#### General rendering strategy

Render a video using:

```
npx remotion render
```

Full list of options: https://www.remotion.dev/docs/cli/render.md

Render a still using:

```
npx remotion still
```

Full list of options: https://www.remotion.dev/docs/cli/still.md

To render several frames as images in one call, use `render --frames`:

```
npx remotion render [composition-id] out/frames --frames=0,30,90 --image-format=png
```

See https://www.remotion.dev/docs/cli/render.md#--frames for more options.

#### Transparent videos

See [Transparent videos](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-render/transparent-videos.md) for rendering out a video with transparency.

---

## Module 08: remotion-interactivity

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-interactivity/SKILL.md

Studio edits the JSX nodes that create timeline items. Structure the code around
what the user should be able to select, move, trim, or style independently.
Keep editable values inline on each instance.

Before writing a scene or refactoring its layers, read
[editable timeline structure](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-interactivity/timeline-structure.md). It covers editing units,
tracks, shared timing, plain layout containers, and a complete component-to-root
example. For a timeline built from footage, also read
editable video timelines.

Use connected compositions when
a scene or reusable group needs its own timeline. Validate both its standalone
view and the full parent timeline; a connection alone does not guarantee fewer
visible rows.

#### Choose schema fields

Each key in the schema is a prop that Studio can read and edit at the call site.
Props that are not in the schema still work, but are not editable in Studio.
Keys may use dot notation, such as `style.color`.

| Type                                                                         | Use for                                                      | Keyframable   |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------- |
| `string`                                                                     | Strings, such as a title, prompt, or code snippet            | No            |
| `number`                                                                     | Numbers, with optional `min`, `max`, `step`, `integer`       | Yes           |
| `boolean`                                                                    | On/off switches                                              | Yes (hold)    |
| `color`                                                                      | CSS color strings                                            | Yes           |
| `enum`                                                                       | A choice between `variants`, each with its own nested schema | Opt-in (hold) |
| `array`                                                                      | Lists of numbers, colors, enums and more                     | No            |
| `asset`                                                                      | Media sources, with optional `assetType`                     | No            |
| `font-family`                                                                | CSS font family                                              | No            |
| `font-weight`                                                                | Font weight                                                  | Yes           |
| `translate`, `scale`, `rotation-css`, `rotation-degrees`, `transform-origin` | Transforms                                                   | Yes           |
| `uv-coordinate`                                                              | A normalized `[x, y]` point on the element                   | Yes           |
| `svg-path`                                                                   | SVG path data                                                | Yes           |
| `remotion-captions`                                                          | `Caption[]` data                                             | No            |
| `hidden`                                                                     | A value kept out of the controls                             | —             |

Every field needs a `default` and should have a `description`, which Studio shows as the label.
Set `keyframable: false` to show a static control.

Expose content and per-instance appearance, such as the text and an accent color.
Do not add fields for `style.translate`, `style.scale`, `style.rotate`, `style.transformOrigin` and `style.opacity`: `Interactive.create()` adds them automatically.

To make CSS properties of the root editable per instance, spread the built-in schema fragments:

```tsx
const cardSchema = {
  ...Interactive.textSchema, // style.color, style.fontSize, style.fontWeight, ...
  ...Interactive.backgroundSchema, // style.backgroundColor
  ...Interactive.borderRadiusSchema, // style.borderRadius, ...
} as const satisfies InteractivitySchema;
```

Also available: `Interactive.borderSchema`, and `Interactive.captionsSchema` for components that accept captions.
For components that accept `React.ReactNode` children, add `...Interactive.childrenSchema`.
It provides controls for children content and may evolve to support richer content.
Currently, it uses a string field labeled "Text" with a default of `''`.
If a component requires string-only children, declare an explicit `children` field with `type: 'string'` instead.
`Interactive.textSchema` controls typography styles; `childrenSchema` controls content.
The children fragment is not included in `baseSchema` or automatically added to custom components.
Nested markup and computed children are currently read-only.
`text-content` is a deprecated alias for the `string` field type.
See [`InteractivitySchema`](https://www.remotion.dev/docs/interactivity-schema) for all options.

#### Make an HTML element interactive using `Interactive`

Every HTML and SVG element (except `<Img>`, it already is interactive) such as `<div>` can be turned interactive using `Interactive`:

```tsx title="Interactive elements"
<Interactive.Div
  name="Greeting card"
  style={{fontSize: 80, padding: 24}}
>
  Hello
</Interactive.Div>
```

Use this for text or graphics that need independent controls. Keep layout-only
containers and decorative internals as plain HTML; an interactive component
already provides controls for its root.

#### Prefer inline text

If text is fixed and only used once, write it directly inside the interactive element instead of extracting it into a constant.

```tsx title="Inline text"
// 👍 Fixed copy stays editable
<Interactive.Div name="Title">
  Remotion Best Practices
</Interactive.Div>
```

Use a prop or variable only when the text is dynamic or reused.

#### Give interactive elements a descriptive name

Add a `name` prop to elements to make them easily identifyable.
Avoid computed names, hardcode them.

```tsx title="Interactive names"
<>
  <Interactive.Div name="Hero title" style={{fontSize: 80}}>
    Launch day
  </Interactive.Div>
  <Img name="Avatar" src="https://remotion.media/image.jpeg" />
  <Video name="Background" src="https://remotion.media/video.mp4" />
  <Interactive.Div name="Title">
    Launch day
  </Interactive.Div>
</>
```

#### Keep all CSS styles inline

The best way is to just pass a plain object to `style` - no referring to constants, no object spreading, no math.

```tsx title="Interactive example"
<Interactive.Div
  style={{
    fontSize: 80,
    color: 'red',
  }}
>
  Hello World!
</Interactive.Div>
```

```tsx title="❌ Bad for interactivity"
const baseStyle = useMemo(() => {
  return {
    fontSize: 12 // ❌ Non-inline styles are not supported
  }
}, []);

<Interactive.Div
  style={{
    ...baseStyle, // ❌ Spreading is not supported
    color: RED, // ❌ Referring to constants is not supported
    scale: frame * 10 // ❌ Math is not supported
  }}
>
  Hello World!
</Interactive.Div>
```

#### Animate using `interpolate()`

Write animations as inline `interpolate()` calls on the property that changes.  
The output range, easing, extrapolation and `output` property should use hardcoded values.

The input range may additionally use `durationInFrames`, `fps`, `width` and `height` destructured directly from `useVideoConfig()`. Bare identifiers such as `durationInFrames`, multiplication with a number such as `2 * fps` or `fps * 2`, and subtraction of a number such as `durationInFrames - 1` are supported.

```tsx title="Inline values"
const {fps, durationInFrames} = useVideoConfig();

// 👍 Inline values can be standardized and keyframed
<Interactive.Div
  name="Product card"
  style={{
    color: 'white',
    fontSize: 80,
    scale: interpolate(frame, [0, fps], [0, 1], {
      easing: Easing.spring({damping: 200}),
      output: 'perceptual-scale',
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp'
    }),
    rotate: interpolate(frame, [0, 1 * fps], ['0deg', '20deg'], {
      easing: Easing.spring({damping: 200}),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp'
    }),
    translate: interpolate(
      frame,
      [durationInFrames - 30, durationInFrames],
      ['0px 0px', '0px 120px'],
      {
        easing: Easing.spring({damping: 200}),
        output: 'perceptual-scale',
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp'
      }
    ),
  }}
/>
```

```tsx title="❌ Bad interactivity"
const translateY = interpolate(frame, [0, 30], [0, 120]); // ❌ Math should be directly in the markup

<Interactive.Div
  name="Product card"
  style={{
    translate: translateY, // ❌ Only inline interpolate() calls are supported,
    rotate: interpolate(frame, [start, start + 10], [0, Math.PI]), // ❌ Cannot use math with arbitrary variables, cannot use constants
    scale: interpolate(anyVariable, [0, 30], [0, 1]) // ❌ Can only interpret the `frame` variable.
  }}
/>
```

#### Keep SVG paths editable with `Interactive.Path`

Use `<Interactive.Path>` from `remotion` instead of `<path>` inside an SVG to make the path visually editable.

Install `@remotion/paths` for path interpolation and Studio path keyframes:

```sh
bunx remotion add @remotion/paths
```

If the geometry is meant to be static, put the path string directly in the `d` prop. Do not extract it into a constant.

```tsx title="Editable static path"
import {Interactive} from 'remotion';

<Interactive.Svg width={300} height={300} viewBox="0 0 300 300">
  <Interactive.Path
    name="Triangle"
    d="M 40 40 L 260 40 L 150 260 Z"
    fill="#0b84f3"
  />
</Interactive.Svg>
```

##### Morph paths using inline `interpolatePaths()`

Use `interpolatePaths()` from `@remotion/paths` directly in `d`.  
It accepts a frame, an input range, an equally sized array of path strings, and options for easing, extrapolation, and posterization.
Keep the output paths, ranges, and options inline, following the same input-range rules as `interpolate()` above.  
Do not use `interpolatePath()` API or extract the interpolated result into a variable when the path keyframes should remain editable in Studio.

```tsx title="Editable path keyframes"
import {interpolatePaths} from '@remotion/paths';
import {Easing, Interactive, useCurrentFrame} from 'remotion';

export const MorphingPath = () => {
  const frame = useCurrentFrame();

  return (
    <Interactive.Svg width={300} height={300} viewBox="0 0 300 300">
      <Interactive.Path
        name="Morphing triangle"
        d={interpolatePaths(
          frame,
          [0, 30, 60],
          [
            'M 40 40 L 260 40 L 150 260 Z',
            'M 40 150 L 150 40 L 260 150 Z',
            'M 40 260 L 150 40 L 260 260 Z',
          ],
          {
            easing: Easing.bezier(0.42, 0, 0.58, 1),
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          },
        )}
        fill="#0b84f3"
      />
    </Interactive.Svg>
  );
};
```

Studio can edit the path at the current frame, add or move keyframes, and adjust their easing.  
Use `strokeDasharray` and `strokeDashoffset` to evolve paths.

#### Use `scale`, `translate`, `rotate` CSS properties

Avoid the `transform` CSS property.  
If possible, use `scale`, `rotate` and `translate` instead because only they are interactively editable.

#### Keep composition metadata inline

When scaffolding a composition, use a JSX string literal for `id`, keep `width`, `height`, `fps`, `durationInFrames` and `defaultProps` inline and make no type assertions.

The Props editor can save visual edits back to your code when `defaultProps` is an inline object literal on `<Composition>` or `<Still>`.

```tsx
// 👍 Static values are in <Composition>, dynamic values are in calculateMetadata()
const calculateMetadata = useMemo(async () => {
  const dimensions = await getDimensions(); // just an example
  return {width: dimensions.width, height: dimensions.height};
});

<Composition
  id="my-video"
  component={MyComponent}
  durationInFrames={150}
  fps={30}
  calculateMetadata={calculateMetadata}
  defaultProps={{title: 'Hello', color: '#0b84ff'}}
/>
```

```tsx title="Negative examples"
const defaultProps = {title: 'Hello', color: '#0b84ff'}; // ❌ Don't extract defaultProps, must be inline
const calculateMetadata = useMemo(() => {
  // ❌ Unnecessary because no calculation is being done,
  return {durationInFrames: 150, fps: 30, width: 1920, height: 1080};
});

<Composition
  id="my-video"
  component={MyComponent}
  calculateMetadata={calculateMetadata}
  defaultProps={{
    title: 'Hello',
  } as Props} // ❌ Don't have type assertions, instead type MyComponent correctly
/>
```

Use only `calculateMetadata()` for the part of the metadata that is dynamic.

#### Effects should be inline too

Keep effect arrays and parameters inline so their shape and keyframes remain editable. See [Inline effects](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-interactivity/inline-effects.md) for examples.

#### Making your own component interactive

To make a custom userland component interactive, use:
[Make a component interactive](https://www.remotion.dev/docs/studio/make-component-interactive.md)

#### Video editing

If a Remotion component mainly consists of video and audio clips, see Video editing for best practices on how to structure Remotion markup so the clips are interactively editable in the timeline.

---

## Module 09: remotion-multimedia

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-multimedia/SKILL.md

Mediabunny is a multimedia library for dealing with audio and video in the browser.
Here is a compact overview of its capabilities: https://mediabunny.dev/llms.txt

#### Getting audio duration

See [get-audio-duration.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-multimedia/get-audio-duration.md) for getting the duration of an audio file in seconds with Mediabunny.

#### Getting video dimensions

See [get-video-dimensions.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-multimedia/get-video-dimensions.md) for getting the width and height of a video file with Mediabunny.

#### Getting video duration

See [get-video-duration.md](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-multimedia/get-video-duration.md) for getting the duration of a video file in seconds with Mediabunny.

---

## Module 10: remotion-maps

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-maps/SKILL.md

### Remotion Maps

Choose exactly one technique from the intended shot, then load only that technique's `TECHNIQUE.md`.
Every technique directory is self-contained and may be removed without breaking the others.

#### [Static map](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-maps/techniques/static-map/TECHNIQUE.md)

- Requires you grab a satellite image and mount it in a `<Img>` tag, and animate on top

#### [Mapbox](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-maps/techniques/mapbox/TECHNIQUE.md)

- Requires a Mapbox key
- Nicer styles by default
- Map can display a round globe when zoomed out
- Includes nice 3D buildings such as the Eiffel tower

#### [MapLibre](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-maps/techniques/maplibre/TECHNIQUE.md)

- Requires no API key, fully free
- Does not include 3D building

#### [MapTiler](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-maps/techniques/maptiler/TECHNIQUE.md)

- Uses MapTiler
- Annotations can be drawn on top of geographic features: borders, rivers, labels

#### [CesiumJS](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-maps/techniques/cesium/TECHNIQUE.md)

- Flythroughs through terrain and mountains
- "Flight simulator" perspective

---

## Module 11: remotion-docs

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-docs/SKILL.md

This skill teaches you how to discover and read current Remotion documentation.
If this is not relevant, load Remotion Best Practices instead.

#### Searching the docs

Use the Algolia search API to find relevant documentation pages:

```
POST https://plsduol1ca-dsn.algolia.net/1/indexes/*/queries?x-algolia-api-key=3e42dbd4f895fe93ff5cf40d860c4a85&x-algolia-application-id=PLSDUOL1CA
Content-Type: application/x-www-form-urlencoded

{
  "requests": [
    {
      "query": "<your search query>",
      "indexName": "remotion",
      "params": "attributesToRetrieve=[\"hierarchy.lvl0\",\"hierarchy.lvl1\",\"hierarchy.lvl2\",\"url\"]&hitsPerPage=10"
    }
  ]
}
```

Each hit contains a `url` field pointing to the documentation page.

#### Fetching a page as Markdown

Append `.md` to any Remotion docs URL to retrieve its Markdown source (saves tokens):

```
https://www.remotion.dev/docs/use-video-config.md
https://www.remotion.dev/docs/sequence.md
https://www.remotion.dev/docs/lambda/rendermediaonlambda.md
```

#### Workflow

1. Search Algolia for the concept or API you need.
2. Pick the most relevant URL(s) from the results.
3. Fetch each URL with the `.md` suffix.
4. Implement using the current documentation rather than memorized API knowledge.

---

## Module 12: remotion-upgrade

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-upgrade/SKILL.md

### Upgrade Remotion

1. Inspect the project manifests and lockfile to identify the package manager and workspaces. Preserve unrelated changes.
2. Determine whether `@remotion/cli` is locally available. If it is, run:

   ```bash
   npx remotion upgrade
   ```

   This also updates project-local Remotion skills. Skip the manual upgrade below.

3. If `@remotion/cli` is not available, upgrade manually:
   - Get the latest stable Remotion version with `npm view remotion version`.
   - Find every installed `remotion` and `@remotion/*` dependency across the project and upgrade them all to that exact version. Preserve their dependency sections and the project's workspace or catalog conventions.
   - Read the `@remotion/studio` dependencies for the target Remotion version using `npm view @remotion/studio@<version> dependencies --json`. Align installed auxiliary packages such as `zod`, `mediabunny`, and `@huggingface/transformers` with the versions listed there. Use the `mediabunny` version for installed `@mediabunny/*` packages.
   - Run the project's package manager to update its lockfile.
4. If `@remotion/cli` is not available, update the installed Remotion skills:

   ```bash
   npx skills update remotion-best-practices remotion-captions remotion-create remotion-docs remotion-interactivity remotion-maps remotion-markup remotion-multimedia remotion-render remotion-saas remotion-studio remotion-upgrade --yes
   ```

5. Review the manifest and lockfile diff. Ensure all Remotion packages use one version and installed auxiliary packages use their recommended versions. If the CLI is available, run `npx remotion versions` as an additional check.

The [Remotion releases](https://github.com/remotion-dev/remotion/releases) contain the changelog and may be useful for summarizing relevant changes after the upgrade.

---

## Module 13: remotion-saas

Source: https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-saas/SKILL.md

One can build apps with Remotion.  
It is possible to have a simple form and hook it up to a render, or have a complex video editor.

#### Choosing a template or a framework

We have several templates for SaaS which can be cloned or used as a reference.
See [Choosing a framework](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-saas/framework.md) for help choosing a template or framework.

#### The `<Player>`

This component allows embedding a Remotion preview in a React app. See [Player](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-saas/player.md) for more information about the Player.

#### Rendering

There are client-side and server-side rendering options available. See [Rendering](https://github.com/remotion-dev/skills/blob/30d4553ecd46fbc5212fd0ff006ae43af522158b/skills/remotion-saas/rendering.md) for advice on how to choose, and about the Lambda, Vercel, Node.js and Cloudflare options.

#### With Vue

See https://www.remotion.dev/docs/vue.md for how to use Remotion with Vue.

#### Angular

See https://www.remotion.dev/docs/angular.md for how to use Remotion with Angular.

#### Svelte

See https://www.remotion.dev/docs/svelte.md for how to use Remotion with Svelte.


## Portability and provenance

Official Remotion Agent Skills: https://github.com/remotion-dev/skills
Pinned revision: 30d4553ecd46fbc5212fd0ff006ae43af522158b
Project custom skill: https://github.com/urfavxbf/video-ai-editor
Third-party notices: https://github.com/urfavxbf/video-ai-editor/blob/main/THIRD_PARTY_NOTICES.md

All 13 main SKILL.md contents are embedded here, so no additional Skill
installation is required. Some optional deep-reference materials are linked
to their exact official source version online instead of duplicated. They
are documentation, not separate Skills. Project-local commands require
an actual checkout of the associated project.

Remotion itself is a separately licensed framework. This compiled Skill
does not relicense upstream code or promise an executable runtime.

## Quality and delivery checklist

- Media and required output format actually verified.
- Authentic story beats, accurate language and subtitle timing.
- Effective motion graphics and appropriate audio balance.
- Proper source attribution and licensed assets.
- Actual rendered file checked for audio/video streams and playback.
- Only verified download links presented, never fabricated files.
