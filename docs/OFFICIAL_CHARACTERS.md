# Official UrFavXBF and PIX — current production character bible

Read [PRODUCTION_POLICY.md](PRODUCTION_POLICY.md) and
[characters/registry.json](../characters/registry.json) before new work. This
summarizes the latest approved 2026-10-29 pixel poses and retained English voices.
Older language/layout policies remain historical references, not competing defaults.

UrFavXBF is the main host across wisdom, science, math, internet culture, AI and
editing; the channel is not science-only. PIX is his distinct, curious, playful,
female-voiced feline AI companion. Preserve both identities and speaker attribution.

| Character | Current approved art | Current English Chatterbox V3 voice |
| --- | --- | --- |
| UrFavXBF | Black/neon-green pixel chibi host, green hair accents and X headphones; six poses | Natural Storyteller, `natural-storyteller-v1` |
| PIX | Cyan/lavender pixel feline, headphones, approved eyes/coat/tail; seven poses | Synthetic Emily reference, `pix-cute-female-emily-v1` |

The **13 approved PNGs are committed** under `public/characters/pixel-default/`.
Their exact paths, dimensions and SHA-256 values are in
[the pose manifest](../characters/pixel-default-manifest.json). Verify using
`python3 scripts/stage_pixel_default_pack.py --verify-workspace` before rendering.
Do not substitute rejected art, crop concept boards or demand the old Library
pack to enable the current default.

Default composition: **HeroCharacterStage**, full-body pixel poses on a cinematic
2.5D stage, 16:9 / 1920×1080 / 30 fps, script/chapter-driven long-form. Motion is
speaker/listener pose selection with short transition glitches. Pose swaps and
RMS envelopes are not phoneme-accurate lip-sync or volumetric 3D rigs.
`PixelProductionProof` verifies artwork; an actual episode still needs real WAVs,
word alignment, readable captions, scene design and audiovisual QA.

English is the default. For current speaker settings use the registry's
`english_voice` fields. The retained `voice` fields describe optional Tagalog
VoxCPM2 Neon Storyteller / Pixel Spark designs, on hold and opt-in only. They do
not establish a verified Tagalog WAV or authorize paid GPU/API usage.

Historical V1/V2 art, portrait-only layouts, canonical rig experiments and old
Tagalog policies remain reproducible only when explicitly selected. See the
[historical portrait policy](PIXEL_GLITCH_PORTRAITS_ONLY.md) and
[historical multilingual policy](MULTILINGUAL_PRODUCTION_POLICY.md).
The Ghost Town pilot and Y2038 teaser are earlier examples, not mandatory topics.
Use [the current quality standard](PRODUCTION_STANDARD.md); preserve authentic
source dialogue and publish only with explicit authorization.
