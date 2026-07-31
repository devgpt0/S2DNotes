from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from types import SimpleNamespace
from typing import Literal
from unittest.mock import Mock, patch

import numpy as np
import numpy.typing as npt
import pytest

from app.rag import (
    BgeM3Embedder,
    CrossEncoderReranker,
    EmbeddingUnavailableError,
    LocalHybridIndex,
    MarkdownChunk,
    RagService,
    RetrievalBackendUnavailableError,
    RetrievalHit,
    Settings,
    UpstashVectorClient,
    chunk_markdown,
    discover_markdown_files,
    read_markdown,
    validate_relative_paths,
)


class UnavailableEmbedder:
    status: Literal["uninitialized", "ready", "unavailable"] = "unavailable"

    def embed(self, texts: Sequence[str]) -> npt.NDArray[np.float32]:
        raise EmbeddingUnavailableError("BGE-M3 is unavailable for this test")


class PassthroughReranker:
    status: Literal["uninitialized", "ready", "unavailable"] = "unavailable"

    def rerank(
        self, query: str, hits: Sequence[RetrievalHit], limit: int
    ) -> tuple[list[RetrievalHit], bool]:
        return list(hits[:limit]), False


class ReadyEmbedder:
    status: Literal["uninitialized", "ready", "unavailable"] = "ready"

    def __init__(self) -> None:
        self.inputs: list[list[str]] = []

    def embed(self, texts: Sequence[str]) -> npt.NDArray[np.float32]:
        self.inputs.append(list(texts))
        vectors = [
            [1.0, 0.0] if index % 2 == 0 else [0.0, 1.0]
            for index, _ in enumerate(texts)
        ]
        return np.asarray(vectors, dtype=np.float32)


class ReversingReranker:
    status: Literal["uninitialized", "ready", "unavailable"] = "ready"

    def __init__(self) -> None:
        self.calls: list[list[RetrievalHit]] = []

    def rerank(
        self, query: str, hits: Sequence[RetrievalHit], limit: int
    ) -> tuple[list[RetrievalHit], bool]:
        self.calls.append(list(hits))
        return list(reversed(hits[:limit])), True


class RecordingUpstash:
    namespace = "genius-test"

    def __init__(self) -> None:
        self.chunk_ids: list[str] = []
        self.deleted_ids: list[list[str]] = []
        self.query_limits: list[int] = []

    def upsert(
        self, chunks: Sequence[MarkdownChunk], vectors: npt.NDArray[np.float32]
    ) -> None:
        assert len(chunks) == len(vectors)
        self.chunk_ids = [chunk.id for chunk in chunks]

    def delete(self, vector_ids: Sequence[str]) -> None:
        self.deleted_ids.append(list(vector_ids))

    def query(self, vector: npt.NDArray[np.float32], limit: int) -> dict[str, float]:
        assert vector.shape == (2,)
        self.query_limits.append(limit)
        return {
            "f" * 64: 1.0,
            self.chunk_ids[0]: 0.9,
            self.chunk_ids[1]: 0.2,
        }


def test_chunk_markdown_uses_nested_heading_paths_and_ignores_fenced_headings() -> None:
    markdown = """# Python
Overview text.

## Lists
List content.

```python
# This is code, not a Markdown heading.
```
"""

    chunks = chunk_markdown(markdown, "python/lesson.md")

    assert [chunk.heading for chunk in chunks] == [("Python",), ("Python", "Lists")]
    assert chunks[0].text == "Overview text."
    assert "# This is code" in chunks[1].text
    assert chunks[1].retrieval_text.startswith("Python > Lists")
    assert chunks[1].topic == "python"
    assert len(chunks[1].checksum) == 64


def test_chunk_markdown_uses_token_limits_and_overlap_without_splitting_code() -> None:
    words = [f"word{index}" for index in range(1_500)]
    chunks = chunk_markdown("# Topic\n" + " ".join(words), "topic/long.md")
    tokenized_chunks = [chunk.text.split() for chunk in chunks]

    assert max(len(tokens) for tokens in tokenized_chunks) <= 700
    assert tokenized_chunks[0][-100:] == tokenized_chunks[1][:100]

    code_block = (
        "```python\n"
        + "\n".join(f"value_{index} = {index}" for index in range(40))
        + "\n```"
    )
    code_chunks = chunk_markdown(
        "# Code\n"
        + " ".join(f"before{index}" for index in range(650))
        + "\n\n"
        + code_block
        + "\n\n"
        + " ".join(f"after{index}" for index in range(200)),
        "topic/code.md",
    )

    assert any(code_block in chunk.text for chunk in code_chunks)
    assert all(chunk.text.count("```") in {0, 2} for chunk in code_chunks)


def test_discover_markdown_files_excludes_build_and_dependency_directories(
    tmp_path: Path,
) -> None:
    included = tmp_path / "notes" / "lesson.md"
    included.parent.mkdir()
    included.write_text("# Lesson\nContent", encoding="utf-8")
    for directory in ("node_modules", ".git", "build", "dist", "venv", "vendor"):
        ignored = tmp_path / directory
        ignored.mkdir()
        (ignored / "ignored.md").write_text("# Ignored", encoding="utf-8")
    (tmp_path / "empty.md").touch()

    assert discover_markdown_files(tmp_path) == [included]


def test_read_markdown_explicitly_supports_windows_1252(tmp_path: Path) -> None:
    document = tmp_path / "legacy.md"
    document.write_bytes("Smart “quotes”".encode("windows-1252"))

    assert read_markdown(document) == "Smart “quotes”"


def test_chunk_ids_stay_stable_when_a_document_is_reindexed() -> None:
    original = chunk_markdown("# Lesson\nOriginal content", "lesson.md")
    updated = chunk_markdown("# Lesson\nUpdated content", "lesson.md")

    assert original[0].id == updated[0].id


def test_hybrid_index_combines_bm25_and_dense_vector_results() -> None:
    chunks = chunk_markdown("# Alpha\nfirst topic", "alpha.md") + chunk_markdown(
        "# Beta\nsecond topic", "beta.md"
    )
    vectors = np.asarray([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    index = LocalHybridIndex(chunks, vectors)

    results = index.search(
        "beta",
        limit=1,
        query_vector=np.asarray([0.0, 1.0], dtype=np.float32),
    )

    assert results[0].chunk.path == "beta.md"
    assert results[0].score > 0


def test_self_hosted_models_use_the_configured_persistent_cache(
    tmp_path: Path,
) -> None:
    bge_constructor_args: dict[str, object] = {}
    reranker_constructor_args: dict[str, object] = {}

    class FakeBgeModel:
        def __init__(self, model_name: str, **kwargs: object) -> None:
            bge_constructor_args["model_name"] = model_name
            bge_constructor_args.update(kwargs)

        def encode(self, texts: list[str], **kwargs: object) -> dict[str, object]:
            assert texts == ["Embedding input"]
            assert kwargs["return_dense"] is True
            return {"dense_vecs": [[1.0, 0.0]]}

    class FakeCrossEncoder:
        def __init__(self, model_name: str, **kwargs: object) -> None:
            reranker_constructor_args["model_name"] = model_name
            reranker_constructor_args.update(kwargs)

        def predict(self, pairs: list[tuple[str, str]]) -> list[float]:
            assert len(pairs) == 1
            return [0.75]

    def fake_import(module_name: str) -> SimpleNamespace:
        if module_name == "FlagEmbedding":
            return SimpleNamespace(BGEM3FlagModel=FakeBgeModel)
        if module_name == "sentence_transformers":
            return SimpleNamespace(CrossEncoder=FakeCrossEncoder)
        raise AssertionError(f"Unexpected import: {module_name}")

    cache_dir = tmp_path / "models"
    chunk = chunk_markdown("# Lesson\nContent", "lesson.md")[0]
    with patch("app.rag.importlib.import_module", side_effect=fake_import):
        embedder = BgeM3Embedder("BAAI/bge-m3", cache_dir)
        reranker = CrossEncoderReranker("BAAI/bge-reranker-v2-m3", cache_dir)
        vectors = embedder.embed(["Embedding input"])
        hits, reranked = reranker.rerank(
            "lesson", [RetrievalHit(chunk=chunk, score=1.0)], limit=1
        )

    assert cache_dir.is_dir()
    assert bge_constructor_args == {
        "model_name": "BAAI/bge-m3",
        "use_fp16": False,
        "cache_dir": str(cache_dir),
    }
    assert reranker_constructor_args == {
        "model_name": "BAAI/bge-reranker-v2-m3",
        "max_length": 512,
        "cache_folder": str(cache_dir),
    }
    assert vectors.shape == (1, 2)
    assert reranked is True
    assert hits[0].score == pytest.approx(0.75)


def test_settings_reads_model_cache_and_local_index_directories(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model_cache_dir = tmp_path / "cache"
    local_index_dir = tmp_path / "index"
    monkeypatch.setenv("LEARNINGS_ROOT", str(tmp_path))
    monkeypatch.setenv("MODEL_CACHE_DIR", str(model_cache_dir))
    monkeypatch.setenv("LOCAL_INDEX_DIR", str(local_index_dir))
    monkeypatch.delenv("RAG_CORPUS_DIR", raising=False)
    monkeypatch.delenv("UPSTASH_VECTOR_REST_URL", raising=False)
    monkeypatch.delenv("UPSTASH_VECTOR_REST_TOKEN", raising=False)

    settings = Settings.from_environment()

    assert settings.model_cache_dir == model_cache_dir.resolve()
    assert settings.local_index_dir == local_index_dir.resolve()


@patch("httpx.request")
def test_upstash_upsert_uses_stable_chunk_ids(request: Mock) -> None:
    response = Mock()
    response.json.return_value = {"result": "Success"}
    request.return_value = response
    chunk = chunk_markdown("# Lesson\nContent", "lesson.md")[0]
    client = UpstashVectorClient("https://example.upstash.io", "token", "genius-rag")

    client.upsert([chunk], np.asarray([[1.0, 0.0]], dtype=np.float32))

    assert request.call_args.args == (
        "POST",
        "https://example.upstash.io/upsert/genius-rag",
    )
    assert chunk.id in request.call_args.kwargs["content"]
    payload = request.call_args.kwargs["content"]
    assert '"source_path": "lesson.md"' in payload
    assert '"topic": "root"' in payload
    assert '"heading_path": "Lesson"' in payload
    assert '"checksum"' in payload
    response.raise_for_status.assert_called_once_with()


@patch("httpx.request")
def test_upstash_delete_uses_the_namespace_and_chunk_ids(request: Mock) -> None:
    response = Mock()
    response.json.return_value = {"result": {"deleted": 1}}
    request.return_value = response
    chunk = chunk_markdown("# Lesson\nContent", "lesson.md")[0]
    client = UpstashVectorClient("https://example.upstash.io", "token", "genius-rag")

    client.delete([chunk.id])

    assert request.call_args.args == (
        "DELETE",
        "https://example.upstash.io/delete/genius-rag",
    )
    assert request.call_args.kwargs["content"] == f'{{"ids": ["{chunk.id}"]}}'


def test_service_keeps_bm25_retrieval_when_embeddings_are_unavailable(
    tmp_path: Path,
) -> None:
    document = tmp_path / "python" / "lesson.md"
    document.parent.mkdir()
    document.write_text(
        "# Python\nPython functions define reusable behavior.", encoding="utf-8"
    )
    service = RagService(
        Settings(corpus_dir=tmp_path),
        embedder=UnavailableEmbedder(),
        reranker=PassthroughReranker(),
    )

    report = service.index()
    result = service.retrieve("Python functions", limit=3)

    assert report.embedding_status == "unavailable"
    assert report.vector_backend == "disabled"
    assert result.mode == "bm25"
    assert result.backend == "local"
    assert result.hits[0].chunk.path == "python/lesson.md"


def test_selected_upstash_retrieval_filters_stale_ids_and_reranks(
    tmp_path: Path,
) -> None:
    alpha = tmp_path / "alpha.md"
    beta = tmp_path / "beta.md"
    alpha.write_text("# Alpha\nFirst lesson.", encoding="utf-8")
    beta.write_text("# Beta\nSecond lesson.", encoding="utf-8")
    embedder = ReadyEmbedder()
    reranker = ReversingReranker()
    upstash = RecordingUpstash()
    service = RagService(
        Settings(corpus_dir=tmp_path, local_index_dir=tmp_path / "index"),
        embedder=embedder,
        reranker=reranker,
        upstash=upstash,
    )

    report = service.index()
    result = service.retrieve("second", limit=2, backend="upstash")

    assert report.upstash_synced is True
    assert result.backend == "upstash"
    assert result.mode == "hybrid"
    assert result.reranked is True
    assert [hit.chunk.path for hit in reranker.calls[0]] == ["alpha.md", "beta.md"]
    assert [hit.chunk.path for hit in result.hits] == ["beta.md", "alpha.md"]
    assert upstash.query_limits == [12]
    assert len(embedder.inputs) == 2


def test_reindex_removes_stale_upstash_vectors_from_prior_manifest(
    tmp_path: Path,
) -> None:
    alpha = tmp_path / "alpha.md"
    beta = tmp_path / "beta.md"
    alpha.write_text("# Alpha\nFirst lesson.", encoding="utf-8")
    beta.write_text("# Beta\nSecond lesson.", encoding="utf-8")
    upstash = RecordingUpstash()
    service = RagService(
        Settings(corpus_dir=tmp_path, local_index_dir=tmp_path / "index"),
        embedder=ReadyEmbedder(),
        reranker=PassthroughReranker(),
        upstash=upstash,
    )

    service.index()
    stale_id = next(
        chunk.id
        for chunk in chunk_markdown(beta.read_text(encoding="utf-8"), "beta.md")
    )
    beta.unlink()
    report = service.index()

    assert report.upstash_synced is True
    assert upstash.deleted_ids == [[stale_id]]


def test_upstash_backend_fails_when_it_has_not_been_configured(tmp_path: Path) -> None:
    document = tmp_path / "lesson.md"
    document.write_text("# Lesson\nA local lesson.", encoding="utf-8")
    service = RagService(
        Settings(corpus_dir=tmp_path),
        embedder=UnavailableEmbedder(),
        reranker=PassthroughReranker(),
    )
    service.index()

    with pytest.raises(RetrievalBackendUnavailableError, match="not configured"):
        service.retrieve("lesson", limit=1, backend="upstash")


@pytest.mark.parametrize(
    "path", ["../secret.md", "/etc/passwd", "folder\\lesson.md", ""]
)
def test_validate_relative_paths_rejects_unsafe_paths(path: str) -> None:
    with pytest.raises(ValueError, match="relative POSIX"):
        validate_relative_paths([path])
