# Design a Recommendation and Ranking System

> **Difficulty:** Hard  
> **Main focus:** candidate generation, online features, feedback loops

## Interview prompt

Design personalized recommendations for a feed, marketplace, or media product.

## 1. Clarify the product and success criteria

**What I would say first:** I will optimize a stated long-term product outcome, not clicks alone. The online system needs candidate generation, feature lookup, ranking, policy reranking, and a safe fallback.

### Functional requirements

- Generate personalized candidates from a very large catalog.
- Rank within a strict latency budget.
- Handle new users/items, diversity, safety, and inventory.
- Learn from impressions and outcomes without amplifying bad feedback loops.

### AI and product constraints

- Only exposed items can receive feedback, creating selection bias.
- Features have different freshness and availability.
- One expensive model cannot score the entire catalog.

## 2. Contracts and data

- POST /v1/recommendations {userId, context, surface, limit}
- Exposure event records request, candidates, scores, final positions, model versions, and actual visibility
- Outcome event records exposure ID, action, value, and delayed timestamp

## 3. High-level design

```text
user/context -> candidate sources
               |-> collaborative retrieval
               |-> content/vector retrieval
               |-> popularity/follow graph
                         |
                 candidate union/dedupe
                         |
               online feature service -> ranker
                         |
         policy/safety/diversity/inventory reranker
                         |
                       response
exposures/outcomes -> training pipeline -> registry -> deployment
```

## 4. Critical request flow

1. Generate a few hundred candidates from multiple independent sources.
2. Fetch point-in-time-consistent online user, item, and context features.
3. Score candidates with a versioned ranker under a deadline.
4. Apply hard policy, availability, diversity, and fatigue constraints.
5. Log actual exposure, then join delayed outcomes for training and evaluation.

## 5. Quality and evaluation

- Measure candidate recall before blaming the ranker.
- Use offline NDCG or ranking loss plus online retention, conversion, satisfaction, and safety guardrails.
- Segment cold-start, heavy users, creators, regions, and protected cohorts.
- Use controlled exploration and propensity logging when learning from policy-chosen data.

## 6. Reliability, scale, observability, and cost

- Fallback to filtered popularity or editorial lists when features or models fail.
- Feature freshness and training-serving skew have explicit alarms.
- Canary models by stable cohorts and retain fast rollback.
- Track latency by stage, candidate coverage, feature misses, fallback rate, diversity, outcome, and cost.

## 7. Safety, security, and privacy

- Enforce policy after ranking so unsafe items cannot win on model score.
- Minimize personal features, restrict sensitive attributes, and honor deletion.
- Monitor manipulation, popularity feedback loops, creator fairness, and harmful optimization.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| One-stage full scoring | Simple but impossible for huge catalogs. |
| Two-stage retrieval/ranking | Scalable with candidate-recall risk. |
| Pure exploitation | Strong short-term metrics but poor learning and novelty. |
| Controlled exploration | Better learning with bounded user cost. |

## 9. 60-second interview summary

Multiple fast sources generate candidates, online features feed a bounded ranker, and deterministic policy/diversity rules produce the final list. Exposure logging, fallback, skew monitoring, exploration controls, and long-term metrics prevent a click-only feedback loop.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

