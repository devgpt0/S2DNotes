# 11 - Common Bugs and Best Practices

## 1) Bug: ConcurrentModificationException

Concept taught: Unsafe structural change during for-each.

```java
List<Integer> list = new ArrayList<>(List.of(1, 2, 3));
for (int n : list) {
    if (n == 2) list.remove(Integer.valueOf(2));
}
```

Expected behavior:

```text
ConcurrentModificationException (typically)
```

Fix: use `Iterator.remove` or `removeIf`.

## 2) Bug: Wrong Remove Overload

Concept taught: `remove(int)` vs `remove(Object)`.

```java
List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 2));
list.remove(2);
list.remove(Integer.valueOf(2));
System.out.println(list);
```

Expected output:

```text
[1]
```

## 3) Bug: Mutable Keys in Hash Maps/Sets

Changing key state after insertion can break lookup.

## 4) Bug: Order Assumption in Unordered Collections

`HashMap`/`HashSet` order is not guaranteed.

## 5) Best Practices Checklist

- code to interfaces
- choose by workload
- document mutability
- use immutable keys
- use atomic methods in concurrent maps
- benchmark with proper tools

## 6) Summary

Most collection bugs are contract misunderstandings, not syntax problems.
