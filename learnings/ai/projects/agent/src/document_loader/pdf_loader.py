from __future__ import annotations

import logging
from pathlib import Path


def load_pdf(path: Path) -> str:
    """Extract text from a PDF file using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ImportError(
            "PDF loading requires `pypdf`. Install it with `uv add pypdf`."
        ) from exc

    pypdf_logger = logging.getLogger("pypdf")
    previous_level = pypdf_logger.level
    pypdf_logger.setLevel(logging.ERROR)
    try:
        reader = PdfReader(str(path), strict=False)
        pages: list[str] = []

        for page in reader.pages:
            text = (page.extract_text() or "").strip()
            if text:
                pages.append(text)
    finally:
        pypdf_logger.setLevel(previous_level)

    return "\n\n".join(pages).strip()
