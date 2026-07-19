# 01 - Map Basics (Complete)

## 1) What Is `Map<K, V>`

`Map` stores data in key-value pairs.

- key (`K`) identifies an entry
- value (`V`) is associated data
- keys are unique
- values may repeat

If you put same key again, old value is replaced.

Concept taught: Key uniqueness and overwrite behavior in `Map`.

```java
Map<String, String> capitals = new HashMap<>();
capitals.put("India", "New Delhi");
capitals.put("Japan", "Tokyo");
capitals.put("India", "Delhi"); // overwrite existing key

System.out.println(capitals.get("India"));
System.out.println(capitals.size());
```

Expected output:

```text
Delhi
2
```

Explanation:

- second `put("India", ...)` updates the same key, not a new entry
- map size stays `2`

## 2) Why Map Is Needed

Map is best for key-based lookup.

Real examples:

- `userId -> User`
- `sku -> price`
- `word -> frequency`
- `token -> expiry`

Without map, many lookups become linear (`O(n)` list scan). With hash-based maps, typical lookup is average `O(1)`.

## 3) `Map` vs `List` vs `Set`

| Type | Stores | Duplicates | Access Style |
|---|---|---|---|
| `List` | values | allowed | index |
| `Set` | values | not allowed | membership/value |
| `Map` | key + value | key: no, value: yes | key |

Important: `Map` is part of collections framework, but it does not extend `Collection`.

## 4) Basic CRUD + Query Methods

Concept taught: Core map operations (`put/get/remove/contains`).

```java
Map<String, Integer> marks = new HashMap<>();
marks.put("Ram", 80);
marks.put("Sita", 92);

System.out.println(marks.get("Ram"));
System.out.println(marks.containsKey("Sita"));
System.out.println(marks.containsValue(92));

marks.remove("Ram");
System.out.println(marks);
```

Expected output (order may vary by implementation):

```text
80
true
true
{Sita=92}
```

## 5) `get` vs `getOrDefault`

Concept taught: Safe reads for missing keys.

```java
Map<String, Integer> stock = new HashMap<>();
stock.put("pen", 10);

System.out.println(stock.get("pen"));
System.out.println(stock.get("book"));
System.out.println(stock.getOrDefault("book", 0));
```

Expected output:

```text
10
null
0
```

Explanation:

- `get` returns `null` when key missing
- `getOrDefault` avoids null handling boilerplate

## 6) Views: `keySet`, `values`, `entrySet`

Concept taught: Iterating over keys, values, and entries.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
map.put("B", 2);

System.out.println(map.keySet());
System.out.println(map.values());

for (Map.Entry<String, Integer> e : map.entrySet()) {
    System.out.println(e.getKey() + " -> " + e.getValue());
}
```

Possible output:

```text
[A, B]
[1, 2]
A -> 1
B -> 2
```

Note: in `HashMap`, order is not guaranteed.

## 7) Null Behavior Snapshot

- `HashMap`: one null key + multiple null values
- `LinkedHashMap`: one null key + multiple null values
- `TreeMap`: usually null key not allowed
- `ConcurrentHashMap`: no null keys/values
- `Map.of` / `Map.copyOf`: no null keys/values

Concept taught: Null behavior differs by implementation.

```java
Map<String, Integer> h = new HashMap<>();
h.put(null, 1);
h.put("x", null);
System.out.println(h);
```

Possible output:

```text
{null=1, x=null}
```

## 8) Java 21 Ordered Map View Note

Java 21 introduces `SequencedMap` APIs (`firstEntry`, `lastEntry`, `reversed`) for ordered map types.

`LinkedHashMap` supports these operations directly.

Concept taught: Reading first/last entries on ordered maps.

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

## 9) First Full Program (Beginner Friendly)

Concept taught: End-to-end map usage in one runnable program.

```java
import java.util.HashMap;
import java.util.Map;

public class MapStarter {
    public static void main(String[] args) {
        Map<String, Integer> score = new HashMap<>();

        score.put("Ram", 80);
        score.put("Sita", 92);
        score.put("Lakshman", 88);
        score.put("Ram", 95); // overwrite

        System.out.println("Ram: " + score.get("Ram"));
        System.out.println("Contains Sita: " + score.containsKey("Sita"));
        System.out.println("Total students: " + score.size());

        for (Map.Entry<String, Integer> e : score.entrySet()) {
            System.out.println(e.getKey() + " -> " + e.getValue());
        }
    }
}
```

Expected output (order may vary):

```text
Ram: 95
Contains Sita: true
Total students: 3
Ram -> 95
Sita -> 92
Lakshman -> 88
```

## 10) Summary

A `Map` is your default structure whenever retrieval by unique key is the primary operation.
