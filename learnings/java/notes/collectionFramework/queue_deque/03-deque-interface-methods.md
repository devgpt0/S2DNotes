# 03 - Deque Interface Methods

## 1) Deque Method Families

Deque supports both ends.

- front: `addFirst`, `offerFirst`, `removeFirst`, `pollFirst`, `getFirst`, `peekFirst`
- back: `addLast`, `offerLast`, `removeLast`, `pollLast`, `getLast`, `peekLast`

Stack aliases on deque:

- `push` = addFirst
- `pop` = removeFirst
- `peek` = peekFirst

## 2) Queue Mode with Deque

Concept taught: Use one end for enqueue and opposite for dequeue (FIFO).

```java
Deque<String> dq = new ArrayDeque<>();
dq.offerLast("A");
dq.offerLast("B");
dq.offerLast("C");
System.out.println(dq.pollFirst());
System.out.println(dq);
```

Expected output:

```text
A
[B, C]
```

## 3) Stack Mode with Deque

Concept taught: Use same end for push/pop (LIFO).

```java
Deque<Integer> st = new ArrayDeque<>();
st.push(1);
st.push(2);
st.push(3);
System.out.println(st.pop());
System.out.println(st);
```

Expected output:

```text
3
[2, 1]
```

## 4) Sliding Window Use Pattern

Deque is heavily used in sliding-window max/min algorithms.

Concept taught: Maintaining index candidates in deque.

```java
int[] arr = {1, 3, -1, -3, 5};
Deque<Integer> idx = new ArrayDeque<>();
for (int i = 0; i < arr.length; i++) {
    while (!idx.isEmpty() && arr[idx.peekLast()] <= arr[i]) idx.pollLast();
    idx.offerLast(i);
}
System.out.println(idx.peekFirst());
System.out.println(arr[idx.peekFirst()]);
```

Expected output:

```text
4
5
```

## 5) Summary

`Deque` is one of the most flexible collection interfaces in Java and should be your default for queue+stack workflows.
