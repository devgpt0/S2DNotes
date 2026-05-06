# 04 - WeakHashMap Core

## 1) Internal Idea

`WeakHashMap` stores keys as weak references.

If a key has no strong reference elsewhere, GC can remove that entry.

## 2) Time Complexity

- average `O(1)` for `put/get/remove` (hash based)
- size may shrink automatically after GC

## 3) Basic Usage

```java
import java.util.Map;
import java.util.WeakHashMap;

public class WeakHashMapCoreDemo {
    public static void main(String[] args) {
        Map<Object, String> map = new WeakHashMap<>();

        Object key = new Object();
        map.put(key, "metadata");
        System.out.println(map.size()); // usually 1

        key = null; // no strong reference left
        System.gc();

        // Entry may disappear after GC.
        System.out.println(map.size());
    }
}
```

## 4) Rules

- use only when key lifecycle should control entry lifecycle
- cleanup timing is GC-dependent (not deterministic)

## 5) When To Use

- metadata caches tied to object lifetime
- memory-sensitive auxiliary mappings
