# 03 - Java Memory Model

The Java Memory Model defines when writes by one thread become visible to another and which reorderings are legal.

## Start with the Problem

Two threads may use different CPU caches and run instructions in optimized orders. Without a rule such as a lock, volatile access, thread start/join, or concurrent collection handoff, one thread is not guaranteed to observe another thread's latest write.

“Happens-before” does not mean wall-clock time. It is a Java guarantee that earlier work becomes visible to later work.

## 1) Atomicity, Visibility, and Ordering

- Atomicity: an operation appears indivisible.
- Visibility: one thread observes another thread's writes.
- Ordering: operations appear in an order allowed by happens-before rules.

`count++` is a read, calculation, and write; it is not atomic.

## 2) Happens-Before

Important happens-before relationships include:

- actions before `Thread.start()` are visible to the started thread
- thread actions are visible after a successful `join()`
- unlocking a monitor happens-before a later lock of that monitor
- a volatile write happens-before a later read of that variable
- completion of a task happens-before `Future.get()` returns its result

```java
int[] value = {0};
Thread worker = Thread.ofPlatform().start(() -> value[0] = 42);
worker.join();
System.out.println(value[0]);
// Output: 42
// join establishes visibility of the worker's write.
```

## 3) `volatile`

```java
final class StopSignal {
    private volatile boolean stopped;

    void stop() {
        stopped = true;
    }

    boolean isStopped() {
        return stopped;
    }
}

StopSignal signal = new StopSignal();
signal.stop();
System.out.println(signal.isStopped());
// Output: true
```

`volatile` provides visibility and ordering for that variable. It does not make compound operations such as increment atomic.

## 4) Safe Publication

Safe publication mechanisms include final fields after correct construction, static initialization, volatile references, locks, concurrent collections, and handoff through a queue.

```java
final class Configuration {
    private final String endpoint;

    Configuration(String endpoint) {
        this.endpoint = Objects.requireNonNull(endpoint);
    }

    String endpoint() {
        return endpoint;
    }
}

System.out.println(new Configuration("https://example.com").endpoint());
// Output: https://example.com
```

Do not allow `this` to escape from a constructor before final fields are established.

## 5) Data Races

A data race exists when threads access the same mutable location concurrently, at least one access is a write, and no happens-before ordering exists. Data-race-free programs have far more predictable behavior.
