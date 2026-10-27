"""Fast, model-free regression tests for the V3 preflight guard."""
from __future__ import annotations

import unittest

from scripts.check_chatterbox_v3 import require_v3_loader


class ChatterboxPreflightTests(unittest.TestCase):
    def test_rejects_pypi_legacy_loader(self) -> None:
        def old_loader(device: str) -> object:
            return object()

        with self.assertRaisesRegex(RuntimeError, "legacy PyPI"):
            require_v3_loader(old_loader)

    def test_accepts_explicit_v3_selector(self) -> None:
        def v3_loader(device: str, t3_model: str | None = None) -> object:
            return object()

        require_v3_loader(v3_loader)


if __name__ == "__main__":
    unittest.main()
