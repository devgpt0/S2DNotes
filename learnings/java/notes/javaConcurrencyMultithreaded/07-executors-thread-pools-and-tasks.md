# 07 - Executors, Thread Pools, and Tasks

## 1) Separate Tasks from Threads

`Runnable` produces no value; `Callable<T>` returns a value and may throw checked exceptions.

```java
Callable<Integer> task = () -> 40 + 2;
try (ExecutorService executor = Executors.newSingleThreadExecutor()) {
    System.out.println(executor.submit(task).get());
}
// Output: 42
```

## 2) Fixed Pool for CPU-Bound Work

```java
int processors = Runtime.getRuntime().availableProcessors();
try (ExecutorService executor = Executors.newFixedThreadPool(processors)) {
    Future<Long> result = executor.submit(() -> LongStream.rangeClosed(1, 100).sum());
    System.out.println(result.get());
}
// Output: 5050
```

Measure CPU workloads. More threads than cores can increase scheduling overhead.

## 3) Explicit Bounded Pool

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
        4,
        4,
        0L,
        TimeUnit.MILLISECONDS,
        new ArrayBlockingQueue<>(100),
        new ThreadPoolExecutor.CallerRunsPolicy());
try {
    System.out.println(executor.getMaximumPoolSize());
} finally {
    executor.shutdown();
}
// Output: 4
```

An unbounded queue can convert overload into memory exhaustion and extreme latency. Define capacity and a deliberate rejection policy.

## 4) Completion Order

```java
try (ExecutorService executor = Executors.newFixedThreadPool(2)) {
    CompletionService<String> completed = new ExecutorCompletionService<>(executor);
    completed.submit(() -> "A");
    completed.submit(() -> "B");
    System.out.println(completed.take().get());
    System.out.println(completed.take().get());
}
// Output: A then B, or B then A.
```

## 5) Shutdown

```java
ExecutorService executor = Executors.newSingleThreadExecutor();
executor.shutdown();
System.out.println(executor.awaitTermination(1, TimeUnit.SECONDS));
// Output: true
```

Use `shutdown` for orderly completion. Use `shutdownNow` to request interruption of running tasks and return queued tasks. Tasks must cooperate with interruption.
