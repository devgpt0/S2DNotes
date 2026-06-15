from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree
import zipfile


_DOCX_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def load_docx(path: Path) -> str:
    """Extract visible text paragraphs from a .docx file."""
    try:
        with zipfile.ZipFile(path) as archive:
            xml_bytes = archive.read("word/document.xml")
    except KeyError as exc:
        raise ValueError("DOCX content file is missing.") from exc
    except zipfile.BadZipFile as exc:
        raise ValueError("Invalid DOCX file format.") from exc

    root = ElementTree.fromstring(xml_bytes)
    paragraphs: list[str] = []

    for paragraph in root.findall(".//w:p", _DOCX_NAMESPACE):
        runs = paragraph.findall(".//w:t", _DOCX_NAMESPACE)
        text = "".join(run.text or "" for run in runs).strip()
        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()
