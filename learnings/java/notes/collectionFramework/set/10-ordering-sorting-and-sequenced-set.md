# 10 - Ordering, Sorting, and Sequenced Set

## 1) Ordering Models

- `HashSet`: no order guarantee
- `LinkedHashSet`: insertion order
- `TreeSet`: sorted order

## 2) Comparison Demo

Concept taught: Same values, different iteration contracts.

```java
Set<Integer> h = new HashSet<>(List.of(3, 1, 2));
Set<Integer> l = new LinkedHashSet<>(List.of(3, 1, 2));
Set<Integer> t = new TreeSet<>(List.of(3, 1, 2));

System.out.println(h);
System.out.println(l);
System.out.println(t);
```

Possible output:

```text
[1, 2, 3]
[3, 1, 2]
[1, 2, 3]
```

## 3) Java 21 SequencedSet (LinkedHashSet)

`LinkedHashSet` supports first/last/reverse workflows in modern JDKs.

Concept taught: First/last and reverse view operations on ordered set.

```java
LinkedHashSet<Integer> s = new LinkedHashSet<>(List.of(10, 20, 30));
System.out.println(s.getFirst());
System.out.println(s.getLast());
System.out.println(s.reversed());
```

Expected output:

```text
10
30
[30, 20, 10]
```

## 4) Sorted Navigation in TreeSet

Concept taught: Navigable set nearest-element operations.

```java
NavigableSet<Integer> ns = new TreeSet<>(Set.of(10, 20, 30));
System.out.println(ns.floor(25));
System.out.println(ns.ceiling(25));
```

Expected output:

```text
20
30
```

## 5) Summary

Choose set type based on order guarantee needs, not just uniqueness.
