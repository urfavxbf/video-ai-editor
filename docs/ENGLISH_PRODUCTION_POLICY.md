# Current English production policy

English (en) is the current default for new original UrFavXBF × PIX scripts,
character dialogue, narration, screen text, captions and publishing metadata.
Read [PRODUCTION_POLICY.md](PRODUCTION_POLICY.md) and
[characters/registry.json](../characters/registry.json) first; a latest explicit
user instruction applies to its request without silently rewriting global defaults.

Use the existing Chatterbox V3 English profiles: UrFavXBF Natural Storyteller
(`natural-storyteller-v1`) and PIX Emily (`pix-cute-female-emily-v1`). Their
settings are in each character's `english_voice`, not the optional Tagalog
`voice` design. Preserve voice conditioning and verify actual audio.

Tagalog/VoxCPM2 remains on hold and explicit opt-in only, with no paid API or GPU
usage authorized by that opt-in. The [older multilingual policy](MULTILINGUAL_PRODUCTION_POLICY.md)
is retained for historical reproduction, not as a current default.

New productions use the 13 committed approved pixel poses, HeroCharacterStage,
cinematic full-body 2.5D scenes and 1920×1080 at 30 fps. Historic portrait-only
and vertical demos remain available when specifically requested.
