# Java Concurrency and Multithreading - Complete Roadmap

These notes target Java 21 or newer. They cover synchronous, asynchronous, concurrent, multithreaded, and parallel programming, followed by the concurrency patterns used in production systems.

Beginner mental model: imagine several workers sharing one kitchen. Concurrency problems happen when workers change the same order or use the same tool without coordination. Learn one thread first, then visibility/locks, then executors/futures, and only then the design patterns.

## Learning Order

1. [Execution models](01-sync-async-concurrent-and-parallel.md)
2. [Threads and lifecycle](02-threads-lifecycle-and-interruption.md)
3. [Java Memory Model](03-java-memory-model.md)
4. [Synchronization and monitors](04-synchronization-and-monitors.md)
5. [Locks and synchronizers](05-locks-atomics-and-synchronizers.md)
6. [Thread-safe design](06-thread-safety-immutability-and-confinement.md)
7. [Executors and task management](07-executors-thread-pools-and-tasks.md)
8. [Future and CompletableFuture](08-future-and-completable-future.md)
9. [Virtual threads](09-virtual-threads.md)
10. [Producer-consumer and bounded buffer](10-producer-consumer-and-bounded-buffer.md)
11. [Worker thread and serial execution](11-worker-thread-thread-per-task-and-serial-executor.md)
12. [Guarded suspension, balking, and termination](12-guarded-suspension-balking-and-termination.md)
13. [Pipeline, fan-out/fan-in, and fork/join](13-pipeline-fanout-fanin-and-forkjoin.md)
14. [Active Object, event loop, and reactive streams](14-active-object-event-loop-and-reactive-streams.md)
15. [Read/write, copy-on-write, cache, and thread-local patterns](15-read-write-copy-on-write-cache-and-thread-local.md)
16. [Resilience and flow-control patterns](16-timeout-retry-backpressure-bulkhead-and-rate-limit.md)
17. [Concurrency failures and diagnosis](17-deadlock-livelock-starvation-and-diagnosis.md)
18. [Testing, interview revision, and practice](18-testing-interview-and-practice.md)
19. [Concurrency pattern coverage map](19-concurrency-design-pattern-coverage-map.md)

## Core Rules

- Prefer immutable data and ownership over shared mutable state.
- Use high-level concurrency utilities before low-level `wait`/`notify`.
- Treat interruption as cancellation and preserve it.
- Bound threads, queues, memory, retries, and downstream concurrency.
- Prove correctness first; measure before optimizing.
