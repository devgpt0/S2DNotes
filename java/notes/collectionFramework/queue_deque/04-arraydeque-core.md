# 04 - ArrayDeque Core (Complete)

## 1) Why `ArrayDeque` Is Default for Queue/Stack

`ArrayDeque` is array-backed and resizable.

- fast at both ends
- no legacy baggage of `Stack`
- generally faster than `LinkedList` for queue/stack workloads

## 2) Complexity

- add/remove first or last: amortized `O(1)`
- peek first or last: `O(1)`

## 3) Queue Usage

Concept taught: `ArrayDeque` as FIFO queue.

```java
Queue<Integer> q = new ArrayDeque<>();
q.offer(10);
q.offer(20);
q.offer(30);
System.out.println(q.poll());
System.out.println(q.peek());
```

Expected output:

```text
10
20
```

## 4) Stack Usage

Concept taught: `ArrayDeque` as modern stack replacement.

```java
Deque<String> st = new ArrayDeque<>();
st.push("A");
st.push("B");
System.out.println(st.pop());
System.out.println(st.peek());
```

Expected output:

```text
B
A
```

## 5) Important Rule: No Nulls

`ArrayDeque` does not allow `null` elements.

Concept taught: null insertion throws exception.

```java
Deque<String> dq = new ArrayDeque<>();
try {
    dq.add(null);
} catch (NullPointerException ex) {
    System.out.println("null not allowed");
}
```

Expected output:

```text
null not allowed
```

## 6) Summary

For non-concurrent queue/deque/stack operations, `ArrayDeque` is usually the best first choice.
