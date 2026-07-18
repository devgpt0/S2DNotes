# 10 - Producer-Consumer and Bounded Buffer Patterns

## 1) Purpose

Producers create work, consumers process it, and a queue separates their execution rates. A bounded queue supplies backpressure and a memory limit.

```java
BlockingQueue<String> queue = new ArrayBlockingQueue<>(2);

Thread producer = Thread.startVirtualThread(() -> {
    try {
        queue.put("job-1");
        queue.put("job-2");
    } catch (InterruptedException exception) {
        Thread.currentThread().interrupt();
    }
});

Thread consumer = Thread.startVirtualThread(() -> {
    try {
        System.out.println(queue.take());
        System.out.println(queue.take());
    } catch (InterruptedException exception) {
        Thread.currentThread().interrupt();
    }
});

producer.join();
consumer.join();
// Output:
// job-1
// job-2
```

## 2) Queue Choices

- `ArrayBlockingQueue`: bounded array with fixed capacity
- `LinkedBlockingQueue`: optionally bounded linked nodes; specify capacity
- `SynchronousQueue`: direct handoff with no storage
- `PriorityBlockingQueue`: priority order but unbounded
- `DelayQueue`: elements become available after a delay

## 3) Poison Pill Shutdown

```java
String stop = "STOP";
BlockingQueue<String> queue = new ArrayBlockingQueue<>(2);
queue.put("job");
queue.put(stop);
while (true) {
    String value = queue.take();
    if (value.equals(stop)) {
        break;
    }
    System.out.println(value);
}
// Output: job
```

Use a unique sentinel that cannot be confused with valid data. Multiple consumers normally require one pill per consumer. Interruption or closing abstractions are often cleaner.

## 4) Batch Draining

```java
BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(10);
queue.addAll(List.of(1, 2, 3));
List<Integer> batch = new ArrayList<>();
queue.drainTo(batch, 2);
System.out.println(batch);
System.out.println(queue);
// Output:
// [1, 2]
// [3]
```

Batching can improve throughput but adds latency. Define maximum batch size and wait time.

## 5) Failure Policy

Specify whether a failed job is retried, dead-lettered, skipped, or stops the consumer. Never catch and silently discard failures. Keep queue capacity, processing rate, retry rate, and shutdown behavior observable.
