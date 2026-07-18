# 02 - Threads, Lifecycle, and Interruption

## 1) Platform Thread

```java
Thread worker = Thread.ofPlatform().name("worker-1").start(
        () -> System.out.println(Thread.currentThread().getName()));
worker.join();
// Output: worker-1
```

Prefer task executors over manually creating many platform threads.

## 2) Thread States

Java exposes `NEW`, `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, and `TERMINATED`.

```java
Thread thread = Thread.ofPlatform().unstarted(() -> {});
System.out.println(thread.getState());
thread.start();
thread.join();
System.out.println(thread.getState());
// Output:
// NEW
// TERMINATED
```

`RUNNABLE` covers both ready-to-run and executing states at the Java level.

## 3) Joining with a Deadline

```java
Thread thread = Thread.ofPlatform().start(() -> {});
thread.join(Duration.ofSeconds(1));
System.out.println(thread.isAlive());
// Output: false
```

Never wait forever when the surrounding operation has a deadline.

## 4) Interruption Is Cooperative Cancellation

```java
Thread worker = Thread.ofPlatform().start(() -> {
    try {
        Thread.sleep(Duration.ofSeconds(10));
    } catch (InterruptedException exception) {
        Thread.currentThread().interrupt();
        System.out.println("cancelled");
    }
});
worker.interrupt();
worker.join();
// Output: cancelled
```

Blocking methods commonly clear the interrupt flag when throwing `InterruptedException`; restore it when the current method cannot rethrow.

## 5) Uncaught Failures

```java
Thread thread = Thread.ofPlatform()
        .uncaughtExceptionHandler((failedThread, error) ->
                System.out.println(failedThread.getName() + ": " + error.getMessage()))
        .name("worker")
        .start(() -> { throw new IllegalStateException("failed"); });
thread.join();
// Output: worker: failed
```

Executor task failures are normally captured by `Future`; inspect or propagate them.

## 6) Deprecated Thread Control

Never use `Thread.stop`, `suspend`, or `resume`. They can leave shared state inconsistent or locks permanently held.
