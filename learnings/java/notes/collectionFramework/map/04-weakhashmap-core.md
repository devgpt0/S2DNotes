# 04 - WeakHashMap Core (Complete)

## 1) Internal Idea

`WeakHashMap` stores keys through weak references.

If a key has no strong references elsewhere, GC can reclaim it and map entry may disappear automatically.

## 2) Complexity

Average hash-map style complexity:

- `put/get/remove`: `O(1)` average

But size and contents can change after GC activity.

## 3) Basic Lifecycle Demo

Concept taught: Entry removal tied to key reachability, not explicit remove.

```java
Map<Object, String> map = new WeakHashMap<>();
Object key = new Object();
map.put(key, "metadata");
System.out.println("before GC: " + map.size());

key = null;
System.gc();

System.out.println("after GC: " + map.size());
```

Possible output:

```text
before GC: 1
after GC: 0
```

GC timing is nondeterministic, so result may vary during very short runs.

## 4) String Literal Trap

String literals are strongly interned; weak-key removal may not happen as expected for literals.

Concept taught: Use non-interned objects for lifecycle-bound keys.

```java
Map<String, String> map = new WeakHashMap<>();
String key = new String("k");
map.put(key, "v");
key = null;
System.gc();
System.out.println(map.size());
```

Possible output:

```text
0
```

## 5) When to Use

- metadata side tables attached to object lifetimes
- memory-sensitive caches where stale entries should disappear automatically

## 6) When Not to Use

- business-critical durable storage
- deterministic cache expiry requirements

## 7) Summary

`WeakHashMap` is a lifecycle-driven map, not a general replacement for `HashMap`.
