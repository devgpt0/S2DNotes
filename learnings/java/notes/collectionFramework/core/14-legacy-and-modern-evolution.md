# 14 - Legacy and Modern Evolution

## 1) Legacy Classes

- `Vector`
- `Stack`
- `Hashtable`
- `Enumeration`

These still exist but are usually replaced by modern alternatives.

## 2) Modern Replacements

- `Vector` -> `ArrayList`
- `Stack` -> `ArrayDeque`
- `Hashtable` -> `ConcurrentHashMap`
- `Enumeration` -> `Iterator` / streams

Concept taught: Modern stack via `ArrayDeque`.

```java
Deque<Integer> st = new ArrayDeque<>();
st.push(10);
st.push(20);
System.out.println(st.pop());
```

Expected output:

```text
20
```

## 3) Java 8+ Additions

- streams
- lambda-friendly collection methods
- `compute`/`merge` map APIs

## 4) Java 9+ and 21+

- immutable factories: `List.of`, `Set.of`, `Map.of`
- `copyOf` methods
- sequenced APIs for first/last/reversed operations

## 5) Summary

Modern collection usage focuses on clear contracts, immutability options, and better concurrent utilities.
