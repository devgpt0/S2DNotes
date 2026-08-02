# Schema Evolution and Data Migrations

## Idea

Production schemas and messages must evolve while old and new application
versions run together. Safe migrations are backward-compatible, observable,
restartable, and reversible where possible.

## Visual model

```text
expand schema -> deploy dual-compatible code -> backfill -> switch reads
              -> verify -> stop old writes -> contract old schema
```

## Design steps

1. Add optional fields/tables/indexes without changing old behavior.
2. Deploy code that can read old and new representations.
3. Backfill in bounded, checkpointed batches with rate limits.
4. Compare old/new results and monitor lag/errors.
5. Switch writes/reads through a controlled flag.
6. Remove old schema only after every producer, consumer, and rollback window is clear.

## When to use it

Use expand-migrate-contract for database, event, API, search-index, and cache
shape changes in systems that cannot stop for a maintenance window.

## Trade-offs

Dual reads/writes increase temporary complexity but reduce deployment risk.
Online index creation protects availability but can still consume I/O and locks.

## Migration safety

- Use stable checkpoints and idempotent batches.
- Throttle from database latency/replica lag, not a fixed guess.
- Version events and tolerate unknown optional fields.
- Keep destructive changes in a separate later deployment.

## Common mistakes

- Renaming/dropping a column in the same release that changes code.
- One huge transaction for a large backfill.
- Assuming all event consumers deploy together.
- Declaring success without reconciliation counts/checksums.
