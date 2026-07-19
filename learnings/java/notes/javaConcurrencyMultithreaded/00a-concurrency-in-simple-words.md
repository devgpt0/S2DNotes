# Java Concurrency in Simple Words

Read this before threads, locks, atomics, executors, futures, and virtual threads.

## The Main Idea

Concurrency means more than one task can make progress during the same period.

Examples include serving many users, waiting for network responses, and processing independent jobs.

## Concurrency vs Parallelism

- **concurrency:** tasks overlap in time
- **parallelism:** tasks run at the same moment on different CPU capacity

A program can be concurrent on one core by switching between tasks.

## First Thread Example

```java
Thread worker = new Thread(() ->
        System.out.println("Worker: " + Thread.currentThread().getName()));

worker.start();
worker.join();
System.out.println("Main finished");
// Output order:
// Worker: Thread-0
// Main finished
```

- `start()` asks the JVM to run the task on the new thread
- `join()` waits for that thread to finish
- calling `run()` directly would not start a new thread

The generated thread name can vary. The ordering after `join()` does not.

## The Real Difficulty: Shared Changing Data

```java
count++;
```

This looks like one action, but it reads, adds, and writes. Two threads can read the same old value and lose one update. That is a **race condition**.

The simplest safe design is often not to share changing data. Give one task ownership or return immutable results.

## What `synchronized` Does

```java
synchronized void increment() {
    count++;
}
```

For the same object monitor, one thread enters at a time. Synchronization also makes protected writes visible to later protected reads.

Do not add `synchronized` randomly. Define which state the lock protects and keep all access under the same rule.

## Use Tasks and Executors

Application code usually submits tasks instead of repeatedly creating raw platform threads:

```java
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    Future<String> result = executor.submit(() -> "Java");
    System.out.println(result.get());
}
// Output: Java
```

- **task:** work to perform
- **executor:** component that runs tasks
- **future:** handle for a later result

Virtual threads make thread-per-blocking-task practical at large scale. They do not make CPU work faster and do not remove data races.

## Cancellation Is Cooperation

Interrupting a thread is a request, not a forced kill. Blocking methods may throw `InterruptedException`. Code should finish cleanup and preserve the interruption when it cannot fully handle it.

## Timeouts and Bounds

Every wait needs a deliberate limit. Every queue needs a capacity or a reason it is safe without one. Otherwise a slow dependency can consume all threads or memory.

- **timeout:** stop waiting after a limit
- **backpressure:** slow or reject new work when capacity is full
- **deadlock:** tasks wait forever for one another
- **starvation:** a task rarely gets the resource it needs

## `volatile` Is Not a General Lock

`volatile` helps threads see the latest write to one field and provides ordering. It does not make `count++` atomic.

Use it for simple state publication or flags only when the complete algorithm fits its guarantees.

## Beginner to Expert Path

1. **Beginner:** start, join, and interrupt one task.
2. **Developer:** use executors, futures, timeouts, and safe ownership.
3. **Senior:** design bounded systems and diagnose races, deadlocks, and starvation.
4. **Expert:** reason with the Java Memory Model, contention, structured lifetimes, and measured workload behavior.

## First Design Questions

Before using a concurrency tool, ask:

1. Is the work CPU-bound or mostly waiting?
2. What state is shared and who owns it?
3. How is work cancelled?
4. What is the timeout?
5. What happens when capacity is full?
6. How will we observe stuck or slow work?
