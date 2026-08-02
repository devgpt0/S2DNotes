# Design Search Autocomplete

> **Difficulty:** Medium  
> **Main focus:** prefix retrieval, ranking, freshness

## Interview prompt

Design low-latency query suggestions while the user types.

## 1. Clarify the scope

**What I would say first:** Autocomplete is a top-k prefix retrieval problem with strict latency, abuse filtering, and rapidly changing popularity.

### Functional requirements

- Return top suggestions for a normalized prefix.
- Rank by popularity, freshness, locale, and optional personalization.
- Update from query events without exposing unsafe or private terms.
- Respond within tens of milliseconds.

### Out of scope for the first version

- Full document search and spelling correction are separate deep dives.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume millions of requests per second because every keystroke can trigger a call.
- Short prefixes are the hottest keys and have the largest candidate sets.
- Responses are tiny and highly cacheable.

## 3. API and data model

### Main contracts

- GET /v1/suggestions?prefix=iph&locale=en-US&limit=10
- POST /internal/query-events {normalizedQuery, locale, count}

### Important data

- PrefixTopK(prefix, locale, version, suggestions[])
- QueryAggregate(query, locale, recent_count, long_count, safety_state)

## 4. High-level design

```text
client debounce -> edge cache -> suggestion API -> in-memory prefix index
                                                   |
query logs -> stream aggregation -> safety filter -> top-k builder
                                                   |
                                                   +-> versioned index publish
```

## 5. Critical request flow

1. Client waits for a short debounce and cancels obsolete requests.
2. Normalize the prefix consistently and check the edge cache.
3. Read precomputed top-k results from an in-memory trie or prefix table.
4. Apply lightweight personalization only within the safe candidate set.
5. Publish query events asynchronously for future ranking updates.

## 6. Deep dive

- Precompute top suggestions for common prefixes instead of scanning all terms at request time.
- Use separate recent and long-term counts so trends can rise without permanently dominating.
- Build indexes off-path, validate them, then atomically switch versions.
- Require a minimum aggregate count to prevent exposing rare private queries.

## 7. Scaling, failures, and observability

- Serve the previous safe index if the latest build fails.
- For an index miss, return an empty result or a slower bounded fallback.
- Use request cancellation and per-prefix rate limiting during bot traffic.
- Monitor p95 latency, cache hit rate, empty-result rate, unsafe suggestion rate, and index age.

## 8. Security and privacy

- Remove personal data, secrets, and abusive terms before aggregation.
- Do not personalize shared-cache entries; separate public and user-specific stages.
- Limit logging of raw query text and enforce retention.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Precomputed prefix top-k | Very fast reads but delayed freshness. |
| Live ranking | Fresh but costly for every keystroke. |
| Trie | Natural prefix lookup but memory-heavy. |
| Sorted terms plus range search | Compact but ranking needs extra structures. |

## 10. 60-second interview summary

I debounce on the client, serve precomputed safe top-k prefix results from memory and edge cache, and rebuild versioned indexes from aggregated query events. Personalization is a final bounded stage so shared caches remain safe.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you test recovery from a dependency timeout?
- Which metric best reflects the user's experience?

