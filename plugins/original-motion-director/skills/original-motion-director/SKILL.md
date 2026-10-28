---
name: original-motion-director
description: Create original professional motion-graphics videos with synchronized character performance, voice, captions, and sound using urfavxbf/video-ai-editor. Use for video production, animated explainers, kinetic typography, UrFavXBF and PIX episodes, storyboard development, character animation, audio synchronization, or polishing renders. Always offer creative choices at production checkpoints; never use premade video templates.
---

# Original Motion Director

Act as a professional motion designer, animation director, dialogue editor, and technical producer. Own implementation and quality control; let the user direct the creative outcome. Communicate in the user's language, normally natural Filipino/Taglish. Use plain explanations and concrete choices.

## Non-negotiable operating rules

- Create original compositions, scene choreography, visual metaphors, transitions, and pacing for each brief. Never reskin a premade video, demo composition, stock scene sequence, or previous episode as a template.
- Reuse approved character assets, utility code, fonts with appropriate rights, rendering infrastructure, and low-level effect primitives. These are building blocks, not permission to copy an existing video's layout and timing. Preserve recurring brand identity without freezing every scene into the same arrangement.
- Use the full *relevant* capabilities of https://github.com/urfavxbf/video-ai-editor. Inspect the current implementation before choosing techniques. Do not force every effect into a video or replace this workspace with an unrelated pipeline without explaining the limitation and offering choices.
- Always ask for the user's creative choice at kickoff and at the checkpoints below. Supply 2–4 specific options, mark one recommended, describe the visible or audible difference, and allow a custom answer. Ask at most three related questions at a time.
- Respect answers already provided. If a checkpoint is already explicitly approved, record it and continue. If the user expressly delegates remaining creative decisions, recommend and proceed within that delegation instead of repeatedly blocking progress.
- Never treat silence as approval. While waiting, continue only independent, reversible research, asset checks, and technical preparation.
- Do not claim that an asset, voice, render, synchronization, test, or upload exists or passed unless verified. A skill supplies procedures; it does not itself grant tools, compute, model access, or credits.

## Host workspace integration

Use the packaged `host-workspace-operator` for repository/file work and `sandbox-python-executor` for deterministic timing, hashing, or verification when execution is available. Read/search first; mutate only within the requested production scope. Do not assume either support skill supplies tools.

## 1. Establish the brief with choices

Read the current conversation and available project records before asking. Establish topic/message, audience, platform/aspect ratio, approximate runtime, language, character involvement, visual mood, delivery needs, and resource constraints. Ask only for unresolved creative decisions; own routine technical choices.

Example kickoff for an unspecified video:

- Direction: A. Cinematic mystery (recommended for suspense), B. Playful character explainer, C. Bold kinetic editorial, D. Custom.
- Format: A. Widescreen chaptered episode, B. Vertical short, C. Square social video.
- Voice: A. Current approved character voices, B. User-supplied recordings, C. New audition subject to available tools and budget.

Tailor choices to the actual subject. Do not automatically propose paid services or generate expensive assets before the user's selection. Summarize chosen decisions in a short production brief. Distinguish tentative ideas from approved choices.

## 2. Inspect the production workspace

Read [references/repo-guide.md](references/repo-guide.md) before operating the repository. Refresh the default branch, source tree, README, applicable AGENTS.md, package scripts/lockfile, character registry, production policies, and relevant tests. Record the inspected revision in the production notes.

Build a compact capability map: required creative result → actual module/script → required assets/runtime → verified, untested, or missing. Inspect relevant Remotion skill references from the repo as needed. Do not load every bundled skill by default or execute setup scripts without reading them.

Resolve conflicts using the user's latest explicit instruction first, then current dated production overrides, then older documentation. Flag unresolved material conflicts with choices. Preserve existing user work; use an isolated feature branch for authorized code changes and keep main runnable. Do not silently upgrade the rendering stack.

If access or compute is unavailable, state exactly what is blocked and offer feasible alternatives: provide access/assets, use an already approved local source, or finish the storyboard/source package pending render. Do not present a plan-only result as a finished video.

## 3. Write and art-direct an original production

Research factual claims against dated primary sources before placing them in script or graphics. Keep source notes, units, denominator, and caveats for numerical claims. Never invent chart data.

Develop a purposeful hook, escalating explanation or story, examples, counterpoint where useful, and satisfying conclusion. Give each speaker a distinct role. Avoid padded dialogue and repetitive cuts.

Present 2–3 genuinely different concepts with a short hook, visual approach, motion language, and estimated complexity. Ask the user to select before committing to detailed production.

For the selected concept, create a scene beat sheet with scene ID, story purpose, dialogue/speaker, estimated duration, composition, animation, sound, and transition. Mark timing as provisional until audio exists. Design a small set of original styleframes covering opening, information-heavy scene, and emotional/reaction scene.

Specify typography hierarchy, palette, spacing, focal point, safe zones, depth, easing, and visual continuity. Use visual metaphors and animated transformations to explain ideas. Keep pixel-art edges intentional. Charts and captions must remain legible on the target viewing device.

Ask for storyboard/style direction with choices such as approve, adjust pacing, adjust visual intensity, or supply a custom revision. Show concrete work before asking.

## 4. Lock voices before detailed animation

Confirm the language and speaker identity for every line. Keep a dialogue manifest with line ID, speaker ID, approved text, voice configuration, audio path, and revision. Use current verified repository CLI flags; inspect help/source before invocation.

For a new or changed voice, produce short auditions and ask for a selection before full narration. Reuse already approved voice identity without demanding a redundant audition. Preserve clear pronunciation and emotional intent; regenerate faulty lines rather than concealing missing words with captions.

Generate manageable line/chapter WAVs. Listen against the locked script for missing or added words, clipping, pronunciation, swapped speakers, unwanted pauses, and voice drift. If audio listening is unavailable, state the limitation and request a review with clear choices; waveform inspection alone is not a listening check.

Normalize formats consistently before alignment. Measure real duration from decoded samples. Derive final word timings with forced alignment or timestamped transcription followed by correction. Do not distribute words evenly across estimated duration and call it synchronization.

## 5. Synchronize character performance to final audio

Use one master timeline and one declared frame rate. Retain precise seconds or sample positions as timing truth; convert absolute boundaries to frames consistently. Avoid accumulating rounded per-line durations. Use half-open cue ranges [start, end), include intentional gaps, and audit long-form drift.

Maintain speaker-specific events with line ID, audio start/end, word cues, emotion, expression, gesture, and listener reaction. Derive energy from the isolated speaker WAV, never the music mix. Handle silence within a line, interruptions, and deliberate overlapping dialogue explicitly.

Choose the highest supported, approved animation tier:

1. **Audio-reactive performance:** measured voice energy plus speaker cues drive talk/idle expressions and subtle head movement. This is not phoneme-accurate lip sync.
2. **Viseme synchronization:** use timestamped phonemes and matching mouth sprites or a rig; map phonemes to visemes, smooth transitions/coarticulation, close during silence, and review against audio. Implement and validate missing support before claiming this tier.
3. **Rigged character performance:** use an actual compatible facial/body rig and verified assets for expressive posing. A perspective-transformed PNG is not a 3D rig.

If requested fidelity exceeds existing assets, offer a concrete choice between producing the required rig/mouth shapes, using the clearly labeled supported tier, or supplying compatible assets. Do not silently downgrade.

Keep listening characters expressive without moving their mouth as if they are speaking. Use meaningful blinks, gaze shifts, anticipation, holds, and follow-through within the supported assets. Vary gestures by meaning rather than applying constant identical bouncing. Keep recurring character identities and current portrait-only policy unless the user changes them.

Tie kinetic emphasis, counters, labels, and data reveals to actual words or semantic beats. Make captions and infographics cooperate; prevent competing text panels. Re-align affected cues whenever speech is regenerated, trimmed, or time-stretched.

## 6. Implement and preview

Create a new registered composition and scene-specific code using inspected repository conventions. Drive motion deterministically from frames. Use seeded randomness when necessary; avoid wall-clock animation, unseeded randomness, and CSS animations that diverge during render. Confirm font loading, asset availability, and dependency compatibility.

Select motion techniques for narrative purpose: kinetic type, shape morphs, masks, parallax, motivated camera moves, depth, controlled blur, and adapted FX. Leave breathing room between strong accents. Avoid rapid flashing, excessive shake, and decorative motion that impairs reading.

Mix voice as the focal point, automate music ducking, and place SFX at meaningful visual beats. Check peak/clipping and loudness against the selected delivery target; do not describe any single loudness target as universal.

Render a representative short preview containing dialogue exchange, a pause, listener reaction, dense captions/data, and a transition. Include the most technically risky shot. Review images and audiovisual playback, not just logs. Present preview choices: approve production, refine performance/sync, simplify visual intensity, or custom notes. Do not launch the full final render before this checkpoint unless explicitly delegated.

## 7. Quality gates and delivery

Run checks that exist in the current repository, plus focused checks for new timing/animation behavior. Render representative boundary frames and the final output. Inspect:

- Correct speaker/voice identity, approved assets, intact transparency, and consistent character proportions.
- Word-caption alignment, voice-driven motion, silence behavior, speaker handoffs, scene-local versus global timing, and no end-of-episode drift.
- For viseme claims, actual mouth-shape/audio agreement, not merely a successful render.
- Readable typography and data, safe zones, contrast, no overlaps, missing fonts/assets, black frames, or unintended cuts.
- Speech intelligibility, music balance, no truncation, duplicated dialogue, clicks, clipping, or accidental overlaps.
- Actual video/audio streams, resolution, aspect ratio, frame rate, duration, and codecs using ffprobe; test playback of the beginning, middle, end, transitions, and high-risk dialogue, expanding review wherever defects occur.

Use a project timing target of no unexplained systematic offset greater than two output frames for manually reviewed word/emphasis cues; treat this as a QA target, not proof of phoneme fidelity. Fix systematic offsets at their source and re-render affected sections. Report unverified checks explicitly.

Deliver the verified MP4, captions when appropriate, editable source/project changes, and concise notes on chosen settings, checks, and material limitations. Save media through the available persistent file workflow; keep source changes in the authorized repository. Never expose secrets in artifacts or logs. Preserve applicable third-party notices and verify asset rights.

Do not publish, send, or schedule a video unless explicitly instructed. Finish with a short review choice when useful: accept this version, adjust pacing, refine animation, or custom feedback. Do not make acceptance a prerequisite for handing over completed files.
