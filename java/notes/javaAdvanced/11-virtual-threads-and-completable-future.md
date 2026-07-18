# 11 - Virtual Threads and CompletableFuture

## 1) Virtual Threads

Virtual threads make thread-per-task practical for large numbers of blocking I/O tasks. They do not make CPU work faster.

```java
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> future = executor.submit(() -> "thread=" + Thread.currentThread().isVirtual());
    System.out.println(future.get());
}
// Output: thread=true
```

Keep tasks independent and avoid long blocking operations while holding a monitor or native lock.

## 2) Failure Propagation

```java
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<Integer> future = executor.submit(() -> 20 + 22);
    System.out.println(future.get());
}
// Output: 42
```

`Future.get()` rethrows task failure as `ExecutionException`; interruption must not be silently ignored.

## 3) CompletableFuture Composition

```java
CompletableFuture<Integer> price = CompletableFuture.completedFuture(100);
CompletableFuture<Integer> taxed = price.thenApply(value -> value + 18);
System.out.println(taxed.join());
// Output: 118
```

Use `thenCompose` when the next operation itself returns a `CompletableFuture`.

```java
CompletableFuture<String> user = CompletableFuture.completedFuture("Asha");
CompletableFuture<String> greeting = user.thenCompose(
        name -> CompletableFuture.completedFuture("Hello " + name));
System.out.println(greeting.join());
// Output: Hello Asha
```

## 4) Timeouts and Executors

```java
String result = CompletableFuture.completedFuture("ready")
        .orTimeout(1, TimeUnit.SECONDS)
        .join();
System.out.println(result);
// Output: ready
```

- Supply an explicit executor when workload isolation matters.
- Bound concurrency at downstream resources such as database connection pools.
- Add timeouts; cancellation does not always stop underlying I/O.
- Prefer simple synchronous code on virtual threads for blocking request flows.
