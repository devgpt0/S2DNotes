# 06 - Pitfalls And Best Practices

## Common Mistakes

1. Mutable key objects.
2. Overriding `equals` but not `hashCode`.
3. Assuming `HashMap` order is fixed.
4. Using `containsValue` in hot paths (usually `O(n)`).
5. Ignoring null rules in `ConcurrentHashMap` and immutable maps.

## Key Best Practices

- Prefer immutable keys.
- Use `entrySet()` when both key and value are needed.
- Use `merge()` for counting.
- Use `computeIfAbsent()` for grouping/list initialization.
- Pick map type by requirement, not habit.

## Null Handling Quick Table

| Map Type | Null Key | Null Value |
|---|---|---|
| HashMap | one allowed | allowed |
| LinkedHashMap | one allowed | allowed |
| TreeMap | usually not allowed | allowed |
| ConcurrentHashMap | not allowed | not allowed |
| Map.of / copyOf | not allowed | not allowed |
