# 03 - ConcurrentHashMap Core (Complete)

## 1) Internal Idea

`ConcurrentHashMap` is built for safe concurrent mutation.

- supports high concurrency
- avoids coarse whole-map synchronization
- provides atomic compound APIs

## 2) Complexity

Average:

- `put/get/remove`: `O(1)`

Under contention, behavior remains safe and scalable compared to legacy synchronized maps.

## 3) Null Restrictions

- null key: not allowed
- null value: not allowed

This prevents ambiguity in concurrent reads.

## 4) Basic Concurrent API Usage

Concept taught: Thread-safe update operations.

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("java", 1);
map.putIfAbsent("python", 0);
map.compute("java", (k, v) -> v == null ? 1 : v + 1);
map.merge("go", 1, Integer::sum);
System.out.println(map);
```

Possible output:

```text
{python=0, java=2, go=1}
```

## 5) Atomic Counter Pattern

Concept taught: `merge` for lock-free style counting per key.

```java
ConcurrentHashMap<String, Long> hits = new ConcurrentHashMap<>();
hits.merge("/api/users", 1L, Long::sum);
hits.merge("/api/users", 1L, Long::sum);
System.out.println(hits.get("/api/users"));
```

Expected output:

```text
2
```

## 6) Weakly Consistent Iteration

Iterators do not throw `ConcurrentModificationException` under normal concurrent updates; they reflect state seen during traversal (not strict snapshot).

Concept taught: Iteration remains safe during concurrent modification.

```java
ConcurrentHashMap<Integer, String> map = new ConcurrentHashMap<>();
map.put(1, "A");
map.put(2, "B");

for (Map.Entry<Integer, String> e : map.entrySet()) {
    if (e.getKey() == 1) map.put(3, "C");
    System.out.println(e.getKey() + "=" + e.getValue());
}
System.out.println(map);
```

Possible output:

```text
1=A
2=B
3=C
{1=A, 2=B, 3=C}
```

## 7) Why Not `HashMap` + Manual Locks Everywhere

`ConcurrentHashMap` simplifies correctness and often performs better than ad-hoc locking patterns.

## 8) When to Use

- shared counters
- shared caches (with custom policies)
- concurrent state maps in servers and worker pools

## 9) Summary

Use `ConcurrentHashMap` whenever multiple threads mutate/read the same map and you need atomic update helpers.
