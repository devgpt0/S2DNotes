# 07 - ConcurrentSkipListSet Core (Complete)

## 1) Internal Idea

`ConcurrentSkipListSet` is a concurrent sorted set based on skip-list structure.

- thread-safe
- sorted order
- scalable concurrent operations

## 2) Complexity

Average:

- `add/remove/contains`: `O(log n)`

## 3) Sorted + Concurrent Demo

Concept taught: Concurrent sorted set operations.

```java
ConcurrentSkipListSet<Integer> s = new ConcurrentSkipListSet<>();
s.add(30);
s.add(10);
s.add(20);
System.out.println(s);
System.out.println(s.ceiling(15));
```

Expected output:

```text
[10, 20, 30]
20
```

## 4) Range View

Concept taught: Sorted subset view in concurrent set.

```java
ConcurrentSkipListSet<Integer> s = new ConcurrentSkipListSet<>(Set.of(1,2,3,4,5,6));
System.out.println(s.subSet(2, true, 5, false));
```

Expected output:

```text
[2, 3, 4]
```

## 5) When to Use

- concurrent sorted leaderboards
- concurrent scheduling windows
- sorted unique IDs/events with multi-threaded updates

## 6) Summary

Use `ConcurrentSkipListSet` when you need both thread safety and sorted set semantics.
