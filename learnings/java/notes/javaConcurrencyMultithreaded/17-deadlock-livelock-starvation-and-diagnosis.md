# 17 - Deadlock, Livelock, Starvation, and Diagnosis

## 1) Deadlock

Deadlock can occur when tasks hold resources while waiting cyclically for one another.

Prevent it with:

- a global lock ordering
- one lock instead of several when practical
- timed or interruptible acquisition
- no remote or blocking calls while holding locks
- immutable ownership-based design

```java
Object first = new Object();
Object second = new Object();
List<Object> ordered = Stream.of(first, second)
        .sorted(Comparator.comparingInt(System::identityHashCode))
        .toList();
synchronized (ordered.get(0)) {
    synchronized (ordered.get(1)) {
        System.out.println("locks acquired in stable order");
    }
}
// Output: locks acquired in stable order
// Production code needs a unique tie-breaker if identity hash codes are equal.
```

## 2) Livelock

Threads are active but repeatedly react to each other without progress, such as both continually backing off and retrying in sync. Add randomized jitter, ownership, or an ordering rule.

## 3) Starvation

A task waits indefinitely because others continually receive the resource. Causes include unfair locking, priority misuse, saturated pools, long tasks in a shared executor, and a hot partition.

## 4) Race Condition

The result depends on timing of unsynchronized operations.

```java
AtomicInteger seats = new AtomicInteger(1);
boolean booked = seats.getAndUpdate(current -> current > 0 ? current - 1 : current) > 0;
System.out.println(booked);
System.out.println(seats.get());
// Output:
// true
// 0
```

Real booking also needs an atomic database constraint or transaction across all relevant state.

## 5) Thread Dumps

A thread dump shows thread states, stacks, held monitors, and detected monitor deadlocks. Capture several dumps seconds apart to distinguish a transient wait from a stuck system.

Useful evidence:

- Java Flight Recorder events
- executor active count and queue depth
- blocked/waited time
- virtual-thread pinning events
- CPU profiles and allocation profiles
- downstream connection-pool saturation

## 6) Operational Rules

- name platform threads and executors
- propagate correlation context explicitly
- record task latency, failures, rejections, and cancellations
- alert on sustained saturation, not a single spike
- never log secrets or entire task payloads
