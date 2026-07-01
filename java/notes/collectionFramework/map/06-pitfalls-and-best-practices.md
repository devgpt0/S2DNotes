# 06 - Pitfalls and Best Practices (Map)

## 1) Pitfall: Mutable Key Object

If key fields used in `equals/hashCode` are changed after insertion, retrieval can fail.

Concept taught: Why map keys should be immutable.

```java
class Key {
    String id;
    Key(String id) { this.id = id; }
    @Override public boolean equals(Object o) {
        return o instanceof Key k && Objects.equals(id, k.id);
    }
    @Override public int hashCode() { return Objects.hash(id); }
}

Map<Key, String> map = new HashMap<>();
Key k = new Key("A");
map.put(k, "value");
k.id = "B"; // dangerous mutation
System.out.println(map.get(k));
```

Possible output:

```text
null
```

## 2) Pitfall: `equals` Without `hashCode`

Concept taught: Both methods must be consistent for hash-based maps.

```java
class BadKey {
    String id;
    BadKey(String id) { this.id = id; }
    @Override public boolean equals(Object o) {
        return o instanceof BadKey b && Objects.equals(id, b.id);
    }
    // hashCode missing -> contract broken
}

Map<BadKey, String> map = new HashMap<>();
map.put(new BadKey("x"), "ok");
System.out.println(map.get(new BadKey("x")));
```

Possible output:

```text
null
```

## 3) Pitfall: Using `get(key) != null` as Existence Check

Concept taught: `containsKey` is the safe existence check when null values are allowed.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", null);

System.out.println(map.get("A") != null);
System.out.println(map.containsKey("A"));
```

Expected output:

```text
false
true
```

## 4) Pitfall: Assuming `HashMap` Iteration Order

Concept taught: Order-sensitive logic needs ordered/sorted map implementation.

```java
Map<Integer, String> map = new HashMap<>();
map.put(3, "C");
map.put(1, "A");
map.put(2, "B");
System.out.println(map);
```

Possible output:

```text
{1=A, 2=B, 3=C}
```

Could print differently in another run/JDK.

## 5) Pitfall: `containsValue` in Hot Path

`containsValue` is linear scan (`O(n)`).

Concept taught: Value lookup at scale often needs reverse map/index.

```java
Map<Integer, String> idToName = new HashMap<>();
System.out.println(idToName.containsValue("Ram"));
```

## 6) Pitfall: Wrong Remove Overload Understanding

Concept taught: `remove(key)` vs `remove(key, value)`.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
System.out.println(map.remove("A", 2));
System.out.println(map.remove("A"));
```

Expected output:

```text
false
1
```

## 7) Pitfall: Null Rules Across Implementations

Concept taught: Null compatibility differs by map type.

```java
Map<String, Integer> hash = new HashMap<>();
hash.put(null, 1); // valid

Map<String, Integer> concurrent = new ConcurrentHashMap<>();
// concurrent.put(null, 1); // NullPointerException

System.out.println(hash);
```

Expected output:

```text
{null=1}
```

## 8) Best Practice Checklist

- choose map by requirement, not habit
- use immutable key classes
- implement `equals` + `hashCode` correctly
- use `entrySet` when key and value both needed
- use `merge` for counting
- use `computeIfAbsent` for grouping and nested initialization
- document map mutability when exposing APIs

## 9) Safe Existence + Update Pattern

Concept taught: null-safe, concise update idioms.

```java
Map<String, Integer> stock = new HashMap<>();
stock.merge("pen", 1, Integer::sum);
stock.merge("pen", 1, Integer::sum);
System.out.println(stock.getOrDefault("book", 0));
System.out.println(stock);
```

Expected output:

```text
0
{pen=2}
```

## 10) Summary

Most map bugs are contract bugs: mutable keys, wrong equality semantics, null assumptions, and order assumptions. Fix contracts first.
