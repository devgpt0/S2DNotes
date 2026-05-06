# 04 - Map Implementations (When To Use Which)

## 1) Quick Selection Table

| Type | Order | Typical Complexity | Null Key | Null Value | Thread Safety | Best Fit |
|---|---|---|---|---|---|---|
| `HashMap` | no guarantee | avg `O(1)` | one allowed | allowed | no | general-purpose fast lookup |
| `LinkedHashMap` | insertion/access order | avg `O(1)` | one allowed | allowed | no | predictable order, LRU base |
| `TreeMap` | sorted by key | `O(log n)` | not allowed | allowed | no | sorted reports, range queries |
| `ConcurrentHashMap` | no guarantee | avg `O(1)` | not allowed | not allowed | yes | concurrent read/write |
| `WeakHashMap` | no guarantee | avg `O(1)` | allowed | allowed | no | lifecycle-bound metadata |
| `IdentityHashMap` | no guarantee | avg `O(1)` | allowed | allowed | no | identity (`==`) semantics |
| `EnumMap` | enum declaration order | near `O(1)` | not allowed | allowed | no | enum-key maps |
| `Hashtable` | no guarantee | avg `O(1)` | not allowed | not allowed | legacy synchronized | legacy APIs |
| `Map.of/copyOf` | iteration order defined by factory contract | read-only | not allowed | not allowed | safe to share | constants, defensive returns |

## 2) HashMap

- fastest common default
- no iteration order contract
- collision + resize behavior matters for large workloads

## 3) LinkedHashMap

- predictable iteration
- optional access order for LRU behavior

```java
LinkedHashMap<Integer, String> m = new LinkedHashMap<>(16, 0.75f, true);
m.put(1, "A");
m.put(2, "B");
m.put(3, "C");
m.get(2);
System.out.println(m); // {1=A, 3=C, 2=B}
```

## 4) TreeMap

- sorted keys via natural order or comparator
- supports navigation: `ceilingKey`, `floorKey`, `higherKey`, `subMap`

## 5) ConcurrentHashMap

- high concurrency without locking whole map
- atomic compound helpers: `putIfAbsent`, `compute`, `merge`
- weakly consistent iteration

## 6) WeakHashMap

- keys are weak references
- entries may disappear after GC when key has no strong reference

## 7) IdentityHashMap

- key equality is `==`, not `equals`
- use only when identity semantics are explicitly needed

## 8) EnumMap

- best map when key domain is one enum type
- memory efficient and very fast

## 9) Immutable Maps

- factories: `Map.of`, `Map.ofEntries`, `Map.copyOf`
- reject null keys/values
- reject duplicate keys at creation

## 10) Java 21 SequencedMap

Ordered map operations to know:

- `firstEntry()`
- `lastEntry()`
- `pollFirstEntry()`
- `pollLastEntry()`
- `reversed()`
