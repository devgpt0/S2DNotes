# 08 - Hashtable Core

## 1) Internal Idea

`Hashtable` is the legacy synchronized hash-based map.

- thread-safe with coarse-grained synchronization
- older API, mostly replaced by `ConcurrentHashMap`

## 2) Time Complexity

- average `O(1)` for `put/get/remove`
- slower under contention vs `ConcurrentHashMap`

## 3) Basic Usage

```java
import java.util.Hashtable;
import java.util.Map;

public class HashtableCoreDemo {
    public static void main(String[] args) {
        Map<Integer, String> table = new Hashtable<>();
        table.put(1, "A");
        table.put(2, "B");
        System.out.println(table);
    }
}
```

## 4) Rules

- no `null` key
- no `null` value

## 5) When To Use

- only when working with legacy APIs that specifically require `Hashtable`
