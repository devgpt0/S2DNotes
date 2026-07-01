# 09 - Set Operations: Union, Intersection, Difference

## 1) Core Set Algebra

For sets `A` and `B`:

- union: all elements in `A` or `B`
- intersection: common elements
- difference: elements in `A` not in `B`
- symmetric difference: elements in either set, not both

## 2) Union

Concept taught: `addAll` performs union.

```java
Set<Integer> a = new HashSet<>(Set.of(1, 2, 3));
Set<Integer> b = Set.of(3, 4, 5);
a.addAll(b);
System.out.println(a);
```

Possible output:

```text
[1, 2, 3, 4, 5]
```

## 3) Intersection

Concept taught: `retainAll` keeps common elements.

```java
Set<Integer> a = new HashSet<>(Set.of(1, 2, 3));
a.retainAll(Set.of(2, 3, 4));
System.out.println(a);
```

Expected output:

```text
[2, 3]
```

## 4) Difference

Concept taught: `removeAll` subtracts another set.

```java
Set<Integer> a = new HashSet<>(Set.of(1, 2, 3, 4));
a.removeAll(Set.of(3, 4, 5));
System.out.println(a);
```

Possible output:

```text
[1, 2]
```

## 5) Symmetric Difference

Concept taught: Combine union minus intersection.

```java
Set<Integer> a = new HashSet<>(Set.of(1, 2, 3));
Set<Integer> b = new HashSet<>(Set.of(3, 4, 5));

Set<Integer> union = new HashSet<>(a);
union.addAll(b);

Set<Integer> inter = new HashSet<>(a);
inter.retainAll(b);

union.removeAll(inter);
System.out.println(union);
```

Possible output:

```text
[1, 2, 4, 5]
```

## 6) Summary

Set algebra operations are powerful building blocks for permission logic, diffing, filtering, and matching tasks.
