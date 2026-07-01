# 13 - Debugging and Testing Maps (Complete)

## 1) Debug Checklist Before Blaming Map

1. Is key class immutable?
2. Are `equals` and `hashCode` implemented correctly?
3. Is chosen map type matching order/sort/thread requirements?
4. Are null assumptions valid for that map implementation?
5. Are concurrent updates atomic?

## 2) Deterministic Debug Printing

Concept taught: Convert to sorted map for stable logs.

```java
Map<String, Integer> map = new HashMap<>();
map.put("b", 2);
map.put("a", 1);
new TreeMap<>(map).forEach((k, v) -> System.out.println(k + " -> " + v));
```

Expected output:

```text
a -> 1
b -> 2
```

## 3) Quick State Inspection

Concept taught: Inspect size + contains + keys to isolate missing-entry bugs.

```java
Map<String, Integer> map = new HashMap<>();
map.put("x", 10);

System.out.println("size=" + map.size());
System.out.println("has x=" + map.containsKey("x"));
System.out.println("value x=" + map.get("x"));
System.out.println("keys=" + map.keySet());
```

Expected output:

```text
size=1
has x=true
value x=10
keys=[x]
```

## 4) Unit Test Pattern: Overwrite Behavior

Concept taught: duplicate-key put should replace value.

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
map.put("A", 2);

assert map.size() == 1;
assert map.get("A") == 2;
```

## 5) Unit Test Pattern: Missing Key Defaults

Concept taught: verify default behavior explicitly.

```java
Map<String, Integer> map = new HashMap<>();
assert map.get("missing") == null;
assert map.getOrDefault("missing", 0) == 0;
```

## 6) Unit Test Pattern: Order Contract

Concept taught: test order only when map type guarantees it.

```java
Map<Integer, String> m = new LinkedHashMap<>();
m.put(2, "B");
m.put(1, "A");

List<Integer> keys = new ArrayList<>(m.keySet());
assert keys.equals(List.of(2, 1));
```

## 7) Unit Test Pattern: Null Contract

Concept taught: null acceptance differs across implementations.

```java
Map<String, Integer> hash = new HashMap<>();
hash.put(null, 1); // allowed

Map<String, Integer> chm = new ConcurrentHashMap<>();
boolean threw = false;
try {
    chm.put(null, 1);
} catch (NullPointerException ex) {
    threw = true;
}
assert threw;
```

## 8) Concurrency Debug Tip

If shared map logic is flaky:

- replace manual check-then-act with atomic API
- log thread name + key + old/new value
- test with repeated stress loops

Concept taught: Atomic counter update prevents race-prone increments.

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.merge("hits", 1, Integer::sum);
map.merge("hits", 1, Integer::sum);
System.out.println(map.get("hits"));
```

Expected output:

```text
2
```

## 9) Edge Cases to Always Test

- empty map
- duplicate key insertion
- null key/value behavior
- large insert volume (rehash behavior)
- ordering/range expectations for ordered/sorted maps
- concurrent writers for thread-safe maps

## 10) Summary

Reliable map code comes from contract-aware tests: key semantics, null policy, ordering guarantees, and atomic concurrency behavior.
