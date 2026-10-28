"""Approved default narration profile for Video AI Editor.

The user's approved October 2026 Chatterbox V3 sample was synthesized with
the upstream V3 *built-in* speaker conditioning (no voice-reference audio),
English and the engine's standard expressive settings.

This is a voice identity/configuration preset, NOT a byte-identical audio
reproduction: V3 sampling may vary emphasis and pacing between generations.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class NarratorProfile:
    identifier: str
    display_name: str
    checkpoint: str
    language: str
    exaggeration: float
    cfg_weight: float
    source: str


DEFAULT_NARRATOR = NarratorProfile(
    identifier="natural-storyteller-v1",
    display_name="Natural Storyteller — Chatterbox V3",
    checkpoint="v3",
    language="en",
    exaggeration=0.5,
    cfg_weight=0.5,
    source="chatterbox-v3-builtin",
)
