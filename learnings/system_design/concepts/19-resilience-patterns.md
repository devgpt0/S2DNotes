# Timeouts, Retries, Circuit Breakers, and Backpressure

## Idea

Partial failure is normal. Bound waiting and work so one slow dependency does
not consume every thread, connection, queue slot, or retry budget.

## Visual model

```text
request -> timeout -> bounded retry with jitter
failure rate high -> circuit opens -> fast failure/fallback
overload -> queue/concurrency bound -> reject or slow producers
```

## Design steps

1. Set deadlines from the end-to-end budget.
2. Retry only transient, idempotent operations with exponential backoff+jitter.
3. Limit retry attempts and total retry budget.
4. Use circuit breakers/bulkheads around failing dependencies.
5. Bound queues and propagate backpressure or shed low-priority work.

## When to use it

Every remote call needs a timeout. Retries require an explicit reason and
idempotency. Backpressure matters whenever producers can outrun consumers.

## Trade-offs

Retries improve isolated failures but amplify widespread overload. Fallbacks
improve availability but may serve stale/incomplete results.

## Common mistakes

- Nested retries at every layer.
- Same timeout for connect and full response.
- Unbounded queues hiding overload until memory fails.
- Circuit breaker without recovery probing and metrics.
