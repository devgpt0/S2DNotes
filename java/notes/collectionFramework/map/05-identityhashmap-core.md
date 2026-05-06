# 05 - IdentityHashMap Core

## 1) Internal Idea

`IdentityHashMap` compares keys by reference identity (`==`), not by `equals`.

So two objects with same value can be treated as different keys.

## 2) Time Complexity

- average `O(1)` for `put/get/remove`

## 3) Basic Usage

```java
import java.util.IdentityHashMap;
import java.util.Map;

public class IdentityHashMapCoreDemo {
    public static void main(String[] args) {
        Map<String, Integer> map = new IdentityHashMap<>();

        String a = new String("x");
        String b = new String("x");

        map.put(a, 1);
        map.put(b, 2);

        System.out.println(map.size()); // 2 (different references)
    }
}
```

## 4) Rules

- break from normal `Map` equality intuition
- use carefully and rarely

## 5) When To Use

- object graph algorithms
- framework internals where identity semantics are required
