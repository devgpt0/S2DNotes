# 04 - Iteration Models and Fail-Fast

## 1) Iteration Styles

- enhanced for loop
- `Iterator`
- `ListIterator` (for lists)
- `forEach`/stream pipelines

## 2) Fail-Fast Iterator Behavior

Most mutable collection iterators are fail-fast (best-effort).

Concept taught: Structural modification during for-each can throw `ConcurrentModificationException`.

```java
List<String> list = new ArrayList<>(List.of("A", "", "B"));
for (String s : list) {
    if (s.isBlank()) list.remove(s);
}
```

Expected behavior:

```text
ConcurrentModificationException (typically)
```

## 3) Safe Removal via Iterator

Concept taught: `Iterator.remove` is safe during traversal.

```java
List<String> list = new ArrayList<>(List.of("A", "", "B"));
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().isBlank()) it.remove();
}
System.out.println(list);
```

Expected output:

```text
[A, B]
```

## 4) Snapshot Iteration (Fail-Safe Style)

`CopyOnWriteArrayList` iterator sees snapshot and does not fail fast for concurrent structural changes.

Concept taught: Snapshot iteration behavior.

```java
CopyOnWriteArrayList<String> c = new CopyOnWriteArrayList<>(List.of("x", "y"));
for (String s : c) {
    if (s.equals("x")) c.add("z");
}
System.out.println(c);
```

Expected output:

```text
[x, y, z]
```

## 5) Summary

Choose iteration strategy based on whether you need mutation, safety, and concurrency support.
