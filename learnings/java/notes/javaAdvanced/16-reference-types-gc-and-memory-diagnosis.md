# 16 - Reference Types, GC, and Memory Diagnosis

## Read This After Basic GC

Normal Java variables use strong references. Weak, soft, and phantom references are specialized tools for infrastructure. They are not required for ordinary domain objects and should not be used as a first attempt at cache design.

## Reference Strength

- strong: ordinary reference; prevents collection
- soft: may survive until memory pressure; unsuitable for predictable caches
- weak: cleared when only weakly reachable
- phantom: post-mortem notification with `ReferenceQueue`; referent is never returned

```java
Object value = new Object();
WeakReference<Object> reference = new WeakReference<>(value);
System.out.println(reference.get() == value);
value = null;
// Output: true
// Later clearing is GC-dependent and must not be asserted by timing.
```

## Collector Concepts

- Serial: simple single-threaded collector for small heaps
- Parallel: throughput-oriented parallel collector
- G1: balanced regional collector and common general-purpose default
- ZGC: low-pause concurrent collector for latency-sensitive large heaps

Collector availability and behavior depend on the JDK. Choose from measured latency, throughput, heap, allocation rate, and operational constraints.

## Memory Failure Types

- Java heap space: retained/allocated heap exceeds capacity
- GC overhead: excessive collection with little recovery
- Metaspace: excessive class metadata/class-loader retention
- Direct buffer memory: off-heap buffer limit pressure
- unable to create native thread: OS/native memory or thread limit

## Diagnosis Workflow

1. Confirm symptom and time window from metrics.
2. Inspect allocation rate, live-set growth, GC pause, and native memory.
3. Capture Java Flight Recorder evidence.
4. Capture a heap dump near failure if safe.
5. Find dominators and paths to GC roots.
6. Fix ownership/retention before increasing memory blindly.

```java
MemoryMXBean memory = ManagementFactory.getMemoryMXBean();
System.out.println(memory.getHeapMemoryUsage().getUsed() >= 0);
// Output: true
// Exact byte count depends on the running JVM.
```
