# 07 - BlockingQueue Overview

## 1) Why BlockingQueue

`BlockingQueue` is for producer-consumer concurrency.

Key difference from normal queues:

- `put` blocks when queue is full
- `take` blocks when queue is empty

## 2) Method Groups

- exception style: `add`, `remove`, `element`
- special value style: `offer`, `poll`, `peek`
- blocking style: `put`, `take`
- timed blocking: `offer(e, timeout, unit)`, `poll(timeout, unit)`

## 3) Producer-Consumer Diagram

```mermaid
flowchart LR
    P[Producer Threads] --> Q[BlockingQueue]
    Q --> C[Consumer Threads]

    P -->|put blocks when full| Q
    C -->|take blocks when empty| Q
```

## 4) Minimal Example

Concept taught: Basic handoff with blocking `put/take`.

```java
BlockingQueue<Integer> q = new ArrayBlockingQueue<>(2);
q.put(10);
q.put(20);
System.out.println(q.take());
System.out.println(q.take());
```

Expected output:

```text
10
20
```

## 5) Implementations to Know

- `ArrayBlockingQueue` (bounded, array)
- `LinkedBlockingQueue` (optionally bounded, linked nodes)
- `DelayQueue` (time-delayed elements)
- `PriorityBlockingQueue` (priority, unbounded)

## 6) Summary

`BlockingQueue` is the core primitive for safe and simple producer-consumer pipelines in Java concurrency.
