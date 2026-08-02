# Design a Distributed Cache Service

> **Difficulty:** Hard  
> **Main focus:** partitioning, eviction, consistency

## Interview prompt

Design a multi-tenant in-memory cache used by many backend services.

## 1. Clarify the scope

**What I would say first:** The cache improves latency but must not become the only copy of critical data. I will define key size, value size, TTL, eviction, and failure semantics.

### Functional requirements

- Get, set, delete, increment, compare-and-set, and TTL.
- Partition and replicate data across cache nodes.
- Enforce tenant quotas and protect hot keys.
- Add/remove nodes without moving every key.

### Out of scope for the first version

- Durable database guarantees are explicitly out of scope.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume tens of millions of operations per second and terabytes of memory.
- Network, serialization, and memory overhead matter as much as algorithmic complexity.
- A small number of hot keys can dominate one shard.

## 3. API and data model

### Main contracts

- GET(key) -> value, version, ttl
- SET(key, value, ttl, expectedVersion?)
- DELETE(key); INCR(key, delta, ttl)

### Important data

- In-memory entry(key_hash, key, value, version, expires_at, size, eviction_metadata)
- Cluster map(node_id, token_ranges, replica_set, epoch)

## 4. High-level design

```text
service clients -> cache SDK / proxy -> cluster map
                         |                  |
                         +-> shard primary -> replica
                         +-> shard primary -> replica
control plane -> membership, rebalancing, quota, health
```

## 5. Critical request flow

1. Client hashes the namespaced key onto a virtual-node ring.
2. Primary validates size and quota, performs the operation, and replicates per durability mode.
3. Reads use primary or replica according to staleness policy.
4. Lazy expiry removes stale entries on access; background sampling reclaims memory.
5. Membership changes stream keys while old owners serve until an epoch cutover.

## 6. Deep dive

- Use consistent hashing with many virtual nodes to reduce movement and balance capacity.
- Eviction can approximate LRU or LFU; tenant memory partitions prevent noisy neighbors.
- Hot-key replication or client request coalescing spreads read load.
- Cache-aside callers need stampede protection and must treat misses and timeouts correctly.

## 7. Scaling, failures, and observability

- Node failure promotes a replica or creates misses; databases absorb load only through controlled refill.
- Use randomized TTLs and single-flight loading to prevent synchronized expiry storms.
- During rebalancing, dual reads or forwarding handle keys in motion.
- Monitor hit ratio by tenant, evictions, memory fragmentation, hot keys, latency, and backend amplification.

## 8. Security and privacy

- Namespace and authenticate tenants; never allow arbitrary cross-tenant key access.
- Encrypt traffic, limit value size, and avoid caching secrets unless explicitly protected.
- Reject unsafe administrative commands from data-plane clients.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Client-side sharding | Low proxy overhead but harder membership rollout. |
| Proxy routing | Centralized policy with another hop. |
| Synchronous replicas | Fewer misses after failure with higher write latency. |
| Asynchronous replicas | Faster writes with possible recent loss. |

## 10. 60-second interview summary

A namespaced, quota-aware cache uses consistent hashing, replication, TTL, and approximate eviction. It remains disposable derived state, while hot-key replication, request coalescing, and controlled refill prevent cache failures from overwhelming databases.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you recover and prove no work was lost?
- Which metric best reflects the user's experience?

