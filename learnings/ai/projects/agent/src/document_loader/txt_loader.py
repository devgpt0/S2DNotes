from __future__ import annotations

from pathlib import Path


def load_txt(path: Path) -> str:
    """Load plain text from a UTF-8 text file."""
    return path.read_text(encoding="utf-8", errors="replace").strip()
