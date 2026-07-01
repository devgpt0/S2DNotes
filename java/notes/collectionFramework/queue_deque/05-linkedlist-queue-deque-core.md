# 05 - LinkedList as Queue/Deque (Core)

## 1) Internal Model

`LinkedList` is doubly-linked and implements both `List` and `Deque`.

For queue/deque workflows it provides natural end operations.

## 2) Complexity (Deque Operations)

- add/remove at ends: `O(1)`
- peek at ends: `O(1)`
- indexed access: `O(n)` (not ideal for list random access heavy workloads)

## 3) Queue Mode

Concept taught: `LinkedList` used as FIFO queue.

```java
Queue<String> q = new LinkedList<>();
q.offer("job1");
q.offer("job2");
System.out.println(q.poll());
System.out.println(q);
```

Expected output:

```text
job1
[job2]
```

## 4) Deque Mode

Concept taught: Bidirectional operations with `Deque` APIs.

```java
Deque<Integer> d = new LinkedList<>();
d.offerFirst(2);
d.offerLast(3);
d.offerFirst(1);
System.out.println(d.pollLast());
System.out.println(d);
```

Expected output:

```text
3
[1, 2]
```

## 5) When to Use

- when list + deque features are both needed
- when API expects `LinkedList`

For pure stack/queue performance in single-threaded flow, `ArrayDeque` often performs better.

## 6) Summary

`LinkedList` is versatile, but not always the fastest general queue/deque choice.
