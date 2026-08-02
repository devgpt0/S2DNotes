# Latency, Throughput, and Availability

## Idea

Latency is time per operation. Throughput is operations per time. Availability
is the fraction of valid requests the system can serve.

## Visual model

```text
p50: typical user
p95: slow tail
p99: worst common tail where queues/retries/failures appear
```

## Design steps

1. Define SLOs per user journey, not one global number.
2. Break end-to-end latency into dependency budgets.
3. Measure throughput at peak and concurrency with Little's Law:
   `concurrency ≈ throughput × latency`.
4. Define which degraded response is acceptable during failure.

## When to use it

Use percentile latency for interactive APIs, throughput for pipelines, and
availability/durability separately for user access and stored data.

## Trade-offs

Batching improves throughput but can add waiting latency. More synchronous
dependencies increase end-to-end failure probability. Stronger durability can
increase write latency.

## Common mistakes

- Reporting averages only.
- Adding percentage availabilities instead of multiplying dependency success.
- Calling an empty/error response “available.”
- Ignoring queue time under overload.
