# Replication

## Idea

Replication keeps copies of data for availability, read scale, and disaster
recovery. A replica is useful only when its consistency and failover behavior
are explicit.

## Visual model

```text
write -> leader -> replica A
                -> replica B

read -> leader (fresh) or replica (possibly stale)
```

## Design steps

1. Choose leader/follower, multi-leader, or leaderless replication.
2. Decide how many replicas must acknowledge a write.
3. Route reads by freshness requirement, not only by load.
4. Define failover, leader fencing, and replica rejoin behavior.
5. Measure replication lag and test losing a zone or region.

## When to use it

Use replicas for machine/zone failure and read capacity. Cross-region replicas
support disaster recovery, but introduce latency and conflict decisions.

## Trade-offs

Synchronous replication improves acknowledged durability but increases write
latency and can reduce availability. Asynchronous replication is faster but a
failover can lose recent acknowledged writes.

## Operational checklist

- Expose per-replica lag in time and bytes.
- Use a leader term/epoch so the old leader cannot keep writing.
- Give read-after-write flows a leader or session-consistent route.
- Test failover and failback; promotion is only half the recovery.

## Common mistakes

- Assuming replicas are instantly consistent.
- Treating replicas as backups; corruption and deletion replicate too.
- Promoting two leaders during a partition.
- Ignoring stale reads in authentication, inventory, or payment flows.
