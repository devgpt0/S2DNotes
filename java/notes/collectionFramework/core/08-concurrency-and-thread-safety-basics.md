# 08 - Concurrency and Thread-Safety Basics

## 1) Thread-Safety Categories

- not thread-safe: `ArrayList`, `HashMap`, `HashSet`
- legacy synchronized: `Vector`, `Hashtable`
- concurrent collections: `ConcurrentHashMap`, `CopyOnWriteArrayList`, `ConcurrentLinkedQueue`, etc.

## 2) Race-Prone Pattern

Concept taught: Check-then-act is unsafe without atomic APIs.

```java
ConcurrentHashMap<String, Integer> m = new ConcurrentHashMap<>();
m.putIfAbsent("x", 0);
m.compute("x", (k, v) -> v + 1);
System.out.println(m.get("x"));
```

Expected output:

```text
1
```

## 3) Synchronized Wrapper

Concept taught: Coarse synchronization via wrapper.

```java
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
syncMap.put("A", 1);
System.out.println(syncMap.get("A"));
```

Expected output:

```text
1
```

## 4) Copy-On-Write Tradeoff

Great for read-heavy, write-rare patterns due to snapshot iteration.

## 5) Summary

Thread safety requires both correct collection choice and atomic update style.
