# UrFavXBF + PIX — production quality standard

**Owner direction recorded:** 2026-10-28. This is the default brief for every new original English-language video featuring UrFavXBF (main host) and PIX (female-voiced AI cat sidekick). AI agents should consult this before creating a screenplay, timeline or rendered video. Keep all visual work original and treat cited creators as technique references, not designs to copy.

## Storytelling & first pilot

- Show **UrFavXBF** and **PIX** as two distinct recurring personalities; the host explains and PIX prompts, reacts, questions or adds humor. Do not replace either speaker with generic narration.
- The agreed pilot direction is **“Is the Internet Becoming a Ghost Town?”**, an approximately **40–50-second**, English-only vertical Short about bots and internet authenticity. Connect internet/AI curiosity with a lesson in critical thinking. The science niche is **not** the channel identity; UrFavXBF covers wisdom, science, math, the internet, AI and editing.
- Treat any numerical claims about bot traffic as *unverified until checked against a dated primary source*. Clearly distinguish **share of web traffic** from **share of people, accounts or comments**. Do not automatically embed a percentage in the render without source and date verification.
- Use a tight hook, dialogue-led explanation and punchy ending. Avoid a long generic introduction or repetitive templates.

## Advanced motion graphics — required quality bar

- Design **custom scene-specific motion**, not a slideshow or static speaking PNGs. Integrate characters into grounded live-action/realistic footage or cinematic backgrounds using appropriate occlusion, shadows, lighting, depth ordering and compositing.
- Combine purposeful **kinetic typography**, UI/HUD overlays, infographics, animated counters, charts, tracked labels, parallax / 2.5D depth, masks/reveals, smooth camera moves, motion blur, spring physics, morph/scale transitions and synced sound effects when narratively useful.
- Use the existing **21 Remotion motion effects** in `src/fx/` as an available creative toolbox. **Select effects to serve the scene; do not force all 21 into one Short**. Study and adapt the effects without destroying their reusable source components.
- Maintain coherent high-contrast **black/yellow** identity for UrFavXBF and **white/black/yellow/cyan** accents for PIX; ensure pixel-art edges stay intentionally crisp when scaled. Text remains legible in phone-safe regions.
- Inspiration by technique: interactive mathematical animation (Alan Becker), footage-plus-game HUD visualization (TierZoo), expressive character reactions (Danno / Riggy), and professional kinetic motion polish (Ben Marriott). Do not reproduce their characters, shots or copyrighted animations.

## Character animation and identity integrity

- Load the **actual approved transparent PNG overlays** listed in `characters/registry.json`, after staging the binaries from the owner's ChatGPT Library into `public/characters/` for a render. Verify each fingerprint where supported. The repository does **not** currently contain those binary images.
- Animate both characters with intentional, scene-specific **idle breathing or bobbing, head tilts, eye blinks, gaze shifts, emphatic poses, ear/tail reactions for PIX, turns, entrance/exit motion and reaction timing**, to the extent actually supported by the available image rig/assets.
- Speaker-specific cues must derive from the final audio and annotated speaker track. Use reaction motion on listening characters; do not animate both as talking simultaneously unless deliberately overlapping dialogue.
- **A static transparent PNG is not a rigged or lip-synced model.** If mouth-shape sprites, an actual face rig or phoneme/viseme mapping are unavailable, avoid claiming real lip sync. Use honest, limited bob/gesture proxies until an authentic rig is created.
- Keep face shapes, pixel style, outfits and character scale consistent; preserve PIX's pet-sized visual relationship to UrFavXBF.

## Voice identity, accuracy & music

- **UrFavXBF**: approved Chatterbox Multilingual V3, profile `natural-storyteller-v1`, English, built-in speaker.
- **PIX**: Chatterbox Multilingual V3, profile `pix-cute-female-emily-v1`, English, pinned synthetic female Emily voice reference. Prefer the character-aware CLI `scripts/character_voiceover.py` to avoid assigning the wrong speaker.
- Generate **distinct WAV lines**, mark the speaker and exact script for each line, retain real start/end times, and sequence them with visual reactions. Avoid accidental overwriting, speech clipping, double audio or overlapping lines.
- **Check voice accuracy by listening**: no missing or invented words, no swapped lines, corrected pronunciation of UrFavXBF, PIX and technical terms, appropriate expressive delivery, no unexplained shifts of voice identity. Chatterbox can vary across generations; voice presets alone do not prove audible quality.
- Build **word-aligned captions from the actual final generated audio** (forced alignment or transcript with human review). Captions, kinetic text, scene changes and reaction animation must track the audible speech; do not invent word timestamps. Check SRT/caption line wrapping, safe-area placement and readability.
- Music and SFX must be licensed and mixed below speech. No auto-upload or publishing without explicit authorization.

## Video output and acceptance checklist

Default new original Short: **9:16 / 1080 × 1920 / 30 fps**, unless the owner specifies another delivery profile.

Before declaring the video complete:
1. Confirm **both approved images** are actually present and rendered with transparent backgrounds, consistent pixelated styling and no cropping/off-screen errors.
2. Confirm **both approved Chatterbox voices** are audible with the right speakers and English speech; independently listen and compare the spoken audio with the locked script.
3. Confirm credible character motion, clearly differentiated speaker turns and character-reactive motion graphics. Check no distracting or excessive effect stacking.
4. Preview representative and transition frames; verify typography, overlays, motion timing, camera/effect continuity and zero missing assets.
5. Validate actual MP4 video + audio streams, encoding, dimensions, length, audio balance, speech-to-caption alignment and playback using ffprobe and preview.
6. Report only **verified** delivered files. If animation, lip sync, character overlays or render have not been implemented/executed, identify the gap honestly.

## Tooling terminology

The repository contains **21 motion-effect implementations** in its effects library and **13 bundled agent workflow skills** (the custom AI video editor skill plus 12 official Remotion agent skills, assembled into CineForge Pro). The 21 effects are **not 21 separate installed agent skills**. Both resources should be available to guide quality.
