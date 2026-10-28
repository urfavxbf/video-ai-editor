# YouTube Beginner Journey — production brief

## Approved creative decisions
- Topic: how YouTube works and how creators earn.
- Beginner journey: PIX creates an everyday-tech channel; UrFavXBF guides her.
- English script, captions, graphics and existing approved English voices.
- Balanced explanation with short playful banter.
- 1920×1080, 30 fps, portrait-only V2 character identity.
- Target 10–12 minutes; final duration follows measured dialogue, not padded pacing.
- Main branch remains unchanged during production.

## Source and assets
Inspected base: f6b80619c64ef1bd7cc2e5410dc897a6d1ab8e08.
No AGENTS.md appears in its complete recursive tree.
Approved pack: PixelGlitch_Complete_Pack.zip, under /UrFavXBF Video Characters/Pixel Glitch V2/.
Stage its urfavxbf and pix directories under public/characters/pixel-glitch/.
Never commit recordings, model weights or generated videos to Git.

## Story choreography
| Scene | Purpose | Original motion treatment | Sound and performance |
|---|---|---|---|
| 01 | Deflate instant-income expectation | Upload progress resolves to a question about the viewer; money fantasy disappears | PIX expectant, host thoughtful; brief silent hold after accountant joke |
| 02 | Define audience | Five topic cards organize into one everyday-tech channel promise | PIX curious; host explains without scolding |
| 03 | Explain discovery | One video card moves through distinct Home, Suggested and Search panels; no fake ranking score | Short transitions, music low; pause before three-hour intro punchline |
| 04 | Match packaging to delivery | Vague title edits into a specific phone-storage promise; first useful example appears immediately | PIX performs both weak and strong hooks; no artificial claim of measured CTR |
| 05 | Distinguish eligibility levels | Reveal two gates sequentially; highlight OR and time windows at spoken mentions | Slow down on thresholds; no jokes over numbers; listener stays silent |
| 06 | Explain RPM | Hold 50,000 views fixed; change invented RPM from $2 to $5 and recompute $100/$250 | Clearly speak hypothetical disclaimer; PIX surprise, then yacht callback |
| 07 | Diversify income | Reveal one revenue category at a time with its obligation | Warm, practical; deadpan unsponsored sentence |
| 08 | Protect originality | Generic copied clip cards turn into original notes, evidence and explanatory graphics | Confident host; no claim AI tools are prohibited |
| 09 | Practical plan and callback | Question bank becomes first-video plan; original upload card returns with a clearer purpose | Music opens slightly after final explanation; hopeful, no income guarantee |

## Visual system
Dark navy (#060d19), near-white (#f1f6ff), host yellow (#ffda00), PIX cyan (#27e8fd).
Inter typography; 52px chapter titles, 24–38px information, 34px captions in styleframes.
Canonical 414×468 portraits at left/right, central 890px graphic field.
Keep chapter titles above portraits and captions below the graphic field.
Glitch only as a motivated brief transition; no repeated flashing.
Use frame-derived easing and registered Remotion compositions.
Styleframe composition is visual development only, not a narrated video.

## Dialogue and audio contract
dialogue.json supplies 68 stable line IDs, speakers, approved voice profiles and null timings.
Each line is under the inspected short-form generator's 700-character limit.
Do not synthesize speaker names, IDs, source notes or production directions.
UrFavXBF: natural-storyteller-v1, en, exaggeration 0.5, cfg 0.5.
PIX: pix-cute-female-emily-v1, en, exaggeration 0.65, cfg 0.35, verified Emily reference.
Never substitute another voice engine without an explicit creative decision.
Generate isolated WAV per line; measure decoded sample counts.
Set listener reactions by story meaning; derive talk state from actual isolated voice energy.
Existing portrait puppetry is audio-reactive, not phoneme/viseme lip sync.
Preserve watermarking and applicable voice/model licenses.
Word captions require reviewed alignment. Null timing fields deliberately prevent false sync claims.

## Preview gate
Build a representative 45–75-second preview from the opening plus selected monetization/RPM beats, with explicit editorial transitions between excerpts.
Include speaker handoff, pause, listener response, dense numeric graphic and a transition.
Before full rendering, review audiovisual playback and collect approval or performance/pacing revisions.
Do not treat approval of this written concept as approval of an unseen preview.

## Implemented audio-driven preview checkpoint

The branch now includes `YouTubeJourneyPreview`, an editorial preview
composition. It uses six **real** short Chatterbox V3 WAV clips after synthesis,
in three deliberately separated excerpts: opening (YT-001..003), early YPP gate
(YT-029), and hypothetical RPM example plus yacht callback (YT-039, YT-042).
A brief chapter card explicitly labels each non-contiguous jump so the edit
never pretends these lines formed a continuous dialogue.

- `scripts/render_youtube_journey_voices.py` loads Chatterbox V3 once per
  speaker. UrFavXBF uses the approved English built-in Natural Storyteller
  identity; PIX uses the SHA-verified, licensed Emily reference. Generated
  WAVs and model weights are never committed.
- `scripts/build_youtube_journey_preview.py` reads PCM sample counts from
  each WAV, places each line at measured 30fps frame positions, extracts
  speaker-specific measured RMS envelopes, and stages audio under the
  gitignored `public/voiceovers/` path. It fails on missing/invalid WAVs
  or mismatched IDs/voice profiles. It prints the measured duration and
  whether it meets the target 45–75 seconds; `--strict-duration` can enforce
  that limit after an editorial revision.
- `src/episodes/YouTubeJourneyPreview.tsx` plays the actual WAVs using
  Remotion's `Audio`/`Sequence` elements and drives portrait reactions
  with the corresponding measured speaker envelope.
- Caption blocks are **editorially estimated from line duration** and visibly
  marked `DRAFT CAPTION TIMING`. They are NOT word-level alignment and the
  preview must not be presented as publish-ready. Obtain reviewed alignment
  and audition audio before a full final render.
- GitHub Actions `YouTube beginner journey — validation` tests the timeline
  using fixture WAVs and runs TypeScript typecheck, without a model download.
  `YouTube beginner journey — CPU English preview voices` synthesizes only
  the preview excerpts using CPU runners and uploads short-lived separate
  speaker artifacts and the measured Remotion props manifest. Model or
  media artifacts are not committed. This workflow may fail or be slow on
  CPU; it is not a guarantee of successful inference.

To use the workflow's audio artifact locally after the voice run succeeds:

```bash
# Download/extract the artifact so these paths exist:
# out/youtube-journey-preview.props.json
# public/voiceovers/youtube-beginner-journey/preview/{pix,urfavxbf}/YT-xxx.wav
# Extract the two approved portrait directories from the original character
# pack to public/characters/pixel-glitch/{pix,urfavxbf}/
npm ci
npm run typecheck
npx remotion render YouTubeJourneyPreview out/youtube-journey-preview.mp4 \
  --props=out/youtube-journey-preview.props.json \
  --codec=h264 --crf=19 --pixel-format=yuv420p \
  --audio-codec=aac
```

Do not render with stand-in full-body characters. Official portrait PNGs are
external assets and are **not** present in this GitHub branch. Voice artifacts
are also external until the CPU workflow completes successfully. No verified
MP4 exists from this commit alone. Recheck peak levels, exact captions,
pronunciation, shot transitions, policies and runtime after audiovisual render.
Do not upload to YouTube automatically.

## Validation
- Readable English script and structured dialogue must agree line-for-line.
- No duplicate line IDs, unknown speakers or blank/oversized lines.
- Every threshold shows its time window and the correct OR relationship.
- Arithmetic examples are explicitly hypothetical.
- Typecheck Remotion changes and inspect all three rendered styleframes.
- After real audio exists: audit speaker identity, missing words, silence, caption offset, peaks and measured duration.
- Final MP4 requires ffprobe plus beginning/middle/end and risky-shot playback.
