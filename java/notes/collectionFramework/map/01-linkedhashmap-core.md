# 01 - LinkedHashMap Core

## 1) Internal Idea

`LinkedHashMap` is a `HashMap` + doubly linked list of entries.

It keeps predictable order:

- insertion order (default)
- access order (`true` in constructor)

## 2) Time Complexity

- `put/get/remove`: average `O(1)`
- iteration: `O(n)` in maintained order

## 3) Constructor for Access Order

```java
LinkedHashMap<Integer, String> map = new LinkedHashMap<>(16, 0.75f, true);
```

When `true`, every successful `get`/`put` moves entry to end (most recently used).

## 4) LRU Cache (Complete Implementation)

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private static final long serialVersionUID = 1L;
    private final int capacity;

    public LRUCache(int capacity) {
        super(Math.max(16, capacity), 0.75f, true);
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be > 0");
        }
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }

    public int capacity() {
        return capacity;
    }

    public static void main(String[] args) {
        LRUCache<Integer, String> cache = new LRUCache<>(3);
        cache.put(1, "A");
        cache.put(2, "B");
        cache.put(3, "C");
        cache.get(1);      // 1 becomes most recently used
        cache.put(4, "D"); // evicts 2
        System.out.println(cache); // {3=C, 1=A, 4=D}
    }
}
```

## 5) When To Use

- deterministic iteration order
- LRU-like behavior
- faster than sorted maps when ordering by insertion/access is enough
