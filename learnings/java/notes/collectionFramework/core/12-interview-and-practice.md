# 12 - Interview and Practice

## 1) High-Frequency Questions

1. Difference between `Collection` and `Map`.
2. Difference between fail-fast and fail-safe iteration.
3. Why `equals/hashCode` matters for hash collections.
4. When to choose `ArrayList`, `HashSet`, `HashMap`, `TreeMap`.
5. Difference between immutable and unmodifiable view.

## 2) Solved Drill: Frequency Counter

Concept taught: Use `merge` for concise counting.

```java
String text = "abbaac";
Map<Character, Integer> freq = new HashMap<>();
for (char c : text.toCharArray()) freq.merge(c, 1, Integer::sum);
System.out.println(freq);
```

Possible output:

```text
{a=3, b=2, c=1}
```

## 3) Solved Drill: Remove Duplicates Preserve Order

Concept taught: `LinkedHashSet` for uniqueness + insertion order.

```java
List<Integer> nums = List.of(4, 2, 4, 1, 2);
List<Integer> unique = new ArrayList<>(new LinkedHashSet<>(nums));
System.out.println(unique);
```

Expected output:

```text
[4, 2, 1]
```

## 4) Practice Set

1. Build LRU cache with `LinkedHashMap`.
2. Group words by first letter and by length.
3. Top-k frequent elements.
4. Sliding window distinct count.
5. Implement immutable-return API boundary.

## 5) Summary

If you can explain structure choice with complexity and contracts, you are interview ready on collection fundamentals.
