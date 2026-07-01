# 06 - CopyOnWriteArraySet Core (Complete)

## 1) Internal Idea

`CopyOnWriteArraySet` is a thread-safe set built on `CopyOnWriteArrayList`.

- each write copies underlying array
- snapshot-style iteration
- excellent for read-heavy, write-rare workloads

## 2) Complexity Profile

- `contains`: `O(n)` (array scan)
- add/remove writes: expensive due to copy

## 3) Basic Usage

Concept taught: Thread-safe unique collection for read-dominant scenarios.

```java
Set<String> listeners = new CopyOnWriteArraySet<>();
listeners.add("L1");
listeners.add("L2");
listeners.add("L1");
System.out.println(listeners);
```

Expected output:

```text
[L1, L2]
```

## 4) Snapshot Iteration

Concept taught: Mutation during iteration does not fail fast.

```java
CopyOnWriteArraySet<String> s = new CopyOnWriteArraySet<>(Set.of("A", "B"));
for (String v : s) {
    if (v.equals("A")) s.add("C");
}
System.out.println(s);
```

Expected output:

```text
[A, B, C]
```

## 5) When to Use

- listener registries
- subscriber lists
- configuration watchers

## 6) Summary

Use `CopyOnWriteArraySet` only when reads dominate and writes are infrequent.
