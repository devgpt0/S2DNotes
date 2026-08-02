# Horizontal Scaling and Load Balancing

## Idea

Horizontal scaling adds service instances. A load balancer routes work only to
healthy instances and prevents one instance from becoming the entry bottleneck.

## Visual model

```text
clients -> DNS/edge -> load balancer -> stateless instances -> shared state
```

## Design steps

1. Keep request handlers stateless where practical.
2. Add health/readiness checks and connection draining.
3. Choose routing: round robin, least requests, weighted, or consistent hash.
4. Autoscale from saturation signals, not CPU alone.
5. Bound concurrency and shed load before collapse.

## When to use it

Scale horizontally when traffic exceeds one instance or availability requires
failure isolation. Sticky routing is useful only when local connection/session
state cannot be externalized.

## Trade-offs

More instances add coordination, rollout, and observability complexity. Sticky
sessions simplify local state but create imbalance and failover pain.

## Common mistakes

- Health check says “process runs” while dependencies are unusable.
- Scaling a stateless tier while the database remains saturated.
- Killing instances without draining requests/connections.
- Infinite queues instead of overload rejection.
