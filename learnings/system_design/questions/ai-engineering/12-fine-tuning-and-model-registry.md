# Design a Fine-Tuning and Model Registry Platform

> **Difficulty:** Hard  
> **Main focus:** training lineage, checkpoints, promotion

## Interview prompt

Design an internal platform for preparing data, fine-tuning models, evaluating artifacts, and deploying approved versions.

## 1. Clarify the product and success criteria

**What I would say first:** I will first verify fine-tuning is the right tool instead of prompting or retrieval. Every registered artifact must be reproducible from versioned data, code, base model, and configuration.

### Functional requirements

- Create validated training datasets and launch jobs.
- Support checkpoints, distributed workers, and parameter-efficient tuning.
- Evaluate and register complete serving artifacts.
- Promote through controlled stages with rollback.

### AI and product constraints

- Training is expensive and can fail after hours.
- Data licensing, privacy, and leakage can invalidate a model.
- Weights alone are insufficient without tokenizer, template, adapters, and runtime.

## 2. Contracts and data

- TrainingSpec {baseModel, datasetVersion, codeVersion, method, hyperparameters, seed, resources}
- Artifact {weights, tokenizer, chatTemplate, adapter, runtime, lineage, checksums}
- Registry stages: candidate, evaluated, approved, canary, production, retired

## 3. High-level design

```text
source data -> validation/dedup/licensing -> versioned dataset
                                            |
training spec -> scheduler -> distributed workers -> checkpoints
                                            |
                                 offline evaluation/safety
                                            |
                               signed model registry
                                            |
                              canary serving -> production
```

## 4. Critical request flow

1. Validate task gap and select full tuning, adapter tuning, or another method.
2. Freeze data and split training, validation, and untouched test sets by leakage-safe keys.
3. Schedule resources, train with periodic complete checkpoints, and record lineage.
4. Run quality, safety, latency, memory, and cost evaluations.
5. Register the full serving package, obtain approval, canary, and retain rollback.

## 5. Quality and evaluation

- Compare against base-model and prompt/RAG baselines to prove tuning adds value.
- Check memorization, contamination, catastrophic forgetting, and subgroup regressions.
- Keep the final test set inaccessible to iterative tuning decisions.
- Evaluate the exact quantized or adapted serving artifact, not only training weights.

## 6. Reliability, scale, observability, and cost

- Retry from verified checkpoints and quarantine corrupted or partial artifacts.
- Track accelerator utilization, checkpoint time, failed workers, data throughput, and cost/job.
- Use immutable registry versions and signed checksums.
- Monitor production drift and connect incidents back to data and training lineage.

## 7. Safety, security, and privacy

- Enforce dataset access, licenses, consent, retention, and deletion obligations.
- Scan artifacts and dependencies; restrict who can approve production stages.
- Do not put secrets or raw personal data into training examples.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Full fine-tuning | Maximum parameter change with high compute and forgetting risk. |
| Adapter tuning | Cheaper and composable with adapter-serving complexity. |
| Prompt/RAG | Fast iteration and fresh knowledge without changing weights. |
| Fine-tuning | Useful for stable behavior changes backed by strong data. |

## 9. 60-second interview summary

Versioned, licensed data and an immutable training spec produce recoverable checkpoints. The full serving package is evaluated for quality, safety, latency, and cost before signed registry promotion, canary deployment, and rollback.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

