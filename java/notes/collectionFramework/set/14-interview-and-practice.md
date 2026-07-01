# 14 - Interview and Practice (Set)

## 1) Common Interview Questions

1. Difference between `HashSet`, `LinkedHashSet`, and `TreeSet`.
2. Why must `equals/hashCode` be correct in `HashSet`?
3. What is complexity of set operations?
4. How does `TreeSet` decide duplicates?
5. When to use `EnumSet`?

## 2) Solved Problem: Remove Duplicates Preserve Order

Concept taught: `LinkedHashSet` as stable dedup tool.

```java
List<Integer> input = List.of(5, 3, 5, 2, 3, 1);
List<Integer> out = new ArrayList<>(new LinkedHashSet<>(input));
System.out.println(out);
```

Expected output:

```text
[5, 3, 2, 1]
```

## 3) Solved Problem: Common Elements of Two Lists

Concept taught: Intersection using set operations.

```java
Set<Integer> a = new HashSet<>(List.of(1, 2, 3, 4));
Set<Integer> b = new HashSet<>(List.of(3, 4, 5));
a.retainAll(b);
System.out.println(a);
```

Expected output:

```text
[3, 4]
```

## 4) Solved Problem: First Repeated Character

Concept taught: membership tracking with set.

```java
String s = "abca";
Set<Character> seen = new HashSet<>();
Character repeated = null;
for (char c : s.toCharArray()) {
    if (!seen.add(c)) {
        repeated = c;
        break;
    }
}
System.out.println(repeated);
```

Expected output:

```text
a
```

## 5) Practice Set

1. Symmetric difference of two sets.
2. Top-k unique values from stream input.
3. Case-insensitive unique words with original first appearance preserved.
4. Range query with `TreeSet` (`subSet/headSet/tailSet`).
5. Enum-based permissions validator with `EnumSet`.

## 6) Summary

Set interviews usually test correctness contracts, structure choice, and set algebra fluency.
