> **Latest owner-approved video *direction* (2026-10-29):** Aim for cinematic 2.5D editorial animation: expressive, frame-animated pixel-styled UrFavXBF/PIX characters composited into depth-rich 3D studio/scene environments, with camera moves, powerful synced motion graphics and kinetic typography. This **supersedes portrait-only layout and rejected primitive-3D artwork as the default creative target**, without changing the locked October 29 character identities or English voices. See [reference analysis and QA target](CINEMATIC_2P5D_REFERENCE_2026-10-29.md). Artwork itself still requires owner visual approval.

> **Character layout update:** User approved **head portraits only**, one on either side of the motion-graphics field. Eliminate the full-body character overlays from future videos. Keep animated face sprites and actual Chatterbox speaker attribution. See [PIXEL_GLITCH_PORTRAITS_ONLY.md](PIXEL_GLITCH_PORTRAITS_ONLY.md).

# UrFavXBF + PIX — production quality standard

**Owner direction recorded:** 2026-10-28. This is the default brief for every new original Tagalog/Taglish video (English remains opt-in) featuring UrFavXBF (main host) and PIX (female-voiced AI cat sidekick). AI agents should consult this before creating a screenplay, timeline or rendered video. Keep all visual work original and treat cited creators as technique references, not designs to copy.

## Storytelling & first pilot

- Show **UrFavXBF** and **PIX** as two distinct recurring personalities; the host explains and PIX prompts, reacts, questions or adds humor. Do not replace either speaker with generic narration.
- The agreed **first long-form episode** is **“Is the Internet Becoming a Ghost Town?”**, an English-language widescreen video about bots, real vs automated web activity, AI and internet authenticity. Build a full explanatory story with room for dialogue, visuals, nuance and takeaways; **do not reuse the retired 40–50-second Short outline as the episode duration**. The final runtime is story-driven and is set per production, not hard-coded in this standard. The science niche is **not** the channel identity; UrFavXBF covers wisdom, science, math, the internet, AI and editing.
- Treat any numerical claims about bot traffic as *unverified until checked against a dated primary source*. Clearly distinguish **share of web traffic** from **share of people, accounts or comments**. Do not automatically embed a percentage in the render without source and date verification.
- Structure a **long-form narrative**: compelling cold open, premise, contextual explanation, evidence, examples, escalating questions, counterpoints and memorable conclusion. Split into titled chapters or sequences as appropriate; keep scene transitions and graphics motivated by changing ideas. Avoid slow generic introductions, unnecessary padding or an endless Shorts-style sequence of cuts.

## Advanced motion graphics — required quality bar

- Design **custom scene-specific motion**, not a slideshow or static speaking PNGs. Integrate characters into grounded live-action/realistic footage or cinematic backgrounds using appropriate occlusion, shadows, lighting, depth ordering and compositing.
- Combine purposeful **kinetic typography**, UI/HUD overlays, infographics, animated counters, charts, tracked labels, parallax / 2.5D depth, masks/reveals, smooth camera moves, motion blur, spring physics, morph/scale transitions and synced sound effects when narratively useful.
- Use the existing **21 Remotion motion effects** in `src/fx/` as an available creative toolbox. **Select effects to serve each scene; do not force all 21 into one video**. Study and adapt the effects without destroying their reusable source components. For longer chapters, alternate graphic-heavy passages with quieter compositions so viewers can follow the explanation.
- Maintain coherent high-contrast **black/yellow** identity for UrFavXBF and **white/black/yellow/cyan** accents for PIX; ensure pixel-art edges stay intentionally crisp when scaled. Compose for a **16:9 landscape canvas**, including legible full-width charts and safe lower thirds, rather than vertical phone-safe framing.
- Inspiration by technique: interactive mathematical animation (Alan Becker), footage-plus-game HUD visualization (TierZoo), expressive character reactions (Danno / Riggy), and professional kinetic motion polish (Ben Marriott). Do not reproduce their characters, shots or copyrighted animations.

## Owner feedback after Ghost Town pilot — priority changes

The first pilot had strong overall motion design, but both characters need visibly more expressive **independent** animation. **Implement and review character animation before data-caption fusion.** Save the second improvement too: infographic data, facts and key numbers should interact with the *same animated captions and speaker timing*, not live in detached panels. The detailed work plan, current 2.5D prototype and real 3D rig prerequisites are in [CHARACTER_ANIMATION_V2.md](CHARACTER_ANIMATION_V2.md). Do not call perspective-spun 2D PNGs true 3D models.

## Character animation and identity integrity

- Load the **actual approved transparent PNG overlays** listed in `characters/registry.json`, after staging the binaries from the owner's ChatGPT Library into `public/characters/` for a render. Verify each fingerprint where supported. The repository does **not** currently contain those binary images.
- Animate both characters with intentional, scene-specific **idle breathing or bobbing, head tilts, eye blinks, gaze shifts, emphatic poses, ear/tail reactions for PIX, turns, entrance/exit motion and reaction timing**, to the extent actually supported by the available image rig/assets.
- Speaker-specific cues must derive from the final audio and annotated speaker track. Use reaction motion on listening characters; do not animate both as talking simultaneously unless deliberately overlapping dialogue.
- **A static transparent PNG is not a rigged or lip-synced model.** If mouth-shape sprites, an actual face rig or phoneme/viseme mapping are unavailable, avoid claiming real lip sync. Use honest, limited bob/gesture proxies until an authentic rig is created.
- Keep face shapes, pixel style, outfits and character scale consistent; preserve PIX's pet-sized visual relationship to UrFavXBF.

## Voice identity, accuracy & music

- **UrFavXBF**: default VoxCPM2 `urfavxbf-neon-storyteller-tl-v1`, Filipino Neon Storyteller voice design; English legacy Chatterbox `natural-storyteller-v1` available explicitly.
- **PIX**: default VoxCPM2 `pix-pixel-spark-tl-v1`, Filipino Pixel Spark voice design; English legacy Chatterbox `pix-cute-female-emily-v1` available explicitly. Prefer the character-aware CLI `scripts/character_voiceover.py` to avoid assigning the wrong speaker.
- Generate **distinct WAV lines or manageable chapter-sized segments**, mark the speaker and exact script for each line, retain real start/end times, and sequence them with visual reactions. Use the existing Chatterbox long-form chunking where appropriate. Avoid accidental overwriting, speech clipping, double audio, overlapping lines or voice drift between chapters.
- **Check voice accuracy by listening**: no missing or invented words, no swapped lines, corrected pronunciation of UrFavXBF, PIX and technical terms, appropriate expressive delivery, no unexplained shifts of voice identity. Chatterbox can vary across generations; voice presets alone do not prove audible quality.
- Build **word-aligned captions from the actual final generated audio** (forced alignment or transcript with human review). Captions, kinetic text, scene changes and reaction animation must track the audible speech; do not invent word timestamps. Check SRT/caption line wrapping, safe-area placement and readability.
- Music and SFX must be licensed and mixed below speech. No auto-upload or publishing without explicit authorization.

## Video output and acceptance checklist

**Default for all new original videos: long-form YouTube, 16:9 landscape / 1920 × 1080 / 30 fps**, H.264 MP4 with AAC audio unless a particular delivery requires another format. The episode duration is set from a developed script and storyboard; do not assume a Short-length limit. Existing 9:16 compositions remain legacy/demo assets and are **not** the new-video default.

For each episode, plan the overall timeline, chapter transitions, recurring graphics, two-character screen geography and audio pacing across the **entire** runtime. Avoid simply stretching a short-form sequence or scaling 1080 × 1920 graphics into landscape.

Before declaring the video complete:
1. Confirm **both approved images** are actually present and rendered with transparent backgrounds, consistent pixelated styling and no cropping/off-screen errors.
2. Confirm **both approved character voice designs** produce understandable Tagalog/Taglish audio, distinct speaker identities and accurate captions; independently listen and compare with the locked script. Existing verified Chatterbox WAVs are English-only and do not validate the new Tagalog designs.
3. Confirm credible character motion, clearly differentiated speaker turns and character-reactive motion graphics. Check no distracting or excessive effect stacking.
4. Preview representative and transition frames; verify typography, overlays, motion timing, camera/effect continuity and zero missing assets.
5. Validate actual MP4 video + audio streams, encoding, dimensions, length, audio balance, speech-to-caption alignment and playback using ffprobe and preview.
6. Report only **verified** delivered files. If animation, lip sync, character overlays or render have not been implemented/executed, identify the gap honestly.

## Tooling terminology

The repository contains **21 motion-effect implementations** in its effects library and **13 bundled agent workflow skills** (the custom AI video editor skill plus 12 official Remotion agent skills, assembled into CineForge Pro). The 21 effects are **not 21 separate installed agent skills**. Both resources should be available to guide quality.
