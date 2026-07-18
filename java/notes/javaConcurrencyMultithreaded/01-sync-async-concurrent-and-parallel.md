# 01 - Synchronous, Asynchronous, Concurrent, and Parallel Execution

## 1) Synchronous Execution

The caller waits until the operation completes.

```java
static String loadUser() {
    return "Asha";
}

System.out.println("before");
System.out.println(loadUser());
System.out.println("after");
// Output:
// before
// Asha
// after
```

Synchronous code is usually the easiest to reason about, test, and debug.

## 2) Asynchronous Execution

The caller starts work and receives a handle to a future result.

```java
try (ExecutorService executor = Executors.newSingleThreadExecutor()) {
    CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> "Asha", executor);
    System.out.println("submitted");
    System.out.println(future.join());
}
// Output:
// submitted
// Asha
```

Asynchronous does not mean parallel. A single-thread executor performs tasks one at a time but callers can submit without doing the work themselves.

## 3) Concurrency vs Parallelism

- Concurrency: multiple tasks make progress during overlapping time.
- Parallelism: multiple tasks execute at the same instant on different CPU cores.
- Multithreading: multiple threads exist in one process; they may be concurrent or parallel.

```java
try (ExecutorService executor = Executors.newFixedThreadPool(2)) {
    Future<String> first = executor.submit(() -> "first");
    Future<String> second = executor.submit(() -> "second");
    System.out.println(first.get() + ", " + second.get());
}
// Output: first, second
// Actual completion order is not guaranteed.
```

## 4) Blocking vs Non-Blocking

- Blocking waits by parking or occupying the current thread until progress is possible.
- Non-blocking algorithms make progress without mutual-exclusion blocking, often using atomic compare-and-set.
- Asynchronous APIs can still use blocking work internally.

## 5) Choose the Simplest Model

- sequential synchronous code for small ordered work
- virtual thread per task for many blocking I/O operations
- fixed CPU-sized pool or parallel algorithm for CPU-bound work
- `CompletableFuture` for explicit asynchronous composition
- queues for decoupled bounded stages
- reactive streams when end-to-end demand and backpressure are required
