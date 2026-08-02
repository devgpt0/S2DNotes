# AI Evaluation and Observability

## Idea

AI output is probabilistic and often has no single exact answer. Evaluation
combines stable offline test sets, human/rubric judgments, online outcomes,
safety checks, and operational telemetry.

## Visual model

```text
request trace: input -> retrieval/tools -> prompt/model -> output -> outcome
                     versions + latency + tokens + cost + quality/safety labels
```

## Design steps

1. Build representative, versioned evaluation cases with protected holdouts.
2. Define task rubrics, safety gates, slices, and acceptable regression bounds.
3. Test retrieval/tool behavior separately from final generation.
4. Compare candidate and baseline with paired results and confidence intervals.
5. Deploy as shadow/canary and monitor user/business guardrails.
6. Capture sampled traces with redaction and consent-aware feedback.

## When to use it

Before every model, prompt, retrieval, policy, or tool change. High-impact
systems require human review and domain-specific acceptance tests.

## Trade-offs

LLM judges scale but inherit bias and can favor certain styles/models. Human
evaluation is richer but slower and inconsistent; calibrate raters and measure
agreement.

## Critical metrics

- Quality by task and hard slice, not one global average.
- Safety violation/refusal false-positive and false-negative rates.
- TTFT, completion latency, tool/retrieval errors, token/GPU cost.
- Drift in inputs, retrieved sources, feedback, and outcome rates.

## Common mistakes

- Reusing a public/tuned-on benchmark as an unbiased test set.
- Changing model and prompt together without attribution.
- Storing raw prompts/responses by default.
- Treating user thumbs-up as a clean ground-truth label.
