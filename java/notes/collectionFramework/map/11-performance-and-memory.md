# 11 - Performance and Memory

## 1) Complexity Reality

- `HashMap`: avg `O(1)` for `put/get/remove`
- `TreeMap`: `O(log n)`
- `LinkedHashMap`: avg `O(1)` with ordering overhead

## 2) Capacity and Load Factor Tuning

If expected size is known, pre-size map to reduce rehashes.

```java
int expected = 10_000;
Map<String, Integer> m = new HashMap<>((int) (expected / 0.75f) + 1);
```

## 3) Avoid Hot-Path Pitfalls

- avoid repeated `containsValue` checks (`O(n)`)
- avoid repeated map lookups for same key in one expression
- choose primitive-friendly structures/libraries for huge numeric workloads when needed

## 4) Key Design Matters

Good key class:

- immutable fields
- stable `equals/hashCode`
- low collision behavior

## 5) Memory Awareness

- `HashMap` stores node objects and bucket array
- `LinkedHashMap` adds linked-order pointers
- `TreeMap` node carries tree links and color metadata
- `EnumMap` is often most memory efficient for enum keys
