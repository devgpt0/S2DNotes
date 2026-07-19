# 09 - Virtual Threads

Virtual threads are lightweight Java threads designed for high-concurrency blocking I/O.

## 1) Start a Virtual Thread

```java
Thread thread = Thread.startVirtualThread(() ->
        System.out.println(Thread.currentThread().isVirtual()));
thread.join();
// Output: true
```

## 2) Thread Per Task

```java
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Integer>> futures = IntStream.rangeClosed(1, 3)
            .mapToObj(value -> executor.submit(() -> value * value))
            .toList();
    for (Future<Integer> future : futures) {
        System.out.println(future.get());
    }
}
// Output:
// 1
// 4
// 9
```

Do not pool virtual threads. Create one per task and limit concurrency at scarce resources.

## 3) Virtual Threads Do Not Remove Capacity Limits

```java
Semaphore databaseConnections = new Semaphore(10);
databaseConnections.acquire();
try {
    System.out.println("using one database permit");
} finally {
    databaseConnections.release();
}
// Output: using one database permit
```

A million virtual threads cannot create a million database connections safely.

## 4) Thread-Local Cost

```java
ThreadLocal<String> requestId = new ThreadLocal<>();
requestId.set("REQ-1");
try {
    System.out.println(requestId.get());
} finally {
    requestId.remove();
}
// Output: REQ-1
```

Avoid large thread-local values when creating many virtual threads. Explicit context passing is often clearer.

## 5) Pinning and Blocking

Long blocking operations inside a `synchronized` section or native call can temporarily pin the carrier thread. Keep critical sections short and diagnose pinning before changing working code.

## 6) Choose Virtual Threads When

- tasks spend most time waiting on blocking I/O
- the synchronous thread-per-request style is clearer
- libraries expose blocking APIs
- downstream capacity is separately bounded

Use a CPU-sized executor for sustained CPU-heavy work. Virtual threads increase concurrency, not CPU capacity.
