from __future__ import annotations

from pathlib import Path


def load_markdown(path: Path) -> str:
    """Load markdown content as plain retrievable text."""
    return path.read_text(encoding="utf-8", errors="replace").strip()
