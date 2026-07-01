# 08 - ArrayBlockingQueue Core

## 1) Internal Idea

`ArrayBlockingQueue` is bounded and array-backed.

- fixed capacity
- thread-safe
- optional fairness setting

## 2) Why Bounded Queue Matters

Bounded queues provide backpressure and prevent unlimited memory growth.

## 3) Basic Usage

Concept taught: Capacity-limited queue with blocking operations.

```java
ArrayBlockingQueue<String> q = new ArrayBlockingQueue<>(2);
q.put("A");
q.put("B");
System.out.println(q.take());
System.out.println(q.take());
```

Expected output:

```text
A
B
```

## 4) Timed Offer/Poll

Concept taught: Timeout-based non-permanent blocking.

```java
ArrayBlockingQueue<Integer> q = new ArrayBlockingQueue<>(1);
q.put(1);
boolean ok = q.offer(2, 100, TimeUnit.MILLISECONDS);
System.out.println(ok);
System.out.println(q.poll(100, TimeUnit.MILLISECONDS));
```

Expected output:

```text
false
1
```

## 5) Fairness Mode

Constructor supports fairness flag:

Concept taught: Demonstrates 5) Fairness Mode in practice.

```java
new ArrayBlockingQueue<>(capacity, true)
```

Fair mode can improve queueing fairness but may reduce throughput.

## 6) Summary

Use `ArrayBlockingQueue` when you need strict bounded capacity and predictable backpressure.
