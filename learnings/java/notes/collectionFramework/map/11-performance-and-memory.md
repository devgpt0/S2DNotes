# 11 - Performance and Memory (Map Deep Dive)

## 1) Complexity Snapshot

- `HashMap`: avg `O(1)` put/get/remove
- `LinkedHashMap`: avg `O(1)` with order maintenance overhead
- `TreeMap`: `O(log n)`
- `ConcurrentHashMap`: avg `O(1)` with concurrency-safe mechanics

## 2) Capacity Tuning for `HashMap`

If you know expected size, pre-size map to avoid repeated rehash.

Concept taught: Capacity hint formula for large inserts.

```java
int expected = 100_000;
int capacity = (int) (expected / 0.75f) + 1;
Map<Integer, Integer> map = new HashMap<>(capacity);
System.out.println("capacity hint applied for " + expected + " entries");
```

Expected output:

```text
capacity hint applied for 100000 entries
```

## 3) Rehash Cost Awareness

Rehashing includes:

- bigger bucket array allocation
- reinsertion of existing entries

In throughput-sensitive workloads, repeated unplanned rehash can be expensive.

## 4) Collision Quality Depends on Key Hash

Concept taught: Poor hashCode quality increases collisions.

```java
record BadKey(int id) {
    @Override
    public int hashCode() { return 1; }
}

Map<BadKey, Integer> map = new HashMap<>();
for (int i = 0; i < 1000; i++) map.put(new BadKey(i), i);
System.out.println(map.size());
```

Expected output:

```text
1000
```

Works correctly, but performance suffers with collision-heavy keys.

## 5) `containsValue` Cost

Concept taught: Value-search is linear in map size.

```java
Map<Integer, String> map = new HashMap<>();
for (int i = 0; i < 5; i++) map.put(i, "V" + i);
System.out.println(map.containsValue("V4"));
```

Expected output:

```text
true
```

For frequent reverse lookup, maintain reverse index map.

## 6) Memory Characteristics

- `HashMap`: bucket array + node objects
- `LinkedHashMap`: hash map nodes plus order links (`before/after`)
- `TreeMap`: tree node overhead (left/right/parent/color)
- `EnumMap`: compact array-backed structure for enum keys

## 7) Iteration Performance Notes

- `LinkedHashMap`: predictable order iteration
- `HashMap`: no order guarantee; often very fast general iteration
- `TreeMap`: sorted iteration with tree traversal

## 8) Concurrency and Performance

- `Collections.synchronizedMap`: coarse lock; simpler but contention-heavy
- `ConcurrentHashMap`: better concurrent throughput, atomic APIs

Concept taught: Concurrent counter map pattern.

```java
ConcurrentHashMap<String, Long> counter = new ConcurrentHashMap<>();
counter.merge("hits", 1L, Long::sum);
counter.merge("hits", 1L, Long::sum);
System.out.println(counter);
```

Expected output:

```text
{hits=2}
```

## 9) Benchmarking Reminder

For serious measurement:

- use JMH
- avoid ad-hoc loops influenced by JIT warmup and dead-code elimination

## 10) Practical Tuning Checklist

- pre-size large maps
- design immutable keys with good `hashCode`
- avoid linear APIs (`containsValue`) in hot path
- select map type by ordering/sorting/concurrency requirement

## 11) Summary

Map performance is mostly about right implementation + good key design + capacity planning.
