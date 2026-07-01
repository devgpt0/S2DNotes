# 01 - List Basics (Complete)

## 1) What Is `List`

`List` is an ordered collection in Java Collections Framework.

Core properties:

- preserves insertion order
- allows duplicate elements
- supports index-based access (`0` to `size()-1`)
- can contain `null` in most mutable implementations

Hierarchy (Java 21+):

- `Iterable` -> `Collection` -> `List` -> `SequencedCollection`

That means modern `List` also supports first/last and reverse-view style operations (`getFirst`, `getLast`, `reversed`, etc.).

## 2) Main Implementations

- `ArrayList`: dynamic array, best general-purpose default
- `LinkedList`: doubly linked list, also implements `Deque`
- `Vector`: legacy synchronized dynamic array
- `Stack`: legacy LIFO stack, extends `Vector`
- `CopyOnWriteArrayList`: concurrent, read-heavy workloads

## 3) How to Declare Lists Correctly

Prefer interface type on left side:

Concept taught: Demonstrates 3) How to Declare Lists Correctly in practice.

```java
List<String> names = new ArrayList<>();
```

Why this is best:

- keeps code implementation-agnostic
- you can switch to `LinkedList`/`CopyOnWriteArrayList` later without changing method signatures

Avoid raw types:

Concept taught: Demonstrates 3) How to Declare Lists Correctly in practice.

```java
// Avoid
List raw = new ArrayList();

// Correct
List<Integer> nums = new ArrayList<>();
```

## 4) Core API Families

### 4.1 Add/Insert

Concept taught: Demonstrates 4.1 Add/Insert in practice.

```java
List<String> list = new ArrayList<>();
list.add("A");
list.add("B");
list.add(1, "X");
System.out.println(list);
```

Expected output:

```text
[A, X, B]
```

Explanation:

- `add(e)` appends at end
- `add(index, e)` inserts and shifts right

### 4.2 Read/Update

Concept taught: Demonstrates 4.2 Read/Update in practice.

```java
List<String> list = new ArrayList<>(List.of("A", "B", "C"));
System.out.println(list.get(0));
list.set(1, "BB");
System.out.println(list);
```

Expected output:

```text
A
[A, BB, C]
```

Explanation:

- `get(index)` reads without structural change
- `set(index, e)` replaces existing element

### 4.3 Remove

Concept taught: Demonstrates 4.3 Remove in practice.

```java
List<Integer> list = new ArrayList<>(List.of(10, 20, 30, 20));
list.remove(1); // remove by index
list.remove(Integer.valueOf(20)); // remove first matching value
System.out.println(list);
```

Expected output:

```text
[10, 30]
```

Explanation:

- `remove(int)` and `remove(Object)` are different overloads
- this is one of the most common beginner bugs

### 4.4 Query

Concept taught: Demonstrates 4.4 Query in practice.

```java
List<String> list = List.of("java", "python", "java");
System.out.println(list.contains("java"));
System.out.println(list.indexOf("java"));
System.out.println(list.lastIndexOf("java"));
System.out.println(list.size());
System.out.println(list.isEmpty());
```

Expected output:

```text
true
0
2
3
false
```

## 5) Java 21+ Sequenced List Methods

Concept taught: Demonstrates 5) Java 21+ Sequenced List Methods in practice.

```java
List<String> list = new ArrayList<>(List.of("B", "C"));
list.addFirst("A");
list.addLast("D");
System.out.println(list.getFirst());
System.out.println(list.getLast());
System.out.println(list.reversed());
```

Expected output:

```text
A
D
[D, C, B, A]
```

Explanation:

- `reversed()` is a reverse-order view (not necessarily a copied new list)
- updates in base list may reflect in view

## 6) Mutability Spectrum (Very Important)

### Mutable list

Concept taught: Demonstrates Mutable list in practice.

```java
List<String> a = new ArrayList<>(List.of("x", "y"));
a.add("z");
System.out.println(a);
```

Output:

```text
[x, y, z]
```

### Fixed-size view

Concept taught: Demonstrates Fixed-size view in practice.

```java
List<String> b = Arrays.asList("x", "y");
b.set(0, "X");
System.out.println(b);
```

Output:

```text
[X, y]
```

`b.add("z")` would throw `UnsupportedOperationException`.

### Immutable list

Concept taught: Demonstrates Immutable list in practice.

```java
List<String> c = List.of("x", "y");
System.out.println(c);
```

Output:

```text
[x, y]
```

Any `add/remove/set` on `c` throws `UnsupportedOperationException`.

## 7) Complexity Snapshot

Typical (implementation-dependent):

- `get(index)`: `O(1)` for `ArrayList`, `O(n)` for `LinkedList`
- `add(e)` end: `O(1)` amortized for `ArrayList`
- `add(index, e)`: `O(n)` for `ArrayList` (shift), traversal cost in `LinkedList`
- `contains`: `O(n)`

## 8) Fail-Fast Iterator Concept

Most list iterators are fail-fast (best-effort): if list is structurally modified outside iterator during iteration, a `ConcurrentModificationException` can occur.

Concept taught: Demonstrates 8) Fail-Fast Iterator Concept in practice.

```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));
for (String s : list) {
    if (s.equals("b")) {
        list.remove(s); // unsafe here
    }
}
```

Expected behavior:

```text
Throws ConcurrentModificationException (typically)
```

Safe options:

- `Iterator.remove()`
- `removeIf(...)`
- collect then remove later

## 9) When to Pick Which List Quickly

- choose `ArrayList` by default
- choose `LinkedList` mainly for deque-style head/tail heavy logic
- choose `CopyOnWriteArrayList` for many reads + very few writes in concurrent code
- avoid new `Vector`/`Stack` unless legacy compatibility is required

## 10) Summary

If you remember only one rule: start with `List<T> list = new ArrayList<>();`, use generics, know mutability type, and be careful with iteration-time modifications.
