# 06 - EnumMap Core

## 1) Internal Idea

`EnumMap` is a specialized map for enum keys.

- internally array-like by enum ordinal
- very fast and memory efficient

## 2) Time Complexity

- near `O(1)` for `put/get/remove`
- iteration follows enum declaration order

## 3) Basic Usage

```java
import java.util.EnumMap;
import java.util.Map;

public class EnumMapCoreDemo {
    enum Status { NEW, IN_PROGRESS, DONE }

    public static void main(String[] args) {
        Map<Status, Integer> counts = new EnumMap<>(Status.class);
        counts.put(Status.NEW, 5);
        counts.put(Status.DONE, 2);

        System.out.println(counts); // {NEW=5, DONE=2}
    }
}
```

## 4) Rules

- key type must be one enum class
- `null` keys not allowed

## 5) When To Use

- whenever key domain is enum constants
- ideal replacement for `HashMap<Enum, V>`
