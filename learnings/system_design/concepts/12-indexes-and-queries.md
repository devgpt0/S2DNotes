# Indexes and Query Design

## Idea

An index is an extra ordered/hashed structure that speeds selected reads while
costing storage and write work.

## Visual model

```text
query filter/order -> matching index prefix -> locate rows -> fetch result
```

## Design steps

1. Start from high-frequency and high-latency queries.
2. Put equality fields before range/order fields in a composite index when the
   database's rules support it.
3. Check selectivity and result size.
4. Inspect the query plan with production-like data.
5. Remove unused/redundant indexes.

## When to use it

Index fields used to locate a small result, enforce uniqueness, or return data
in required order. Partitioning and indexes solve different problems.

## Trade-offs

Covering indexes avoid row fetches but grow larger. Many indexes accelerate
reads and slow every mutation.

## Common mistakes

- Indexing a low-selectivity boolean alone.
- Function/cast prevents index use.
- Returning millions of rows despite an index.
- Offset pagination scanning increasingly many entries.
