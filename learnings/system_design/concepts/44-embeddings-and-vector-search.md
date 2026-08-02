# Embeddings and Vector Search

## Idea

Embeddings map content into vectors where distance approximates semantic
similarity. Approximate nearest-neighbor (ANN) indexes trade perfect recall for
lower latency and memory.

## Visual model

```text
content -> preprocess/chunk -> embedding model(version) -> vector + metadata
query   -> same embedding model -> ANN candidates -> filter/rerank -> results
```

## Design steps

1. Define retrieval unit, chunk boundaries, metadata, and access controls.
2. Version preprocessing and embedding model together.
3. Choose distance metric consistent with model training/normalization.
4. Select HNSW, IVF, product quantization, or exact search from scale/SLO.
5. Apply tenant/permission filters safely and rerank promising candidates.
6. Measure recall@k, relevance, latency, index freshness, and memory.

## When to use it

Use vector search for semantic similarity, recommendations, deduplication, and
RAG. Keep lexical search when exact terms, identifiers, or rare names matter;
hybrid retrieval often performs best.

## Trade-offs

Higher ANN recall uses more probes, memory, or latency. Smaller quantized vectors
reduce cost but can lose ranking quality. Larger chunks preserve context but
reduce retrieval precision.

## Versioning and operations

- Store model/version beside every vector.
- Re-embed into a new index and cut over; do not mix incompatible vectors.
- Track deleted/expired source documents through the index.
- Evaluate by language, content type, tenant, and query class.

## Common mistakes

- Calling cosine similarity “semantic correctness.”
- Mixing vectors from different embedding models.
- Applying permissions after retrieval and leaking existence/content.
- Tuning ANN latency without measuring recall and end-task quality.
