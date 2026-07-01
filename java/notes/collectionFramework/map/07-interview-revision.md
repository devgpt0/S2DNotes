# 07 - Interview Revision Sheet (Map)

## 1) One-Line Differences (Must Memorize)

- `HashMap`: fast average `O(1)`, no order guarantee.
- `LinkedHashMap`: insertion/access ordered hash map.
- `TreeMap`: sorted keys, `O(log n)` operations.
- `ConcurrentHashMap`: thread-safe mutable map.
- `EnumMap`: fastest for enum keys.
- `WeakHashMap`: entries tied to key reachability.
- `IdentityHashMap`: key identity (`==`) semantics.

## 2) Must-Know Defaults

For `HashMap`:

- initial capacity: `16`
- load factor: `0.75`
- first threshold: `12`

## 3) Must-Know APIs

- CRUD: `put`, `get`, `remove`, `clear`
- Query: `containsKey`, `containsValue`, `size`, `isEmpty`
- Useful default ops: `getOrDefault`, `putIfAbsent`, `replace`
- Compute ops: `computeIfAbsent`, `computeIfPresent`, `compute`, `merge`

## 4) Explain HashMap in 30 Seconds

Template answer:

"HashMap stores key-value pairs using hashing. `put/get/remove` are average `O(1)`. It allows one null key and multiple null values. Collisions are handled per bucket, and high-collision buckets may be treeified in modern JDK. It is not thread-safe, and custom keys must follow `equals/hashCode` contract."

## 5) High-Value Tricky Points

- `HashMap` nulls allowed; `ConcurrentHashMap` nulls not allowed.
- `containsValue` is `O(n)`.
- `TreeMap` order is key sort order, not insertion order.
- `LinkedHashMap` can run in insertion-order or access-order mode.
- comparator consistency matters in sorted maps.

## 6) Quick Interview Demo Snippets

Concept taught: Frequency counting in one line of logic.

```java
Map<String, Integer> freq = new HashMap<>();
for (String w : List.of("a", "b", "a")) {
    freq.merge(w, 1, Integer::sum);
}
System.out.println(freq);
```

Expected output:

```text
{a=2, b=1}
```

Concept taught: Grouping with lazy list creation.

```java
Map<Integer, List<String>> byLen = new HashMap<>();
for (String w : List.of("to", "tea", "go")) {
    byLen.computeIfAbsent(w.length(), k -> new ArrayList<>()).add(w);
}
System.out.println(byLen);
```

Possible output:

```text
{2=[to, go], 3=[tea]}
```

## 7) Common Interview Mistakes

- saying `HashMap` is always `O(1)` (ignore worst-case/collision reality)
- forgetting null rules per map type
- ignoring key immutability
- choosing wrong map for ordering requirement

## 8) Self-Check Before Interview

You are ready when you can:

1. justify map choice from requirements
2. explain overwrite behavior for duplicate keys
3. design safe key class with `equals/hashCode`
4. solve counting/grouping/top-k patterns
5. explain thread-safe map strategy

## 9) Summary

Map interviews reward clarity of tradeoffs more than memorizing API names. Speak in terms of requirements, complexity, and contracts.
