# 04 - Map Implementations (When To Use Which)

## 1) HashMap

- Fast average `O(1)` for `put/get/remove`.
- No order guarantee.
- Allows one `null` key and multiple `null` values.

Use when order is not needed and speed is priority.

## 2) LinkedHashMap

- Maintains insertion order.
- Can also maintain access order.

```java
LinkedHashMap<Integer, String> m = new LinkedHashMap<>(16, 0.75f, true);
m.put(1, "A");
m.put(2, "B");
m.put(3, "C");
m.get(2);
System.out.println(m); // access order changes
```

Great for predictable iteration and LRU cache base.

## 3) TreeMap

- Keys are always sorted.
- Core operations are `O(log n)`.

```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(20, "B");
tm.put(10, "A");
tm.put(30, "C");
System.out.println(tm); // {10=A, 20=B, 30=C}
```

Use for sorted reports and range queries.

## 4) ConcurrentHashMap

- Thread-safe map for concurrent read/write.
- Does not allow `null` key or value.
- Iterators are weakly consistent.

## 5) WeakHashMap

- Keys are weak references.
- Entry can disappear after GC if key has no strong reference.

Use only for memory-sensitive lifecycle-based metadata.

## 6) IdentityHashMap

- Uses `==` for key comparison (not `equals`).

Use rarely, mainly framework internals.

## 7) EnumMap

- Best map when keys are enum constants.
- Fast and memory efficient.

## 8) Immutable Maps

- `Map.of(...)`, `Map.ofEntries(...)`, `Map.copyOf(...)`
- No structural modification allowed.

## 9) Java 21 SequencedMap

Useful ordered operations:

- `firstEntry()`
- `lastEntry()`
- `pollFirstEntry()`
- `pollLastEntry()`
- `reversed()`
