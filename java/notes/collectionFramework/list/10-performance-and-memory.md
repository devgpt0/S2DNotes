# 10 - Performance and Memory

## 1) Choose by Access Pattern

- mostly random read by index: `ArrayList`
- frequent end operations and deque use: `LinkedList` or `ArrayDeque` (for deque)
- read-heavy concurrent iteration: `CopyOnWriteArrayList`

## 2) Micro-Cost Insights

- boxing (`int` -> `Integer`) adds overhead
- large object lists increase GC pressure
- avoid repeated `contains` on list in hot loops (`Set` may be better)

## 3) Pre-size for Large Loads

```java
ArrayList<Integer> list = new ArrayList<>(1_000_000);
```

Reduces resize operations during bulk insert.

## 4) Bulk Operations

Prefer bulk methods when possible:

```java
list.addAll(other);
list.removeIf(x -> x < 0);
```

## 5) Measure, Do Not Guess

For serious optimization, use JMH benchmark, not ad-hoc timing loops.

