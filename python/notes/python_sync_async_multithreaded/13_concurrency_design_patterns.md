# Concurrency Design Patterns

## 1) Producer-Consumer

Use bounded queue between producers and consumers.
Benefits:
- decouples rates
- supports backpressure
- simplifies worker scaling

## 2) Worker Pool

Use fixed-size thread/process pools for bounded parallelism.
Avoid unbounded worker creation.

## 3) Pipeline Pattern

Split workflow into stages:
- ingest
- parse
- transform
- persist

Each stage can use different concurrency model based on bottleneck type.

## 4) Fan-Out / Fan-In

- fan-out: dispatch work to many workers
- fan-in: aggregate results safely

Requires:
- error aggregation strategy
- partial-result handling policy

## 5) Bulkhead Isolation

Isolate critical components so failure in one area does not exhaust all workers/resources.

## 6) Supervisor Pattern

Track child tasks/workers with explicit lifecycle and restart policy when appropriate.

## 7) Rate Limiter + Semaphore Pattern

Combine:
- rate limiter (requests/time)
- semaphore (max concurrent in-flight)

Helps protect external dependencies.

## 8) Pattern Selection Heuristics

1. I/O wait heavy -> async + semaphore + queue
2. blocking library heavy -> thread pool
3. CPU-heavy stage -> process pool
4. mixed workflow -> staged pipeline with per-stage model choice

## 9) Anti-Patterns

- fire-and-forget tasks without supervision
- unbounded queues
- one global lock around whole service
- retries without timeout/deadline

## 10) Interview Questions

1. Which pattern for variable producer/consumer speeds?
2. How to isolate failures between subsystems?
3. How to choose concurrency per pipeline stage?
4. How to supervise lifecycle of worker tasks?
