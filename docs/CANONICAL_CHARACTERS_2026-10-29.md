# Official characters — canonical visual replacement (29 October 2026)

**This specification supersedes every earlier UrFavXBF/PIX visual model.** The three uploaded references, not previous V2 packs or rejected V4 vector artwork, are authoritative. Preserve the existing English Chatterbox speaker profiles and speech-turn timing. Production language remains English while Tagalog voice generation is budget-deferred.

## UrFavXBF
- Friendly anime/chibi male host, medium warm skin tone, emerald-green eyes.
- Messy black layered hair with vivid neon-green streaks, over-ear X-branded green headphones.
- Deep-forest-green cyber hoodie with luminous green piping; black X shirt, black cargo trousers and chunky green-black sneakers.
- Full-body illustration: front view, both hands open at the sides (palms up), natural relaxed scan/A-pose.
- Facial expression source is the user-supplied 10-pose sheet, with 7 mouth references.

## PIX
- Light cyan/ice-blue fluffy futuristic cat; large blue-purple expressive eyes.
- Pink inner ears and cheeks; cyan/purple/pink circular headphones and glowing blue collar.
- Must remain a **cat**, never a human, yellow/black V2 robot or substitute pet.
- Facial sheet supplies 10 illustrated expressions plus 7 mouth shapes. **No official full-body reference was uploaded for PIX.**

## Approved expression + mouth IDs
- Expressions: neutral, happy, curious, excited, surprised, thinking, focused, sleepy, glitch, blink.
- Mouths: rest, small, medium, wide, round, closed, fv.

## Authenticity and production gating
1. The source PNGs under `assets/character-references/` are **unaltered reference boards (RGB), not RGBA production sprites**. Verify byte SHA256 against `characters/canonical-references.json`. Their full artwork must not be replaced by generic vector stand-ins.
2. Draw real aligned transparent production layers, with exact face identity consistency, before enabling facial rendering. Never crop the illustrated sheet and mislabel every crop as a production-ready face or viseme.
3. Mouth intensity from a WAV RMS envelope is **not** phoneme-accurate lip sync. Use real timed phoneme cues if and when available.
4. Full-body arm/head/tail motion is permitted only after independently rigged layers exist. A single image may move as one piece, not pretend to have poseable arms.
5. Never load any visual from `characters/pixel-glitch/`, the old portrait assets, or previously rejected V4 vector faces as fallback.
6. If canonical runtime assets are missing, show a clear **canonical artwork pending** state; do not quietly use legacy visual assets.
7. Runtime portrait and full-body sprites remain **not production-ready** until new art assets are staged and visually reviewed. Do not claim video rendering has been verified.

## Replacing local references
Download the reference ZIP attached in the originating ChatGPT conversation, extract it at repository root, then verify `assets/character-references/` files with the canonical SHA256 manifest. Those originals are not committed to the repository by this PR because the connected GitHub action only handles text assets in this workflow. Its PR only provides the canonical source contract and removes default legacy model references.

## Brand palette
- UrFavXBF: neon-green #6FFB8B, dark forest green #0B241A, black.
- PIX: cyan #70E8FF, blue #14C7F8, purple #8955FF, pink #F588D9.

**Past episodes and source code histories remain archival; no previous character design is authorized for new videos.**
