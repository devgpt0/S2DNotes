# 03 - Senior Engineer Coverage: 5 to 8 Years

## Design and Architecture

- module and service boundaries from domain ownership
- layered vs hexagonal architecture
- all GoF patterns and when not to use them
- repository, outbox, saga, CQRS tradeoffs
- backward-compatible API and schema evolution
- modular monolith vs microservices

## Distributed Systems

- partial failure, timeout, retry, jitter, bulkhead, circuit breaker
- at-least-once delivery and idempotent consumers
- consistency, replication, partitioning, ordering
- cache invalidation and stale-data policy
- rate limiting and overload behavior
- tracing and correlation across async boundaries

## Performance

- measure latency percentiles, throughput, saturation, allocation
- identify N+1, missing index, pool exhaustion, lock contention
- use JFR, heap dump, thread dump, GC logs, query plans
- load test with realistic data and think time
- distinguish CPU, memory, I/O, database, and downstream bottlenecks

## Security

- threat modeling and least privilege
- OAuth2/OIDC/JWT validation and object authorization
- injection, SSRF, path traversal, XSS, deserialization
- secret management and dependency vulnerabilities
- audit without sensitive-data leakage

## Leadership Evidence

- review design and code with actionable reasoning
- mentor engineers and reduce recurring defects
- own rollout, observability, migration, and rollback
- communicate tradeoffs to engineering/product/operations
- improve a system rather than only deliver a feature
