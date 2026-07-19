# 04 - TreeSet Core (Complete)

## 1) Internal Idea

`TreeSet` is a sorted set backed by `TreeMap` (Red-Black Tree).

- unique elements
- always sorted
- supports navigation operations

## 2) Complexity

- `add/remove/contains`: `O(log n)`
- navigation (`floor`, `ceiling`, `higher`, `lower`): `O(log n)`

## 3) Sorted Behavior

Concept taught: Automatic sorting on insert.

```java
Set<Integer> set = new TreeSet<>();
set.add(20);
set.add(10);
set.add(30);
System.out.println(set);
```

Expected output:

```text
[10, 20, 30]
```

## 4) Navigation APIs

Concept taught: nearest-element lookups in sorted sets.

```java
NavigableSet<Integer> ns = new TreeSet<>(Set.of(10, 20, 30));
System.out.println(ns.floor(25));
System.out.println(ns.ceiling(25));
System.out.println(ns.lower(20));
System.out.println(ns.higher(20));
```

Expected output:

```text
20
30
10
30
```

## 5) Custom Comparator

Concept taught: Case-insensitive ordering in `TreeSet`.

```java
Set<String> s = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);
s.add("Apple");
s.add("apple");
s.add("Banana");
System.out.println(s);
```

Expected output:

```text
[Apple, Banana]
```

## 6) Rules

- null not allowed in natural-order `TreeSet`
- comparator consistency is critical

## 7) Summary

Use `TreeSet` when you need uniqueness plus sorted and navigable behavior.
