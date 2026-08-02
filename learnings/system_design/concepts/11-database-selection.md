# Choosing a Database

## Idea

Choose storage from access patterns and correctness needs, not fashion.

## Visual model

```text
relational: rows + constraints + joins + transactions
key-value:  key -> opaque value
document:   key -> nested document
wide-column: partition key -> ordered rows
graph:      vertices + relationships
```

## Design steps

1. List reads/writes, query shapes, size, and growth.
2. Identify transactions, uniqueness, joins, and consistency.
3. Choose partitioning and indexing needs.
4. Test failure, backup, restore, and operational maturity.

## When to use it

Relational databases are a strong default for integrity and flexible queries.
Specialized stores earn their place through a required access pattern or scale.

## Trade-offs

Schema flexibility moves validation burden to applications. Multiple databases
optimize workloads but multiply operational and consistency complexity.

## Common mistakes

- “NoSQL scales, SQL does not.”
- Choosing from data shape without query shape.
- Making search/cache the source of truth.
- Ignoring backup restore and schema migration.
