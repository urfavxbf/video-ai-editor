#!/usr/bin/env python3
"""Validate installed Chatterbox Multilingual V3 API without downloading weights.

This is a capability check, not an audible model-inference test.
Run from the project's isolated Chatterbox virtual environment.
"""
from __future__ import annotations

import inspect
import sys
from typing import Callable


def require_v3_loader(loader: Callable[..., object]) -> None:
    """Reject installed versions that do not accept the V3 checkpoint selector."""
    try:
        parameters = inspect.signature(loader).parameters
    except (TypeError, ValueError) as exc:
        raise RuntimeError("Cannot inspect the Chatterbox model loader.") from exc
    if "t3_model" not in parameters:
        raise RuntimeError(
            "Installed Chatterbox does not expose t3_model=; it is likely the "
            "legacy PyPI 0.1.7 wheel. Reinstall from requirements-chatterbox.txt."
        )


def main() -> int:
    try:
        import torch
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        require_v3_loader(ChatterboxMultilingualTTS.from_pretrained)
    except (ImportError, OSError, RuntimeError) as exc:
        print(f"FAIL: Chatterbox V3 preflight: {exc}", file=sys.stderr)
        return 1

    if torch.cuda.is_available():
        print("OK: CUDA GPU detected")
    else:
        print("NOTE: CUDA not detected; CPU inference is possible but can be slow")
    print("OK: Chatterbox V3 model-loader API is available")
    print("NOTE: This preflight does not download model weights or synthesize audio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
