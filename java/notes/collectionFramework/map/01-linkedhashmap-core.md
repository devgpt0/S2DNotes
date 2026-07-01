# 01 - LinkedHashMap Core (Complete)

## 1) Internal Idea

`LinkedHashMap` = `HashMap` + doubly linked list of entries.

This adds deterministic iteration order.

Order modes:

- insertion order (default)
- access order (`new LinkedHashMap<>(cap, loadFactor, true)`)

## 2) Complexity

- `put/get/remove`: average `O(1)`
- iteration: `O(n)` in maintained order

## 3) Insertion-Order Demo

Concept taught: Entries retain insertion sequence.

```java
Map<Integer, String> map = new LinkedHashMap<>();
map.put(3, "C");
map.put(1, "A");
map.put(2, "B");
System.out.println(map);
```

Expected output:

```text
{3=C, 1=A, 2=B}
```

## 4) Access-Order Demo

Concept taught: Recently accessed entries move to end in access-order mode.

```java
LinkedHashMap<Integer, String> map = new LinkedHashMap<>(16, 0.75f, true);
map.put(1, "A");
map.put(2, "B");
map.put(3, "C");
map.get(2);
map.get(1);
System.out.println(map);
```

Expected output:

```text
{3=C, 2=B, 1=A}
```

## 5) LRU Cache Implementation

Concept taught: Evict least-recently-used entry by overriding `removeEldestEntry`.

```java
import java.util.LinkedHashMap;
import java.util.Map;

class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    LRUCache(int capacity) {
        super(Math.max(16, capacity), 0.75f, true);
        if (capacity <= 0) throw new IllegalArgumentException("capacity must be > 0");
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}

LRUCache<Integer, String> cache = new LRUCache<>(3);
cache.put(1, "A");
cache.put(2, "B");
cache.put(3, "C");
cache.get(1);
cache.put(4, "D");
System.out.println(cache);
```

Expected output:

```text
{3=C, 1=A, 4=D}
```

## 6) Java 21 Sequenced Operations

Concept taught: First/last and reverse view on ordered maps.

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

## 7) When to Use

- stable output order required
- JSON/report generation where key order matters
- LRU cache base structure

## 8) Summary

`LinkedHashMap` is the best choice when you need hash-map speed plus deterministic iteration order.
