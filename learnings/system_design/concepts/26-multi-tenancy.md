# Multi-Tenancy

## Idea

A multi-tenant system serves organizations on shared infrastructure while
isolating data, performance, configuration, and billing.

## Classroom board

```text
authenticated user -> tenant context -> authorization
tenant ID -> every row/cache key/event/object/metric
heavy tenant -> quota or dedicated partition
```

## Design steps

1. Derive tenant identity from trusted authentication.
2. Include tenant in storage, cache, search, queue, and object keys.
3. Enforce row/resource policies and per-tenant quotas.
4. Meter usage and provide deletion/export/audit workflows.

## When to use it

Use shared tables for efficiency, separate schemas/databases for stronger
isolation, or a hybrid for very large/compliance tenants.

## Trade-offs and mistakes

Isolation costs efficiency. The worst bug is a missing tenant predicate; test
cross-tenant access explicitly and prevent noisy-neighbor resource capture.
