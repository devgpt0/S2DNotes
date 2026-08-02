# Recommendation and Ranking Systems

## Idea

A recommender first finds a small set of possible items, then ranks those items carefully.

This two-stage design avoids scoring millions of items with an expensive model for every request.

## Visual model

```text
user + context
      |
candidate generation ---- popularity / graph / vector retrieval
      |
feature lookup
      |
ranking model
      |
rules, safety, diversity, availability
      |
final list -> interaction events -> training data
```

## Design steps

1. Define the long-term user outcome, not only clicks.
2. Generate candidates from several sources to improve coverage.
3. Fetch point-in-time-correct user, item, and context features.
4. Rank candidates within a strict latency budget.
5. Re-rank for policy, safety, freshness, diversity, and inventory.
6. Log candidates, scores, positions, model version, and actual exposure.
7. Handle new users and items with content, popularity, or exploration methods.
8. Fall back to a safe deterministic list when features or models fail.

## Pattern clues

This pattern fits feeds, search results, products, videos, notifications, ads, and matching systems.

## Evaluation

- Measure candidate recall before judging the ranking model.
- Use ranking metrics such as NDCG or mean reciprocal rank offline.
- Use controlled experiments for clicks, conversion, retention, and guardrails.
- Segment metrics so improvements do not hide harm to smaller groups.

## Trade-offs

- Personalization improves relevance but needs more data and privacy controls.
- Exploration learns new preferences but can reduce short-term performance.
- Fresh features improve ranking but increase serving complexity.

## Common mistakes

- Optimizing click-through rate when the real goal is user value.
- Training on displayed items without correcting selection bias.
- Logging clicks but not what the user actually saw.
- Allowing feedback loops to remove diversity.
- Having no cold-start or model-failure fallback.
