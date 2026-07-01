# 10 - ConcurrentLinkedQueue Core

## 1) Internal Idea

`ConcurrentLinkedQueue` is a non-blocking lock-free FIFO queue.

- thread-safe
- unbounded
- does not block on empty/full

## 2) API Style

Use non-blocking methods:

- `offer`
- `poll`
- `peek`

## 3) Basic Usage

Concept taught: Lock-free concurrent FIFO operations.

```java
ConcurrentLinkedQueue<Integer> q = new ConcurrentLinkedQueue<>();
q.offer(10);
q.offer(20);
System.out.println(q.poll());
System.out.println(q.peek());
```

Expected output:

```text
10
20
```

## 4) Empty Poll Semantics

Concept taught: Poll on empty returns null (no blocking).

```java
ConcurrentLinkedQueue<String> q = new ConcurrentLinkedQueue<>();
System.out.println(q.poll());
```

Expected output:

```text
null
```

## 5) When to Use

- high-throughput concurrent pipelines where blocking is not required
- event queues with lightweight polling loops

## 6) Summary

Use `ConcurrentLinkedQueue` when you need thread-safe non-blocking FIFO behavior.
