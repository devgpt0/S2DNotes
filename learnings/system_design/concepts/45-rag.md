# Retrieval-Augmented Generation (RAG)

## Idea

RAG retrieves trusted evidence at request time and gives it to a model. Its
quality depends on ingestion, retrieval, context construction, generation, and
evaluation—not only the LLM.

## Visual model

```text
sources -> parse/chunk -> index + ACL + version
query -> rewrite -> hybrid retrieve -> rerank -> context with citations
      -> LLM -> grounded answer -> verification/feedback
```

## Design steps

1. Define answerable scope, freshness, citation, refusal, latency, and cost.
2. Build idempotent ingestion with source lineage and deletion propagation.
3. Retrieve lexical/vector candidates under the caller's access controls.
4. Rerank, deduplicate, diversify, and fit evidence into a token budget.
5. Instruct the model to distinguish evidence from user instructions and abstain.
6. Return citations tied to immutable source spans/versions.
7. Evaluate retrieval and generation separately, then end-to-end.

## When to use it

Use RAG for changing/private knowledge that can be retrieved. Fine-tuning is
better for behavior/style or learned task patterns; it is not a reliable factual
database.

## Trade-offs

More retrieved context can lower answer quality through noise and raise cost.
Fresh indexing improves knowledge but can expose unreviewed or poisoned content.

## Critical metrics

- Retrieval recall/precision and reranker quality.
- Citation correctness, groundedness, answer relevance, abstention quality.
- Index freshness, permission failures, p95 latency, tokens, and cost.

## Common mistakes

- Evaluating only fluent final answers.
- Treating retrieved text as trusted instructions.
- Chunking by fixed length without document structure.
- Returning citations that do not support the generated claim.
