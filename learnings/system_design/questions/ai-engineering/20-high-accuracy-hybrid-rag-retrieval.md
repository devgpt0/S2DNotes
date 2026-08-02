# Design High-Accuracy Hybrid Retrieval for RAG

> **Difficulty:** Hard  
> **Main focus:** keyword search, semantic search, fusion, reranking, and evaluation

## Interview prompt

Design retrieval for a premium RAG product whose users expect very high
accuracy. It must find both exact keywords and semantically similar content.

## 1. Start by defining "high accuracy"

No retrieval design is accurate for every query. Define quality with a labeled
evaluation set and measure every stage separately.

**What I would say first:** I will use keyword and semantic retrieval in
parallel, fuse their ranked results, rerank the best candidates, and measure
retrieval independently from answer generation.

### Functional requirements

- Find exact IDs, names, error codes, quoted phrases, and version numbers.
- Find paraphrases and conceptually related text even when words differ.
- Apply tenant, document, and user permissions before text reaches the LLM.
- Return source versions and precise citations.
- Prefer an honest no-answer result when evidence is weak.
- Reflect document updates and deletes within a defined freshness target.

### Quality and service targets

Agree on targets for:

- **Recall@k:** did the candidate set contain the relevant source?
- **nDCG@k:** were the most useful sources ranked near the top?
- **MRR:** how early did the first relevant result appear?
- **Citation precision:** does each citation support its claim?
- **Grounded answer rate:** is the answer supported by retrieved evidence?
- **Authorization leakage:** must be zero.
- **Freshness, p95 latency, availability, and cost per query.**

For a high-value domain, an illustrative gate might require Recall@100 of at
least 98% on critical query classes before reranking. That number is not
universal; set it from product risk and validate that the benchmark represents
real traffic.

## 2. Recognize when hybrid retrieval is required

| Query pattern | Best first signal |
|---|---|
| `ERR_CONN_RESET`, SKU, ticket ID, function name | Keyword/lexical search |
| Exact quoted phrase | Keyword/phrase search |
| "Why does the connection suddenly close?" | Semantic/vector search |
| `ERR_CONN_RESET fix for client 2.4` | Both keyword and semantic search |
| Query with tenant, date, product, or language constraints | Search plus metadata filters |

Use hybrid retrieval when the collection contains both exact identifiers and
natural-language concepts, or when user wording often differs from document
wording. That describes most enterprise RAG systems.

## 3. Classroom-board view

```text
                              INDEXING

documents -> parse -> parent sections -> child chunks -> ACL + metadata
                               |                |
                               |                +-> lexical index (BM25)
                               +-> embed chunks ---> vector index (ANN)
                               +-> source/version store

                             QUERY TIME

user query -> auth + filters + query understanding
                  |                         |
                  +-> BM25 top candidates  +-> vector top candidates
                              \              /
                               rank fusion
                                    |
                         permission check + dedupe
                                    |
                            cross-encoder reranker
                                    |
                       parent expansion + context budget
                                    |
                       LLM -> claims + checked citations
                                    |
                            answer or abstain
```

Keyword search and vector search are candidate generators. Neither one should
be asked to make the final ranking decision alone.

## 4. Build the indexes correctly

### Document record

```text
document_id
document_version
tenant_id
acl_reference
title
section_path
child_chunk_id
parent_section_id
language
product
effective_date
content_hash
embedding_model_version
index_version
source_offsets
```

Source offsets let the system create citations from the original document
instead of citing rewritten or generated text.

### Progressive indexing steps

1. Validate the connector event and fetch the authorized source version.
2. Scan and parse the document in an isolated process.
3. Preserve headings, lists, tables, code blocks, and page or line offsets.
4. Split each document into meaningful parent sections.
5. Split parents into smaller child chunks for precise retrieval.
6. Attach tenant, ACL, version, language, product, date, and source metadata.
7. Add title, heading, body, and exact-identifier fields to the lexical index.
8. Embed the child text with one pinned embedding model version.
9. Write the vector record and lexical record idempotently.
10. Mark the new document version searchable only after required index writes succeed.

Use content hashes to skip unchanged chunks. Propagate deletes with tombstones
to the lexical index, vector index, caches, and source store.

### Chunking rule

Chunks should express one coherent idea and remain understandable without the
whole document. Do not use one fixed character count for every format.

```text
large parent section: enough context for the final prompt
small child chunk:    precise unit used for retrieval
```

Retrieve child chunks, then expand the winners to their parent sections. This
often gives both precise matching and readable context.

## 5. Understand both retrieval signals

### Keyword retrieval

BM25-like lexical search rewards terms that occur in a document but are rare
across the collection. It is strong for exact identifiers, names, and phrases.

Useful tuning controls include:

- phrase and exact-match boosts;
- stronger title and heading fields;
- language-aware tokenization;
- careful handling of punctuation in error codes and code symbols;
- a small, reviewed synonym list for domain terms;
- spelling correction that preserves the original query as another branch.

Do not expand every query with a large synonym dictionary. It can increase
recall while destroying precision.

### Semantic retrieval

An embedding converts the query and chunks into vectors. Approximate nearest
neighbor search finds vectors that are close even when their words differ.

Semantic quality depends on:

- the embedding model and language/domain coverage;
- the text given to the model, including useful title or section context;
- chunk boundaries;
- vector distance metric;
- ANN settings such as candidate exploration;
- consistent embedding versions.

Never compare query vectors from one incompatible embedding model with document
vectors from another.

## 6. Critical query flow

1. Authenticate the caller and resolve current tenant and group permissions.
2. Validate query size, filters, requested result count, and language.
3. Preserve the original query. Extract structured filters such as product,
   version, date, or document type only when confidence is high.
4. Run lexical retrieval and vector retrieval in parallel with supported
   tenant/ACL filters and an intentionally oversized candidate budget.
5. Perform an authoritative permission check before any content leaves the
   retrieval boundary.
6. Fuse rankings, remove duplicate chunks, and limit repeated results from one document.
7. Rerank a bounded candidate set using the full query and candidate text.
8. Expand selected child chunks to parent context and pack them within a token budget.
9. Generate an answer that identifies its supporting source IDs and offsets.
10. Validate citation existence and support. Abstain when evidence is insufficient.

### Starting candidate budget for a premium tier

```text
BM25 candidates:               100
vector candidates:             100
fused candidates:              100
cross-encoder rerank:        top 50
final context:               top 5-10 coherent sections
```

These are starting values, not magic constants. Tune them with recall, latency,
and cost measurements. A high-accuracy tier can search and rerank more
candidates than a lower-cost tier.

## 7. Fuse ranks instead of raw scores

BM25 scores and vector similarity scores have different scales. Adding them
directly makes tuning fragile. Reciprocal Rank Fusion (RRF) combines positions:

```text
RRF score(document) = sum over result lists of 1 / (K + rank(document))
```

`K` controls how strongly the first few positions dominate. Tune it on labeled
queries. A document returned by both systems receives evidence from both lists.

Other valid choices are learned fusion or carefully normalized weighted
scores. Start with RRF because it is simple, stable, and easy to explain. Move
to a learned ranker only when labeled data proves the benefit.

## 8. Worked classroom example

User query:

```text
How do I fix ERR_CONN_RESET in desktop client 2.4?
```

The user needs the exact error and version, but also expresses the intent
"fix." The indexes return:

```text
BM25 list                              Vector list
1. ERR_CONN_RESET reference            1. Recover from sudden connection closure
2. Desktop 2.4 networking fixes         2. Desktop client network troubleshooting
3. General error catalog                3. ERR_CONN_RESET reference
```

Board view of the decision:

```text
exact term match -----------+
                            +-> RRF -> reranker -> final evidence
meaning: connection closes -+
version filter: 2.4 --------+
```

The exact reference appears at rank 1 in BM25 and rank 3 in vector search, so
fusion rewards it. The reranker then reads the query and candidates together.
It can put a version-specific repair guide above a generic definition.

```text
Final order
1. Desktop 2.4: Repair ERR_CONN_RESET       <- exact + version + solution
2. ERR_CONN_RESET reference                 <- exact but mostly definition
3. Recover from sudden connection closure   <- semantic but not version-specific
```

This example shows why keyword-only misses paraphrases, vector-only can
underweight exact codes, and fusion plus reranking handles both.

## 9. Reranking and context construction

A cross-encoder-style reranker scores the query and each candidate together.
It is slower than vector similarity, so use it only on a bounded fused set.

The reranker should receive:

- original query and confident structured filters;
- title, section path, chunk text, and relevant metadata;
- document freshness or authority signals when the product requires them.

After reranking:

- remove near-duplicate chunks;
- limit repeated chunks from one document unless they add new evidence;
- prefer authoritative and current versions;
- retain conflicting sources when the answer must disclose disagreement;
- expand to parent context without crossing permission or document boundaries;
- fit evidence into the prompt's token budget.

Do not use the LLM's fluent answer as proof that retrieval was correct.

## 10. Design the evaluation set

### Golden-query record

```text
query
query_class
tenant_and_permission_fixture
required_relevant_source_ids
acceptable_source_ids
forbidden_source_ids
expected_filters
answer_or_abstain_criteria
dataset_version
reviewer
```

### Required query slices

- exact IDs, error codes, quoted phrases, and product names;
- semantic paraphrases with little word overlap;
- hybrid queries containing both an identifier and an intent;
- misspellings, acronyms, and ambiguous short queries;
- product, language, date, and version filters;
- multi-hop questions whose evidence spans documents;
- permission boundaries and deleted documents;
- stale versus current or conflicting documents;
- no-answer questions;
- adversarial documents containing prompt-injection text.

Add hard negatives: documents that look highly relevant but do not answer the
question. They test whether the system can distinguish a nearby topic from
actual evidence.

### Evaluate stage by stage

```text
BM25 recall -----+
                 +-> fused recall -> reranker nDCG -> context recall
vector recall ---+                         |
                                           v
                              answer + citation evaluation
```

If the correct source never enters the candidate set, the reranker and LLM
cannot recover it. If retrieval is correct but the answer is wrong, fix the
generation or context stage instead of changing the index blindly.

Report metrics both globally and by query slice. A strong average can hide
failure on exact codes, one language, one tenant, or permission-filtered queries.

## 11. Improve quality scientifically

Change one major variable at a time and run an ablation:

1. lexical only;
2. vector only;
3. hybrid with fusion;
4. hybrid plus reranker;
5. hybrid, reranker, and parent expansion.

For every version, record quality, p95 latency, infrastructure cost, and the
queries helped or harmed. Typical tuning order:

1. repair parsing and missing metadata;
2. repair chunk boundaries;
3. tune lexical analyzers and field boosts;
4. evaluate embedding candidates;
5. tune ANN recall and candidate count;
6. tune fusion;
7. add or tune the reranker;
8. tune context selection and abstention.

This order prevents an expensive model from hiding a broken ingestion pipeline.

### Online evaluation

Use controlled experiments and collect explicit relevance judgments for
valuable or failed queries. Clicks, answer copy events, and repeated searches
are useful signals, but they are biased. Never treat a click as unquestionable
ground truth.

## 12. Freshness and model migrations

An embedding migration creates a new index version:

```text
old index serves traffic
        |
        +-> backfill new embedding index
        +-> dual-write new changes
        +-> shadow queries and evaluate
        +-> atomically switch read alias
        +-> retain old index for rollback
```

Do not mix incompatible vector versions in one search space. Version the
lexical analyzer, embedding model, chunker, reranker, and fusion configuration
in every evaluation trace.

## 13. Reliability and safe degradation

| Failure | Correct behavior |
|---|---|
| Vector service unavailable | Continue with lexical retrieval and mark the degraded mode. |
| Lexical service unavailable | Use vector retrieval only if quality and policy allow it. |
| Reranker unavailable | Return fused ranking with stricter confidence or abstention. |
| Embedding version mismatch | Reject the index/query combination; never compare incompatible vectors. |
| Indexing lag | Expose freshness metrics and use the last complete document version. |
| Delete or ACL change | Invalidate caches and remove access from every serving index promptly. |
| No strong evidence | Abstain or ask a clarifying question. |
| Conflicting current sources | Show the conflict with citations rather than inventing certainty. |

Caches must include tenant, identity or permission version, query, filters,
index version, and ranking version. A cache hit must never bypass authorization.

## 14. Security

- Apply supported ACL prefilters during retrieval and always perform an
  authoritative check before returning text.
- Treat retrieved text as untrusted data, not as system instructions.
- Isolate parsers and defend connectors against malicious files and SSRF.
- Escape snippets in the user interface to prevent script execution.
- Limit query and document logging; preserve only policy-approved data.
- Test that deleted and forbidden documents never appear in results, prompts,
  traces, caches, or citations.

## 15. Observability

Trace one query across:

- index and embedding versions;
- BM25 and vector candidate IDs and ranks;
- fusion contribution and reranker scores;
- ACL removals and deduplication;
- selected context IDs and source versions;
- stage latency, token count, answer status, and citations.

Aggregate indexing lag, zero-result rate, abstention, Recall@k on sampled judged
queries, click reformulation, citation failures, p95 latency, and cost. Restrict
trace content according to data policy.

## 16. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Keyword only | Exact, explainable, inexpensive | Misses paraphrases and conceptual matches |
| Vector only | Strong semantic recall | Can miss exact identifiers and is model-dependent |
| Hybrid + RRF | Robust across query types | Two indexes and fusion tuning |
| Cross-encoder reranker | Stronger final relevance | Added latency and compute cost |
| Larger candidate set | Higher chance of finding evidence | More search and reranking latency |
| Parent-child chunks | Precise retrieval with useful context | More ingestion and context logic |
| Multi-query expansion | Can recover difficult recall cases | Higher cost and possible topic drift |

For premium users, spend additional compute only where evaluation shows a
quality gain: larger candidate pools, a stronger reranker, or carefully bounded
query expansion. More components do not automatically mean more accuracy.

## 17. 60-second interview summary

I would build versioned lexical and vector indexes over permission-aware child
chunks. At query time, BM25 and ANN retrieval run in parallel, their rankings
are fused with RRF, permissions are authoritatively checked, and a bounded set
is reranked before parent context is assembled. Exact identifiers come from
lexical search; paraphrases come from semantic search. A slice-based golden set
measures candidate recall, ranking, citations, security, freshness, latency,
and cost separately. The system abstains when evidence is weak and falls back
to one retrieval path when the other is degraded.

## Likely follow-up questions

- Why should raw BM25 and vector scores not be added directly?
- How would you choose chunk size for code, tables, and prose?
- How do you measure retrieval separately from generation?
- When is query rewriting useful, and how can it cause topic drift?
- How do ACL filters affect ANN recall and latency?
- How would you migrate to a new embedding model without downtime?
- What evidence threshold should cause the system to abstain?

