# 04 - Synchronization and Monitors

## 1) Intrinsic Lock

Every Java object can act as a monitor lock.

```java
final class Counter {
    private int value;

    synchronized void increment() {
        value++;
    }

    synchronized int value() {
        return value;
    }
}

Counter counter = new Counter();
try (ExecutorService executor = Executors.newFixedThreadPool(4)) {
    List<Callable<Void>> tasks = IntStream.range(0, 1_000)
            .mapToObj(index -> (Callable<Void>) () -> { counter.increment(); return null; })
            .toList();
    for (Future<Void> future : executor.invokeAll(tasks)) {
        future.get();
    }
}
System.out.println(counter.value());
// Output: 1000
```

The same lock must protect every access participating in the invariant.

## 2) Synchronized Block

```java
final class Account {
    private final Object lock = new Object();
    private long balance;

    void deposit(long amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("amount must be positive");
        }
        synchronized (lock) {
            balance += amount;
        }
    }

    long balance() {
        synchronized (lock) {
            return balance;
        }
    }
}

Account account = new Account();
account.deposit(100);
System.out.println(account.balance());
// Output: 100
```

A private lock prevents external code from participating accidentally.

## 3) Monitor Object Pattern

The object owns its lock, state, and operations. Callers cannot manipulate state without acquiring the monitor. The `Account` above is a monitor object.

## 4) `wait`, `notify`, and `notifyAll`

```java
synchronized (lock) {
    while (!conditionIsTrue()) {
        lock.wait();
    }
    useProtectedState();
    // Result: state is used only after the guarded condition becomes true.
}
```

Always wait in a loop because wakeups may be spurious and another thread may consume the condition first. Prefer `BlockingQueue`, `CountDownLatch`, `Semaphore`, or `Condition` when they express the requirement directly.

## 5) Lock Scope

Keep critical sections small, but do not split an invariant across separate lock acquisitions. Never perform slow remote I/O while holding a lock.
