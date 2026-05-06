# 04 - Vector and Stack Core

## 1) Vector

`Vector` is a legacy synchronized dynamic array.

- thread-safe via method-level synchronization
- slower than `ArrayList` in single-threaded usage

Use mostly for legacy compatibility.

Core complexity:

- `get/set`: `O(1)`
- `add` end: `O(1)` amortized
- `add/remove` middle: `O(n)`
- `remove(value)`: `O(n)`
- `contains`: `O(n)`
- `indexOf/lastIndexOf`: `O(n)`

Capacity helpers:

```java
vector.ensureCapacity(50);
vector.trimToSize();
int cap = vector.capacity();
```

Common operations:

```java
Vector<Integer> vector = new Vector<>();
vector.add(3);
vector.add(5);
vector.add(6);
vector.add(7);
vector.remove(2);
vector.add(2, 4);
vector.set(2, 6);
int x = vector.get(3);
int n = vector.size();
boolean e = vector.isEmpty();
boolean ok = vector.contains(3);
int i1 = vector.indexOf(3);
int i2 = vector.lastIndexOf(3);
Object[] arr = vector.toArray();
vector.clear();
```

Java 21 list operations:

```java
vector.addFirst(10);
vector.addLast(20);
int first = vector.getFirst();
int last = vector.getLast();
vector.removeFirst();
vector.removeLast();
List<Integer> rev = vector.reversed(); // view
```

- `reversed()` returns reverse-order view, not copied list.
- changes in original are reflected in view.

Capacity behavior:

- default initial capacity: `10`
- when full, capacity usually grows about `2x`
- constructors:

```java
Vector<Integer> v1 = new Vector<>(20);
Vector<Integer> v2 = new Vector<>(10, 5); // capacityIncrement
```

## 2) Stack

`Stack` extends `Vector` (legacy LIFO stack).

```java
Stack<Integer> st = new Stack<>();
st.push(10);
st.push(20);
int top = st.peek();
int pos = st.search(10); // 1-based from top, -1 if absent
boolean empty = st.isEmpty();
System.out.println(st.pop()); // 20
```

Method behavior:

- in-place: `push`, `pop`, `clear`
- read: `peek`, `search`, `isEmpty`, `size`

Complexity:

- `push`: `O(1)` amortized
- `pop`: `O(1)`
- `peek`: `O(1)`
- `isEmpty`: `O(1)`
- `search`: `O(n)`

## 3) Modern Recommendation

Prefer `Deque` implementation (`ArrayDeque`) instead of `Stack` for new code.

```java
Deque<Integer> st2 = new ArrayDeque<>();
st2.push(10);
st2.push(20);
System.out.println(st2.pop()); // 20
```

LinkedList as stack (keep same end for LIFO):

```java
LinkedList<Integer> ls = new LinkedList<>();
ls.addLast(1);           // push
int top2 = ls.getLast(); // peek
int x2 = ls.removeLast();// pop
```

ArrayList as manual stack:

```java
ArrayList<Integer> arr = new ArrayList<>();
arr.add(10);
int top3 = arr.get(arr.size() - 1);
int x3 = arr.remove(arr.size() - 1);
```

Guard against empty list before `get/remove(size - 1)`.

## 4) Thread Safety Reality

- `Vector`/`Stack` synchronize individual methods.
- Compound operations are still not atomic by default.

Example non-atomic compound action:

```java
if (!vector.contains(5)) {
    vector.add(5);
}
```

This is not atomic as a pair.

Concurrent add demo:

```java
Vector<Integer> vector = new Vector<>();
Thread t1 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) vector.add(i);
});
Thread t2 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) vector.add(i);
});
t1.start();
t2.start();
```

Notes:

- `Stack`: legacy thread-safe behavior per method, with locking overhead
- `LinkedList`, `ArrayList`, `ArrayDeque`: not thread-safe by default
- for heavy-read concurrent list scenarios, prefer `CopyOnWriteArrayList`
- for most non-concurrent list scenarios, prefer `ArrayList`

Common mistakes:

- wrong import `java.utils.*` (correct is `java.util.*`)
- mixing list ends in stack simulation breaks LIFO (`addLast` with `removeFirst`)
