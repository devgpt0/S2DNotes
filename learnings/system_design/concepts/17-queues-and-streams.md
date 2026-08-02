# Queues and Streams

## Idea

A queue decouples work in time. A stream/log preserves ordered records for
independent consumers and replay.

## Visual model

```text
producer -> broker partitions -> consumer group -> durable effect
                              -> another group -> different projection
```

## Design steps

1. Define message key, schema, ownership, and retention.
2. Choose queue semantics or replayable stream semantics.
3. Partition by the ordering/parallelism unit.
4. Process, persist effect, then acknowledge/commit.
5. Add retries, dead-letter handling, lag metrics, and replay procedure.

## When to use it

Use asynchronous messaging for slow work, traffic smoothing, fan-out, and
decoupled derived views. Keep synchronous calls for immediate required answers.

## Trade-offs

More partitions improve throughput but weaken global order. Longer retention
enables replay but costs storage and governance work.

## Common mistakes

- Claiming global order across partitions.
- Acknowledging before durable effect.
- Infinite poison-message retries.
- Treating broker retention as permanent source-of-truth storage.
