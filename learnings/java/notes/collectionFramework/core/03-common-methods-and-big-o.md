# 03 - Common Methods and Big-O

## 1) Method Families

Across collections, methods fall into:

- read/query: `contains`, `size`, `isEmpty`
- write: `add`, `remove`, `clear`
- bulk: `addAll`, `removeAll`, `retainAll`
- conversion: `toArray`

## 2) Complexity Depends on Implementation

Example:

- `ArrayList.get(i)` -> `O(1)`
- `LinkedList.get(i)` -> `O(n)`

Concept taught: Same API name, different complexity across implementations.

```java
List<Integer> a = new ArrayList<>(List.of(10, 20, 30));
List<Integer> b = new LinkedList<>(List.of(10, 20, 30));
System.out.println(a.get(2));
System.out.println(b.get(2));
```

Expected output:

```text
30
30
```

## 3) Bulk Operations

Concept taught: Use bulk APIs for clearer intent.

```java
Collection<Integer> c = new ArrayList<>(List.of(1, 2, 3, 4, 5));
c.removeAll(List.of(2, 4));
System.out.println(c);
```

Expected output:

```text
[1, 3, 5]
```

## 4) `contains` Cost Reality

Concept taught: `contains` on list is linear search.

```java
List<Integer> list = new ArrayList<>(List.of(1, 2, 3, 4, 5));
System.out.println(list.contains(5));
```

Expected output:

```text
true
```

For frequent membership queries, prefer `Set`.

## 5) Summary

Always read complexity in terms of concrete implementation, not only interface.
