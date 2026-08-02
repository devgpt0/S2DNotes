# Consistency and CAP

## Idea

Consistency describes what values reads may return. CAP says that during a
network partition, a distributed system cannot guarantee both linearizable
responses and availability for every request.

## Visual model

```text
partition separates replicas
choose: reject/delay some operations for one current truth
   or: accept on both sides and reconcile later
```

## Design steps

1. Define consistency per operation: balance read, feed read, profile update.
2. Decide behavior during replica lag and partition.
3. Use session guarantees/read-your-writes where full strong consistency is
   unnecessary.
4. Design conflict detection and repair for concurrent writes.

## When to use it

Use strong consistency for uniqueness, money, inventory ownership, and access
control. Eventual consistency often fits feeds, counters, and derived indexes.

## Trade-offs

The choice is not one label for the whole product. Different data paths can
make different consistency/latency/availability choices.

## Common mistakes

- Saying “choose two of three” outside partition behavior.
- Confusing consistency with durability.
- Eventual consistency without a convergence rule.
- Reading from a lagging replica after a user's own write.
