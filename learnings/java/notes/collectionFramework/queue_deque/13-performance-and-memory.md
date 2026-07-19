# 13 - Performance and Memory

## 1) Quick Comparison

- `ArrayDeque`: fast amortized end ops, array-backed
- `LinkedList`: end ops `O(1)`, higher node overhead
- `PriorityQueue`: `O(log n)` for insert/remove by priority
- `ArrayBlockingQueue`: bounded, predictable memory
- `LinkedBlockingQueue`: flexible size, node allocation overhead
- `ConcurrentLinkedQueue`: non-blocking, unbounded

## 2) Throughput vs Latency Tradeoff

- blocking queues reduce busy-wait CPU usage
- lock-free queues reduce blocking overhead under high contention

## 3) Capacity Planning

Concept taught: Bounded queue protects memory under producer spikes.

```java
BlockingQueue<Integer> q = new ArrayBlockingQueue<>(1000);
System.out.println(q.remainingCapacity());
```

Expected output:

```text
1000
```

## 4) Avoid Unbounded Growth by Default

`LinkedBlockingQueue()` default capacity is huge; use explicit capacity for production pipelines.

## 5) PriorityQueue Notes

Heap operations are `O(log n)`.

Do not expect sorted iteration; only head is guaranteed min/max according to comparator.

## 6) Summary

Queue performance tuning is mostly about choosing bounded vs unbounded, blocking vs non-blocking, and required ordering semantics.
