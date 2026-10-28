#!/usr/bin/env python3
"""Download and integrity-check the pinned, open-source synthetic PIX reference.

This does not train a model or generate dialogue. Chatterbox V3 consumes the
verified WAV as its optional audio_prompt_path during subsequent synthesis.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import urllib.request
import wave

from pix_voice_profile import PIX_CANDIDATE


def prepare(destination: Path) -> Path:
    url = PIX_CANDIDATE.reference_url
    if not url.startswith("https://raw.githubusercontent.com/devnen/Chatterbox-TTS-Server/"):
        raise ValueError("Unexpected reference origin")
    with urllib.request.urlopen(url, timeout=30) as response:
        payload = response.read(2_000_000 + 1)
    if not payload or len(payload) > 2_000_000:
        raise ValueError("Reference recording has an unexpected size")
    git_object = b"blob " + str(len(payload)).encode() + b"\0" + payload
    actual = hashlib.sha1(git_object).hexdigest()
    if actual != PIX_CANDIDATE.reference_git_blob_sha:
        raise RuntimeError(f"Reference Git blob mismatch: {actual}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    try:
        with wave.open(str(destination), "rb") as audio:
            if audio.getnframes() == 0 or audio.getframerate() < 16000:
                raise ValueError("Invalid WAV reference")
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    return destination


if __name__ == "__main__":
    output = prepare(Path("input/pix-reference.wav"))
    print(f"Verified PIX reference recording: {output} ({output.stat().st_size} bytes)")
