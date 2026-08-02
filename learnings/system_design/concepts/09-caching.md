# Caching

## Idea

A cache stores a cheaper copy of expensive data. It improves latency and load
only when hit rate, freshness, and invalidation are designed.

## Visual model

```text
cache-aside read: cache hit -> return
                  cache miss -> database -> cache -> return
write: database -> invalidate/update cache
```

## Design steps

1. Choose what is safe and valuable to cache.
2. Define key, value, TTL, size, and eviction.
3. Choose cache-aside, read-through, write-through, or write-behind.
4. Prevent stampedes with request coalescing, jitter, or stale-while-revalidate.
5. Measure hit rate, miss latency, evictions, and hot keys.

## When to use it

Use caches for read-heavy reused data or expensive computation. Do not cache
sensitive responses under keys that omit identity/authorization context.

## Trade-offs

Long TTL improves hit rate but increases staleness. Distributed caches add a
network dependency; local caches are faster but inconsistent across instances.

## Common mistakes

- Treating cache as authoritative storage.
- No TTL or invalidation path.
- Caching “not found” forever.
- One hot key overwhelming a shard after expiry.
