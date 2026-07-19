# 03 - LinkedHashSet Core (Complete)

## 1) Internal Idea

`LinkedHashSet` = hash-based uniqueness + linked insertion order.

- same uniqueness semantics as `HashSet`
- predictable iteration order (insertion order)

## 2) Complexity

Average:

- `add/remove/contains`: `O(1)`

with slight memory overhead vs `HashSet` due to order links.

## 3) Insertion Order Demo

Concept taught: Preserves insertion order while removing duplicates.

```java
Set<Integer> set = new LinkedHashSet<>();
set.add(3);
set.add(1);
set.add(2);
set.add(1);
System.out.println(set);
```

Expected output:

```text
[3, 1, 2]
```

## 4) Dedup While Keeping First Occurrence

Concept taught: Stable dedup pipeline.

```java
List<String> names = List.of("Ram", "Sita", "Ram", "Lakshman", "Sita");
List<String> unique = new ArrayList<>(new LinkedHashSet<>(names));
System.out.println(unique);
```

Expected output:

```text
[Ram, Sita, Lakshman]
```

## 5) When to Use

- dedup output where input order matters
- deterministic iteration for APIs/reports

## 6) Summary

Choose `LinkedHashSet` over `HashSet` when uniqueness plus stable insertion order is required.
