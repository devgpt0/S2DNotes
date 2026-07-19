# 15 - Read/Write, Copy-on-Write, Cache, and Thread-Local Patterns

## 1) Read-Write Lock Pattern

Many readers may proceed together; writers are exclusive.

```java
final class ReadMostlyValue {
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    private String value = "initial";

    String read() {
        lock.readLock().lock();
        try {
            return value;
        } finally {
            lock.readLock().unlock();
        }
    }

    void write(String newValue) {
        lock.writeLock().lock();
        try {
            value = Objects.requireNonNull(newValue);
        } finally {
            lock.writeLock().unlock();
        }
    }
}

ReadMostlyValue value = new ReadMostlyValue();
value.write("updated");
System.out.println(value.read());
// Output: updated
```

Read-write locks help only with sufficient read contention and non-trivial protected work. Measure against a simple lock.

## 2) Copy-on-Write Pattern

```java
CopyOnWriteArrayList<String> listeners = new CopyOnWriteArrayList<>();
listeners.add("audit");
for (String listener : listeners) {
    listeners.addIfAbsent("metrics");
    System.out.println(listener);
}
System.out.println(listeners);
// Output:
// audit
// [audit, metrics]
```

Iteration sees a stable snapshot. Writes copy the array, so this fits small, read-heavy collections.

## 3) Memoization / Concurrent Cache Pattern

```java
ConcurrentHashMap<String, Integer> lengths = new ConcurrentHashMap<>();
System.out.println(lengths.computeIfAbsent("Java", String::length));
System.out.println(lengths.computeIfAbsent("Java", String::length));
// Output:
// 4
// 4
```

The mapping function must be short, deterministic, and must not recursively modify the same map. Production caches also need bounds, expiry, invalidation, and failure policy.

## 4) Thread-Local Storage Pattern

```java
ThreadLocal<String> context = ThreadLocal.withInitial(() -> "none");
context.set("REQ-10");
try {
    System.out.println(context.get());
} finally {
    context.remove();
}
// Output: REQ-10
```

Always remove values in pooled platform threads. Do not use thread-local state to hide required business dependencies.

## 5) Stamped Optimistic Read

`StampedLock` supports optimistic reads, but it is not reentrant and requires careful validation. Use it only after evidence shows a normal lock is insufficient.

```java
StampedLock lock = new StampedLock();
long stamp = lock.tryOptimisticRead();
System.out.println(lock.validate(stamp));
// Output: true when no writer acquired the lock after the stamp.
```
