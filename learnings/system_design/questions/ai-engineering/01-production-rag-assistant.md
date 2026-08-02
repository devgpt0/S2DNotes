# Design a Production RAG Assistant

> **Difficulty:** Hard  
> **Main focus:** ingestion, retrieval quality, grounding

## Interview prompt

Design an enterprise assistant that answers questions from private documents and cites evidence.

## 1. Clarify the product and success criteria

**What I would say first:** I will define answer quality and access control before choosing a model. Retrieval must enforce document permissions before any text enters the prompt.

### Functional requirements

- Ingest documents from multiple connectors and keep them fresh.
- Answer questions with citations and an honest no-answer state.
- Respect user, group, tenant, and document permissions.
- Evaluate retrieval, groundedness, latency, safety, and cost.

### AI and product constraints

- Documents change, permissions change, and formats vary.
- The context window is finite; irrelevant text can reduce answer quality.
- Retrieved content is untrusted and can contain prompt injection.

## 2. Contracts and data

- POST /v1/sources/{id}/sync
- POST /v1/answers {conversationId, query, filters} -> streamed answer and citations
- Chunk metadata includes documentId, version, ACL reference, section path, offsets, and content hash

## 3. High-level design

```text
connectors -> parse/scan -> chunk -> embed -> vector index
     |                         |                |
     +-> source versions ------+-> keyword index
     +-> ACL/change log

query -> auth/intent -> hybrid retrieval -> ACL filter -> reranker
      -> context builder -> model -> citation/grounding checks -> stream
                         |
                      evaluation traces
```

## 4. Critical request flow

1. Resolve the authenticated user's tenant and current group permissions.
2. Rewrite or expand the query only when evaluation proves it helps.
3. Retrieve candidates from keyword and vector indexes with metadata filters.
4. Apply authoritative ACL checks, rerank, deduplicate, and enforce a token budget.
5. Generate with source boundaries, validate citations, and abstain when evidence is insufficient.

## 5. Quality and evaluation

- Measure retrieval recall at k separately from answer correctness.
- Maintain versioned golden queries with expected sources, answer criteria, and refusal cases.
- Evaluate citation entailment: the cited text must actually support the claim.
- Run online feedback analysis carefully because clicks and thumbs are noisy signals.

## 6. Reliability, scale, observability, and cost

- Use content hashes for idempotent ingestion and tombstones for deletes.
- Keep keyword fallback when embedding service or vector index is degraded.
- Cache only permission-safe retrieval or final results with tenant, identity, version, and policy in the key.
- Track ingestion lag, retrieval recall proxies, abstention, citation failures, latency by stage, tokens, and cost.

## 7. Safety, security, and privacy

- Treat documents as data, never as higher-priority instructions.
- Strip active content, scan files, isolate parsers, and defend connectors against SSRF.
- Log document references rather than unrestricted content and honor deletion across derived indexes.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Large chunks | More context per result but less precise retrieval. |
| Small chunks | Precise matches with lost surrounding meaning. |
| Vector-only | Semantic recall but weaker exact identifiers. |
| Hybrid retrieval | Better coverage with tuning and operational complexity. |

## 9. 60-second interview summary

A versioned ingestion pipeline builds keyword and vector indexes with document lineage and ACL metadata. Query-time hybrid retrieval is authorization-filtered and reranked before a budgeted prompt. Citations, abstention, staged evaluation, and deletion propagation make the system trustworthy.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

