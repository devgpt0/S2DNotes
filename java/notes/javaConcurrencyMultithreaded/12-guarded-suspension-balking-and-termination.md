# 12 - Guarded Suspension, Balking, and Two-Phase Termination

## 1) Guarded Suspension

An operation waits until a required condition becomes true.

```java
final class OneValueBox<T> {
    private final Lock lock = new ReentrantLock();
    private final Condition available = lock.newCondition();
    private T value;

    void put(T newValue) {
        lock.lock();
        try {
            value = Objects.requireNonNull(newValue);
            available.signalAll();
        } finally {
            lock.unlock();
        }
    }

    T awaitValue() throws InterruptedException {
        lock.lockInterruptibly();
        try {
            while (value == null) {
                available.await();
            }
            return value;
        } finally {
            lock.unlock();
        }
    }
}

OneValueBox<String> box = new OneValueBox<>();
Thread.startVirtualThread(() -> box.put("ready")).join();
System.out.println(box.awaitValue());
// Output: ready
```

Use a loop around `await` and support interruption.

## 2) Balking Pattern

Return immediately when the operation is already running or its precondition is false.

```java
AtomicBoolean started = new AtomicBoolean();
if (started.compareAndSet(false, true)) {
    System.out.println("started once");
}
if (!started.compareAndSet(false, true)) {
    System.out.println("second start rejected");
}
// Output:
// started once
// second start rejected
```

The state check and transition must be atomic.

## 3) Two-Phase Termination

Phase one requests shutdown. Phase two lets the worker clean up and terminate.

```java
Thread worker = Thread.startVirtualThread(() -> {
    try {
        while (!Thread.currentThread().isInterrupted()) {
            Thread.sleep(Duration.ofSeconds(1));
        }
    } catch (InterruptedException exception) {
        Thread.currentThread().interrupt();
    } finally {
        System.out.println("cleanup complete");
    }
});
worker.interrupt();
worker.join();
// Output: cleanup complete
```

## 4) Double-Checked Initialization

Prefer static initialization or an initialization-on-demand holder. If double-checked locking is necessary, the shared reference must be `volatile`.

```java
final class SettingsHolder {
    private SettingsHolder() {}

    private static final class Lazy {
        private static final Map<String, String> VALUE = Map.of("mode", "safe");
    }

    static Map<String, String> settings() {
        return Lazy.VALUE;
    }
}

System.out.println(SettingsHolder.settings().get("mode"));
// Output: safe
```

Class initialization supplies thread-safe lazy publication without explicit locking.
