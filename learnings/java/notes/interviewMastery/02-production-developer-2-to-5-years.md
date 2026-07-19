# 02 - Production Developer Coverage: 2 to 5 Years

## Core Java Depth

- type erasure and wildcard API design
- records, sealed types, pattern matching
- streams: laziness, reduction, collectors, parallel constraints
- java.time and timezone correctness
- NIO files, serialization risks, HTTP client
- annotations/reflection and proxy concepts
- JUnit, Mockito, integration tests, Testcontainers

## Concurrency

- atomicity, visibility, ordering, happens-before
- synchronized, locks, atomics, concurrent collections
- executors, queue capacity, rejection, shutdown
- Future, CompletableFuture, timeout, cancellation
- virtual threads for blocking I/O
- deadlock prevention and thread dumps

## Spring Boot

- dependency injection and bean scopes
- auto-configuration conditions
- MVC request lifecycle, validation, Problem Details
- JPA persistence context, transactions, N+1
- Spring Security authentication/authorization
- configuration properties and profiles
- MVC/repository/full-context testing
- Actuator, metrics, logs, traces

## Database and APIs

- joins, indexes, normalization, ACID, isolation
- pagination and stable ordering
- optimistic locking and uniqueness constraints
- idempotent HTTP methods and status codes
- retries only for safe transient failures

## Expected Production Discussion

Explain one bug from symptom to root cause, evidence, fix, test, rollout, and prevention. Avoid answers that stop at adding a catch block, increasing memory, or restarting the service.
