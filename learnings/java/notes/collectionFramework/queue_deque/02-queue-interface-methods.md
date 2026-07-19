# 02 - Queue Interface Methods

## 1) Core Queue Contract

`Queue<E>` focuses on head/tail workflow.

Read these method pairs carefully:

- insert: `add(e)` vs `offer(e)`
- remove head: `remove()` vs `poll()`
- inspect head: `element()` vs `peek()`

## 2) Exception vs Special-Value Methods

- `add/remove/element` throw exception on failure/empty
- `offer/poll/peek` return special value (`false` or `null`)

Concept taught: `poll` and `peek` are safe on empty queue.

```java
Queue<Integer> q = new ArrayDeque<>();
System.out.println(q.poll());
System.out.println(q.peek());
```

Expected output:

```text
null
null
```

Concept taught: `remove` and `element` throw on empty queue.

```java
Queue<Integer> q = new ArrayDeque<>();
try {
    q.remove();
} catch (NoSuchElementException ex) {
    System.out.println("remove failed");
}
try {
    q.element();
} catch (NoSuchElementException ex) {
    System.out.println("element failed");
}
```

Expected output:

```text
remove failed
element failed
```

## 3) Basic Queue Workflow

Concept taught: Standard enqueue/dequeue lifecycle.

```java
Queue<String> q = new ArrayDeque<>();
q.offer("task1");
q.offer("task2");
q.offer("task3");

System.out.println(q.peek());
System.out.println(q.poll());
System.out.println(q);
```

Expected output:

```text
task1
task1
[task2, task3]
```

## 4) Capacity-Aware Queues

In bounded queues (`ArrayBlockingQueue`), `offer` is often preferred over `add` because it avoids exceptions when full.

## 5) Summary

Use `offer/poll/peek` for robust queue code, especially in production pipelines.
