# 04 - Map Implementations (When To Use Which)

## 1) Selection Table

| Type | Order | Typical Complexity | Null Key | Null Value | Thread Safety | Best Fit |
|---|---|---|---|---|---|---|
| `HashMap` | no order guarantee | avg `O(1)` | one | yes | no | default fast lookup |
| `LinkedHashMap` | insertion/access order | avg `O(1)` | one | yes | no | deterministic iteration, LRU base |
| `TreeMap` | sorted by key | `O(log n)` | no | yes | no | sorted/range queries |
| `ConcurrentHashMap` | no stable order | avg `O(1)` | no | no | yes | concurrent mutable maps |
| `WeakHashMap` | no order guarantee | avg `O(1)` | yes | yes | no | lifecycle-bound metadata |
| `IdentityHashMap` | no order guarantee | avg `O(1)` | yes | yes | no | identity (`==`) key semantics |
| `EnumMap` | enum declaration order | near `O(1)` | no | yes | no | enum-key maps |
| `Hashtable` | no order guarantee | avg `O(1)` | no | no | legacy sync | legacy compatibility |
| `Map.of/copyOf` | immutable | read-only | no | no | safe share | constants/defensive returns |

## 2) `HashMap` Example

Concept taught: Unordered fast key-value storage.

```java
Map<String, Integer> map = new HashMap<>();
map.put("c", 3);
map.put("a", 1);
map.put("b", 2);
System.out.println(map);
```

Possible output:

```text
{a=1, b=2, c=3}
```

Order is not guaranteed; printed order may differ.

## 3) `LinkedHashMap` Example

Concept taught: Insertion-order iteration.

```java
Map<Integer, String> map = new LinkedHashMap<>();
map.put(3, "C");
map.put(1, "A");
map.put(2, "B");
System.out.println(map);
```

Expected output:

```text
{3=C, 1=A, 2=B}
```

## 4) `LinkedHashMap` Access-Order Mode

Concept taught: Access-order map for LRU-like behavior.

```java
LinkedHashMap<Integer, String> m = new LinkedHashMap<>(16, 0.75f, true);
m.put(1, "A");
m.put(2, "B");
m.put(3, "C");
m.get(2);
System.out.println(m);
```

Expected output:

```text
{1=A, 3=C, 2=B}
```

## 5) `TreeMap` Example

Concept taught: Sorted-key map with navigation methods.

```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");

System.out.println(tm);
System.out.println(tm.floorKey(25));
System.out.println(tm.ceilingKey(25));
```

Expected output:

```text
{10=A, 20=B, 30=C}
20
30
```

## 6) `ConcurrentHashMap` Example

Concept taught: Thread-safe atomic update methods.

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

## 7) `EnumMap` Example

Concept taught: Best map when key domain is an enum.

```java
enum Status { NEW, IN_PROGRESS, DONE }
Map<Status, Integer> count = new EnumMap<>(Status.class);
count.put(Status.NEW, 5);
count.put(Status.DONE, 2);
System.out.println(count);
```

Expected output:

```text
{NEW=5, DONE=2}
```

## 8) `IdentityHashMap` Example

Concept taught: Key identity (`==`) instead of logical equality (`equals`).

```java
Map<String, Integer> map = new IdentityHashMap<>();
String a = new String("x");
String b = new String("x");
map.put(a, 1);
map.put(b, 2);
System.out.println(map.size());
```

Expected output:

```text
2
```

## 9) `WeakHashMap` Example

Concept taught: Entries can disappear when key has no strong reference.

```java
Map<Object, String> map = new WeakHashMap<>();
Object key = new Object();
map.put(key, "meta");
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

GC timing is nondeterministic.

## 10) Immutable Map Factory

Concept taught: Create read-only map safely.

```java
Map<String, Integer> m = Map.of("A", 1, "B", 2);
System.out.println(m);
// m.put("C", 3); // UnsupportedOperationException
```

Expected output:

```text
{A=1, B=2}
```

## 11) Practical Decision Guide

- need fastest general map -> `HashMap`
- need predictable iteration/LRU base -> `LinkedHashMap`
- need sorted keys/range queries -> `TreeMap`
- need concurrent mutation -> `ConcurrentHashMap`
- key type is enum -> `EnumMap`
- need immutable constant map -> `Map.of/copyOf`

## 12) Summary

Choose map type from requirements: ordering, sorting, null rules, concurrency, and memory profile.
