# 08 - Hashtable Core (Complete)

## 1) Internal Idea

`Hashtable` is a legacy synchronized hash map.

- hash-table based storage
- synchronized at method level
- mostly replaced by `ConcurrentHashMap`

## 2) Complexity

Average:

- `put/get/remove`: `O(1)`

But synchronization overhead and coarse locking reduce throughput under contention.

## 3) Basic Usage

Concept taught: Core `Hashtable` operations.

```java
Map<Integer, String> table = new Hashtable<>();
table.put(1, "A");
table.put(2, "B");
System.out.println(table.get(1));
System.out.println(table);
```

Expected output:

```text
A
{2=B, 1=A}
```

Order not guaranteed.

## 4) Null Restrictions

Concept taught: `Hashtable` rejects null keys and values.

```java
Map<Integer, String> table = new Hashtable<>();
boolean keyError = false;
boolean valError = false;

try { table.put(null, "X"); } catch (NullPointerException ex) { keyError = true; }
try { table.put(1, null); } catch (NullPointerException ex) { valError = true; }

System.out.println(keyError);
System.out.println(valError);
```

Expected output:

```text
true
true
```

## 5) Legacy Iteration APIs

`Hashtable` historically used `Enumeration`, but modern code should prefer entry iteration.

Concept taught: Modern entry iteration still works with `Hashtable`.

```java
Map<Integer, String> table = new Hashtable<>();
table.put(1, "A");
table.put(2, "B");
for (Map.Entry<Integer, String> e : table.entrySet()) {
    System.out.println(e.getKey() + "=" + e.getValue());
}
```

Possible output:

```text
2=B
1=A
```

## 6) `Hashtable` vs `ConcurrentHashMap`

- both thread-safe
- `ConcurrentHashMap` has better scalability and atomic helpers (`compute`, `merge`)
- prefer `Hashtable` only for legacy API compatibility

## 7) Summary

Understand `Hashtable` for legacy maintenance, but use `ConcurrentHashMap` for new concurrent code.
