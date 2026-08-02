# Design Long-Term Memory for an AI Assistant

> **Difficulty:** Hard  
> **Main focus:** memory selection, privacy, correction

## Interview prompt

Design an assistant that remembers useful user preferences and past interactions across sessions.

## 1. Clarify the product and success criteria

**What I would say first:** Memory is permission-aware application data, not unlimited conversation replay. The system needs explicit write criteria, provenance, expiry, correction, and deletion.

### Functional requirements

- Remember stable preferences and useful prior facts.
- Retrieve only relevant memories for the current task.
- Let users inspect, correct, disable, and delete memory.
- Prevent cross-user leakage and stale assumptions.

### AI and product constraints

- Model-generated facts may be wrong.
- More memories can distract the model and increase cost.
- Some categories should never be stored without explicit consent.

## 2. Contracts and data

- Memory {memoryId, userId, type, statement, provenance, confidence, createdAt, expiresAt, status}
- POST /v1/memories/proposals requires evidence and write-policy decision
- GET /v1/memories:retrieve {task, filters, limit}
- DELETE /v1/memories/{id} propagates to derived indexes

## 3. High-level design

```text
conversation/tool facts -> memory proposal extractor
                           |
                    write policy/consent
                           |
              authoritative memory store -> embedding/search index
                           |                       |
user controls/corrections -+             retrieval + reranking
                                                   |
current task -> context builder <- selected memories with provenance
```

## 4. Critical request flow

1. Extract a candidate only from supported user statements or verified application data.
2. Classify sensitivity, stability, confidence, retention, and required consent.
3. Write an immutable-provenance memory or reject the proposal.
4. For a new task, retrieve by user, permission, type, relevance, recency, and expiry.
5. Present selected memories as data with provenance and allow correction or deletion.

## 5. Quality and evaluation

- Evaluate useful recall, irrelevant-memory rate, contradiction rate, and task improvement.
- Include time-shifted cases where preferences changed or memories expired.
- Measure whether the assistant appropriately asks instead of relying on uncertain memory.
- Audit deletion completeness and cross-user isolation continuously.

## 6. Reliability, scale, observability, and cost

- Keep the database authoritative and the vector index rebuildable.
- Version extraction, write policy, and retrieval ranking separately.
- Limit memory count and context budget; compact only with retained provenance.
- Track write acceptance, retrieval use, correction, deletion lag, contradiction, tokens, and cost.

## 7. Safety, security, and privacy

- Never infer or store highly sensitive traits merely because a model guessed them.
- Use strict tenant/user keys in every store and cache.
- Expose controls in plain language and honor deletion across backups according to policy.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Store full conversations | High recall with privacy, cost, and noise. |
| Curated atomic memories | Controllable and inspectable but may miss context. |
| Automatic writes | Smooth experience with error risk. |
| Confirmed sensitive writes | Safer with more user interaction. |

## 9. 60-second interview summary

Verified facts become provenance-bearing memory proposals, a policy decides consent and retention, and an authoritative store plus rebuildable index supports bounded retrieval. Users can inspect and correct memories, while sensitive inference, isolation, expiry, and deletion are enforced.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

