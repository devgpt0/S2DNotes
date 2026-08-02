# Search Systems

## Idea

Search uses a derived index optimized for text relevance and filtering; the
authoritative database remains the source of truth.

## Classroom board

```text
database change -> outbox/stream -> indexer -> inverted/vector index
query -> parse -> retrieve candidates -> rank -> filter permissions -> results
```

## Design steps

1. Define searchable fields, filters, freshness, ranking, and permissions.
2. Build documents through a replayable indexing pipeline.
3. Retrieve candidates, rank them, and enforce access control.
4. Version indexes and rebuild/alias-switch safely.

## When to use it

Use inverted indexes for lexical search and vector indexes for semantic
similarity; hybrid retrieval often combines both.

## Trade-offs and mistakes

Freshness costs indexing throughput. Never dual-write DB and index without
recovery, trust stale index permissions, or confuse retrieval score with
business ranking quality.
