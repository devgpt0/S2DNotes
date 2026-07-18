# 16 - Timeout, Retry, Backpressure, Bulkhead, and Rate-Limit Patterns

## 1) Deadline and Timeout

Every wait should be bounded by the caller's remaining deadline.

```java
try (ExecutorService executor = Executors.newSingleThreadExecutor()) {
    Future<String> result = executor.submit(() -> "ready");
    System.out.println(result.get(500, TimeUnit.MILLISECONDS));
}
// Output: ready
```

Cancelling the future may not cancel underlying network or database work; configure timeouts at that boundary too.

## 2) Retry Pattern

Retry only known transient failures and only when repeating the operation is safe.

```java
static String retry(int maxAttempts, Supplier<String> operation) {
    if (maxAttempts <= 0) {
        throw new IllegalArgumentException("maxAttempts must be positive");
    }
    for (int attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            return operation.get();
        } catch (IllegalStateException exception) {
            if (attempt == maxAttempts) {
                throw exception;
            }
        }
    }
    throw new AssertionError("unreachable");
}

AtomicInteger attempts = new AtomicInteger();
String result = retry(3, () -> {
    if (attempts.incrementAndGet() < 2) {
        throw new IllegalStateException("temporary");
    }
    return "ready";
});
System.out.println(result + " after " + attempts.get() + " attempts");
// Output: ready after 2 attempts
```

Production retries need exponential backoff, jitter, an overall deadline, metrics, and an explicit exception predicate. Never retry invalid input or authorization failures.

## 3) Backpressure Pattern

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
        1, 1, 0, TimeUnit.MILLISECONDS,
        new ArrayBlockingQueue<>(1),
        new ThreadPoolExecutor.CallerRunsPolicy());
try {
    System.out.println(executor.getQueue().remainingCapacity());
} finally {
    executor.shutdown();
}
// Output: 1
```

A bounded queue limits retained work. `CallerRunsPolicy` slows submitters, but it is inappropriate when the caller must never block.

## 4) Bulkhead Pattern

Isolate scarce capacity so one dependency cannot consume everything.

```java
Semaphore paymentBulkhead = new Semaphore(2);
if (!paymentBulkhead.tryAcquire()) {
    System.out.println("payment capacity unavailable");
} else {
    try {
        System.out.println("payment admitted");
    } finally {
        paymentBulkhead.release();
    }
}
// Output: payment admitted
```

Use separate pools or semaphores for independent failure domains.

## 5) Rate Limiter Pattern

```java
Semaphore oneRequest = new Semaphore(1);
System.out.println(oneRequest.tryAcquire());
System.out.println(oneRequest.tryAcquire());
// Output:
// true
// false
// A real token-bucket limiter replenishes permits according to elapsed monotonic time.
```

Rate limits control work per time period; bulkheads control simultaneous work.

## 6) Scheduler Pattern

```java
try (ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor()) {
    ScheduledFuture<String> future = scheduler.schedule(
            () -> "scheduled", 10, TimeUnit.MILLISECONDS);
    System.out.println(future.get());
}
// Output: scheduled
```

Use fixed rate when cadence matters and overlapping work is controlled. Use fixed delay when the pause should begin after the previous run finishes. A multi-instance service needs distributed coordination when a job must run only once globally.

## 7) Circuit Breaker Pattern

A circuit breaker moves through closed, open, and half-open states. It stops calls after repeated failures, waits for a cooldown, then permits limited probes. Use a proven library because time, concurrency, rolling statistics, and state transitions are easy to implement incorrectly.

Fallbacks must be semantically valid. Returning stale or invented data can be worse than failing explicitly.
