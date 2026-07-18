# 06 - Thread-Safe Design, Immutability, and Confinement

## 1) Stateless Objects

```java
final class PriceCalculator {
    BigDecimal addTax(BigDecimal price) {
        return price.multiply(new BigDecimal("1.18"));
    }
}

System.out.println(new PriceCalculator().addTax(new BigDecimal("100.00")));
// Output: 118.0000
```

Stateless objects are naturally thread-safe when their dependencies are thread-safe.

## 2) Immutable Objects

```java
record Snapshot(List<String> values) {
    Snapshot {
        values = List.copyOf(values);
    }
}

List<String> source = new ArrayList<>(List.of("A"));
Snapshot snapshot = new Snapshot(source);
source.add("B");
System.out.println(snapshot.values());
// Output: [A]
```

Immutability requires defensive copies of mutable components.

## 3) Thread Confinement

```java
try (ExecutorService executor = Executors.newSingleThreadExecutor()) {
    Future<Integer> result = executor.submit(() -> {
        List<Integer> local = new ArrayList<>();
        local.add(10);
        local.add(20);
        return local.stream().mapToInt(Integer::intValue).sum();
    });
    System.out.println(result.get());
}
// Output: 30
```

The mutable list never escapes its task, so it needs no synchronization.

## 4) Ownership Transfer

Passing an immutable value through a `BlockingQueue` transfers work safely between threads.

```java
record Job(long id) {}

BlockingQueue<Job> queue = new ArrayBlockingQueue<>(1);
queue.put(new Job(7));
System.out.println(queue.take());
// Output: Job[id=7]
```

## 5) Safe Collection Choices

- `ConcurrentHashMap` for scalable concurrent key access
- `CopyOnWriteArrayList` for small, read-heavy listener snapshots
- `BlockingQueue` for bounded handoff
- immutable collection snapshots for read-only sharing
- synchronized compound operation when multiple calls must be atomic together

A thread-safe collection does not make a multi-step check-then-act sequence atomic. Use methods such as `computeIfAbsent` that express the compound action.
