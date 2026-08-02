# Design a Deep Research Agent

> **Difficulty:** Hard  
> **Main focus:** search planning, source provenance, synthesis

## Interview prompt

Design an agent that researches an open-ended question across web and enterprise sources and produces a cited report.

## 1. Clarify the product and success criteria

**What I would say first:** The system must optimize evidence quality, not answer length. Every material claim should trace to retrieved evidence, and untrusted sources cannot control the agent.

### Functional requirements

- Decompose a research question into subquestions.
- Search, browse, extract, compare, and synthesize sources.
- Produce citations, uncertainty, and a resumable trace.
- Bound time, sources, tokens, and external requests.

### AI and product constraints

- Sources may be stale, contradictory, paywalled, malicious, or low quality.
- Research can loop indefinitely without a stopping criterion.
- Web pages can contain indirect prompt injection.

## 2. Contracts and data

- POST /v1/research-runs {question, allowedSources, recency, depth, budget}
- Evidence {sourceId, fetchedAt, passage, location, contentHash, trustSignals}
- Claim {text, supportingEvidenceIds, contradictingEvidenceIds, confidence}

## 3. High-level design

```text
user -> durable research orchestrator
                    |
              planner/subquestions
                    |
         search connectors + safe fetch/browser
                    |
          extraction/dedup/source scoring
                    |
             evidence and claim graph
                    |
          gap checker / contradiction pass
                    |
             cited report + trace
```

## 4. Critical request flow

1. Clarify scope, recency, acceptable sources, and output depth.
2. Create bounded subquestions and search plans.
3. Fetch through isolated tools, extract relevant passages, hash, deduplicate, and retain provenance.
4. Build claims only from evidence, then search specifically for gaps and contradictions.
5. Stop on coverage or budget, verify citation support, and generate a structured report.

## 5. Quality and evaluation

- Evaluate factual claim precision, citation entailment, source diversity, coverage, and contradiction handling.
- Use time-sensitive questions so stale-source behavior is visible.
- Human reviewers grade whether uncertainty matches evidence strength.
- Penalize unsupported synthesis even when prose sounds convincing.

## 6. Reliability, scale, observability, and cost

- Durable checkpoints let long runs pause for approval or resume after tool failure.
- Cache public fetches by URL, content hash, time, and permissions; never bypass access controls.
- Apply per-domain concurrency, robots or source policy, and total budgets.
- Track source fetch success, duplicate evidence, unsupported claims, run duration, tool calls, tokens, and cost.

## 7. Safety, security, and privacy

- Treat every source as hostile data and keep system policy outside extracted content.
- Use SSRF-safe fetching, malware isolation, content-size limits, and credential boundaries.
- Respect copyright, source terms, privacy, and enterprise ACLs.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| More sources | Potentially better coverage with higher noise and cost. |
| Trusted-source allowlist | Higher precision but may miss emerging evidence. |
| Fully autonomous run | Convenient with runaway and wrong-scope risk. |
| Checkpoints/approvals | Safer and steerable with more interaction. |

## 9. 60-second interview summary

A durable agent decomposes the question, retrieves through isolated policy-aware tools, and stores a provenance-rich evidence graph. Claim building, contradiction search, citation entailment, stopping budgets, and explicit uncertainty prioritize defensible research over fluent volume.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

