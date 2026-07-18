# 13 - Pipeline, Fan-Out/Fan-In, and Fork/Join Patterns

## 1) Pipeline Pattern

Each stage performs one transformation and hands results to the next stage.

```java
BlockingQueue<String> input = new ArrayBlockingQueue<>(4);
BlockingQueue<String> normalized = new ArrayBlockingQueue<>(4);
input.put(" java ");

Thread stage = Thread.startVirtualThread(() -> {
    try {
        normalized.put(input.take().strip().toUpperCase());
    } catch (InterruptedException exception) {
        Thread.currentThread().interrupt();
    }
});
stage.join();
System.out.println(normalized.take());
// Output: JAVA
```

Bound every stage. A slow downstream stage must push pressure upstream rather than grow memory without limit.

## 2) Fan-Out

Split independent work across several tasks.

```java
try (ExecutorService executor = Executors.newFixedThreadPool(3)) {
    List<Callable<Integer>> tasks = IntStream.rangeClosed(1, 3)
            .mapToObj(value -> (Callable<Integer>) () -> value * value)
            .toList();
    List<Integer> results = executor.invokeAll(tasks).stream()
            .map(future -> {
                try {
                    return future.get();
                } catch (InterruptedException exception) {
                    Thread.currentThread().interrupt();
                    throw new CancellationException("interrupted");
                } catch (ExecutionException exception) {
                    throw new CompletionException(exception.getCause());
                }
            })
            .toList();
    System.out.println(results);
}
// Output: [1, 4, 9]
```

## 3) Fan-In

Combine independent results into one result.

```java
CompletableFuture<Integer> a = CompletableFuture.completedFuture(10);
CompletableFuture<Integer> b = CompletableFuture.completedFuture(20);
CompletableFuture<Integer> c = CompletableFuture.completedFuture(30);
int total = a.thenCombine(b, Integer::sum).thenCombine(c, Integer::sum).join();
System.out.println(total);
// Output: 60
```

Define partial-failure, cancellation, and deadline behavior for the whole operation.

## 4) Fork/Join Divide and Conquer

```java
final class SumTask extends RecursiveTask<Long> {
    private final long start;
    private final long end;

    SumTask(long start, long end) {
        this.start = start;
        this.end = end;
    }

    protected Long compute() {
        if (end - start <= 10) {
            return LongStream.rangeClosed(start, end).sum();
        }
        long middle = (start + end) >>> 1;
        SumTask left = new SumTask(start, middle);
        left.fork();
        long right = new SumTask(middle + 1, end).compute();
        return left.join() + right;
    }
}

try (ForkJoinPool pool = new ForkJoinPool()) {
    System.out.println(pool.invoke(new SumTask(1, 100)));
}
// Output: 5050
```

Fork/join suits CPU-bound recursive decomposition. Choose a threshold large enough to make splitting worthwhile and avoid blocking I/O in the pool.

## 5) Map-Reduce Pattern

Map inputs into independent intermediate values, then reduce them associatively. Java streams implement this shape; parallel use requires stateless mapping and an associative reduction.
