# 09 - LinkedBlockingQueue Core

## 1) Internal Idea

`LinkedBlockingQueue` uses linked nodes.

- optionally bounded (default effectively unbounded)
- thread-safe
- common in executors and async pipelines

## 2) Capacity Warning

Default constructor creates very large capacity (`Integer.MAX_VALUE`), which can risk memory pressure if producers outrun consumers.

## 3) Basic Usage

Concept taught: Producer-consumer flow with linked blocking queue.

```java
BlockingQueue<String> q = new LinkedBlockingQueue<>(3);
q.put("m1");
q.put("m2");
System.out.println(q.take());
System.out.println(q.size());
```

Expected output:

```text
m1
1
```

## 4) Drain Pattern

Concept taught: Bulk retrieval using `drainTo`.

```java
LinkedBlockingQueue<Integer> q = new LinkedBlockingQueue<>();
q.add(1);
q.add(2);
q.add(3);
List<Integer> batch = new ArrayList<>();
q.drainTo(batch);
System.out.println(batch);
System.out.println(q.size());
```

Expected output:

```text
[1, 2, 3]
0
```

## 5) Summary

Use `LinkedBlockingQueue` for flexible producer-consumer pipelines, but prefer explicit capacity for safety.
