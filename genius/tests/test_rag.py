from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
import pytest

from genius_app.rag import (
    EMBEDDING_DIMENSION,
    DocumentChunk,
    InMemoryVectorStore,
    LocalEmbeddingModel,
    UpstashVectorStore,
    discover_documents,
    index_corpus,
    load_document,
    search_documents,
    split_document,
)


def test_split_document_creates_stable_overlapping_chunks() -> None:
    text = "word " * 1_000

    first = split_document(text, "notes/example.md")
    second = split_document(text, "notes/example.md")

    assert len(first) > 1
    assert [chunk.id for chunk in first] == [chunk.id for chunk in second]
    assert all(chunk.source == "notes/example.md" for chunk in first)


def test_in_memory_store_returns_closest_vector() -> None:
    chunks = split_document("first document", "first.md") + split_document(
        "second document", "second.md"
    )
    first = np.zeros(EMBEDDING_DIMENSION, dtype=np.float32)
    second = np.zeros(EMBEDDING_DIMENSION, dtype=np.float32)
    first[0] = 1
    second[1] = 1
    store = InMemoryVectorStore()
    store.replace(chunks, [first, second])

    results = store.search(second, top_k=1)

    assert results[0].chunk.source == "second.md"
    assert results[0].score == pytest.approx(1.0)


def test_discover_documents_excludes_hidden_and_virtual_environment_files(
    tmp_path: Path,
) -> None:
    included = tmp_path / "lesson.md"
    included.write_text("lesson", encoding="utf-8")
    ignored_directory = tmp_path / ".venv"
    ignored_directory.mkdir()
    (ignored_directory / "package.txt").write_text("package", encoding="utf-8")
    metadata_directory = tmp_path / "package.egg-info"
    metadata_directory.mkdir()
    (metadata_directory / "metadata.txt").write_text("metadata", encoding="utf-8")
    (tmp_path / "empty.md").touch()

    assert discover_documents(tmp_path) == [included]


def test_load_document_supports_windows_1252_text(tmp_path: Path) -> None:
    document = tmp_path / "legacy.md"
    document.write_bytes("Smart “quotes”".encode("windows-1252"))

    assert load_document(document) == "Smart “quotes”"


@patch("genius_app.rag.requests.post")
def test_upstash_batch_upsert_sends_vector_array(post: Mock) -> None:
    response = Mock()
    post.return_value = response
    store = UpstashVectorStore("https://example.upstash.io", "token")
    chunk = DocumentChunk(id="chunk-id", source="lesson.md", index=0, text="lesson")
    vector = [0.0] * EMBEDDING_DIMENSION

    store.upsert([chunk], [vector])

    payload = post.call_args.kwargs["json"]
    assert isinstance(payload, list)
    assert payload == [
        {
            "id": "chunk-id",
            "vector": vector,
            "metadata": {
                "source": "lesson.md",
                "chunk_index": 0,
                "text": "lesson",
            },
        }
    ]
    response.raise_for_status.assert_called_once_with()


@pytest.mark.parametrize(
    ("vector_count", "pending_vector_count", "expected"),
    [(0, 0, False), (1, 0, True), (0, 1, True)],
)
@patch("genius_app.rag.requests.get")
def test_upstash_detects_existing_vectors(
    get: Mock,
    vector_count: int,
    pending_vector_count: int,
    expected: bool,
) -> None:
    response = Mock()
    response.json.return_value = {
        "result": {
            "dimension": EMBEDDING_DIMENSION,
            "namespaces": {
                "": {
                    "vectorCount": vector_count,
                    "pendingVectorCount": pending_vector_count,
                }
            },
        }
    }
    get.return_value = response
    store = UpstashVectorStore("https://example.upstash.io", "token")

    assert store.contains_vectors() is expected
    response.raise_for_status.assert_called_once_with()


@patch("genius_app.rag.requests.post")
def test_upstash_uses_embedding_namespace(post: Mock) -> None:
    post.return_value = Mock()
    store = UpstashVectorStore(
        "https://example.upstash.io",
        "token",
        "local-bge",
    )
    chunk = DocumentChunk(id="chunk-id", source="lesson.md", index=0, text="lesson")

    store.upsert([chunk], [[0.0] * EMBEDDING_DIMENSION])

    assert post.call_args.args[0] == "https://example.upstash.io/upsert/local-bge"


@patch("sentence_transformers.SentenceTransformer")
def test_local_embedding_model_returns_native_normalized_vectors(
    sentence_transformer: Mock,
) -> None:
    expected = np.zeros((1, EMBEDDING_DIMENSION), dtype=np.float32)
    expected[0, :2] = [0.6, 0.8]
    sentence_transformer.return_value.encode.return_value = expected
    model = LocalEmbeddingModel()

    vector = model.embed_texts(["document"], "RETRIEVAL_DOCUMENT")[0]

    assert len(vector) == EMBEDDING_DIMENSION
    assert vector[:2] == pytest.approx([0.6, 0.8])
    sentence_transformer.return_value.encode.assert_called_once()


def test_index_corpus_embeds_once_and_populates_both_stores(tmp_path: Path) -> None:
    document = tmp_path / "lesson.md"
    document.write_text("lesson", encoding="utf-8")
    vector = [0.0] * EMBEDDING_DIMENSION
    vector[0] = 1.0
    embedding_model = Mock(spec=LocalEmbeddingModel)
    embedding_model.cache_key = "local-test-model"
    embedding_model.embed_texts.return_value = [vector]
    memory_store = InMemoryVectorStore()
    upstash_store = Mock(spec=UpstashVectorStore)

    stats = index_corpus(
        tmp_path,
        memory_store,
        embedding_model,
        mirror_store=upstash_store,
    )

    assert stats.document_count == 1
    assert stats.chunk_count == 1
    embedding_model.embed_texts.assert_called_once()
    upstash_store.upsert.assert_called_once()
    assert not memory_store.is_empty


def test_index_corpus_reuses_local_embedding_checkpoint(tmp_path: Path) -> None:
    document = tmp_path / "lesson.md"
    document.write_text("lesson", encoding="utf-8")
    vector = [0.0] * EMBEDDING_DIMENSION
    vector[0] = 1.0
    embedding_model = Mock(spec=LocalEmbeddingModel)
    embedding_model.cache_key = "local-test-model"
    embedding_model.embed_texts.return_value = [vector]
    cache_file = tmp_path / "cache" / "embeddings.npz"

    index_corpus(
        tmp_path,
        InMemoryVectorStore(),
        embedding_model,
        cache_file=cache_file,
    )
    index_corpus(
        tmp_path,
        InMemoryVectorStore(),
        embedding_model,
        cache_file=cache_file,
    )

    embedding_model.embed_texts.assert_called_once()


def test_index_corpus_skips_existing_upstash_vectors(tmp_path: Path) -> None:
    document = tmp_path / "lesson.md"
    document.write_text("lesson", encoding="utf-8")
    vector = [0.0] * EMBEDDING_DIMENSION
    vector[0] = 1.0
    embedding_model = Mock(spec=LocalEmbeddingModel)
    embedding_model.cache_key = "local-test-model"
    embedding_model.embed_texts.return_value = [vector]
    upstash_store = Mock(spec=UpstashVectorStore)

    index_corpus(
        tmp_path,
        InMemoryVectorStore(),
        embedding_model,
        mirror_store=upstash_store,
        mirror_existing_count=1,
    )

    upstash_store.upsert.assert_not_called()


def test_index_corpus_uses_bge_m3_embedding_model(tmp_path: Path) -> None:
    document = tmp_path / "lesson.md"
    document.write_text("lesson", encoding="utf-8")
    vector = [0.0] * EMBEDDING_DIMENSION
    vector[0] = 1.0
    local_model = Mock(spec=LocalEmbeddingModel)
    local_model.cache_key = "local-test-model"
    local_model.embed_texts.return_value = [vector]

    index_corpus(
        tmp_path,
        InMemoryVectorStore(),
        local_model,
    )

    local_model.embed_texts.assert_called_once()


def test_search_documents_reports_retrieval_activities() -> None:
    vector = [0.0] * EMBEDDING_DIMENSION
    vector[0] = 1.0
    embedding_model = Mock(spec=LocalEmbeddingModel)
    embedding_model.embed_texts.return_value = [vector]
    store = Mock(spec=InMemoryVectorStore)
    result = Mock()
    store.search.return_value = [result]
    activity = Mock()

    results = search_documents("question", store, 3, embedding_model, activity)

    assert results == [result]
    assert [call.args[0] for call in activity.call_args_list] == [
        "Creating a query embedding",
        "Searching the selected vector store",
        "Reading 1 relevant chunks",
    ]
