# Data Modeling and Access Patterns

## Idea

Model data from the reads, writes, constraints, and lifecycle—not from nouns
alone.

## Visual model

```text
access patterns -> keys/indexes -> entities/relationships -> storage choice
```

## Design steps

1. List critical reads and writes with expected scale.
2. Identify ownership, uniqueness, ordering, and transaction boundaries.
3. Choose partition and sort keys from access paths.
4. Add indexes only for real queries.
5. Plan retention, archival, deletion, and schema evolution.

## Example

A message table may use `(conversation_id, sequence)` so history is an ordered
range read. A separate message ID supports deduplication, not history order.

## When to use it

Before choosing SQL/NoSQL. The same domain can need an authoritative write
model, cached read model, search index, and analytics copy.

## Trade-offs

Normalization protects integrity and avoids duplicate writes. Denormalization
makes reads faster but requires explicit synchronization and repair.

## Common mistakes

- One table/document per screen without ownership rules.
- Indexing every field and slowing writes.
- Using a timestamp alone as a unique cursor.
- Ignoring deletion across derived stores.
