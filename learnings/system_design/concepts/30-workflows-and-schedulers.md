# Durable Workflows and Job Schedulers

## Idea

A durable workflow records progress so multi-step work survives process crashes,
retries, and long waits. A scheduler decides when work becomes eligible; workers
execute it with leases and idempotency.

## Visual model

```text
schedule/event -> durable workflow state -> task queue -> leased worker
                         ^                    |
                         +-- result/retry ----+
```

## Design steps

1. Model the workflow as explicit states and durable transitions.
2. Store input, current state, attempts, next run time, and idempotency key.
3. Lease tasks with visibility timeout; renew only while progress is healthy.
4. Retry transient errors with backoff; classify permanent failures.
5. Add compensation for completed steps that cannot be atomically rolled back.
6. Support cancellation, pause, timeout, versioning, and operator repair.

## When to use it

Use durable workflows for payments, order fulfillment, onboarding, media/ML
pipelines, and jobs lasting longer than one request or process lifetime.

## Trade-offs

Central workflow engines improve visibility and recovery but add infrastructure
and deterministic/versioning constraints. Choreographed events reduce central
coupling but make end-to-end state harder to understand.

## Reliability rules

- Assume a task can execute more than once.
- Make external effects idempotent or record a deduplication key.
- Separate task timeout from workflow deadline.
- Dead-letter only with replay and operator context.

## Common mistakes

- Holding a database transaction open across remote calls.
- Treating cron as a durable workflow engine.
- Retrying validation/business failures forever.
- Changing workflow code without supporting in-flight old versions.
