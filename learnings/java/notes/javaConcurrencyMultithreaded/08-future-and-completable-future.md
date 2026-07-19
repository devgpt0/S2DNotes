# 08 - Future and CompletableFuture

## Beginner Meaning

A `Future` is a receipt for work that may finish later. You can wait for its value, observe failure, or request cancellation. `CompletableFuture` also lets you describe what should happen after that value arrives.

## 1) `Future`

```java
try (ExecutorService executor = Executors.newSingleThreadExecutor()) {
    Future<String> future = executor.submit(() -> "ready");
    System.out.println(future.get(1, TimeUnit.SECONDS));
}
// Output: ready
```

`get` blocks and wraps task failure in `ExecutionException`. Always use a deadline when indefinite waiting is unsafe.

## 2) Transform a Result

```java
CompletableFuture<Integer> future = CompletableFuture
        .completedFuture("Java")
        .thenApply(String::length);
System.out.println(future.join());
// Output: 4
```

## 3) Compose Asynchronous Operations

```java
CompletableFuture<String> user = CompletableFuture.completedFuture("Asha");
CompletableFuture<String> greeting = user.thenCompose(name ->
        CompletableFuture.completedFuture("Hello " + name));
System.out.println(greeting.join());
// Output: Hello Asha
```

Use `thenCompose` instead of producing `CompletableFuture<CompletableFuture<T>>`.

## 4) Combine Independent Results

```java
CompletableFuture<Integer> price = CompletableFuture.completedFuture(100);
CompletableFuture<Integer> tax = CompletableFuture.completedFuture(18);
System.out.println(price.thenCombine(tax, Integer::sum).join());
// Output: 118
```

## 5) Error Handling

```java
CompletableFuture<String> failed = CompletableFuture.failedFuture(
        new IllegalStateException("unavailable"));
String result = failed.exceptionally(error -> "fallback").join();
System.out.println(result);
// Output: fallback
```

Fallbacks must be valid business behavior, not a way to hide data corruption or authorization failures.

## 6) Timeout and Cancellation

```java
String result = CompletableFuture.completedFuture("ready")
        .orTimeout(1, TimeUnit.SECONDS)
        .join();
System.out.println(result);
// Output: ready
```

Cancellation of a `CompletableFuture` does not guarantee that underlying work or I/O stops. Propagate deadlines to the resource performing the work.

## 7) Executor Choice

Async methods without an executor commonly use the shared common pool. Supply a bounded executor when isolation, capacity, naming, or workload ownership matters.
