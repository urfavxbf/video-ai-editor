"""Approved default Chatterbox V3 English voice for PIX, UrFavXBF's talking AI pet.

This is intentionally independent of DEFAULT_NARRATOR; Chatterbox's V3 built-in
voice is not a catalogue of selectable cute/female speakers. PIX uses a pinned,
openly licensed synthetic female reference to condition Chatterbox V3.
A real Chatterbox WAV sample passed workflow checks, and the owner requested that\nthis two-character setup be saved on 2026-10-28. Final audio still requires QC.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class PixVoiceProfile:
    identifier: str
    display_name: str
    engine: str
    checkpoint: str
    language: str
    exaggeration: float
    cfg_weight: float
    reference_url: str
    reference_git_blob_sha: str
    license_url: str


PIX_CANDIDATE = PixVoiceProfile(
    identifier="pix-cute-female-emily-v1",
    display_name="PIX — Cute AI Companion (Emily reference)",
    engine="chatterbox-multilingual",
    checkpoint="v3",
    language="en",
    exaggeration=0.65,
    cfg_weight=0.35,
    reference_url=(
        "https://raw.githubusercontent.com/devnen/Chatterbox-TTS-Server/"
        "915ae289340e10c6047f27f47e22eae9bf350c32/voices/Emily.wav"
    ),
    reference_git_blob_sha="a6f9c9f04fdf7bbb4b0de35e6a7111ea0f5a2fa0",
    license_url=(
        "https://github.com/devnen/Chatterbox-TTS-Server/blob/"
        "915ae289340e10c6047f27f47e22eae9bf350c32/LICENSE"
    ),
)

PIX_SAMPLE_SCRIPT = (
    "Hey, UrFavXBF! I'm PIX, your tiny AI sidekick! "
    "Got a big question? Let's figure it out together! "
    "Ooh, I love this part!"
)

# Stable default for all new PIX dialogue. Keep the previous name for older jobs.
DEFAULT_PIX = PIX_CANDIDATE
