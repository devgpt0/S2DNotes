# 06 - PriorityQueue Core (Complete)

## 1) Internal Idea

`PriorityQueue` is a heap-based queue.

- not FIFO
- head is highest-priority element (min by default)

## 2) Complexity

- `offer`: `O(log n)`
- `poll`: `O(log n)`
- `peek`: `O(1)`

## 3) Min-Heap Default Behavior

Concept taught: smallest element comes out first.

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(30);
pq.offer(10);
pq.offer(20);
System.out.println(pq.poll());
System.out.println(pq.poll());
```

Expected output:

```text
10
20
```

## 4) Max-Heap with Comparator

Concept taught: custom comparator changes priority order.

```java
PriorityQueue<Integer> max = new PriorityQueue<>(Comparator.reverseOrder());
max.offer(30);
max.offer(10);
max.offer(20);
System.out.println(max.poll());
System.out.println(max.poll());
```

Expected output:

```text
30
20
```

## 5) Custom Objects

Concept taught: priority by object field.

```java
record Task(String name, int priority) {}
PriorityQueue<Task> tasks = new PriorityQueue<>(Comparator.comparingInt(Task::priority));
tasks.offer(new Task("low", 5));
tasks.offer(new Task("high", 1));
System.out.println(tasks.poll());
```

Expected output:

```text
Task[name=high, priority=1]
```

## 6) Important Notes

- iteration order of `PriorityQueue` is not sorted order
- no null elements allowed

## 7) Summary

Use `PriorityQueue` when processing order depends on priority, not insertion time.
