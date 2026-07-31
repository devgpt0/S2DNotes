from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Literal

import numpy as np
import numpy.typing as npt
from fastapi.testclient import TestClient

from app.main import create_app
from app.rag import EmbeddingUnavailableError, RagService, RetrievalHit, Settings


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


def test_api_indexes_tree_and_returns_citations(tmp_path: Path) -> None:
    document = tmp_path / "python" / "lesson.md"
    document.parent.mkdir()
    document.write_text("# Functions\nFunctions reuse behavior.", encoding="utf-8")
    service = RagService(
        Settings(corpus_dir=tmp_path),
        embedder=UnavailableEmbedder(),
        reranker=PassthroughReranker(),
    )
    app = create_app(Settings(corpus_dir=tmp_path), service)

    with TestClient(app) as client:
        health = client.get("/health")
        indexed = client.post("/index")
        tree = client.get("/tree")
        retrieved = client.post("/retrieve", json={"query": "Functions", "limit": 3})

    assert health.status_code == 200
    assert health.json()["index_state"] == "idle"
    assert indexed.status_code == 200
    assert indexed.json()["embedding_status"] == "unavailable"
    assert tree.json()["files"] == ["python/lesson.md"]
    assert retrieved.json()["citations"][0]["heading"] == "Functions"
    assert retrieved.json()["backend"] == "local"


def test_retrieve_rejects_coerced_request_values(tmp_path: Path) -> None:
    app = create_app(
        Settings(corpus_dir=tmp_path), RagService(Settings(corpus_dir=tmp_path))
    )

    with TestClient(app) as client:
        response = client.post("/retrieve", json={"query": "lesson", "limit": "3"})

    assert response.status_code == 422


def test_retrieve_rejects_unknown_backend(tmp_path: Path) -> None:
    app = create_app(
        Settings(corpus_dir=tmp_path), RagService(Settings(corpus_dir=tmp_path))
    )

    with TestClient(app) as client:
        response = client.post(
            "/retrieve", json={"query": "lesson", "backend": "remote"}
        )

    assert response.status_code == 422


def test_retrieve_uses_a_nonempty_heading_for_preamble_content(tmp_path: Path) -> None:
    document = tmp_path / "preamble.md"
    document.write_text("Preamble content about queues.", encoding="utf-8")
    service = RagService(
        Settings(corpus_dir=tmp_path),
        embedder=UnavailableEmbedder(),
        reranker=PassthroughReranker(),
    )
    app = create_app(Settings(corpus_dir=tmp_path), service)

    with TestClient(app) as client:
        client.post("/index")
        response = client.post("/retrieve", json={"query": "queues"})

    assert response.status_code == 200
    assert response.json()["citations"][0]["heading"] == "Document"
