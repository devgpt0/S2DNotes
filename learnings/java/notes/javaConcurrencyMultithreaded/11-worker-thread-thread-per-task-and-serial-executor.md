# 11 - Worker Thread, Thread-Per-Task, and Serial Executor Patterns

## 1) Worker Thread Pattern

A stable set of workers repeatedly takes tasks from a queue. `ThreadPoolExecutor` is the standard implementation.

```java
try (ExecutorService workers = Executors.newFixedThreadPool(2)) {
    List<Callable<String>> tasks = List.of(
            () -> "processed-A",
            () -> "processed-B");
    for (Future<String> result : workers.invokeAll(tasks)) {
        System.out.println(result.get());
    }
}
// Output:
// processed-A
// processed-B
```

`invokeAll` returns futures in input order, even if completion order differs.

## 2) Thread-Per-Task Pattern

Virtual threads make one thread per blocking task practical.

```java
try (ExecutorService tasks = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> result = tasks.submit(() -> "handled by virtual thread");
    System.out.println(result.get());
}
// Output: handled by virtual thread
```

Thread-per-task simplifies call stacks, exceptions, and thread-local reasoning. Bound access to downstream resources.

## 3) Serial Executor Pattern

A single-thread executor preserves task order and confines mutable state.

```java
try (ExecutorService serial = Executors.newSingleThreadExecutor()) {
    List<String> events = new ArrayList<>();
    Future<?> first = serial.submit(() -> events.add("A"));
    Future<?> second = serial.submit(() -> events.add("B"));
    first.get();
    second.get();
    System.out.println(events);
}
// Output: [A, B]
```

This is useful for per-key ordering, but one global serial executor can become a bottleneck.

## 4) Keyed Serial Execution

Partition work by a stable key and route each key to one serial lane. Events for the same account remain ordered while different accounts progress concurrently.

```java
int lane = Math.floorMod("account-42".hashCode(), 4);
System.out.println(lane >= 0 && lane < 4);
// Output: true
```

Use a fixed lane count rather than creating an unbounded executor per key. Hot keys can still overload one lane.

## 5) Leader-Follower Pattern

A pool waits for events; one thread becomes leader, receives an event, promotes another leader, and processes the event. Modern Java servers and event libraries implement this internally. Prefer their tested implementations over custom coordination.
