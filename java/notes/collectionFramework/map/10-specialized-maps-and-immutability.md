# 10 - Specialized Maps and Immutability

## 1) EnumMap

Use when keys are enum constants.

- compact and fast
- iteration in enum declaration order

## 2) WeakHashMap

Keys are weak references.

Entry may be GC-removed when key is no longer strongly referenced.

## 3) IdentityHashMap

Key match uses `==`, not `equals`.

Use only when identity semantics are intentionally required.

## 4) Hashtable

Legacy synchronized map.

Prefer `ConcurrentHashMap` for modern concurrent code.

## 5) Immutable Maps

```java
Map<String, Integer> a = Map.of("A", 1, "B", 2);
Map<String, Integer> b = Map.copyOf(a);
```

Rules:

- no null key/value
- duplicate keys rejected at creation
- structural modifications throw `UnsupportedOperationException`
