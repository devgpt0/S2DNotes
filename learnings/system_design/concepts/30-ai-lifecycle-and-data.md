# AI System Lifecycle and Data

## Idea

An AI system is a versioned loop: collect governed data, train/configure,
evaluate, deploy, observe, and improve.

## Classroom board

```text
data snapshot -> model/prompt build -> offline evaluation -> staged release
user traffic -> quality/safety/cost signals -> reviewed improvements
```

## Design steps

1. Define task, users, harm, quality, latency, and cost targets.
2. Version data, code, prompts, model, tools, and evaluation set.
3. Gate deployment with offline tests, human review, and canary traffic.
4. Monitor quality, drift, safety, latency, and spend; keep rollback.

## Trade-offs and mistakes

Fresh feedback improves relevance but can create privacy and feedback-loop bias.
Never train on ungoverned production data, compare models on changing test sets,
or ship without a deterministic fallback.
