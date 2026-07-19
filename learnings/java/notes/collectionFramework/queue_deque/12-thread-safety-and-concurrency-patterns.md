# 12 - Thread Safety and Concurrency Patterns

## 1) Pattern: Producer-Consumer with BlockingQueue

Concept taught: Safe handoff between producer and consumer threads.

```java
BlockingQueue<Integer> q = new ArrayBlockingQueue<>(2);

Thread producer = new Thread(() -> {
    try {
        q.put(1);
        q.put(2);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
});

Thread consumer = new Thread(() -> {
    try {
        System.out.println(q.take());
        System.out.println(q.take());
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
    }
});

producer.start();
consumer.start();
```

Expected output:

```text
1
2
```

## 2) Pattern: Work Queue with Poison Pill

Concept taught: Graceful consumer shutdown signal.

```java
final int POISON = -1;
BlockingQueue<Integer> q = new LinkedBlockingQueue<>();
q.put(10);
q.put(20);
q.put(POISON);

while (true) {
    int x = q.take();
    if (x == POISON) break;
    System.out.println("processed " + x);
}
```

Expected output:

```text
processed 10
processed 20
```

## 3) Pattern: Non-Blocking Event Queue

Concept taught: Poll loop with `ConcurrentLinkedQueue`.

```java
ConcurrentLinkedQueue<String> q = new ConcurrentLinkedQueue<>();
q.offer("e1");
q.offer("e2");

String e;
while ((e = q.poll()) != null) {
    System.out.println("event=" + e);
}
```

Expected output:

```text
event=e1
event=e2
```

## 4) Pattern: Priority Task Scheduling

Concept taught: Process highest-priority tasks first.

```java
PriorityQueue<Integer> pq = new PriorityQueue<>(Comparator.reverseOrder());
pq.offer(1);
pq.offer(5);
pq.offer(3);
while (!pq.isEmpty()) {
    System.out.println(pq.poll());
}
```

Expected output:

```text
5
3
1
```

## 5) Summary

Concurrency queues are about the right balance of blocking, ordering, and throughput requirements.
