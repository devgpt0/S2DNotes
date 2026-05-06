# 02 - TreeMap Core

## 1) Internal Idea

`TreeMap` is a Red-Black Tree based map.

- keys are always sorted
- natural order or custom `Comparator`

## 2) Time Complexity

- `put/get/remove`: `O(log n)`
- ordered navigation: efficient (`firstKey`, `lastKey`, `ceilingKey`, `floorKey`)

## 3) Basic Usage

```java
import java.util.TreeMap;

public class TreeMapCoreDemo {
    public static void main(String[] args) {
        TreeMap<Integer, String> tm = new TreeMap<>();
        tm.put(20, "B");
        tm.put(10, "A");
        tm.put(30, "C");

        System.out.println(tm);              // {10=A, 20=B, 30=C}
        System.out.println(tm.firstKey());   // 10
        System.out.println(tm.lastKey());    // 30
        System.out.println(tm.ceilingKey(15)); // 20
    }
}
```

## 4) Rules

- no `null` keys
- values can be `null`
- key type must be comparable (or provide comparator)

## 5) When To Use

- sorted reports
- range queries
- nearest key lookups
