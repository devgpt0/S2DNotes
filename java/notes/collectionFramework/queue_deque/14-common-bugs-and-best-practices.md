# 14 - Common Bugs and Best Practices

## 1) Bug: Using `remove()` on Empty Queue

Concept taught: `remove` throws on empty queue; `poll` is safer.

```java
Queue<Integer> q = new ArrayDeque<>();
try {
    q.remove();
} catch (NoSuchElementException ex) {
    System.out.println("remove failed");
}
System.out.println(q.poll());
```

Expected output:

```text
remove failed
null
```

## 2) Bug: Mixing Ends Incorrectly in Deque

Concept taught: Wrong end choice can accidentally switch FIFO/LIFO semantics.

```java
Deque<Integer> d = new ArrayDeque<>();
d.addLast(1);
d.addLast(2);
System.out.println(d.removeFirst()); // FIFO
System.out.println(d);
```

Expected output:

```text
1
[2]
```

If you expected stack behavior, this is wrong end usage.

## 3) Bug: Forgetting Null Restrictions

`ArrayDeque`, `PriorityQueue`, and most concurrent queues do not allow nulls.

## 4) Bug: Unbounded Queue Memory Growth

Using default unbounded queues in high-producer systems can cause memory pressure.

## 5) Bug: Assuming PriorityQueue Iteration Is Sorted

Concept taught: Priority queue iterator order is not sorted order.

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.addAll(List.of(5, 1, 3, 2));
System.out.println(pq);
System.out.println(pq.poll());
```

Possible output:

```text
[1, 2, 3, 5]
1
```

Printed structure can vary; only head priority is guaranteed.

## 6) Best Practices

- prefer `offer/poll/peek` for robust queue code
- choose explicit bounded capacity for blocking queues
- use `ArrayDeque` for non-concurrent queue/stack workflows
- use `PriorityQueue` only when priority ordering is needed
- document shutdown protocols (poison pill/cancellation)

## 7) Summary

Most queue/deque bugs are semantics bugs: wrong method family, wrong end, wrong ordering assumption, or wrong queue type for concurrency.
