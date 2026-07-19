# 05 - Locks, Atomics, and Synchronizers

## Beginner Meaning

A lock is like the single key to a room: only the thread holding the key enters the protected section. An atomic variable performs one small state change safely without a normal lock. A synchronizer coordinates groups of threads for a specific purpose such as waiting or limiting permits.

## 1) `ReentrantLock`

```java
Lock lock = new ReentrantLock();
lock.lock();
try {
    System.out.println("protected");
} finally {
    lock.unlock();
}
// Output: protected
```

Always unlock in `finally`. Use explicit locks when timed, interruptible, fair, or multiple-condition locking is required.

## 2) Timed Lock Acquisition

```java
if (lock.tryLock(100, TimeUnit.MILLISECONDS)) {
    try {
        System.out.println("acquired");
    } finally {
        lock.unlock();
    }
} else {
    System.out.println("timed out");
}
// Output: acquired or timed out, depending on contention.
```

## 3) Atomic Variables

```java
AtomicInteger counter = new AtomicInteger();
IntStream.range(0, 1_000).parallel().forEach(index -> counter.incrementAndGet());
System.out.println(counter.get());
// Output: 1000
```

Atomics are appropriate for independent state transitions. Multiple related fields usually need a lock or immutable state held in one atomic reference.

## 4) Compare-and-Set

```java
AtomicReference<String> state = new AtomicReference<>("NEW");
System.out.println(state.compareAndSet("NEW", "RUNNING"));
System.out.println(state.get());
// Output:
// true
// RUNNING
```

CAS succeeds only when the current value equals the expected value.

## 5) Synchronizers

```java
CountDownLatch ready = new CountDownLatch(2);
ready.countDown();
ready.countDown();
System.out.println(ready.await(1, TimeUnit.SECONDS));
// Output: true
```

- `CountDownLatch`: one-time gate
- `CyclicBarrier`: reusable meeting point for a fixed party count
- `Phaser`: flexible multi-phase coordination
- `Semaphore`: limit concurrent permits
- `Exchanger`: pairwise data exchange

```java
Semaphore permits = new Semaphore(2);
permits.acquire();
try {
    System.out.println(permits.availablePermits());
} finally {
    permits.release();
}
// Output: 1
```
