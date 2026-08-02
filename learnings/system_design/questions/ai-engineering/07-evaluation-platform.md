# Design a Prompt, Model, and Evaluation Platform

> **Difficulty:** Hard  
> **Main focus:** reproducibility, offline/online evaluation, lineage

## Interview prompt

Design an internal platform for developing prompts, comparing models, running evaluations, and promoting versions.

## 1. Clarify the product and success criteria

**What I would say first:** An evaluation result is meaningful only when dataset, code, prompt, model, tools, sampling, policy, and judge versions are reproducible.

### Functional requirements

- Version prompts, models, datasets, tools, and evaluation definitions.
- Run large offline comparisons with deterministic caching where valid.
- Support exact metrics, rubric judges, and human review.
- Promote through shadow, canary, production, and rollback stages.

### AI and product constraints

- LLM outputs and model-based judges are stochastic.
- Evaluation data can leak into training or prompt development.
- One aggregate score hides regressions in important task segments.

## 2. Contracts and data

- EvaluationSpec {datasetVersion, candidateVersions, metrics, repetitions, budget}
- Trace {inputRef, outputRef, retrievedRefs, toolCalls, latency, usage, versions}
- PromotionGate {qualityThresholds, safetyThresholds, latency, cost, requiredApprovals}

## 3. High-level design

```text
prompt/model/tool registries + dataset registry
                     |
             evaluation orchestrator
          / model endpoints / retrieval / tools
                     |
               immutable traces
        / exact metrics / judge models / human review
                     |
            segmented report + gate
                     |
             shadow -> canary -> production
```

## 4. Critical request flow

1. Freeze a dataset version and evaluation specification before execution.
2. Run candidate and baseline with controlled parameters and repeated trials where needed.
3. Store complete lineage and traces, then calculate exact metrics first.
4. Use blinded rubric judges and sampled human review for subjective dimensions.
5. Apply segmented promotion gates and preserve a one-click known-good rollback.

## 5. Quality and evaluation

- Separate capability, groundedness, policy, tool accuracy, latency, and cost metrics.
- Calibrate judge models against human labels and detect position or verbosity bias.
- Maintain hidden holdout and adversarial sets to reduce test overfitting.
- Report confidence intervals and paired differences rather than only mean scores.

## 6. Reliability, scale, observability, and cost

- Queue evaluation jobs by priority and budget; batch model calls when semantics allow.
- Cache only deterministic reusable stages keyed by every relevant version.
- Redact or isolate sensitive traces and expire them by dataset policy.
- Track job completion, flaky cases, judge agreement, tokens, cost, and release regression rate.

## 7. Safety, security, and privacy

- Keep evaluation secrets and hidden answers out of model-visible metadata.
- Restrict production trace access and remove personal data from reusable datasets.
- Require human approval for safety-sensitive promotion gates.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| One benchmark score | Simple but hides task and safety regressions. |
| Segmented gate suite | More trustworthy with maintenance cost. |
| Model judge | Scalable but biased and version-dependent. |
| Human review | Higher confidence but slower and expensive. |

## 9. 60-second interview summary

Immutable registries and traces make every run reproducible. The platform compares candidates with exact, judge, and human metrics segmented by risk, then enforces promotion gates through shadow and canary stages with a retained rollback version.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

