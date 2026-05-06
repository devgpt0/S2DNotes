# 07 - Interview Revision Sheet

## 1) One-Line Differences

- `HashMap`: fast, unordered.
- `LinkedHashMap`: ordered (insertion or access).
- `TreeMap`: sorted keys, `O(log n)`.
- `ConcurrentHashMap`: thread-safe.
- `WeakHashMap`: weak keys.
- `EnumMap`: enum keys only.

## 2) Must-Know Defaults

- HashMap capacity: `16`
- Load factor: `0.75`
- Resize threshold: `capacity * loadFactor`

## 3) Must-Know Methods

- CRUD: `put`, `get`, `remove`, `clear`
- Query: `containsKey`, `containsValue`, `size`, `isEmpty`
- Useful defaults: `getOrDefault`, `putIfAbsent`, `replace`, `replaceAll`
- Compute family: `computeIfAbsent`, `computeIfPresent`, `compute`, `merge`

## 4) Speaking Template: Explain HashMap

"HashMap stores key-value pairs using hashing.
Average `put/get/remove` is `O(1)`.
It allows one null key and multiple null values.
Collisions are handled inside buckets.
It is not thread-safe.
Custom keys must follow `equals/hashCode` contract."

## 5) High-Value Tricky Points

- `HashMap` allows one null key, `ConcurrentHashMap` allows none.
- `containsValue` is linear; avoid in performance-sensitive paths.
- `TreeMap` key ordering is based on comparator/natural order, not insertion.
- `LinkedHashMap` can be insertion-ordered or access-ordered.
- bad comparator/`equals` contract can break sorted maps/sets behavior.

## 6) Final Self-Check

You are ready if you can:

- explain key uniqueness,
- explain collision and resize,
- choose map type from a requirement,
- solve counting and grouping with `merge` and `computeIfAbsent`.
