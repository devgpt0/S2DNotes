# Reliability: Timeouts, Retries, Backpressure, Shutdown

## 1) Reliability First Principle

Concurrency without reliability controls creates fragile systems.

## 2) Timeout Strategy

Define timeout layers:
- per operation timeout
- per request/job deadline
- graceful global shutdown timeout

Never rely on infinite waits.

## 3) Retry Strategy

Retry only retryable failures:
- timeout/transient network issues
- temporary service unavailable

Do not retry:
- validation errors
- deterministic domain failures

Use:
- bounded attempts
- exponential backoff
- jitter to avoid retry storms

## 4) Backpressure Strategy

Backpressure must be end-to-end:
1. bounded ingress
2. bounded queue size
3. bounded workers
4. bounded retries

If only one stage is bounded, overload can still move elsewhere.

## 5) Circuit-Breaker Thinking

If downstream keeps failing:
- reduce pressure
- fail fast or degrade gracefully
- recover after cooldown health checks

## 6) Graceful Shutdown Lifecycle

1. stop accepting new work
2. signal workers to stop
3. drain in-flight tasks safely
4. close resources
5. force-stop only as last resort

## 7) Idempotency and Exactly-Once Myth

In distributed/concurrent workflows:
- design for at-least-once effects with idempotent operations.
- deduplicate by idempotency keys where needed.

## 8) Reliability Anti-Patterns

- infinite retries without deadlines
- unbounded internal queues
- silent task failures
- no visibility into dropped/retried jobs

## 9) Interview Questions

1. How do you design retries safely?
2. What is backpressure and where to enforce it?
3. How do you shutdown without losing in-flight work?
4. Why idempotency matters in concurrent systems?
