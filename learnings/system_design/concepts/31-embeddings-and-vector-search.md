# Embeddings and Vector Search

## Idea

An embedding maps content to a numeric vector; nearby vectors should represent
similar meaning. Approximate nearest-neighbor indexes trade exactness for speed.

## Classroom board

```text
document -> chunk -> embedding -> vector index + metadata
query -> embedding -> nearest candidates -> filter/rerank
```

## Design steps

1. Choose chunk/entity boundaries and embedding version.
2. Store vector with source ID, tenant, permissions, and freshness metadata.
3. Retrieve more candidates than needed, filter, then rerank.
4. Measure recall@k, latency, index freshness, and cost.

## Trade-offs and mistakes

Smaller chunks improve precision but lose context and increase volume. Never
mix incompatible embedding versions, filter permissions only after leaking
content, or evaluate retrieval only by anecdotal queries.
