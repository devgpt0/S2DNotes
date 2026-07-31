from __future__ import annotations

import hashlib
import importlib
import json
import math
import os
import re
import threading
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path, PurePosixPath
from typing import Any, Literal, Protocol
from urllib.parse import quote, urlparse

import numpy as np
import numpy.typing as npt

MARKDOWN_SUFFIXES = frozenset({".markdown", ".md"})
EXCLUDED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "__pycache__",
        "build",
        "coverage",
        "dist",
        "node_modules",
        "site-packages",
        "target",
        "vendor",
        "venv",
    }
)
DEFAULT_EMBEDDING_MODEL = "BAAI/bge-m3"
DEFAULT_RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"
DEFAULT_UPSTASH_NAMESPACE = "genius-rag"
DEFAULT_CHUNK_TOKENS = 700
DEFAULT_CHUNK_OVERLAP_TOKENS = 100
DEFAULT_MODEL_CACHE_DIR = Path.home() / ".cache" / "genius" / "models"
DEFAULT_LOCAL_INDEX_DIR = Path.home() / ".cache" / "genius" / "index"
EMBEDDING_BATCH_SIZE = 12
UPSERT_BATCH_SIZE = 32
RRF_K = 60
UPSTASH_MANIFEST_VERSION = 1
UPSTASH_MANIFEST_PREFIX = "upstash-vectors-"

ATX_HEADING_PATTERN = re.compile(
    r"^(?P<marks>#{1,6})[ \t]+(?P<title>.*?)(?:[ \t]+#+)?[ \t]*$"
)
FENCE_PATTERN = re.compile(r"^[ \t]*(`{3,}|~{3,})")
TOKEN_PATTERN = re.compile(r"\w+", flags=re.UNICODE)
CHUNK_TOKEN_PATTERN = re.compile(r"\S+", flags=re.UNICODE)
CHUNK_ID_PATTERN = re.compile(r"[a-f0-9]{64}")


class RagError(RuntimeError):
    """Base error for the retrieval service."""


class CorpusError(RagError):
    """The configured Markdown corpus cannot be indexed."""


class EmbeddingUnavailableError(RagError):
    """The optional local embedding model is not usable."""


class UpstashVectorError(RagError):
    """An optional Upstash Vector request failed."""


class RetrievalBackendUnavailableError(RagError):
    """The requested retrieval backend cannot serve a query."""


class IndexingInProgressError(RagError):
    """An index operation is already running."""


@dataclass(frozen=True, slots=True)
class Settings:
    corpus_dir: Path
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    reranker_model: str = DEFAULT_RERANKER_MODEL
    model_cache_dir: Path = field(default_factory=lambda: DEFAULT_MODEL_CACHE_DIR)
    local_index_dir: Path = field(default_factory=lambda: DEFAULT_LOCAL_INDEX_DIR)
    auto_index: bool = False
    upstash_url: str | None = None
    upstash_token: str | None = None
    upstash_namespace: str = DEFAULT_UPSTASH_NAMESPACE
    chunk_tokens: int = DEFAULT_CHUNK_TOKENS
    chunk_overlap_tokens: int = DEFAULT_CHUNK_OVERLAP_TOKENS

    @classmethod
    def from_environment(cls) -> Settings:
        upstash_url = os.getenv("UPSTASH_VECTOR_REST_URL") or None
        upstash_token = os.getenv("UPSTASH_VECTOR_REST_TOKEN") or None
        if (upstash_url is None) != (upstash_token is None):
            raise ValueError(
                "UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN must be set together"
            )
        if upstash_url is not None:
            _validate_upstash_url(upstash_url)

        embedding_model = os.getenv("RAG_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
        reranker_model = os.getenv("RAG_RERANKER_MODEL", DEFAULT_RERANKER_MODEL)
        namespace = os.getenv("UPSTASH_VECTOR_NAMESPACE", DEFAULT_UPSTASH_NAMESPACE)
        if not embedding_model:
            raise ValueError("RAG_EMBEDDING_MODEL must not be empty")
        if not reranker_model:
            raise ValueError("RAG_RERANKER_MODEL must not be empty")
        _validate_namespace(namespace)

        chunk_tokens = _read_positive_integer_environment(
            "RAG_CHUNK_TOKENS", DEFAULT_CHUNK_TOKENS
        )
        chunk_overlap_tokens = _read_nonnegative_integer_environment(
            "RAG_CHUNK_OVERLAP_TOKENS", DEFAULT_CHUNK_OVERLAP_TOKENS
        )
        if chunk_overlap_tokens >= chunk_tokens:
            raise ValueError(
                "RAG_CHUNK_OVERLAP_TOKENS must be less than RAG_CHUNK_TOKENS"
            )

        return cls(
            corpus_dir=resolve_corpus_dir(_corpus_directory_from_environment()),
            embedding_model=embedding_model,
            reranker_model=reranker_model,
            model_cache_dir=_environment_directory(
                "MODEL_CACHE_DIR", DEFAULT_MODEL_CACHE_DIR
            ),
            local_index_dir=_environment_directory(
                "LOCAL_INDEX_DIR", DEFAULT_LOCAL_INDEX_DIR
            ),
            auto_index=_read_boolean_environment("RAG_AUTO_INDEX", default=False),
            upstash_url=upstash_url,
            upstash_token=upstash_token,
            upstash_namespace=namespace,
            chunk_tokens=chunk_tokens,
            chunk_overlap_tokens=chunk_overlap_tokens,
        )


@dataclass(frozen=True, slots=True)
class MarkdownChunk:
    id: str
    path: str
    topic: str
    heading: tuple[str, ...]
    ordinal: int
    checksum: str
    text: str

    @property
    def retrieval_text(self) -> str:
        if not self.heading:
            return self.text
        return f"{' > '.join(self.heading)}\n\n{self.text}"


@dataclass(frozen=True, slots=True)
class RetrievalHit:
    chunk: MarkdownChunk
    score: float


@dataclass(frozen=True, slots=True)
class IndexReport:
    document_count: int
    chunk_count: int
    embedding_status: Literal["ready", "unavailable"]
    vector_backend: Literal["disabled", "faiss", "numpy"]
    upstash_synced: bool
    warnings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    hits: tuple[RetrievalHit, ...]
    mode: Literal["unavailable", "bm25", "hybrid"]
    backend: Literal["local", "upstash"]
    reranked: bool
    indexed: bool


@dataclass(frozen=True, slots=True)
class ServiceStatus:
    state: Literal["idle", "indexing", "indexed", "failed"]
    document_count: int
    chunk_count: int
    embedding_status: Literal["uninitialized", "ready", "unavailable"]
    reranker_status: Literal["uninitialized", "ready", "unavailable"]
    vector_backend: Literal["disabled", "faiss", "numpy"]
    upstash_enabled: bool
    upstash_synced: bool
    last_error: str | None
    warnings: tuple[str, ...]


class EmbeddingProvider(Protocol):
    @property
    def status(self) -> Literal["uninitialized", "ready", "unavailable"]: ...

    def embed(self, texts: Sequence[str]) -> npt.NDArray[np.float32]: ...


class RerankerProvider(Protocol):
    @property
    def status(self) -> Literal["uninitialized", "ready", "unavailable"]: ...

    def rerank(
        self, query: str, hits: Sequence[RetrievalHit], limit: int
    ) -> tuple[list[RetrievalHit], bool]: ...


def _read_boolean_environment(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValueError(f"{name} must be exactly 'true' or 'false'")


def _read_positive_integer_environment(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    if not value.isdecimal():
        raise ValueError(f"{name} must be a positive integer")
    parsed = int(value)
    if parsed < 1:
        raise ValueError(f"{name} must be a positive integer")
    return parsed


def _read_nonnegative_integer_environment(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    if not value.isdecimal():
        raise ValueError(f"{name} must be a non-negative integer")
    return int(value)


def _environment_directory(name: str, default: Path) -> Path:
    value = os.getenv(name)
    if value is None:
        return default.expanduser().resolve()
    if not value:
        raise ValueError(f"{name} must not be empty")
    return Path(value).expanduser().resolve()


def _corpus_directory_from_environment() -> str | None:
    learnings_root = os.getenv("LEARNINGS_ROOT")
    legacy_root = os.getenv("RAG_CORPUS_DIR")
    if learnings_root is not None and legacy_root is not None:
        if learnings_root != legacy_root:
            raise ValueError(
                "LEARNINGS_ROOT and RAG_CORPUS_DIR must match when both are set"
            )
    return learnings_root if learnings_root is not None else legacy_root


def _validate_upstash_url(value: str) -> None:
    parsed = urlparse(value)
    if (
        parsed.scheme != "https"
        or not parsed.netloc
        or parsed.username
        or parsed.password
    ):
        raise ValueError(
            "UPSTASH_VECTOR_REST_URL must be an HTTPS URL without credentials"
        )


def _validate_namespace(value: str) -> None:
    if not value or not all(
        character.isalnum() or character in "-_" for character in value
    ):
        raise ValueError(
            "UPSTASH_VECTOR_NAMESPACE may contain only letters, numbers, '-' and '_'"
        )


def resolve_corpus_dir(configured_directory: str | None) -> Path:
    if configured_directory is not None:
        if not configured_directory:
            raise ValueError("RAG_CORPUS_DIR must not be empty")
        return Path(configured_directory).expanduser().resolve()

    container_directory = Path("/workspace/learnings")
    if container_directory.is_dir():
        return container_directory.resolve()

    for parent in Path(__file__).resolve().parents:
        candidate = parent / "learnings"
        if candidate.is_dir():
            return candidate.resolve()

    return container_directory


def discover_markdown_files(corpus_dir: Path) -> list[Path]:
    if not corpus_dir.is_dir():
        raise CorpusError(f"Markdown corpus directory does not exist: {corpus_dir}")

    documents: list[Path] = []
    for path in corpus_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in MARKDOWN_SUFFIXES:
            continue
        if path.stat().st_size == 0:
            continue
        relative_parts = path.relative_to(corpus_dir).parts
        if any(
            part in EXCLUDED_DIRECTORY_NAMES or part.startswith(".")
            for part in relative_parts[:-1]
        ):
            continue
        documents.append(path)
    return sorted(documents)


def read_markdown(path: Path) -> str:
    document_bytes = path.read_bytes()
    try:
        content = document_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            content = document_bytes.decode("windows-1252")
        except UnicodeDecodeError as error:
            raise CorpusError(
                f"Markdown file is neither valid UTF-8 nor Windows-1252: {path}"
            ) from error

    if not content.strip():
        raise CorpusError(f"Markdown file is empty: {path}")
    return content


def _markdown_sections(markdown: str) -> list[tuple[tuple[str, ...], str]]:
    sections: list[tuple[tuple[str, ...], str]] = []
    heading_stack: list[str] = []
    current_heading: tuple[str, ...] = ()
    current_lines: list[str] = []
    fence_character: str | None = None

    def append_section() -> None:
        content = "\n".join(current_lines).strip()
        if content:
            sections.append((current_heading, content))

    for line in markdown.splitlines():
        fence_match = FENCE_PATTERN.match(line)
        if fence_match is not None:
            marker = fence_match.group(1)
            if fence_character is None:
                fence_character = marker[0]
            elif marker[0] == fence_character:
                fence_character = None
            current_lines.append(line)
            continue

        heading_match = ATX_HEADING_PATTERN.match(line)
        if fence_character is None and heading_match is not None:
            append_section()
            current_lines.clear()
            level = len(heading_match.group("marks"))
            title = heading_match.group("title").strip()
            if not title:
                raise CorpusError("Markdown headings must contain text")
            heading_stack[level - 1 :] = [title]
            current_heading = tuple(heading_stack)
            continue

        current_lines.append(line)

    append_section()
    return sections


def _chunk_token_count(text: str) -> int:
    return len(CHUNK_TOKEN_PATTERN.findall(text))


def _split_plain_text(text: str, maximum_tokens: int) -> list[str]:
    matches = list(CHUNK_TOKEN_PATTERN.finditer(text))
    if len(matches) <= maximum_tokens:
        return [text.strip()] if text.strip() else []

    chunks: list[str] = []
    for start in range(0, len(matches), maximum_tokens):
        end = min(start + maximum_tokens, len(matches))
        start_offset = matches[start].start()
        end_offset = matches[end - 1].end()
        chunk = text[start_offset:end_offset].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def _section_units(text: str, maximum_plain_tokens: int) -> list[tuple[str, bool]]:
    units: list[tuple[str, bool]] = []
    paragraph: list[str] = []
    code_block: list[str] = []
    fence_character: str | None = None

    def append_paragraph() -> None:
        content = "".join(paragraph).strip()
        paragraph.clear()
        if content:
            units.extend(
                (chunk, False)
                for chunk in _split_plain_text(content, maximum_plain_tokens)
            )

    for line in text.splitlines(keepends=True):
        fence_match = FENCE_PATTERN.match(line)
        if fence_character is not None:
            code_block.append(line)
            if fence_match is not None and fence_match.group(1)[0] == fence_character:
                content = "".join(code_block).strip()
                if content:
                    units.append((content, True))
                code_block.clear()
                fence_character = None
            continue

        if fence_match is not None:
            append_paragraph()
            code_block = [line]
            fence_character = fence_match.group(1)[0]
            continue

        if not line.strip():
            append_paragraph()
            continue
        paragraph.append(line)

    if fence_character is not None:
        raise CorpusError("Markdown code fences must be closed")
    append_paragraph()
    return units


def _tail_overlap(
    units: Sequence[tuple[str, bool]], overlap_tokens: int
) -> list[tuple[str, bool]]:
    if overlap_tokens == 0:
        return []

    result: list[tuple[str, bool]] = []
    remaining = overlap_tokens
    for text, is_code_block in reversed(units):
        if is_code_block:
            break
        token_count = _chunk_token_count(text)
        if token_count <= remaining:
            result.append((text, False))
            remaining -= token_count
        else:
            matches = list(CHUNK_TOKEN_PATTERN.finditer(text))
            start = matches[len(matches) - remaining].start()
            result.append((text[start:].strip(), False))
            remaining = 0
        if remaining == 0:
            break
    result.reverse()
    return result


def _split_text(text: str, maximum_tokens: int, overlap_tokens: int) -> list[str]:
    if maximum_tokens < 1 or overlap_tokens < 0 or overlap_tokens >= maximum_tokens:
        raise ValueError("Chunk size must be positive and greater than overlap")

    maximum_plain_tokens = maximum_tokens - overlap_tokens
    units = _section_units(text, maximum_plain_tokens)
    chunks: list[str] = []
    current: list[tuple[str, bool]] = []
    current_tokens = 0

    def append_current() -> None:
        nonlocal current, current_tokens
        if not current:
            return
        chunks.append("\n\n".join(text for text, _ in current))
        current = _tail_overlap(current, overlap_tokens)
        current_tokens = sum(_chunk_token_count(text) for text, _ in current)

    for unit_text, is_code_block in units:
        unit_tokens = _chunk_token_count(unit_text)
        if current and current_tokens + unit_tokens > maximum_tokens:
            append_current()
            if current and current_tokens + unit_tokens > maximum_tokens:
                current = []
                current_tokens = 0
        current.append((unit_text, is_code_block))
        current_tokens += unit_tokens

    if current:
        chunks.append("\n\n".join(text for text, _ in current))
    return chunks


def _topic_for_path(path: str) -> str:
    parts = PurePosixPath(path).parts
    return parts[0] if len(parts) > 1 else "root"


def _chunk_checksum(heading: Sequence[str], text: str) -> str:
    digest = hashlib.sha256()
    digest.update(" > ".join(heading).encode("utf-8"))
    digest.update(b"\0")
    digest.update(text.encode("utf-8"))
    return digest.hexdigest()


def chunk_markdown(
    markdown: str,
    path: str,
    chunk_tokens: int = DEFAULT_CHUNK_TOKENS,
    chunk_overlap_tokens: int = DEFAULT_CHUNK_OVERLAP_TOKENS,
) -> list[MarkdownChunk]:
    if not markdown.strip():
        raise CorpusError(f"Markdown file is empty: {path}")

    chunks: list[MarkdownChunk] = []
    for heading, section in _markdown_sections(markdown):
        for text in _split_text(section, chunk_tokens, chunk_overlap_tokens):
            ordinal = len(chunks)
            digest = hashlib.sha256()
            for value in (path, str(ordinal)):
                encoded = value.encode("utf-8")
                digest.update(len(encoded).to_bytes(8, byteorder="big"))
                digest.update(encoded)
            chunks.append(
                MarkdownChunk(
                    id=digest.hexdigest(),
                    path=path,
                    topic=_topic_for_path(path),
                    heading=heading,
                    ordinal=ordinal,
                    checksum=_chunk_checksum(heading, text),
                    text=text,
                )
            )
    if not chunks:
        raise CorpusError(f"Markdown file contains no indexable text: {path}")
    return chunks


def load_corpus(
    corpus_dir: Path,
    chunk_tokens: int = DEFAULT_CHUNK_TOKENS,
    chunk_overlap_tokens: int = DEFAULT_CHUNK_OVERLAP_TOKENS,
) -> tuple[list[Path], list[MarkdownChunk]]:
    documents = discover_markdown_files(corpus_dir)
    if not documents:
        raise CorpusError(f"No Markdown documents found in {corpus_dir}")

    chunks: list[MarkdownChunk] = []
    for document in documents:
        path = document.relative_to(corpus_dir).as_posix()
        chunks.extend(
            chunk_markdown(
                read_markdown(document),
                path,
                chunk_tokens,
                chunk_overlap_tokens,
            )
        )
    return documents, chunks


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


class Bm25Index:
    def __init__(self, chunks: Sequence[MarkdownChunk]) -> None:
        self._tokenized_documents = [tokenize(chunk.retrieval_text) for chunk in chunks]
        self._rank_bm25: Any | None = None
        self.backend: Literal["rank-bm25", "native"] = "native"
        self._term_frequencies: list[dict[str, int]] = []
        self._document_frequencies: dict[str, int] = {}
        self._average_length = 0.0

        try:
            rank_bm25 = importlib.import_module("rank_bm25")
            bm25_okapi = getattr(rank_bm25, "BM25Okapi")
        except (AttributeError, ImportError):
            self._build_native_index()
        else:
            self._rank_bm25 = bm25_okapi(self._tokenized_documents)
            self.backend = "rank-bm25"

    def _build_native_index(self) -> None:
        lengths: list[int] = []
        for tokens in self._tokenized_documents:
            frequencies: dict[str, int] = {}
            for token in tokens:
                frequencies[token] = frequencies.get(token, 0) + 1
            self._term_frequencies.append(frequencies)
            lengths.append(len(tokens))
            for token in frequencies:
                self._document_frequencies[token] = (
                    self._document_frequencies.get(token, 0) + 1
                )
        self._average_length = sum(lengths) / len(lengths) if lengths else 0.0

    def scores(self, query: str) -> npt.NDArray[np.float32]:
        tokens = tokenize(query)
        if not tokens:
            return np.zeros(len(self._tokenized_documents), dtype=np.float32)
        if self._rank_bm25 is not None:
            return np.asarray(self._rank_bm25.get_scores(tokens), dtype=np.float32)

        result = np.zeros(len(self._tokenized_documents), dtype=np.float32)
        if not self._term_frequencies or self._average_length == 0:
            return result

        document_count = len(self._term_frequencies)
        k1 = 1.5
        b = 0.75
        for token in set(tokens):
            document_frequency = self._document_frequencies.get(token, 0)
            if document_frequency == 0:
                continue
            inverse_frequency = math.log(
                1
                + (document_count - document_frequency + 0.5)
                / (document_frequency + 0.5)
            )
            for index, frequencies in enumerate(self._term_frequencies):
                term_frequency = frequencies.get(token, 0)
                if term_frequency == 0:
                    continue
                length = len(self._tokenized_documents[index])
                denominator = term_frequency + k1 * (
                    1 - b + b * length / self._average_length
                )
                result[index] += (
                    inverse_frequency * term_frequency * (k1 + 1) / denominator
                )
        return result


class LocalHybridIndex:
    def __init__(
        self,
        chunks: Sequence[MarkdownChunk],
        vectors: npt.NDArray[np.float32] | None = None,
    ) -> None:
        if not chunks:
            raise ValueError("At least one chunk is required")

        self.chunks = tuple(chunks)
        self._chunk_ids = {chunk.id: index for index, chunk in enumerate(self.chunks)}
        self._bm25 = Bm25Index(self.chunks)
        self._vectors: npt.NDArray[np.float32] | None = None
        self._faiss_index: Any | None = None
        self.vector_backend: Literal["disabled", "faiss", "numpy"] = "disabled"

        if vectors is not None:
            self._vectors = _normalise_vectors(vectors, len(self.chunks))
            self._build_vector_index()

    @property
    def has_vectors(self) -> bool:
        return self._vectors is not None

    def _build_vector_index(self) -> None:
        if self._vectors is None:
            return
        try:
            faiss = importlib.import_module("faiss")
        except (AttributeError, ImportError):
            self.vector_backend = "numpy"
            return

        try:
            index = faiss.IndexFlatIP(self._vectors.shape[1])
            index.add(self._vectors)
        except (OSError, RuntimeError):
            self.vector_backend = "numpy"
            return
        self._faiss_index = index
        self.vector_backend = "faiss"

    def _rank_lexical(
        self,
        query: str,
        candidate_count: int,
        allowed_paths: frozenset[str] | None,
    ) -> list[int]:
        scores = self._bm25.scores(query)
        ranked_indexes = np.argsort(-scores, kind="stable")
        result: list[int] = []
        for raw_index in ranked_indexes:
            index = int(raw_index)
            if scores[index] <= 0:
                break
            if (
                allowed_paths is not None
                and self.chunks[index].path not in allowed_paths
            ):
                continue
            result.append(index)
            if len(result) == candidate_count:
                break
        return result

    def _rank_vectors(
        self,
        query_vector: npt.NDArray[np.float32] | None,
        candidate_count: int,
        allowed_paths: frozenset[str] | None,
    ) -> list[int]:
        if self._vectors is None or query_vector is None:
            return []
        if query_vector.shape != (self._vectors.shape[1],):
            raise ValueError("Query embedding dimension does not match the local index")

        search_count = (
            len(self.chunks) if allowed_paths is not None else candidate_count
        )
        if self._faiss_index is not None:
            _, indexes = self._faiss_index.search(
                query_vector.reshape(1, -1), search_count
            )
            ranked_indexes = [int(index) for index in indexes[0] if int(index) >= 0]
        else:
            scores = self._vectors @ query_vector
            ranked_indexes = [
                int(index) for index in np.argsort(-scores, kind="stable")
            ]

        result: list[int] = []
        for index in ranked_indexes:
            if (
                allowed_paths is not None
                and self.chunks[index].path not in allowed_paths
            ):
                continue
            result.append(index)
            if len(result) == candidate_count:
                break
        return result

    def search(
        self,
        query: str,
        limit: int,
        query_vector: npt.NDArray[np.float32] | None = None,
        allowed_paths: frozenset[str] | None = None,
    ) -> list[RetrievalHit]:
        if limit < 1:
            raise ValueError("Retrieval limit must be at least one")
        candidate_count = min(len(self.chunks), max(limit * 4, 12))
        lexical = self._rank_lexical(query, candidate_count, allowed_paths)
        vectors = self._rank_vectors(query_vector, candidate_count, allowed_paths)
        rankings = [ranking for ranking in (lexical, vectors) if ranking]
        if not rankings:
            return []
        weights = _ranking_weights(len(rankings))
        scores: dict[int, float] = {}
        for ranking, weight in zip(rankings, weights, strict=True):
            for rank, index in enumerate(ranking, start=1):
                scores[index] = scores.get(index, 0.0) + weight / (RRF_K + rank)

        normaliser = sum(weights) / (RRF_K + 1)
        ranked = sorted(scores, key=lambda index: (-scores[index], index))[:limit]
        return [
            RetrievalHit(chunk=self.chunks[index], score=scores[index] / normaliser)
            for index in ranked
        ]

    def remote_hits(
        self,
        remote_scores: dict[str, float],
        limit: int,
        allowed_paths: frozenset[str] | None = None,
    ) -> list[RetrievalHit]:
        if limit < 1:
            raise ValueError("Retrieval limit must be at least one")

        hits: list[RetrievalHit] = []
        for chunk_id, score in sorted(
            remote_scores.items(), key=lambda item: item[1], reverse=True
        ):
            index = self._chunk_ids.get(chunk_id)
            if index is None:
                continue
            chunk = self.chunks[index]
            if allowed_paths is not None and chunk.path not in allowed_paths:
                continue
            hits.append(RetrievalHit(chunk=chunk, score=score))
            if len(hits) == limit:
                break
        return hits


def _ranking_weights(ranking_count: int) -> tuple[float, ...]:
    if ranking_count == 1:
        return (1.0,)
    if ranking_count == 2:
        return (0.5, 0.5)
    if ranking_count == 3:
        return (0.45, 0.45, 0.10)
    raise ValueError("Unexpected number of retrieval rankings")


def _normalise_vectors(
    vectors: npt.NDArray[np.float32], expected_count: int
) -> npt.NDArray[np.float32]:
    matrix = np.asarray(vectors, dtype=np.float32)
    if matrix.ndim != 2 or matrix.shape[0] != expected_count or matrix.shape[1] == 0:
        raise ValueError("Embedding matrix dimensions do not match indexed chunks")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("Embedding matrix contains non-finite values")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Embedding matrix contains zero vectors")
    return matrix / norms


def _prepare_model_cache(cache_dir: Path) -> str:
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise OSError(f"Unable to create model cache directory: {cache_dir}") from error
    if not cache_dir.is_dir():
        raise OSError(f"Model cache path is not a directory: {cache_dir}")

    cache_path = str(cache_dir)
    os.environ.setdefault("HF_HOME", cache_path)
    os.environ.setdefault("HF_HUB_CACHE", str(cache_dir / "hub"))
    return cache_path


class BgeM3Embedder:
    def __init__(self, model_name: str, cache_dir: Path) -> None:
        self._model_name = model_name
        self._cache_dir = cache_dir
        self._model: Any | None = None
        self._error: str | None = None
        self._lock = threading.Lock()

    @property
    def status(self) -> Literal["uninitialized", "ready", "unavailable"]:
        if self._model is not None:
            return "ready"
        if self._error is not None:
            return "unavailable"
        return "uninitialized"

    def _get_model(self) -> Any:
        with self._lock:
            if self._model is not None:
                return self._model
            if self._error is not None:
                raise EmbeddingUnavailableError(self._error)
            try:
                flag_embedding = importlib.import_module("FlagEmbedding")
                bge_m3_flag_model = getattr(flag_embedding, "BGEM3FlagModel")

                self._model = bge_m3_flag_model(
                    self._model_name,
                    use_fp16=False,
                    cache_dir=_prepare_model_cache(self._cache_dir),
                )
            except (
                AttributeError,
                ImportError,
                OSError,
                RuntimeError,
                TypeError,
            ) as error:
                self._error = f"BGE-M3 embeddings are unavailable: {type(error).__name__}: {error}"
                raise EmbeddingUnavailableError(self._error) from error
            return self._model

    def embed(self, texts: Sequence[str]) -> npt.NDArray[np.float32]:
        if not texts or any(not text.strip() for text in texts):
            raise ValueError("Embedding input must contain non-empty text")
        model = self._get_model()
        try:
            response = model.encode(
                list(texts),
                batch_size=EMBEDDING_BATCH_SIZE,
                max_length=8_192,
                return_dense=True,
                return_sparse=False,
                return_colbert_vecs=False,
            )
        except (OSError, RuntimeError) as error:
            self._error = (
                f"BGE-M3 embeddings are unavailable: {type(error).__name__}: {error}"
            )
            raise EmbeddingUnavailableError(self._error) from error

        if not isinstance(response, dict) or "dense_vecs" not in response:
            raise ValueError("BGE-M3 did not return dense embeddings")
        vectors = np.asarray(response["dense_vecs"], dtype=np.float32)
        return _normalise_vectors(vectors, len(texts))


class CrossEncoderReranker:
    def __init__(self, model_name: str, cache_dir: Path) -> None:
        self._model_name = model_name
        self._cache_dir = cache_dir
        self._model: Any | None = None
        self._error: str | None = None
        self._lock = threading.Lock()

    @property
    def status(self) -> Literal["uninitialized", "ready", "unavailable"]:
        if self._model is not None:
            return "ready"
        if self._error is not None:
            return "unavailable"
        return "uninitialized"

    def _get_model(self) -> Any:
        with self._lock:
            if self._model is not None:
                return self._model
            if self._error is not None:
                raise EmbeddingUnavailableError(self._error)
            try:
                sentence_transformers = importlib.import_module("sentence_transformers")
                cross_encoder = getattr(sentence_transformers, "CrossEncoder")

                self._model = cross_encoder(
                    self._model_name,
                    max_length=512,
                    cache_folder=_prepare_model_cache(self._cache_dir),
                )
            except (
                AttributeError,
                ImportError,
                OSError,
                RuntimeError,
                TypeError,
            ) as error:
                self._error = f"Cross-encoder reranking is unavailable: {type(error).__name__}: {error}"
                raise EmbeddingUnavailableError(self._error) from error
            return self._model

    def rerank(
        self, query: str, hits: Sequence[RetrievalHit], limit: int
    ) -> tuple[list[RetrievalHit], bool]:
        if not hits:
            return [], False
        try:
            model = self._get_model()
            raw_scores = model.predict(
                [(query, hit.chunk.retrieval_text) for hit in hits]
            )
        except EmbeddingUnavailableError:
            return list(hits[:limit]), False
        except (OSError, RuntimeError) as error:
            self._error = f"Cross-encoder reranking is unavailable: {type(error).__name__}: {error}"
            return list(hits[:limit]), False

        scores = np.asarray(raw_scores, dtype=np.float32)
        if scores.shape != (len(hits),):
            raise ValueError("Cross-encoder returned an unexpected score shape")
        order = np.argsort(-scores, kind="stable")[:limit]
        return [
            replace(hits[int(index)], score=float(scores[int(index)]))
            for index in order
        ], True


class UpstashVectorStore(Protocol):
    @property
    def namespace(self) -> str: ...

    def upsert(
        self, chunks: Sequence[MarkdownChunk], vectors: npt.NDArray[np.float32]
    ) -> None: ...

    def delete(self, vector_ids: Sequence[str]) -> None: ...

    def query(
        self, vector: npt.NDArray[np.float32], limit: int
    ) -> dict[str, float]: ...


class UpstashVectorClient:
    def __init__(self, rest_url: str, token: str, namespace: str) -> None:
        _validate_upstash_url(rest_url)
        if not token:
            raise ValueError("UPSTASH_VECTOR_REST_TOKEN must not be empty")
        _validate_namespace(namespace)
        self._rest_url = rest_url.rstrip("/")
        self._token = token
        self._namespace = namespace

    @property
    def namespace(self) -> str:
        return self._namespace

    def _endpoint(self, operation: str) -> str:
        return f"{self._rest_url}/{operation}/{quote(self._namespace, safe='')}"

    def _request(
        self, method: Literal["POST", "DELETE"], operation: str, payload: object
    ) -> dict[str, object]:
        try:
            import httpx
        except ImportError as error:
            raise UpstashVectorError(
                "httpx is required for Upstash Vector integration"
            ) from error

        try:
            response = httpx.request(
                method,
                self._endpoint(operation),
                headers={
                    "Authorization": f"Bearer {self._token}",
                    "Content-Type": "application/json",
                },
                content=json.dumps(payload),
                timeout=30.0,
            )
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise UpstashVectorError(
                f"Upstash Vector {operation} failed: {error}"
            ) from error

        try:
            body = response.json()
        except json.JSONDecodeError as error:
            raise UpstashVectorError("Upstash Vector returned invalid JSON") from error
        if not isinstance(body, dict):
            raise UpstashVectorError("Upstash Vector returned an invalid response")
        return body

    def upsert(
        self, chunks: Sequence[MarkdownChunk], vectors: npt.NDArray[np.float32]
    ) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("Upstash vectors do not match indexed chunks")
        for start in range(0, len(chunks), UPSERT_BATCH_SIZE):
            batch_chunks = chunks[start : start + UPSERT_BATCH_SIZE]
            batch_vectors = vectors[start : start + UPSERT_BATCH_SIZE]
            payload = [
                {
                    "id": chunk.id,
                    "vector": vector.tolist(),
                    "metadata": {
                        "path": chunk.path,
                        "source_path": chunk.path,
                        "topic": chunk.topic,
                        "heading": " > ".join(chunk.heading),
                        "heading_path": " > ".join(chunk.heading),
                        "ordinal": chunk.ordinal,
                        "checksum": chunk.checksum,
                    },
                }
                for chunk, vector in zip(batch_chunks, batch_vectors, strict=True)
            ]
            self._request("POST", "upsert", payload)

    def delete(self, vector_ids: Sequence[str]) -> None:
        if any(not CHUNK_ID_PATTERN.fullmatch(vector_id) for vector_id in vector_ids):
            raise ValueError("Upstash vector ids must be SHA-256 chunk identifiers")
        for start in range(0, len(vector_ids), UPSERT_BATCH_SIZE):
            self._request(
                "DELETE",
                "delete",
                {"ids": list(vector_ids[start : start + UPSERT_BATCH_SIZE])},
            )

    def query(self, vector: npt.NDArray[np.float32], limit: int) -> dict[str, float]:
        body = self._request(
            "POST",
            "query",
            {
                "vector": vector.tolist(),
                "topK": limit,
                "includeMetadata": False,
                "includeVectors": False,
            },
        )
        result = body.get("result")
        if not isinstance(result, list):
            raise UpstashVectorError(
                "Upstash Vector query response does not contain results"
            )

        scores: dict[str, float] = {}
        for item in result:
            if not isinstance(item, dict):
                raise UpstashVectorError("Upstash Vector query result is invalid")
            vector_id = item.get("id")
            score = item.get("score")
            if not isinstance(vector_id, str):
                raise UpstashVectorError("Upstash Vector query result is missing an id")
            if not isinstance(score, (int, float)) or isinstance(score, bool):
                raise UpstashVectorError(
                    "Upstash Vector query result is missing a numeric score"
                )
            scores[vector_id] = float(score)
        return scores


class RagService:
    def __init__(
        self,
        settings: Settings,
        embedder: EmbeddingProvider | None = None,
        reranker: RerankerProvider | None = None,
        upstash: UpstashVectorStore | None = None,
    ) -> None:
        self._settings = settings
        self._embedder = embedder or BgeM3Embedder(
            settings.embedding_model, settings.model_cache_dir
        )
        self._reranker = reranker or CrossEncoderReranker(
            settings.reranker_model, settings.model_cache_dir
        )
        self._upstash = upstash
        if self._upstash is None and settings.upstash_url and settings.upstash_token:
            self._upstash = UpstashVectorClient(
                settings.upstash_url,
                settings.upstash_token,
                settings.upstash_namespace,
            )
        self._index: LocalHybridIndex | None = None
        self._document_paths: tuple[str, ...] = ()
        self._state: Literal["idle", "indexing", "indexed", "failed"] = "idle"
        self._last_error: str | None = None
        self._warnings: tuple[str, ...] = ()
        self._upstash_synced = False
        self._state_lock = threading.RLock()
        self._index_lock = threading.Lock()

    @property
    def corpus_dir(self) -> Path:
        return self._settings.corpus_dir

    def status(self) -> ServiceStatus:
        with self._state_lock:
            index = self._index
            return ServiceStatus(
                state=self._state,
                document_count=len(self._document_paths),
                chunk_count=len(index.chunks) if index is not None else 0,
                embedding_status=self._embedder.status,
                reranker_status=self._reranker.status,
                vector_backend=index.vector_backend
                if index is not None
                else "disabled",
                upstash_enabled=self._upstash is not None,
                upstash_synced=self._upstash_synced,
                last_error=self._last_error,
                warnings=self._warnings,
            )

    def document_paths(self) -> list[str]:
        return [
            path.relative_to(self._settings.corpus_dir).as_posix()
            for path in discover_markdown_files(self._settings.corpus_dir)
        ]

    def _begin_index(self) -> None:
        if not self._index_lock.acquire(blocking=False):
            raise IndexingInProgressError("An index operation is already running")
        with self._state_lock:
            self._state = "indexing"
            self._last_error = None
            self._warnings = ()
            self._upstash_synced = False

    def _set_failure(self, error: str) -> None:
        with self._state_lock:
            self._state = "failed"
            self._last_error = error

    def _append_warning(self, warning: str) -> None:
        with self._state_lock:
            self._warnings = (*self._warnings, warning)[-4:]

    def _upstash_manifest_path(self) -> Path:
        if self._upstash is None:
            raise RuntimeError("Upstash manifest requested without an Upstash client")
        return self._settings.local_index_dir / (
            f"{UPSTASH_MANIFEST_PREFIX}{self._upstash.namespace}.json"
        )

    def _read_upstash_manifest(self) -> frozenset[str]:
        path = self._upstash_manifest_path()
        try:
            raw_manifest = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return frozenset()
        except OSError as error:
            raise OSError(f"Unable to read Upstash manifest: {path}") from error

        try:
            manifest = json.loads(raw_manifest)
        except json.JSONDecodeError as error:
            raise ValueError(f"Upstash manifest is not valid JSON: {path}") from error
        if not isinstance(manifest, dict):
            raise ValueError(f"Upstash manifest must be an object: {path}")
        if set(manifest) != {"version", "namespace", "chunk_ids"}:
            raise ValueError(f"Upstash manifest has an invalid schema: {path}")
        version = manifest["version"]
        namespace = manifest["namespace"]
        if type(version) is not int or version != UPSTASH_MANIFEST_VERSION:
            raise ValueError(f"Upstash manifest has an unsupported version: {path}")
        if (
            not isinstance(namespace, str)
            or self._upstash is None
            or namespace != self._upstash.namespace
        ):
            raise ValueError(f"Upstash manifest namespace does not match: {path}")
        chunk_ids = manifest["chunk_ids"]
        if (
            not isinstance(chunk_ids, list)
            or any(
                not isinstance(chunk_id, str)
                or CHUNK_ID_PATTERN.fullmatch(chunk_id) is None
                for chunk_id in chunk_ids
            )
            or len(chunk_ids) != len(set(chunk_ids))
        ):
            raise ValueError(f"Upstash manifest has invalid chunk ids: {path}")
        return frozenset(chunk_ids)

    def _write_upstash_manifest(self, chunk_ids: frozenset[str]) -> None:
        if any(CHUNK_ID_PATTERN.fullmatch(chunk_id) is None for chunk_id in chunk_ids):
            raise ValueError("Upstash manifest chunk ids must be SHA-256 identifiers")
        directory = self._settings.local_index_dir
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            raise OSError(
                f"Unable to create local index directory: {directory}"
            ) from error
        if not directory.is_dir():
            raise OSError(f"Local index path is not a directory: {directory}")

        path = self._upstash_manifest_path()
        temporary_path = path.with_suffix(".tmp")
        payload = {
            "version": UPSTASH_MANIFEST_VERSION,
            "namespace": self._upstash.namespace if self._upstash is not None else "",
            "chunk_ids": sorted(chunk_ids),
        }
        try:
            temporary_path.write_text(
                json.dumps(payload, separators=(",", ":")), encoding="utf-8"
            )
            temporary_path.replace(path)
        except OSError as error:
            raise OSError(f"Unable to write Upstash manifest: {path}") from error

    def _run_index(self, sync_upstash: bool) -> IndexReport:
        report: IndexReport | None = None
        known_failure = False
        try:
            documents, chunks = load_corpus(
                self._settings.corpus_dir,
                self._settings.chunk_tokens,
                self._settings.chunk_overlap_tokens,
            )
            warnings: list[str] = []
            vectors: npt.NDArray[np.float32] | None = None
            try:
                vectors = self._embedder.embed(
                    [chunk.retrieval_text for chunk in chunks]
                )
            except EmbeddingUnavailableError as error:
                warnings.append(str(error))

            index = LocalHybridIndex(chunks, vectors)
            upstash_synced = False
            if vectors is not None and sync_upstash and self._upstash is not None:
                try:
                    previous_chunk_ids = self._read_upstash_manifest()
                except (OSError, ValueError) as error:
                    previous_chunk_ids = frozenset()
                    warnings.append(
                        f"Upstash stale-vector cleanup was skipped: {error}"
                    )
                try:
                    self._upstash.upsert(chunks, vectors)
                    current_chunk_ids = frozenset(chunk.id for chunk in chunks)
                    stale_chunk_ids = previous_chunk_ids - current_chunk_ids
                    if stale_chunk_ids:
                        self._upstash.delete(sorted(stale_chunk_ids))
                    self._write_upstash_manifest(current_chunk_ids)
                    upstash_synced = True
                except (OSError, UpstashVectorError, ValueError) as error:
                    warnings.append(str(error))

            report = IndexReport(
                document_count=len(documents),
                chunk_count=len(chunks),
                embedding_status="ready" if vectors is not None else "unavailable",
                vector_backend=index.vector_backend,
                upstash_synced=upstash_synced,
                warnings=tuple(warnings),
            )
            with self._state_lock:
                self._index = index
                self._document_paths = tuple(
                    document.relative_to(self._settings.corpus_dir).as_posix()
                    for document in documents
                )
                self._state = "indexed"
                self._warnings = report.warnings
                self._upstash_synced = report.upstash_synced
            return report
        except (CorpusError, OSError, RuntimeError, ValueError) as error:
            known_failure = True
            self._set_failure(str(error))
            raise
        finally:
            if report is None and not known_failure:
                self._set_failure("Indexing stopped unexpectedly")
            self._index_lock.release()

    def index(self, sync_upstash: bool = True) -> IndexReport:
        self._begin_index()
        return self._run_index(sync_upstash)

    def _run_background_index(self, sync_upstash: bool) -> None:
        try:
            self._run_index(sync_upstash)
        except (CorpusError, OSError, RuntimeError, ValueError):
            return

    def start_background_index(self, sync_upstash: bool = True) -> bool:
        try:
            self._begin_index()
        except IndexingInProgressError:
            return False
        worker = threading.Thread(
            target=self._run_background_index,
            args=(sync_upstash,),
            name="rag-auto-index",
            daemon=True,
        )
        try:
            worker.start()
        except RuntimeError as error:
            self._set_failure(str(error))
            self._index_lock.release()
            raise
        return True

    def retrieve(
        self,
        query: str,
        limit: int,
        paths: frozenset[str] | None = None,
        backend: Literal["local", "upstash"] = "local",
    ) -> RetrievalResult:
        if not query.strip():
            raise ValueError("Query must not be blank")
        if limit < 1:
            raise ValueError("Retrieval limit must be at least one")
        with self._state_lock:
            index = self._index
            upstash_synced = self._upstash_synced
        if index is None:
            return RetrievalResult((), "unavailable", backend, False, False)

        if backend == "upstash":
            if self._upstash is None:
                raise RetrievalBackendUnavailableError(
                    "Upstash retrieval is not configured. Set UPSTASH_VECTOR_REST_URL and UPSTASH_VECTOR_REST_TOKEN."
                )
            if not upstash_synced:
                raise RetrievalBackendUnavailableError(
                    "Upstash retrieval is not indexed. Run indexing after configuring Upstash."
                )
            if not index.has_vectors:
                raise RetrievalBackendUnavailableError(
                    "Upstash retrieval requires the self-hosted BGE-M3 embedding model."
                )
            try:
                remote_query_vector = self._embedder.embed([query])[0]
            except EmbeddingUnavailableError as error:
                raise RetrievalBackendUnavailableError(str(error)) from error
            remote_scores = self._upstash.query(remote_query_vector, max(limit * 4, 12))
            hits = index.remote_hits(
                remote_scores,
                limit=max(limit * 4, 12),
                allowed_paths=paths,
            )
            reranked_hits, reranked = self._reranker.rerank(query, hits, limit)
            return RetrievalResult(
                tuple(reranked_hits), "hybrid", "upstash", reranked, True
            )

        query_vector: npt.NDArray[np.float32] | None = None
        if index.has_vectors:
            try:
                query_vector = self._embedder.embed([query])[0]
            except EmbeddingUnavailableError as error:
                self._append_warning(str(error))

        hits = index.search(
            query,
            limit=max(limit * 4, 12),
            query_vector=query_vector,
            allowed_paths=paths,
        )
        reranked_hits, reranked = self._reranker.rerank(query, hits, limit)
        mode: Literal["bm25", "hybrid"] = (
            "hybrid" if query_vector is not None else "bm25"
        )
        return RetrievalResult(tuple(reranked_hits), mode, "local", reranked, True)


def validate_relative_paths(paths: Sequence[str]) -> frozenset[str]:
    validated: set[str] = set()
    for path in paths:
        pure_path = PurePosixPath(path)
        if (
            not path
            or "\\" in path
            or pure_path.is_absolute()
            or any(part in {"", ".", ".."} for part in pure_path.parts)
        ):
            raise ValueError("Retrieval paths must be relative POSIX document paths")
        validated.add(path)
    return frozenset(validated)
