# 09 - Thread Safety and Concurrency

## 1) Non-Thread-Safe by Default

`HashMap`, `LinkedHashMap`, `TreeMap` are not thread-safe.

Concurrent writes without protection can corrupt behavior.

## 2) ConcurrentHashMap Essentials

- safe concurrent read/write
- high throughput under contention
- null key/value not allowed
- weakly consistent iterators

```java
ConcurrentHashMap<String, Integer> freq = new ConcurrentHashMap<>();
freq.merge("java", 1, Integer::sum);
freq.computeIfAbsent("go", k -> 0);
```

## 3) Atomic Compound Operations

Prefer built-ins over manual check-then-act:

```java
map.putIfAbsent(key, value);
map.compute(key, (k, v) -> v == null ? 1 : v + 1);
map.merge(key, 1, Integer::sum);
```

## 4) Synchronized Wrapper

```java
Map<String, Integer> sync = Collections.synchronizedMap(new HashMap<>());
```

Use when you must keep specific map type but need coarse synchronization.

## 5) Quick Decision

- read/write concurrent map: `ConcurrentHashMap`
- very frequent iteration + rare writes on list-like structures: `CopyOnWrite...` patterns (not map)
- legacy API requirement: `Hashtable`
