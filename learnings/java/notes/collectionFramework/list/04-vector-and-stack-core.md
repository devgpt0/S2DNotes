# 04 - Vector and Stack Core (Complete)

## 1) Why These Are Called Legacy

`Vector` and `Stack` are older collection classes from early Java versions.

- `Vector` is a synchronized dynamic array.
- `Stack` extends `Vector` and models LIFO.

They still work, but modern code usually prefers:

- `ArrayList` over `Vector`
- `ArrayDeque` over `Stack`

## 2) `Vector` Internals and Behavior

Like `ArrayList`, `Vector` stores elements in an array and grows when full.

Differences:

- methods are synchronized (thread-safe per method)
- extra locking overhead in single-threaded workloads
- has legacy APIs like `elements()` (Enumeration)

### 2.1 Basic `Vector` Example

Concept taught: Demonstrates 2.1 Basic `Vector` Example in practice.

```java
Vector<Integer> vector = new Vector<>();
vector.add(10);
vector.add(20);
vector.add(1, 15);
System.out.println(vector);

vector.remove(Integer.valueOf(20));
System.out.println(vector);
```

Expected output:

```text
[10, 15, 20]
[10, 15]
```

### 2.2 Capacity-Oriented APIs

Concept taught: Demonstrates 2.2 Capacity-Oriented APIs in practice.

```java
Vector<Integer> v = new Vector<>(2, 3); // initialCapacity=2, capacityIncrement=3
v.add(1);
v.add(2);
System.out.println(v.capacity());
v.add(3); // triggers growth by increment
System.out.println(v.capacity());
```

Expected output:

```text
2
5
```

Notes:

- second constructor argument controls growth step
- if not set, growth policy is implementation-dependent

### 2.3 Java 21+ Sequenced Methods

Concept taught: Demonstrates 2.3 Java 21+ Sequenced Methods in practice.

```java
Vector<String> v = new Vector<>(List.of("B", "C"));
v.addFirst("A");
v.addLast("D");
System.out.println(v.getFirst());
System.out.println(v.getLast());
System.out.println(v.reversed());
```

Expected output:

```text
A
D
[D, C, B, A]
```

## 3) Thread-Safety Reality for `Vector`

`Vector` synchronizes individual method calls, but compound actions are still not atomic.

Concept taught: Demonstrates 3) Thread-Safety Reality for `Vector` in practice.

```java
if (!vector.contains(50)) {
    vector.add(50);
}
```

Two threads can still interleave this block and insert duplicates.

For high-contention concurrent logic, modern alternatives (`ConcurrentHashMap`, queues, explicit locks, etc.) are usually better design choices.

## 4) `Stack` Core APIs

`Stack` methods:

- `push(e)`
- `pop()`
- `peek()`
- `search(e)` (1-based from top)
- `empty()`/`isEmpty()`

Concept taught: Demonstrates 4) `Stack` Core APIs in practice.

```java
Stack<Integer> st = new Stack<>();
st.push(10);
st.push(20);
st.push(30);

System.out.println(st.peek());
System.out.println(st.search(10));
System.out.println(st.pop());
System.out.println(st);
```

Expected output:

```text
30
3
30
[10, 20]
```

Complexity:

- push/pop/peek: generally `O(1)` amortized for push
- search: `O(n)`

## 5) Why `ArrayDeque` Is Preferred for Stack

Concept taught: Demonstrates 5) Why `ArrayDeque` Is Preferred for Stack in practice.

```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(10);
stack.push(20);
System.out.println(stack.peek());
System.out.println(stack.pop());
System.out.println(stack);
```

Expected output:

```text
20
20
[10]
```

Advantages:

- cleaner stack/deque semantics
- better modern API fit
- no legacy baggage from `Vector`

## 6) Enumeration vs Iterator

`Vector` supports legacy `Enumeration`:

Concept taught: Demonstrates 6) Enumeration vs Iterator in practice.

```java
Enumeration<Integer> en = v.elements();
while (en.hasMoreElements()) {
    System.out.println(en.nextElement());
}
```

But in modern Java, use `Iterator`/enhanced for loops for consistency across collections.

## 7) Common Mistakes

- importing `java.utils.*` (wrong) instead of `java.util.*`
- using `Stack` for new production code when `ArrayDeque` is better
- assuming synchronized methods make all multi-step logic thread-safe
- confusing `search` return indexing (it is 1-based from top)

## 8) Migration Tip

Legacy code often has:

Concept taught: Demonstrates 8) Migration Tip in practice.

```java
Vector<String> list = new Vector<>();
Stack<Integer> st = new Stack<>();
```

Modern equivalent (if no strict legacy constraint):

Concept taught: Demonstrates 8) Migration Tip in practice.

```java
List<String> list = new ArrayList<>();
Deque<Integer> st = new ArrayDeque<>();
```

## 9) Summary

Keep `Vector`/`Stack` for legacy compatibility and understanding old codebases. For new code, choose modern collections unless a compatibility contract requires these classes.
