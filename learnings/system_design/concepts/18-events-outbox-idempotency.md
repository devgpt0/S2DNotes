# Events, Transactional Outbox, and Idempotency

## Idea

Database writes and event publication cannot be made reliable by two separate
uncoordinated calls. Write domain state and an outbox row in one transaction;
a relay publishes later. Consumers must tolerate duplicates.

## Visual model

```text
transaction -> domain rows + outbox row
outbox relay -> broker -> idempotent consumer -> effect + processed ID
```

## Design steps

1. Give commands/events stable IDs and schema versions.
2. Commit state plus outbox atomically.
3. Publish outbox rows with retry; mark/retain safely.
4. Consumer checks message/idempotency key inside its effect transaction.
5. Reconcile stuck outbox rows and consumer failures.

## When to use it

Use for reliable integration events after a local state transition and for any
mutation clients/brokers may retry.

## Trade-offs

At-least-once plus idempotency is practical; “exactly once” is scoped to a
specific transaction boundary, not the entire external world.

## Common mistakes

- Publish then write, or write then publish, without recovery.
- Event says an action happened before commit.
- Idempotency record and effect committed separately.
- Reusing a key for a different request payload.
