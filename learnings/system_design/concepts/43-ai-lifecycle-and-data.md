# AI System Lifecycle and Data Contracts

## Idea

An AI system is a versioned pipeline, not only a model: product objective, data,
training, evaluation, deployment, feedback, monitoring, and retirement must stay
traceable to one another.

## Visual model

```text
product goal -> data/version -> train -> offline evaluation -> registry
            -> staged deployment -> online outcomes -> feedback/retraining
```

## Design steps

1. Define the user outcome, baseline, acceptable errors, latency, and cost.
2. Create data contracts for source, schema, labels, consent, and retention.
3. Version datasets, code, features, prompts, model weights, and evaluation sets.
4. Split data by time/entity to prevent leakage.
5. Gate deployment on quality, safety, performance, and fairness checks.
6. Monitor online drift/outcomes and define rollback/retirement.

## When to use it

Every production ML/LLM system. The rigor increases with autonomy, user impact,
regulatory exposure, and the difficulty of correcting an error.

## Trade-offs

Frequent retraining adapts faster but raises cost and instability. More lineage
storage and approvals slow iteration but make results reproducible and auditable.

## Critical artifacts

- Model card, intended use, exclusions, and owners.
- Dataset snapshot/lineage and label definition.
- Evaluation report with slices and known limitations.
- Deployment record linking model, prompt/config, code, and traffic.

## Common mistakes

- Optimizing a model metric that is not connected to product value.
- Random train/test split when future or same-user leakage exists.
- Deploying an artifact whose training data/config cannot be reproduced.
- Collecting feedback without consent, quality controls, or label semantics.
