# 06 - List Iteration Patterns (Complete)

## 1) Why Iteration Style Matters

Different iteration APIs are not just syntax differences.

They affect:

- readability
- mutation safety
- performance characteristics
- available capabilities (reverse traversal, in-place update, etc.)

## 2) Index-Based `for` Loop

Concept taught: Demonstrates 2) Index-Based `for` Loop in practice.

```java
List<String> list = List.of("A", "B", "C");
for (int i = 0; i < list.size(); i++) {
    System.out.println(i + " => " + list.get(i));
}
```

Expected output:

```text
0 => A
1 => B
2 => C
```

Use when:

- index is needed
- random access list (`ArrayList`) is used

Avoid for heavy `LinkedList` index reads.

## 3) Enhanced `for` Loop (for-each)

Concept taught: Demonstrates 3) Enhanced `for` Loop (for-each) in practice.

```java
List<String> list = List.of("java", "python", "go");
for (String lang : list) {
    System.out.println(lang.toUpperCase());
}
```

Expected output:

```text
JAVA
PYTHON
GO
```

Use when:

- simple read-only traversal
- no need for explicit index

## 4) `Iterator` for Safe Removals

Concept taught: Demonstrates 4) `Iterator` for Safe Removals in practice.

```java
List<String> list = new ArrayList<>(List.of("A", "", "B", " ", "C"));
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String s = it.next();
    if (s.isBlank()) {
        it.remove();
    }
}
System.out.println(list);
```

Expected output:

```text
[A, B, C]
```

Why this is important:

- avoids `ConcurrentModificationException` during structural modification while iterating

## 5) `ListIterator` (Bidirectional + Update + Insert)

`ListIterator` supports:

- forward and backward movement
- `set()` replace current element
- `add()` insert during iteration

Concept taught: Demonstrates 5) `ListIterator` (Bidirectional + Update + Insert) in practice.

```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));
ListIterator<String> li = list.listIterator();
while (li.hasNext()) {
    String v = li.next();
    if (v.equals("b")) {
        li.set("B");
        li.add("x");
    }
}
System.out.println(list);

while (li.hasPrevious()) {
    System.out.println(li.previous());
}
```

Expected output:

```text
[a, B, x, c]
c
x
B
a
```

## 6) `forEach` Method

Concept taught: Demonstrates 6) `forEach` Method in practice.

```java
List<Integer> nums = List.of(1, 2, 3);
nums.forEach(n -> System.out.println("n=" + n));
```

Expected output:

```text
n=1
n=2
n=3
```

Guideline:

- keep side effects minimal in lambda bodies
- avoid structural modifications on same source list inside `forEach`

## 7) Stream Iteration Style

Concept taught: Demonstrates 7) Stream Iteration Style in practice.

```java
List<String> names = List.of(" Ram ", "Shyam", "ram", "");
names.stream()
     .map(String::trim)
     .filter(s -> !s.isEmpty())
     .map(String::toLowerCase)
     .distinct()
     .forEach(System.out::println);
```

Expected output:

```text
ram
shyam
```

Use streams when:

- pipeline readability is better than manual loop
- transformation/filtering/aggregation is primary goal

## 8) Reverse Iteration Techniques

### 8.1 Index reverse loop

Concept taught: Demonstrates 8.1 Index reverse loop in practice.

```java
List<Integer> nums = List.of(10, 20, 30);
for (int i = nums.size() - 1; i >= 0; i--) {
    System.out.println(nums.get(i));
}
```

Output:

```text
30
20
10
```

### 8.2 Java 21+ `reversed()` view

Concept taught: Demonstrates 8.2 Java 21+ `reversed()` view in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(10, 20, 30));
System.out.println(nums.reversed());
```

Output:

```text
[30, 20, 10]
```

## 9) Fail-Fast vs Snapshot Iteration

- `ArrayList`/`LinkedList` iterators are usually fail-fast (best effort)
- `CopyOnWriteArrayList` iterator is snapshot-based

Concept taught: Demonstrates 9) Fail-Fast vs Snapshot Iteration in practice.

```java
List<String> a = new ArrayList<>(List.of("x", "y"));
for (String s : a) {
    if (s.equals("x")) a.add("z"); // likely throws CME
}
```

Concept taught: Demonstrates 9) Fail-Fast vs Snapshot Iteration in practice.

```java
CopyOnWriteArrayList<String> b = new CopyOnWriteArrayList<>(List.of("x", "y"));
for (String s : b) {
    if (s.equals("x")) b.add("z"); // safe snapshot iteration
}
System.out.println(b);
```

Possible output for second snippet:

```text
[x, y, z]
```

## 10) Best-Practice Decision Guide

- need index -> index loop
- need safe removal during loop -> iterator
- need bidirectional edit while traversing -> listIterator
- need declarative transform pipeline -> stream
- need thread-safe read-heavy concurrent iteration -> `CopyOnWriteArrayList`

## 11) Summary

Iteration is not one-size-fits-all in Java. Pick iteration strategy based on mutation needs, list type, and clarity of intent.
