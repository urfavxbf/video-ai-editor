# UrFavXBF × PIX — cinematic 2.5D reference direction

**Status:** Owner's preferred **video presentation** as of 2026-10-29. This is a visual, editorial and animation brief, **not** permission to copy the characters, source art, voice or scene assets from the example.

**Reference:** Conversation upload `50976.mp4` · 119.853 s · 952×472 at 30000/1001 fps · SHA-256 `d0cf43164c99fc95f424d727190be4804605d7e43b69e8ca5b15c120a4ee7186`. This file is in the initiating conversation and **is not committed to GitHub**. Timestamps below refer to that original upload.

**Overrides, for future episodes:** previous portrait-only layouts, generic whole-body puppets, unapproved V2/V4 draft cutouts, and primitive-sphere GLTF actors are **not** visual-production defaults. Preserve the approved October 29 **identities** and existing English voice profiles.

## What makes this reference work

1. **Cinematic environments + 2D characters:** the human mascot and the small companion are crisp pixel-art characters placed in a cinematic, depth-rich environment. They do not need photorealistic volumetric 3D bodies to look convincing. The environment uses physically motivated warm practical lights, dark walls, wood textures, neon signs/monitors and blurred depth layers.
2. **Intentional individual gestures:** distinguish walking, direct pointing, conversational explanation, jumping, laughing, surprise and a listening state. Shots of the protagonist occupy noticeably different scales and positions, not one repeated PNG wobble.
3. **Narration = motion score:** large kinetic text lands on the meaningful word/phrase; characters point to or react to text, boxes and charts. A companion reacts on a different beat, not synchronously pretending to be speaking.
4. **Purposeful camera and editorial rhythm:** alternate room-establishing wides, mid-shots, face close-ups, extreme text/graphic inserts and minimal technical diagrams. Push-ins, soft parallax, occlusion and selective rack focus create depth. Use occasional glitch or hard beat cuts; do not shake or zoom constantly.
5. **Composited motion graphics:** contextual cards, diagrams, UI fragments, charts, and titles occupy physical or screen space with consistent depth, shadows, glow and perspective. White text is legible, emphasized words use bold accents. Avoid generic caption cards disconnected from the story.
6. **Sound reinforces editing:** narration leads, background music stays below voices and short SFX accentuate reveals and camera cuts. Do not reuse the reference's sound or soundtrack without appropriate rights.

## Specific observed references

| Sample time | Production technique to study |
| --- | --- |
| 00:04–00:13 | Bold high-contrast typographic storytelling and animated sprite character; aggressive but readable reveal staging |
| 00:15–00:36 | Pixel protagonist beside cinematic workstations / 3D monitor scene, establishing angles, practical lights |
| 00:43–00:46 | Brief minimal black technical sequence with floating data field, contrast before next scene |
| 00:46–00:59 | Two-character room performance with directional pointing, reactive labels, scripted text emphasis, glowing signage |
| 01:03–01:17 | Abstract graph / diagram stage with characters spatially interacting with information |
| 01:21–01:37 | Character framed against different tech props and processing steps, motivated graphic staging |
| 01:39–01:59 | Highly colored graphic insert and compelling, minimal closing call-to-action |

These time ranges are for understanding **visual techniques only**, not to copy shot-for-shot or recreate its exact graphics.

## Locked character art

- **UrFavXBF**: canonical chibi/anime male identity, warm skin, expressive emerald eyes, disheveled black hair with fluorescent green streaks, over-ear black/green X headphones, dark forest-green cyber hoodie, black pants and green/black sneakers. His final pixel/sprite interpretation must remain recognizable against owner-provided references.
- **PIX**: canonically a **cyan fluffy cat**, blue/purple eyes, pink inner ears/cheeks, violet/cyan/pink circular headphone set and luminous collar; preserve pet-sized scale, tail and feline four-leg or sit/stand movement. Never substitute the orange box mascot seen in the reference.
- **Two modes:** (A) high-fidelity pixel-styled *real animated 2D sprites* drawn in multiple pose/action frames, positioned into 3D environments; (B) truly rigged stylized 3D models only if visually approved and comparable in quality. Use A as the first zero-budget target; do **not** use unapproved primitive geometry as character artwork.
- Do not crop an illustration into false action poses. Each movement needs uniquely authored transition drawings or a visibly adequate skeletal rig with real independent joints. Approval of reference artwork does not automatically approve generated sprite art.

## Standard scene construction

1. Write the scene's **specific claim, dialogue, emotional beat and visual goal** first.
2. Place source-accurate original UrFavXBF/PIX performance clips into a composited scene (walking, pointing, talk, laugh, jump, listening, etc.). Include eye and mouth states only with genuine frame content; WAV RMS movement **is not** phoneme-level lip sync.
3. Build a lightweight 3D room or staged layered photo/low-poly environment behind characters. Establish scale, contact shadow, depth/occlusion, light direction and lens style. Avoid primitives for hero character faces.
4. Build original infographics/callouts with the existing Remotion effects and frame-deterministic transforms. Time emphasized words to the **verified speech audio** and to the character gesture.
5. Use cinematic camera language and transitions motivated by information hierarchy, not random motion.
6. Render a short sample and manually inspect first frame, mid-action, end of each shot, transitions and audio. Validate character likeness and motion *before* producing the full long-form episode.

### Example first visual proof (not a fixed template)

- **00:00–00:03:** original dark editing studio, a monitor wakes up, UrFavXBF enters with an authentic multi-frame walk cycle, PIX follows from an independent action.
- **00:03–00:06:** medium shot: UrFavXBF points at a floating chart; kinetic headline text appears as he speaks. PIX looks between host and graphic.
- **00:06–00:09:** cut to a tight character shot: expressive reaction or laugh; short icon, typography and camera-depth transition.
- **00:09–00:12:** wider shot reveals both and a changing 3D visualized data element; hold long enough for the viewer to read.

Storyboard is a demonstration of scene construction, **not** a production template to reuse unmodified.

## Color and format

- **Delivery:** story-driven 16:9 long-form YouTube, 1920×1080, 30fps, H.264/AAC. The uploaded reference has an approximately 2:1 frame; do **not** blindly stretch or crop it into the episode.
- **Host:** green `#6FFB8B`, forest `#0B241A` + black/neutral.
- **PIX:** ice-cyan `#70E8FF`, blue `#14C7F8`, violet `#8955FF`, pink `#F588D9`.
- **Background:** deep charcoal / warm amber and monitor glow; cinematic palettes adapt to scene narrative. Red seen in reference is *reference-specific*, not our new brand default.
- **Readability:** white/near-white primary text, restrained accent words, safe placement around character bodies, avoid motion overload during dense narration.
- **Voice:** keep currently approved English Chatterbox profiles by default; no automatic paid Tagalog/GPU synthesis. Maintain correct speaker attribution and caption timestamps.

## Budget-safe implementation target

- Remotion 4 for compositing, kinetic type, timing, SFX and final render. Existing `src/fx` collection is a toolbox, never an obligatory bundle.
- Blender (free) or original layered 3D/2.5D environments. Three.js/R3F/`@remotion/three` only when actually installed and render-tested; WebGL may need software `swangle` at lower throughput on a CPU runner.
- Original approved frame-based sprite assets, transparent aligned PNGs and typed action manifests. No scraping/copying of the example's protected assets.
- No subscription, paid AI-generation credits, rented GPU or auto YouTube publishing.

## Visual QA acceptance gates

1. **Owner-visible identity review** for both characters. Source references are fixed, visual fidelity must be signed off.
2. Independent walking/pointing/reaction/speaking states that clearly demonstrate true articulation or unique action drawings.
3. Character and 3D/background space relate via believable perspective, occlusion, contact, depth and lighting.
4. Kinetic text and graphics are original and genuinely timed to speech; any facts are verifiable.
5. No cropping of heads/ears/tail, no flat throwaway placeholder faces, no artifact reuse from rejected draft models.
6. Watch full sample and inspect extracted frames; verify actual MP4 and its audio with ffprobe; do not claim success from passing unit tests alone.
7. Keep `main` green and stage design/engine changes in small PRs. Reject PR #41 primitive 3D artwork from the final creative path until complete visual redesign and approval.

**Acceptance priority:** recognizable character identity → authentic movement → readable story graphics → camera and lighting polish → voice and caption sync → full-episode integration. Technical validity alone is not creative approval.
