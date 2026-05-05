# 01 - Map Basics

## 1) What Is a Map?

`Map<K, V>` stores data as key-value pairs.

- `K` is key type.
- `V` is value type.
- Keys are unique.
- Values can repeat.

Example:

```java
Map<String, String> capitals = new HashMap<>();
capitals.put("India", "New Delhi");
capitals.put("Japan", "Tokyo");
capitals.put("India", "Delhi"); // update existing key

System.out.println(capitals.get("India"));
```

Output:

```text
Delhi
```

## 2) Why Do We Need Map?

Map is best when you search by key often.

Examples:

- `employeeId -> Employee`
- `username -> passwordHash`
- `word -> frequency`
- `productCode -> price`

Without map, list search is usually `O(n)`.
With `HashMap`, lookup is average `O(1)`.

## 3) Map vs List vs Set

| Type | Stores | Duplicates | Order | Access |
|---|---|---|---|---|
| `List` | values | allowed | insertion | index |
| `Set` | values | not allowed | depends | by value |
| `Map` | key + value | key no, value yes | depends | by key |

Note: `Map` is in collection framework but does not extend `Collection`.

## 4) First Complete Example

```java
import java.util.*;

public class MapStarter {
    public static void main(String[] args) {
        Map<String, Integer> marks = new HashMap<>();

        marks.put("Ram", 80);
        marks.put("Sita", 92);
        marks.put("Laxman", 88);
        marks.put("Ram", 95); // overwrite

        System.out.println("Ram: " + marks.get("Ram"));
        System.out.println("Has Sita: " + marks.containsKey("Sita"));
        System.out.println("Size: " + marks.size());

        for (Map.Entry<String, Integer> e : marks.entrySet()) {
            System.out.println(e.getKey() + " -> " + e.getValue());
        }
    }
}
```
