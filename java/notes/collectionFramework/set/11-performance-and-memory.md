# 11 - Performance and Memory (Set)

## 1) Complexity Snapshot

- `HashSet`: avg `O(1)` add/contains/remove
- `LinkedHashSet`: avg `O(1)` with ordering overhead
- `TreeSet`: `O(log n)` add/contains/remove
- `EnumSet`: near `O(1)` with compact representation

## 2) Membership Benchmark Intuition

Concept taught: Set membership is usually faster than list membership for large data.

```java
List<Integer> list = IntStream.range(0, 100_000).boxed().toList();
Set<Integer> set = new HashSet<>(list);
System.out.println(list.contains(99_999));
System.out.println(set.contains(99_999));
```

Expected output:

```text
true
true
```

Both true, but set lookup is typically much faster at scale.

## 3) Memory Notes

- `HashSet` uses backing hash map nodes
- `LinkedHashSet` adds order linkage overhead
- `TreeSet` stores tree node structure
- `EnumSet` is very compact for enum domains

## 4) Pre-sizing HashSet

Concept taught: Capacity hint reduces rehashes for large inserts.

```java
int expected = 100_000;
Set<Integer> s = new HashSet<>((int) (expected / 0.75f) + 1);
System.out.println("pre-sized");
```

Expected output:

```text
pre-sized
```

## 5) Summary

Pick set implementation by membership speed, order requirements, and memory tradeoffs.
