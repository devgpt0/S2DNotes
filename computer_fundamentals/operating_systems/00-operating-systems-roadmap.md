# Operating Systems Roadmap

This track explains how one machine isolates, schedules, coordinates, and performs I/O for many programs.

1. [Processes, threads, scheduling, context switches, and signals](01-processes-threads-scheduling-and-signals.md)
2. [Locks, mutexes, semaphores, spinlocks, and deadlocks](02-synchronization-locks-and-deadlocks.md)
3. [Allocation, paging, virtual memory, and memory-mapped files](03-memory-allocation-paging-and-mmap.md)
4. [epoll, io_uring, and scalable I/O](04-epoll-io-uring-and-scalable-io.md)

## Learning Flow

```text
isolated process -> scheduled thread -> shared-state coordination -> virtual memory -> event-driven I/O
```

## Mastery Outcome

You can choose a process/thread model, explain context-switch and lock costs, diagnose deadlocks, distinguish virtual from physical memory, and choose an appropriate I/O readiness or completion model.

[Return to Computer Fundamentals](../README.md)

