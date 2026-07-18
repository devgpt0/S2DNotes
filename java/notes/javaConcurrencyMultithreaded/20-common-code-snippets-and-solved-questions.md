# 20 - Common Concurrency Code Questions with Solutions

## 1) Thread-Safe Counter

```java
LongAdder counter = new LongAdder();
try (ExecutorService executor = Executors.newFixedThreadPool(4)) {
    List<Callable<Void>> tasks = IntStream.range(0, 1_000)
            .mapToObj(index -> (Callable<Void>) () -> { counter.increment(); return null; })
            .toList();
    for (Future<Void> future : executor.invokeAll(tasks)) future.get();
}
System.out.println(counter.sum());
// Output: 1000
```

`LongAdder` scales under contention for statistics but is not appropriate for a linearizable sequence ID.

## 2) Bounded Producer-Consumer

```java
BlockingQueue<String> queue = new ArrayBlockingQueue<>(2);
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<?> producer = executor.submit(() -> {
        queue.put("A"); queue.put("B"); return null;
    });
    Future<List<String>> consumer = executor.submit(() -> List.of(queue.take(), queue.take()));
    producer.get();
    System.out.println(consumer.get());
}
// Output: [A, B]
```

The bounded queue limits retained work and blocks the producer when full.

## 3) Combine Independent CompletableFutures

```java
CompletableFuture<Integer> price = CompletableFuture.completedFuture(100);
CompletableFuture<Integer> tax = CompletableFuture.completedFuture(18);
CompletableFuture<Integer> total = price.thenCombine(tax, Integer::sum)
        .orTimeout(1, TimeUnit.SECONDS);
System.out.println(total.join());
// Output: 118
```

Use `thenCompose` for dependent asynchronous operations and `thenCombine` for independent results.

## 4) Safe Account Transfer with Lock Ordering

```java
final class Account {
    final long id;
    long balance;
    Account(long id, long balance) { this.id = id; this.balance = balance; }
}
static void transfer(Account from, Account to, long amount) {
    Account first = from.id < to.id ? from : to;
    Account second = from.id < to.id ? to : from;
    synchronized (first) {
        synchronized (second) {
            if (amount <= 0 || from.balance < amount) throw new IllegalArgumentException("invalid transfer");
            from.balance -= amount;
            to.balance += amount;
        }
    }
}
Account from = new Account(1, 100);
Account to = new Account(2, 0);
transfer(from, to, 40);
System.out.println(from.balance + ", " + to.balance);
// Output: 60, 40
```

A stable unique lock order prevents cyclic lock acquisition. Real money transfer belongs in a database transaction.

## 5) Graceful Executor Shutdown

```java
ExecutorService executor = Executors.newSingleThreadExecutor();
executor.submit(() -> System.out.println("task complete"));
executor.shutdown();
if (!executor.awaitTermination(1, TimeUnit.SECONDS)) executor.shutdownNow();
// Output: task complete
```

Preserve interruption if the surrounding method catches `InterruptedException`.

## 6) Virtual Threads with Downstream Limit

```java
Semaphore permits = new Semaphore(2);
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<Integer>> futures = IntStream.rangeClosed(1, 4)
            .mapToObj(value -> executor.submit(() -> {
                permits.acquire();
                try { return value * value; }
                finally { permits.release(); }
            })).toList();
    for (Future<Integer> future : futures) System.out.println(future.get());
}
// Output in submission retrieval order:
// 1
// 4
// 9
// 16
```

Virtual threads are cheap; database connections and remote concurrency are not.

## 7) One-Time Coordination with CountDownLatch

```java
CountDownLatch ready = new CountDownLatch(2);
Thread.startVirtualThread(ready::countDown);
Thread.startVirtualThread(ready::countDown);
System.out.println(ready.await(1, TimeUnit.SECONDS));
// Output: true
```

## Most-Asked Concurrency Questions

1. Process vs thread? Isolated program resources vs execution path sharing process memory.
2. Concurrency vs parallelism? Overlapping progress vs simultaneous execution.
3. Race condition? Result depends on unsafe interleaving of shared mutable access.
4. `volatile`? Visibility/order for one variable, not atomic compound updates.
5. synchronized? Mutual exclusion plus happens-before visibility using an intrinsic monitor.
6. Atomic vs lock? CAS-based small state transition vs protected multi-step invariant.
7. wait vs sleep? Wait releases owned monitor and requires it; sleep pauses without releasing locks.
8. notify vs notifyAll? Wake one arbitrary waiter vs all; guarded loops remain required.
9. Deadlock conditions? Mutual exclusion, hold-and-wait, no preemption, circular wait.
10. Executor queue risk? Unbounded queue converts overload into memory/latency failure.
11. Callable vs Runnable? Value/checked failure vs no result.
12. Future vs CompletableFuture? Blocking result handle vs composable completion stages.
13. Virtual thread benefit? Scales blocking I/O concurrency, not CPU throughput.
14. ThreadLocal risk? Hidden context and leaks in pooled threads; large values costly at scale.
15. ConcurrentHashMap compound action? Use atomic APIs such as compute/merge, not check-then-put.
16. Starvation vs livelock? Never receives resource vs active reactions without progress.
17. ForkJoinPool use? CPU-bound recursive decomposition/work stealing, not blocking I/O.
18. How diagnose? Thread dumps, JFR, pool/queue/lock/downstream metrics.
