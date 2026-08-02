# Consensus, Leader Election, and Distributed Locks

## Idea

Consensus lets nodes agree on an ordered state despite failures. Leader
election chooses one coordinator for a term. A distributed lock is safe only
when stale owners cannot keep acting after their lease expires.

## Visual model

```text
proposal -> replicated log -> majority commit -> state machines apply in order
                         term/epoch increases on each leadership change
```

## Design steps

1. Ask whether coordination can be removed through partitioning or idempotency.
2. If coordination is required, use a proven consensus-backed system.
3. Define quorum, membership changes, and behavior without a majority.
4. Give each leader/lock owner a fencing token that increases monotonically.
5. Make the protected resource reject operations with an older token.

## When to use it

Use consensus for metadata, membership, leader election, configuration, or a
small critical control plane. Do not place high-volume user data through a
consensus group without understanding its throughput and latency limits.

## Trade-offs

A majority survives minority failure but cannot make progress after losing
quorum. Cross-region quorums improve failure tolerance but add network latency.

## Lock safety

```text
client A lease expires -> client B gets token 42
delayed client A writes with token 41 -> storage rejects it
```

Leases alone are insufficient because a paused process can wake after expiry.

## Common mistakes

- Building a custom consensus or lock protocol from database rows and timers.
- Assuming exactly one leader without terms/fencing.
- Using wall-clock time as the only ordering authority.
- Choosing an even quorum size and expecting extra fault tolerance.
