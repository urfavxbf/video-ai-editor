# Eight-beat visual direction — YouTube Beginner Journey

**Creative source:** the owner's 0:00–11:30 visual-aid timeline. The authored
source of truth is [visual-aid.json](./visual-aid.json); it is implemented
as original, frame-derived React/Remotion drawings in
[src/episodes/YouTubeJourneyVisuals.tsx](../../src/episodes/YouTubeJourneyVisuals.tsx).

| Editorial target | Beat | Visual implementation |
|---|---|---|
| 0:00–0:40 | PIX expects instant money | Upload completes; imaginary $0.00 counter dissolves to “What actually happens after Upload?” |
| 0:40–2:10 | Who is the viewer? | Five topic cards reorganize into a single beginner-tech audience promise |
| 2:10–3:50 | How discovery works | One video becomes three viewing situations: Home, Suggested and Search; never claim an undisclosed ranking score |
| 3:50–5:10 | Fix the package | Vague title changes into a specific storage explanation; thumbnail and direct opening appear |
| 5:10–7:10 | Eligibility has two gates | Expanded-YPP early access (500 subs + 3 uploads / 90 days + 3,000 eligible public hours / 12 months OR 3M eligible public Shorts views / 90 days), then ad-sharing eligibility (1,000 subs + 4,000 valid hours / 12 months OR 10M Shorts views / 90 days); policy and review caveats |
| 7:10–8:40 | Understand RPM | Hypothetical **50,000** views × **$2** vs **$5** RPM produces **$100** vs **$250**; no earnings promise |
| 8:40–10:00 | Revenue is diversified | Premium, memberships, sponsorships, affiliate offers and original products; each has requirements or ongoing work |
| 10:00–11:30 | Practical plan | Original research and explanations replace recycled shortcuts; audience → useful videos → review results → improve; close on PIX's next phone-storage video, not a money counter |

## Script and actual recording continuity

The approved English audio script has **nine dialogue chapters**, while this
creative storyboard has **eight editorial beats**. Preserve every approved
line. Map chapters 1–7 to visual beats 1–7; integrate chapter 8 (originality)
and chapter 9 (first-month plan) into beat 8. No dialogue is omitted or replaced
simply to force the script into eight blocks.

The 0:00–11:30 timestamps are *editorial goals*, **not** actual measured spoken
timestamps. The current existing voice artifact contains **six** selected lines
from scenes 1, 5, 6: **47.9 s** including pauses and transitions, verified by
the successful October 28 CPU GitHub Actions run.

All **68 WAV lines** have now been generated and the assembled measured narration is **485.867 seconds**, not the target 690 seconds. Use
`scripts/build_youtube_journey_full.py` to measure every real PCM sample,
stage audio under gitignored `public/voiceovers/`, derive per-speaker
audio-envelope events, and generate a draft full-composition props file.
The assembler reports actual chapter starts alongside these editorial
timecode targets. **Do not add silence, speed up narration, or fake metrics
merely to hit a schedule.**

## Render/test gates

- Visual-art-only reference: Remotion composition `YouTubeJourneyVisualBoard`,
  **1920×1080/30fps** for the 690-second storyboard. It intentionally contains
  no narration or official character PNGs and makes no claim of a finished MP4.
- Six-audio-turn excerpt: `YouTubeJourneyPreview`. Its graphics use the
  revised beat 1, 5, 6 treatments. The two **approved transparent full-body** character sprites load from
  `public/characters/UrFavXBF_Transparent.png` and `public/characters/PIX_Transparent.png`; never substitute generic characters. Full-body puppet gestures are audio-reactive; independent limb animation requires aligned character rig layers.
- Full-length production: `YouTubeJourneyFullEpisode`, registered with
  dynamic duration, character-specific real RMS energy and timing supplied
  by all 68 actual WAV files. It deliberately refuses an audio-backed render
  when `assetsReady=false`.
- Captions currently use **unreviewed estimated sub-line duration**. Speaker
  identity and line start/end are measured, not phoneme or word boundaries.
  This is an editing draft, not a claim of word-aligned captions or visemes.
- Rendering should pass TypeScript compilation, the eight frame stills, audio
  clip presence/duration checks, actual MP4 inspection and reviewed captions.
  Official full-body PNGs remain an external staging requirement; validate them using `scripts/validate_youtube_journey_fullbody.py` before marking render props `assetsReady=true`.
- Full-body animated characters replace portrait-only characters, without a GPU runner or a video template. No automated YouTube upload and no unverified earnings claims. See `FULL_BODY_ANIMATION.md`.

### Commands when the full approved audio and portrait files are staged

```bash
python scripts/build_youtube_journey_full.py \
  --audio-root out/youtube-journey-voices-full \
  --output out/youtube-journey-full.props.json

# Manually inspect + audition the measured props, then stage approved
# public/characters/pixel-glitch/{pix,urfavxbf}/*.png.
# Set assetsReady=true in the local props only after verifying those files.
npm ci
npm run typecheck
npx remotion render YouTubeJourneyFullEpisode out/youtube-journey-full.mp4 \
  --props=out/youtube-journey-full.props.json \
  --codec=h264 --crf=18 --pixel-format=yuv420p --audio-codec=aac
```

This does not certify the final video. Review playback, caption offsets, pacing,
actual numbers, audio peaks and image framing before publishing.
