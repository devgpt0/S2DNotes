# 03 - LinkedList Core (Complete)

## 1) Internal Model

`LinkedList` is a doubly linked list.

Each node stores:

- element value
- reference to previous node
- reference to next node

`LinkedList` implements both:

- `List`
- `Deque`

So you can use it as list, queue, deque, or stack.

## 2) Complexity Reality

- `addFirst/addLast/removeFirst/removeLast`: `O(1)`
- `offer/poll/peek` at ends: `O(1)`
- `get(index)`: `O(n)`
- `set(index, e)`: `O(n)` traversal
- `add(index, e)`: `O(n)` traversal
- `remove(index)`: `O(n)` traversal
- `contains`: `O(n)`

Important: though insertion after locating a node is cheap, finding that location by index is still linear.

## 3) Basic Operations with Output

Concept taught: Demonstrates 3) Basic Operations with Output in practice.

```java
LinkedList<String> list = new LinkedList<>();
list.add("B");
list.addFirst("A");
list.addLast("C");
System.out.println(list);

System.out.println(list.getFirst());
System.out.println(list.getLast());

list.removeFirst();
list.removeLast();
System.out.println(list);
```

Expected output:

```text
[A, B, C]
A
C
[B]
```

## 4) Queue / Deque Usage (Natural Fit)

Concept taught: Demonstrates 4) Queue / Deque Usage (Natural Fit) in practice.

```java
Deque<Integer> dq = new LinkedList<>();
dq.offerLast(10);
dq.offerLast(20);
dq.offerFirst(5);

System.out.println(dq);
System.out.println(dq.pollFirst());
System.out.println(dq.pollLast());
System.out.println(dq);
```

Expected output:

```text
[5, 10, 20]
5
20
[10]
```

## 5) Stack Using `LinkedList`

Use one end consistently for true LIFO.

Concept taught: Demonstrates 5) Stack Using `LinkedList` in practice.

```java
LinkedList<Integer> st = new LinkedList<>();
st.addLast(1); // push
st.addLast(2); // push
System.out.println(st.getLast());   // peek
System.out.println(st.removeLast()); // pop
System.out.println(st);
```

Expected output:

```text
2
2
[1]
```

Wrong pattern:

- `addLast` with `removeFirst` -> becomes FIFO behavior

## 6) Index-Based Access Example

Concept taught: Demonstrates 6) Index-Based Access Example in practice.

```java
LinkedList<String> list = new LinkedList<>(List.of("A", "B", "C", "D"));
System.out.println(list.get(2));
list.add(2, "X");
System.out.println(list);
```

Expected output:

```text
C
[A, B, X, C, D]
```

Explanation:

- operation works, but traversal cost makes repeated indexed operations expensive

## 7) Occurrence-Based Removals

Concept taught: Demonstrates 7) Occurrence-Based Removals in practice.

```java
LinkedList<String> list = new LinkedList<>(List.of("A", "B", "A", "C", "A"));
list.removeFirstOccurrence("A");
list.removeLastOccurrence("A");
System.out.println(list);
```

Expected output:

```text
[B, A, C]
```

## 8) Iterator and ListIterator

Concept taught: Demonstrates 8) Iterator and ListIterator in practice.

```java
LinkedList<String> list = new LinkedList<>(List.of("a", "b", "c"));
ListIterator<String> it = list.listIterator();
while (it.hasNext()) {
    String v = it.next();
    if (v.equals("b")) {
        it.set("B");
        it.add("x");
    }
}
System.out.println(list);
```

Expected output:

```text
[a, B, x, c]
```

Why this is good:

- safe structural updates during traversal through iterator API

## 9) Java 21+ Sequenced Methods

`LinkedList` already had head/tail style APIs; Java 21 list sequencing makes these operations more uniform across list types.

Concept taught: Demonstrates 9) Java 21+ Sequenced Methods in practice.

```java
LinkedList<Integer> nums = new LinkedList<>(List.of(2, 3));
nums.addFirst(1);
nums.addLast(4);
System.out.println(nums.reversed());
```

Output:

```text
[4, 3, 2, 1]
```

## 10) When to Use `LinkedList`

Use it when:

- you mainly operate at both ends (queue/deque/stack style)
- you want `Deque` + `List` behavior in one object

Avoid when:

- you perform frequent random index reads
- memory pressure is high (node overhead per element)

## 11) Common Pitfalls

- choosing `LinkedList` expecting it to beat `ArrayList` for all inserts
- heavy `get(i)` in loops (`O(n^2)` style anti-pattern)
- mixing list API and deque API inconsistently

Anti-pattern:

Concept taught: Demonstrates 11) Common Pitfalls in practice.

```java
for (int i = 0; i < linked.size(); i++) {
    System.out.println(linked.get(i)); // can become expensive
}
```

Prefer:

Concept taught: Demonstrates 11) Common Pitfalls in practice.

```java
for (String s : linked) {
    System.out.println(s);
}
```

## 12) Summary

Think of `LinkedList` primarily as a deque-friendly structure, not as a random-access list.
