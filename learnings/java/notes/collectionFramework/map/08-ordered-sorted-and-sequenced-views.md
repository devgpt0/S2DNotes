# 08 - Ordered, Sorted, and Sequenced Views (Complete)

## 1) Three Different Ideas

- unordered map: no iteration order guarantee (`HashMap`)
- ordered map: insertion/access order (`LinkedHashMap`)
- sorted map: comparator/natural key order (`TreeMap`)

## 2) Insertion-Order `LinkedHashMap`

Concept taught: Deterministic insertion-order iteration.

```java
Map<Integer, String> m = new LinkedHashMap<>();
m.put(30, "C");
m.put(10, "A");
m.put(20, "B");
System.out.println(m);
```

Expected output:

```text
{30=C, 10=A, 20=B}
```

## 3) Access-Order `LinkedHashMap`

Concept taught: Recency ordering with `accessOrder=true`.

```java
LinkedHashMap<Integer, String> m = new LinkedHashMap<>(16, 0.75f, true);
m.put(1, "A");
m.put(2, "B");
m.put(3, "C");
m.get(2);
m.get(1);
System.out.println(m);
```

Expected output:

```text
{3=C, 2=B, 1=A}
```

## 4) Sorted `TreeMap`

Concept taught: Keys auto-sorted by natural order.

```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(30, "C");
tm.put(10, "A");
tm.put(20, "B");
System.out.println(tm);
```

Expected output:

```text
{10=A, 20=B, 30=C}
```

## 5) Navigation APIs (`NavigableMap`)

Concept taught: Nearest key lookups.

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

## 6) Range Views

Concept taught: Efficient sub-range views in sorted maps.

```java
TreeMap<Integer, String> tm = new TreeMap<>();
for (int i = 1; i <= 6; i++) tm.put(i, "V" + i);

System.out.println(tm.subMap(2, true, 5, false));
System.out.println(tm.headMap(4, true));
System.out.println(tm.tailMap(4, false));
```

Expected output:

```text
{2=V2, 3=V3, 4=V4}
{1=V1, 2=V2, 3=V3, 4=V4}
{5=V5, 6=V6}
```

## 7) Java 21 `SequencedMap` APIs

Ordered maps now expose first/last and reverse operations directly.

Concept taught: First/last entry operations for ordered map workflows.

```java
LinkedHashMap<Integer, String> lm = new LinkedHashMap<>();
lm.put(10, "A");
lm.put(20, "B");
lm.put(30, "C");

System.out.println(lm.firstEntry());
System.out.println(lm.lastEntry());
System.out.println(lm.reversed());
```

Expected output:

```text
10=A
30=C
{30=C, 20=B, 10=A}
```

## 8) Choosing Ordered vs Sorted

- if you only need predictable insertion/access order: `LinkedHashMap`
- if you need range queries or nearest-key search: `TreeMap`

## 9) Summary

Ordering and sorting are different requirements. Pick `LinkedHashMap` for stable iteration order and `TreeMap` for sorted/queryable key space.
