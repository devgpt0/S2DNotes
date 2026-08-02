# Transactions and Isolation

## Idea

A transaction makes related changes succeed or fail as one unit. Isolation
defines which concurrent effects a transaction may observe.

## Visual model

```text
begin -> check invariant -> write related rows -> commit
                                      failure -> rollback
```

## Design steps

1. State the business invariant: no double reservation, balanced ledger, etc.
2. Put invariant checks and writes in one database transaction where possible.
3. Choose isolation/locking that prevents the actual anomaly.
4. Keep transactions short and retry serialization/deadlock failures safely.

## When to use it

Use local ACID transactions for one database boundary. Across services, use a
saga/workflow with compensations and explicit intermediate states.

## Trade-offs

Stronger isolation simplifies reasoning but can reduce concurrency. Sagas scale
organizational boundaries but expose partial progress and compensation limits.

## Common mistakes

- Read-then-write outside one transaction.
- Calling remote services while holding database locks.
- Saying distributed rollback erases irreversible external effects.
- Retrying a transaction with non-idempotent side effects.
