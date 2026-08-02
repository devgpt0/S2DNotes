# Sharding and Consistent Hashing

## Idea

Sharding divides data across nodes. The shard key decides placement, query
routing, balance, and which transactions stay local.

## Visual model

```text
key -> routing/hash -> shard
tenant A -> shard 1
tenant B -> shard 3
```

## Design steps

1. Choose a high-cardinality key aligned with main access patterns.
2. Estimate skew and hot tenants/keys.
3. Keep a routing map and plan online movement.
4. Avoid cross-shard joins/transactions on critical paths.
5. Add virtual nodes/ranges or split large tenants.

## When to use it

Shard when one database's storage/write capacity or failure domain is
insufficient—not as the first step.

## Trade-offs

Hashing balances point access but loses range locality. Range sharding supports
scans but risks hotspots. Consistent hashing reduces movement on membership
changes but does not solve hot keys.

## Common mistakes

- Low-cardinality or monotonically hot shard key.
- No resharding plan.
- Globally unique IDs requiring one central bottleneck.
- Assuming even key count means even workload.
