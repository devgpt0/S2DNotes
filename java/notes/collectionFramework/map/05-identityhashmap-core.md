# 05 - IdentityHashMap Core (Complete)

## 1) Internal Idea

`IdentityHashMap` compares keys by reference identity (`==`), not by `equals`.

That means two logically equal objects can still be treated as different keys.

## 2) Complexity

Average hash-map style operations:

- `put/get/remove`: `O(1)` average

## 3) Identity Behavior Demo

Concept taught: Equal-content objects can become different keys due to identity semantics.

```java
Map<String, Integer> map = new IdentityHashMap<>();
String a = new String("x");
String b = new String("x");

map.put(a, 1);
map.put(b, 2);

System.out.println(map.size());
System.out.println(map.get(a));
System.out.println(map.get(b));
```

Expected output:

```text
2
1
2
```

## 4) Contrast with `HashMap`

Concept taught: Same data with `HashMap` collapses to one key due to `equals`.

```java
Map<String, Integer> map = new HashMap<>();
String a = new String("x");
String b = new String("x");
map.put(a, 1);
map.put(b, 2);
System.out.println(map.size());
System.out.println(map.get("x"));
```

Expected output:

```text
1
2
```

## 5) Real Use Cases

- object graph traversal bookkeeping (visited by identity)
- framework internals and proxy tracking
- serialization/DI internals where object instance identity matters

## 6) Warning

Do not use `IdentityHashMap` for normal business keys (IDs, names, codes). It violates normal map equality expectations for most teams.

## 7) Summary

Use `IdentityHashMap` only when identity semantics are explicitly required by design.
