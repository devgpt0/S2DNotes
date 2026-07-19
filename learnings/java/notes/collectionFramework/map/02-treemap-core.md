# 02 - TreeMap Core (Complete)

## 1) Internal Idea

`TreeMap` is a Red-Black Tree based map.

- keys are always sorted
- sorted by natural key order or custom comparator
- supports navigation and range queries

## 2) Complexity

- `put/get/remove`: `O(log n)`
- `firstKey/lastKey/floorKey/ceilingKey`: `O(log n)`

## 3) Basic Sorted Behavior

Concept taught: Keys auto-sort regardless of insertion sequence.

```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
System.out.println(tm);
```

Expected output:

```text
{10=A, 20=B, 30=C}
```

## 4) Navigation Methods

Concept taught: Nearest-key lookup APIs.

```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(10, "A");
tm.put(20, "B");
tm.put(30, "C");

System.out.println(tm.floorKey(25));
System.out.println(tm.ceilingKey(25));
System.out.println(tm.lowerKey(20));
System.out.println(tm.higherKey(20));
```

Expected output:

```text
20
30
10
30
```

## 5) Range Views

Concept taught: Efficient sub-range extraction.

```java
TreeMap<Integer, String> tm = new TreeMap<>();
for (int i = 1; i <= 6; i++) tm.put(i, "V" + i);

System.out.println(tm.subMap(2, true, 5, false));
System.out.println(tm.headMap(3, true));
System.out.println(tm.tailMap(4, true));
```

Expected output:

```text
{2=V2, 3=V3, 4=V4}
{1=V1, 2=V2, 3=V3}
{4=V4, 5=V5, 6=V6}
```

## 6) Custom Comparator

Concept taught: Tree order can be customized.

```java
TreeMap<String, Integer> tm = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);
tm.put("banana", 2);
tm.put("Apple", 1);
tm.put("cherry", 3);
System.out.println(tm);
```

Expected output:

```text
{Apple=1, banana=2, cherry=3}
```

## 7) Rules and Pitfalls

- null keys not allowed
- comparator must be consistent and transitive
- key mutability can break ordering assumptions

## 8) When to Use

- sorted reports
- leaderboard/ranking views
- nearest key and range query workloads

## 9) Summary

Choose `TreeMap` when sorted key operations are a core requirement, not just occasional formatting.
