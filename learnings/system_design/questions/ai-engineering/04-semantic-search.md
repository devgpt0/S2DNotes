# Design a Semantic Search System

> **Difficulty:** Medium  
> **Main focus:** hybrid retrieval, indexing, relevance

## Interview prompt

Design search that understands meaning while preserving exact keyword and filter behavior.

## 1. Clarify the product and success criteria

**What I would say first:** Semantic retrieval complements lexical search; it does not replace exact identifiers, filters, or access control. I will build a hybrid candidate and reranking pipeline.

### Functional requirements

- Index documents and support text, semantic, and metadata queries.
- Return relevant ranked results with snippets.
- Apply tenant and document permissions.
- Keep updates, deletes, and model migrations correct.

### AI and product constraints

- Embedding versions change and are not directly comparable.
- Approximate nearest-neighbor search trades recall for latency.
- Exact terms such as error codes often matter more than semantic similarity.

## 2. Contracts and data

- POST /v1/documents {id, version, textRef, metadata, aclRef}
- POST /v1/search {query, filters, limit, cursor}
- Indexed record includes content version, embedding version, lexical fields, metadata, and ACL reference

## 3. High-level design

```text
documents -> validate/chunk -> lexical index
                    |         -> embedding service -> vector index
                    +-> change/delete log

query -> normalize -> lexical retrieval ----\
                -> query embedding -> ANN ----> merge -> ACL -> rerank -> snippets
                -> filters -----------------/
```

## 4. Critical request flow

1. Parse query, structured filters, tenant, and permission context.
2. Retrieve lexical and vector candidates independently.
3. Merge by rank-aware fusion, then apply authoritative ACL and metadata checks.
4. Rerank a bounded candidate set with a stronger model or learned score.
5. Generate snippets from original text and return stable result IDs and versions.

## 5. Quality and evaluation

- Build labeled query-result judgments and report recall, NDCG, MRR, and zero-result rate.
- Segment exact-ID, navigational, broad semantic, and filtered queries.
- Compare embedding or reranker changes using shadow indexes and online experiments.
- Measure permission-filter effects separately so security filtering is not mistaken for poor retrieval.

## 6. Reliability, scale, observability, and cost

- Use idempotent versioned indexing and tombstones for delete propagation.
- During embedding migration, dual-index or backfill into a new version then atomically switch.
- Fallback to lexical search if vector infrastructure fails.
- Track indexing lag, ANN latency/recall proxy, reranker latency, stale deletes, and cost per query.

## 7. Safety, security, and privacy

- Apply tenant and ACL filtering before content leaves the search boundary.
- Treat documents and snippets as untrusted output and sanitize rendering.
- Limit sensitive query logging and support deletion from every index version.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Lexical search | Excellent exact matching but weaker paraphrase recall. |
| Vector search | Semantic recall but approximate and model-dependent. |
| Hybrid search | Robust relevance with tuning and duplicate candidates. |
| Heavy reranker | Higher quality with added latency and cost. |

## 9. 60-second interview summary

Documents feed versioned lexical and vector indexes. A query retrieves from both, fuses candidates, enforces ACLs, reranks a bounded set, and builds snippets from the source. Shadow migrations, relevance datasets, lexical fallback, and delete lineage make it operable.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

