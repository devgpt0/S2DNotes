# AI Evaluation and Observability

## Idea

AI quality is probabilistic and multidimensional. Evaluation needs versioned
datasets, task-specific metrics, human judgment, and production signals.

## Classroom board

```text
trace = input -> retrieval -> prompt -> model -> tools -> output
join trace with versions, latency, tokens, cost, safety and user outcome
```

## Design steps

1. Build representative, adversarial, and safety evaluation sets.
2. Score retrieval, answer quality, groundedness, tool success, and refusal.
3. Calibrate model judges with human labels; track disagreement.
4. Compare changes with paired tests and staged traffic.

## Trade-offs and mistakes

Online feedback is real but biased; offline sets are repeatable but can become
stale. Never use one score, leak test data into prompts/training, or log raw
sensitive content by default.
