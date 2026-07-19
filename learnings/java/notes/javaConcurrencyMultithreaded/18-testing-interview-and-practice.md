# 18 - Testing, Interview Revision, and Practice

## 1) Deterministic Coordination

Use latches, barriers, and futures instead of arbitrary sleeps.

```java
CountDownLatch started = new CountDownLatch(1);
Thread worker = Thread.startVirtualThread(() -> started.countDown());
System.out.println(started.await(1, TimeUnit.SECONDS));
worker.join();
// Output: true
```

## 2) Test Completion and Failure

```java
try (ExecutorService executor = Executors.newSingleThreadExecutor()) {
    Future<Integer> result = executor.submit(() -> 42);
    System.out.println(result.get(1, TimeUnit.SECONDS));
}
// Output: 42
```

Tests should fail on timeout rather than hang forever.

## 3) Stress Testing

Run the same state transition many times with coordinated starts and assert invariants, but remember that passing a stress test does not prove correctness. Use tools designed for concurrency testing and Java Memory Model outcomes when validating lock-free algorithms.

```java
AtomicInteger counter = new AtomicInteger();
IntStream.range(0, 100_000).parallel().forEach(index -> counter.incrementAndGet());
System.out.println(counter.get());
// Output: 100000
```

## 4) Interview Quick Answers

- Concurrency is overlapping progress; parallelism is simultaneous execution.
- `volatile` supplies visibility and ordering, not atomic compound updates.
- `synchronized` supplies mutual exclusion and happens-before visibility.
- `wait` must be used inside a loop while owning the monitor.
- `Future.get` establishes visibility of task results and propagates failure.
- Interruption is a cooperative cancellation request, not forced termination.
- A bounded queue prevents overload from becoming unbounded memory growth.
- Virtual threads scale blocking I/O, not CPU capacity.
- `CompletableFuture.thenCompose` flattens dependent asynchronous operations.
- Deadlock is no progress due to cyclic waiting; livelock is activity without progress.
- Copy-on-write fits read-heavy, write-light data.
- Fork/join fits CPU-bound recursive decomposition.

## 5) Pattern Selection Guide

- sequential steps: synchronous call
- many blocking requests: virtual thread per task
- bounded CPU work: fixed executor
- decoupled stages: producer-consumer pipeline
- ordered mutable state: serial executor or event loop
- asynchronous method interface: Active Object / future
- parallel independent calls: fan-out/fan-in with a deadline
- recursive CPU task: fork/join
- demand-driven stream: reactive streams
- read-heavy listener list: copy-on-write
- overload containment: bounded queue, bulkhead, rate limiter
- transient remote failure: bounded retry plus timeout and jitter

## 6) Practice Tasks

1. Build a bounded producer-consumer system with graceful shutdown.
2. Implement a thread-safe account transfer using global lock ordering.
3. Compose three independent futures with one overall deadline.
4. Replace a platform-thread pool used for blocking HTTP calls with virtual threads and preserve downstream limits.
5. Build a three-stage bounded pipeline and expose queue-depth metrics.
6. Demonstrate a data race, then fix it using a lock and an atomic variable separately.
7. Implement per-customer serial processing with a fixed number of lanes.
8. Test interruption and two-phase termination without using `Thread.sleep` for coordination.
9. Diagnose a supplied thread dump for deadlock, starvation, or pool exhaustion.
10. Design retry, bulkhead, rate-limit, and circuit-breaker policies for an idempotent external call.

## 7) Final Production Checklist

- shared state and its synchronization policy are documented
- all queues and executors are bounded or intentionally task-per-virtual-thread
- interruption and shutdown propagate correctly
- waits and external calls have deadlines
- retry and fallback behavior is explicit and safe
- downstream capacity is protected
- task failures are observed
- metrics reveal latency, saturation, rejection, and cancellation
- correctness is tested under contention
- performance decisions are backed by measurement
