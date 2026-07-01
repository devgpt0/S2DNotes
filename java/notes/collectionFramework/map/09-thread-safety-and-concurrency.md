# 09 - Thread Safety and Concurrency (Map)

## 1) Non-Thread-Safe Maps by Default

These are not safe for concurrent writes without external synchronization:

- `HashMap`
- `LinkedHashMap`
- `TreeMap`

## 2) `ConcurrentHashMap` Essentials

- thread-safe concurrent read/write
- no null keys/values
- high throughput under contention
- weakly consistent iterators (no fail-fast guarantee like normal map iterators)

Concept taught: Atomic counter updates with `merge` in concurrent map.

```java
ConcurrentHashMap<String, Integer> freq = new ConcurrentHashMap<>();
freq.merge("java", 1, Integer::sum);
freq.merge("java", 1, Integer::sum);
System.out.println(freq);
```

Expected output:

```text
{java=2}
```

## 3) Avoid Manual Check-Then-Act

Unsafe pattern (race-prone):

Concept taught: Demonstrates 3) Avoid Manual Check-Then-Act in practice.

```java
// if (!map.containsKey(k)) map.put(k, v);
```

Use atomic methods instead.

Concept taught: `putIfAbsent` avoids race in insert-if-missing.

```java
ConcurrentHashMap<String, String> m = new ConcurrentHashMap<>();
m.putIfAbsent("token", "A");
m.putIfAbsent("token", "B");
System.out.println(m.get("token"));
```

Expected output:

```text
A
```

## 4) `compute` / `merge` for Atomic Updates

Concept taught: Atomic read-modify-write in one method call.

```java
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.compute("x", (k, v) -> v == null ? 1 : v + 1);
m.compute("x", (k, v) -> v == null ? 1 : v + 1);
System.out.println(m);
```

Expected output:

```text
{x=2}
```

## 5) Synchronized Wrapper Option

Concept taught: Coarse-grained synchronization with wrapper map.

```java
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
syncMap.put("A", 1);
System.out.println(syncMap.get("A"));
```

Expected output:

```text
1
```

If iterating, you must synchronize externally on same lock.

Concept taught: Correct synchronized iteration over synchronized wrapper.

```java
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
syncMap.put("A", 1);
syncMap.put("B", 2);

synchronized (syncMap) {
    for (Map.Entry<String, Integer> e : syncMap.entrySet()) {
        System.out.println(e.getKey() + "=" + e.getValue());
    }
}
```

Possible output:

```text
A=1
B=2
```

## 6) `Hashtable` vs `ConcurrentHashMap`

- `Hashtable`: legacy, synchronized whole-method style
- `ConcurrentHashMap`: modern, higher concurrency and richer atomic APIs

## 7) Decision Guide

- shared mutable map across threads -> `ConcurrentHashMap`
- low-concurrency legacy code needing minimal change -> synchronized wrapper
- new concurrent code -> avoid `Hashtable`

## 8) Summary

Concurrency safety in maps is about choosing the right map and using atomic methods (`putIfAbsent`, `compute`, `merge`) instead of race-prone multi-step logic.
