# 09 - Performance and Memory Fundamentals

## 1) Performance Is Workload-Dependent

Pick by operation profile:

- indexed reads -> `ArrayList`
- membership checks -> `HashSet`
- sorted queries -> `TreeMap`/`TreeSet`
- concurrent updates -> `ConcurrentHashMap`

## 2) Cache Locality and Node Overhead

- array-backed structures often iterate faster
- node-based structures carry pointer overhead and poorer locality

## 3) Pre-sizing Matters

Concept taught: Pre-size large maps/lists to reduce resize cost.

```java
int expected = 100_000;
List<Integer> list = new ArrayList<>(expected);
Map<Integer, Integer> map = new HashMap<>((int) (expected / 0.75f) + 1);
System.out.println("pre-sized");
```

Expected output:

```text
pre-sized
```

## 4) Avoid Linear APIs in Hot Path

- list `contains` is `O(n)`
- map `containsValue` is `O(n)`

## 5) Measure Correctly

Use JMH for microbenchmarks; avoid naive timing loops.

## 6) Summary

Performance wins usually come from structure choice and workload-fit, not micro-optimizing syntax.
