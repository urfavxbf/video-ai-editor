# Becky G — Quote-First Podcast Short

## Creative direction

This is a **quote-first** video, not a gossip recap or AI-voice imitation. Preserve Becky G's **real speaking voice**, facial expressions, pauses, and the full context of her interview. Alternate authentic speaker camera close-ups with original animated kinetic-typography cards (white paper background, black type, restrained red hand-drawn emphasis) inspired by the **editing principles** of the user's reference, not a copied design.

**Default preview deliberately includes neither copyrighted podcast footage nor copyrighted podcast audio.** It is a silent motion storyboard with quotes/keywords only. It is not the publish-ready edit.

## Editorial selection standard — quotes that stay with viewers

**Primary brief:** Find the lines people remember, save, replay, send to a friend, and reflect on after the video ends. Fame, gossip, controversy and sensational headlines are secondary. Do NOT choose "I called off my engagement" as the emotional thesis; it is useful as context, but not the memorable takeaway.

Select a quote only when it meets these checks:

1. **Universal relevance:** Someone unfamiliar with the celebrity can still relate to the feeling or lesson.
2. **A real insight:** It expresses an uncomfortable truth, a surprising reversal, self-respect, faith, forgiveness, regret, accountability, or a hard-earned life lesson.
3. **Self-contained meaning:** The thought can be understood with minimal context and is not falsely absolute when isolated.
4. **Authentic delivery:** Keep the actual guest's voice, pacing, silence, and emotional facial expression. No AI celebrity imitation and no invented dialogue.
5. **Source integrity:** Verify exact words and in/out points from the original interview; keep contextual qualifications. Use original quotes on captions; any rewritten idea must be explicitly labeled as commentary.
6. **Production payoff:** The strongest thought gets a natural pause and visual emphasis, not louder sound effects or a cluttered montage.

**First-choice message:** "You don't trust yourself anymore." Becky G is discussing how experiencing betrayal damaged her confidence in her own judgment. Lead the *story* with that emotionally universal truth, retaining the preceding words about betrayal in the real audio wherever feasible. Her engagement is supporting context, not the reason for the clip.

**On-screen treatment:** Start with a compelling fragment of the authentic source voice, cut to an off-white typography frame for the highest-impact phrase, highlight **TRUST YOURSELF** in red, then return to the real interview for the consequence and insight. Allow a 0.5–1s pause only when it respects the natural recording. Use the original source audio continuously beneath text animation; no celebrity voice cloning. The same editorial principles apply to relationships, faith and ethical discussions.

**Do not confuse sample storyboards with final clips:** current beat times are placeholders for silent preview. Frame-accurate, context-preserving segmentation must be constructed from the rights-cleared audio and checked before publishing.

## Source research and accuracy

- Episode: [Becky G: Cheating & People Pleasing — Call Her Daddy (official)](https://www.youtube.com/watch?v=YLAVyH-efSE), April 1, 2026.
- [Transcript index / rough entry near 42:19](https://podscripts.co/podcasts/call-her-daddy/becky-g-cheating-people-pleasing).
- **Research windows:** ~42:19, when she says she called off her engagement and removed her ring; ~42:53, when she describes the emotional effects of betrayal and the choice to prioritize herself. These are **transcript paragraph markers, not video frame-verified in-points**.
- Cross-check: [iHeart's April 2 report](https://www.iheart.com/content/2026-04-02-becky-g-breaks-silence-on-ending-engagement-amid-cheating-claims/) and [official SiriusXM episode](https://www.siriusxm.com/blog/becky-g-call-her-daddy/).
- Factual nuance: Becky said she called off her engagement; she also said she and Sebastian Lletget were still together as of the interview. Do **not** imply they permanently separated or add fictional dialogue. Frame allegations accurately.
- **Copyright:** The source interview and audio are not licensed merely because they are public. Obtain permission/rights or appropriate legal review before importing source assets or distributing a derivative clip. Captions, credit, and edits alone do not grant a license or guarantee fair use.

## Select the quote, then edit

Key quote: **"You don't trust yourself anymore."** This is Becky G's actual statement and the strongest emotional thesis. Open on the guest speaking or a tightly edited contextual statement. Avoid opening with narrator exposition.

Approved short quotation/select phrase for on-screen emphasis:
- Engagement revealed: "I called off my engagement."
- Emotional emphasis: "I took off my ring."
- Betrayal setup: "The thing about betrayal"
- Main reveal: "You don't trust yourself anymore."
- Choice to prioritize herself: "No, I come first."

These snippets are NOT a contiguous verbatim transcript. The final audio must follow the real sequence and retain all context necessary for meaning; the final word-by-word captions must match everything audibly spoken, not merely the selected display phrases. Existing `BECKY_G_BEATS` are a storyboard, **not evidence of timing**.

## Draft silent visual preview (27s)

| Preview time | Mode | On-screen emphasis |
|---|---|---|
| 0–5s | Speaker close-up (or original mic illustration if no rights) | Engagement decision |
| 5–10s | White kinetic typography + red circle | Ring |
| 10–15s | Speaker close-up | Betrayal |
| 15–22s | White typography + red underline | Trust yourself |
| 22–27s | Speaker close-up | Choosing herself |

The editor may change all five segment lengths to match the real recording. A polished cut can run ~25–45 seconds depending on pauses and context; do **not** time-stretch quotations to fit a predetermined number.

## Render and media integration

```sh
npm ci
npm run typecheck
npm run render:becky-g
# output: out/becky-g-editorial-preview.mp4
```

The silent preview requires no downloads, paid APIs, synthetic celebrity voice or source footage. To make a lawful source-driven cut:

1. Supply a rights-cleared interview clip under `public/` and pass its relative path as `videoPath`.
2. Set `playSourceAudio: true` to use that clip's actual dialogue; or provide a separate `audioPath` (which automatically mutes the video track). **Never clone the celebrity's voice.**
3. Map each segment's verified media in-point with `beats[].mediaStartSeconds` (or use continuous `sourceStartSeconds`), and ensure no words or contextual caveats are cut misleadingly. Typed phrases are not a substitute for complete word-aligned subtitles.
4. Generate exact transcripts from authorized media; forced-align the real spoken words and adjust every `tokens[].at` timestamp. Only then set `approximateTiming=false`.
5. QA for copyright/licensing, factual accuracy, source A/V sync, subtitle accuracy, speaker framing, crop, clean typography, natural pauses, and audio loudness. Remove preview-only labels.

## Proposed metadata

**Title:** Becky G on Betrayal: The Part Nobody Talks About

**Description:** Becky G discusses betrayal, self-trust, and reclaiming her decisions on Call Her Daddy. Watch the full original episode: https://www.youtube.com/watch?v=YLAVyH-efSE

The description is for a cleared, contextually faithful edit. Source credit does not substitute for rights clearance.
