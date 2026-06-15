from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from document_loader.docx_loader import load_docx
from document_loader.markdown_loader import load_markdown
from document_loader.pdf_loader import load_pdf
from document_loader.txt_loader import load_txt


Loader = Callable[[Path], str]


@dataclass(frozen=True)
class LoadedDocument:
    source_path: str
    content: str


@dataclass(frozen=True)
class LoadResult:
    loaded: list[LoadedDocument]
    skipped: list[str]
    errors: list[str]


class DocumentManager:
    """Load documents from disk and normalize them for agent ingestion."""

    def __init__(self) -> None:
        self._loaders: dict[str, Loader] = {
            ".txt": load_txt,
            ".md": load_markdown,
            ".markdown": load_markdown,
            ".pdf": load_pdf,
            ".docx": load_docx,
        }
        self._loaded_sources: set[str] = set()

    def supported_extensions(self) -> tuple[str, ...]:
        return tuple(sorted(self._loaders.keys()))

    def load(self, path_like: str) -> LoadResult:
        target = Path(path_like).expanduser()

        if not target.exists():
            return LoadResult(
                loaded=[],
                skipped=[],
                errors=[f"Path does not exist: {target}"],
            )

        if target.is_file():
            return self._load_file(target)

        if target.is_dir():
            return self._load_directory(target)

        return LoadResult(
            loaded=[],
            skipped=[],
            errors=[f"Unsupported path type: {target}"],
        )

    def _load_directory(self, directory: Path) -> LoadResult:
        loaded: list[LoadedDocument] = []
        skipped: list[str] = []
        errors: list[str] = []

        candidates = [
            path
            for path in sorted(directory.rglob("*"))
            if path.is_file() and path.suffix.lower() in self._loaders
        ]

        if not candidates:
            supported = ", ".join(self.supported_extensions())
            return LoadResult(
                loaded=[],
                skipped=[],
                errors=[
                    f"No supported files found in {directory}. "
                    f"Supported extensions: {supported}"
                ],
            )

        for path in candidates:
            result = self._load_file(path)
            loaded.extend(result.loaded)
            skipped.extend(result.skipped)
            errors.extend(result.errors)

        return LoadResult(loaded=loaded, skipped=skipped, errors=errors)

    def _load_file(self, path: Path) -> LoadResult:
        extension = path.suffix.lower()
        loader = self._loaders.get(extension)

        if loader is None:
            supported = ", ".join(self.supported_extensions())
            return LoadResult(
                loaded=[],
                skipped=[],
                errors=[
                    f"Unsupported file type `{extension or '<none>'}` for {path}. "
                    f"Supported extensions: {supported}"
                ],
            )

        resolved_source = str(path.resolve())
        if resolved_source in self._loaded_sources:
            return LoadResult(loaded=[], skipped=[resolved_source], errors=[])

        try:
            content = loader(path)
        except Exception as exc:
            return LoadResult(
                loaded=[],
                skipped=[],
                errors=[f"Failed to load {path}: {exc}"],
            )

        if not content.strip():
            return LoadResult(
                loaded=[],
                skipped=[],
                errors=[f"File has no extractable text: {path}"],
            )

        self._loaded_sources.add(resolved_source)
        normalized = self._normalize_document(path, content)
        document = LoadedDocument(source_path=resolved_source, content=normalized)
        return LoadResult(loaded=[document], skipped=[], errors=[])

    def _normalize_document(self, path: Path, text: str) -> str:
        """Prefix metadata so retrieval can explain where content came from."""
        source_name = path.name
        body = text.strip()
        return (
            f"# {source_name}\n\n"
            f"Source: {path.resolve()}\n\n"
            f"## Content\n"
            f"{body}"
        ).strip()
