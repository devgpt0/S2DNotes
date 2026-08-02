# AI Cost and FinOps

## Idea

AI cost must be measured per successful product outcome, not only per token or GPU hour.

Cost is an architectural constraint alongside quality, safety, latency, and reliability.

## Visual model

```text
request cost = input + output generation
             + retrieval and reranking
             + tool calls
             + GPU or API time
             + storage, networking, and evaluation

quality + safety + latency + reliability
                  versus
             total cost
```

## Design steps

1. Attribute usage and cost to product, tenant, model, feature, and request class.
2. Measure cost per successful task and per active user.
3. Set budgets, quotas, alerts, and safe overload behavior.
4. Route simple work to the smallest model that passes quality gates.
5. Reduce irrelevant prompt and retrieval context.
6. Cache deterministic or reusable work with strict tenant isolation and expiry.
7. Batch delay-tolerant jobs and keep accelerators well utilized.
8. Bound retries, agent steps, output length, and tool spending.
9. Re-evaluate the quality-cost frontier whenever models or traffic change.

## High-value techniques

- Semantic or exact caching when correctness and privacy permit it.
- Small-model routing with escalation for harder requests.
- Prompt and context compression backed by regression tests.
- Asynchronous batch inference for offline workloads.
- Autoscaling that includes model load time and reserved capacity.
- Budgets based on business value and service priority.

## Trade-offs

- Aggressive caching lowers cost but risks stale or incorrectly shared answers.
- Smaller models cost less but may increase retries or failures.
- Scaling to zero saves idle cost but creates cold starts.
- Reserved accelerators improve predictability but can remain unused.

## Common mistakes

- Tracking API spend without retrieval, evaluation, storage, or engineering cost.
- Optimizing token count while task success falls.
- Ignoring retries, abandoned streams, and runaway agent loops.
- Sharing cached results across security boundaries.
- Buying accelerator capacity without measuring utilization.
