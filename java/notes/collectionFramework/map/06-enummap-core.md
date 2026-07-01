# 06 - EnumMap Core (Complete)

## 1) Internal Idea

`EnumMap` is specialized for one enum key type.

- key domain fixed to enum constants
- internally optimized (array-like indexing by enum ordinal)
- usually faster and lighter than `HashMap<Enum, V>`

## 2) Complexity

- `put/get/remove`: near `O(1)`
- iteration order: enum declaration order

## 3) Basic Usage

Concept taught: Enum-key map with deterministic declaration-order iteration.

```java
enum Status { NEW, IN_PROGRESS, DONE }

Map<Status, Integer> counts = new EnumMap<>(Status.class);
counts.put(Status.NEW, 5);
counts.put(Status.DONE, 2);
counts.put(Status.IN_PROGRESS, 3);
System.out.println(counts);
```

Expected output:

```text
{NEW=5, IN_PROGRESS=3, DONE=2}
```

## 4) Counter Pattern

Concept taught: Efficient status counter map.

```java
enum Status { NEW, IN_PROGRESS, DONE }
List<Status> items = List.of(Status.NEW, Status.DONE, Status.NEW, Status.IN_PROGRESS);
Map<Status, Integer> freq = new EnumMap<>(Status.class);
for (Status s : items) {
    freq.merge(s, 1, Integer::sum);
}
System.out.println(freq);
```

Expected output:

```text
{NEW=2, IN_PROGRESS=1, DONE=1}
```

## 5) Rules

- key type must be exactly one enum class
- null key not allowed
- null value allowed

## 6) When to Use

- finite state/status counters
- permission/flag configuration by enum
- switch-like map behavior with fast lookups

## 7) Summary

If your keys are enum constants, `EnumMap` should usually be your first choice.
