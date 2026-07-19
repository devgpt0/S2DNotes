# 02 - HashMap Core (Complete)

## 1) Internal Model

`HashMap` is hash-table based.

For each key:

1. hash is computed
2. bucket index is derived
3. bucket is searched for matching key (`equals`)
4. value inserted/updated/retrieved

## 2) Core Complexity

Average case:

- `put`: `O(1)`
- `get`: `O(1)`
- `remove`: `O(1)`

Worst case can degrade if many collisions happen, but modern JDK uses tree bins to improve high-collision buckets.

## 3) Collision Concept

Concept taught: Different keys can land in same bucket and still coexist.

```java
record Key(int id) {
    @Override
    public int hashCode() { return 1; } // forced collision
}

Map<Key, String> map = new HashMap<>();
map.put(new Key(1), "A");
map.put(new Key(2), "B");
map.put(new Key(3), "C");

System.out.println(map.size());
System.out.println(map.get(new Key(2)));
```

Expected output:

```text
3
B
```

Explanation:

- all keys collide in same bucket
- retrieval still works using `equals`

## 4) Resize, Capacity, Load Factor

Defaults:

- initial capacity: `16`
- load factor: `0.75`
- threshold: `capacity * loadFactor` (starts at `12`)

When size crosses threshold, map resizes (usually doubles capacity).

Concept taught: Pre-sizing a map to reduce rehash cost.

```java
int expectedEntries = 10_000;
int capacity = (int) (expectedEntries / 0.75f) + 1;
Map<String, Integer> map = new HashMap<>(capacity);

System.out.println("created with capacity hint for " + expectedEntries + " entries");
```

Expected output:

```text
created with capacity hint for 10000 entries
```

## 5) Treeification in High Collision Buckets

Important JDK thresholds (implementation detail, still interview-relevant):

- treeify threshold: bucket size >= `8`
- untreeify threshold: bucket size <= `6`
- minimum capacity to treeify: `64`

This improves performance when collisions are severe.

## 6) `equals` / `hashCode` Contract

If custom object is key, override both.

Concept taught: Correct key behavior with immutable fields and contract-safe overrides.

```java
import java.util.Objects;

final class UserKey {
    private final String country;
    private final long id;

    UserKey(String country, long id) {
        this.country = country;
        this.id = id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof UserKey other)) return false;
        return id == other.id && Objects.equals(country, other.country);
    }

    @Override
    public int hashCode() {
        return Objects.hash(country, id);
    }
}

Map<UserKey, String> users = new HashMap<>();
users.put(new UserKey("IN", 101), "Ram");
System.out.println(users.get(new UserKey("IN", 101)));
```

Expected output:

```text
Ram
```

## 7) Null Handling

Concept taught: `HashMap` allows null key/value.

```java
Map<String, Integer> map = new HashMap<>();
map.put(null, 99);
map.put("A", null);
System.out.println(map.get(null));
System.out.println(map.get("A"));
```

Expected output:

```text
99
null
```

## 8) Iteration Best Practice

Concept taught: Use `entrySet` when key and value both needed.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
map.put("B", 2);

for (Map.Entry<String, Integer> e : map.entrySet()) {
    System.out.println(e.getKey() + " => " + e.getValue());
}
```

Possible output:

```text
A => 1
B => 2
```

## 9) Not Thread-Safe

`HashMap` is unsafe for concurrent writes without external synchronization.

Use:

- `ConcurrentHashMap` for shared concurrent mutation
- `Collections.synchronizedMap(...)` only for coarse-grained synchronization scenarios

## 10) Common Mistakes

- mutable keys (changing key fields after insertion)
- overriding only `equals` or only `hashCode`
- relying on iteration order of `HashMap`
- using `containsValue` in hot path (`O(n)`)

## 11) Summary

`HashMap` is the default map for single-threaded/general use where order is not required. Correct key design is the most important factor for correctness and performance.
