# 03 - ConcurrentHashMap Core

## 1) Internal Idea

`ConcurrentHashMap` is thread-safe for concurrent reads and writes.

- high concurrency without whole-map lock
- supports atomic operations (`putIfAbsent`, `compute`, `merge`)

## 2) Time Complexity

- average `O(1)` for `put/get/remove`

## 3) Basic Usage

```java
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class ConcurrentHashMapCoreDemo {
    public static void main(String[] args) {
        Map<String, Integer> freq = new ConcurrentHashMap<>();

        freq.put("java", 1);
        freq.putIfAbsent("python", 0);
        freq.compute("java", (k, v) -> v == null ? 1 : v + 1);
        freq.merge("go", 1, Integer::sum);

        System.out.println(freq);
    }
}
```

## 4) Rules

- does not allow `null` key
- does not allow `null` value
- iterators are weakly consistent (no `ConcurrentModificationException` in normal concurrent iteration)

## 5) When To Use

- shared mutable maps in multithreaded apps
- counters and caches updated by many threads
