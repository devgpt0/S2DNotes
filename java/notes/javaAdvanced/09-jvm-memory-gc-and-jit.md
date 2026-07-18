# 09 - JVM, Memory, Garbage Collection, and JIT

## 1) Runtime Memory Model

- Heap stores objects and arrays.
- Each thread has stack frames for calls and local variables.
- Metaspace stores class metadata.
- Native memory is also used by threads, buffers, code cache, and the JVM itself.

```java
Object object = new Object();
int identity = System.identityHashCode(object);
System.out.println(identity == System.identityHashCode(object));
// Output: true
// The numeric identity value is JVM-run dependent.
```

Java references are not raw memory addresses.

## 2) Reachability and Garbage Collection

An object becomes eligible for collection when it is no longer strongly reachable. Eligibility does not guarantee immediate collection.

```java
Object value = new Object();
value = null;
System.out.println(value);
// Output: null
// The former object is eligible for collection; collection timing is unspecified.
```

Never use finalization for resource management. Use try-with-resources.

## 3) Common Memory Leaks

- unbounded static collections
- caches without eviction
- listeners that are never removed
- `ThreadLocal` values not cleared in pooled threads
- retaining a small view backed by a large object

```java
Map<String, byte[]> cache = new HashMap<>();
cache.put("report", new byte[1024]);
System.out.println(cache.size());
cache.clear();
// Output: 1
```

## 4) JIT Compilation

The JVM interprets and profiles code, then compiles hot paths. This is why realistic benchmarks need warm-up and a framework such as JMH.

```java
long sum = 0;
for (int i = 0; i < 1_000; i++) {
    sum += i;
}
System.out.println(sum);
// Output: 499500
// This loop is not a valid microbenchmark.
```

## 5) Production Diagnosis

- Inspect GC logs and allocation rate before tuning.
- Capture a heap dump for retained-object analysis.
- Use Java Flight Recorder for low-overhead runtime evidence.
- Set container-aware heap limits and leave room for non-heap memory.
- Choose a collector based on measured latency and throughput requirements.
