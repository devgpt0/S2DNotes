# 06 - Pitfalls And Best Practices

## 1) Common Mistakes

1. using mutable key objects
2. overriding `equals` without `hashCode` (or vice versa)
3. assuming `HashMap` iteration order is fixed
4. using `containsValue` in hot path (`O(n)`)
5. using `get(key) == null` to test existence when null values are possible
6. wrong `remove` overload expectations (`remove(key)` vs `remove(key, value)`)
7. forgetting null restrictions in `ConcurrentHashMap` and immutable maps

## 2) Key Best Practices

- prefer immutable keys (`String`, records, immutable DTOs)
- always keep `equals/hashCode` contract correct
- use `entrySet()` when you need both key and value
- use `merge()` for counting
- use `computeIfAbsent()` for grouping/list initialization
- choose map by requirements (order/sort/thread safety), not habit

## 3) `equals/hashCode` Golden Rule

If `a.equals(b)` is true, then `a.hashCode() == b.hashCode()` must be true.

## 4) Null Handling Quick Table

| Map Type | Null Key | Null Value |
|---|---|---|
| `HashMap` | one allowed | allowed |
| `LinkedHashMap` | one allowed | allowed |
| `TreeMap` | usually not allowed | allowed |
| `ConcurrentHashMap` | not allowed | not allowed |
| `Hashtable` | not allowed | not allowed |
| `Map.of/copyOf` | not allowed | not allowed |

## 5) Correct Existence Check

Prefer:

```java
if (map.containsKey(key)) {
    // key exists even if value is null
}
```

instead of:

```java
if (map.get(key) != null) { ... } // ambiguous when null values allowed
```
