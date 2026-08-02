# Retrieval-Augmented Generation (RAG)

## Idea

RAG retrieves trusted context for a model at request time so answers can use
current private knowledge and cite sources.

## Classroom board

```text
question -> rewrite -> hybrid retrieve -> rerank -> context budget
         -> model with instructions -> cited answer / abstain
```

## Design steps

1. Ingest, parse, chunk, deduplicate, embed, and track source versions.
2. Enforce tenant/ACL filters during retrieval.
3. Combine lexical/vector candidates and rerank.
4. Build a bounded prompt with citations and injection-resistant boundaries.
5. Evaluate retrieval separately from generation.

## Trade-offs and mistakes

More context costs latency and may reduce focus. Do not treat retrieved text as
instructions, hide missing evidence, ignore document deletion, or blame the
model for retrieval failures.
