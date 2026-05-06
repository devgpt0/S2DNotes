# 08 - Ordered, Sorted, and Sequenced Views

## 1) Three Different Concepts

- unordered map: no iteration order guarantee (`HashMap`)
- ordered map: insertion/access order (`LinkedHashMap`)
- sorted map: key order by comparator (`TreeMap`)

## 2) LinkedHashMap Order Modes

Insertion order:

```java
Map<Integer, String> m = new LinkedHashMap<>();
```

Access order:

```java
Map<Integer, String> m = new LinkedHashMap<>(16, 0.75f, true);
```

## 3) TreeMap Navigation

```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(10, "A");
tm.put(20, "B");
tm.put(30, "C");

tm.floorKey(25);   // 20
tm.ceilingKey(25); // 30
tm.subMap(10, true, 30, false);
```

## 4) Java 21 SequencedMap Notes

Common operations:

- `firstEntry()`, `lastEntry()`
- `pollFirstEntry()`, `pollLastEntry()`
- `reversed()`

Use when you need explicit first/last entry workflows.
