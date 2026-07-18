# 10 - Parallel Streams

## Beginner Rule

Keep a stream sequential unless measurement shows that parallel execution helps. Parallel streams split work across threads, so operations must be independent and the final reduction must be safe to combine in any grouping.

## 1) Parallel Execution

```java
long sum = LongStream.rangeClosed(1, 1_000_000)
        .parallel()
        .sum();
System.out.println(sum);
// Output: 500000500000
```

Parallel does not automatically mean faster. Splitting, coordination, cache behavior, and workload size determine the result.

## 2) Associative Reduction

```java
int sum = Stream.of(1, 2, 3, 4)
        .parallel()
        .reduce(0, Integer::sum);
System.out.println(sum);
// Output: 10
```

Addition is associative with identity zero. Subtraction is not a valid parallel reduction.

## 3) Avoid Shared Mutation

```java
List<Integer> safe = IntStream.rangeClosed(1, 5)
        .parallel()
        .boxed()
        .toList();
System.out.println(safe);
// Output: [1, 2, 3, 4, 5]
// Do not add from parallel tasks into a shared ArrayList.
```

## 4) Ordering

```java
IntStream.rangeClosed(1, 3)
        .parallel()
        .forEachOrdered(System.out::println);
// Output:
// 1
// 2
// 3
```

Ordering can reduce parallel performance.

## 5) When Parallel Streams Fit

- large in-memory data
- CPU-heavy independent operations
- easily splittable sources such as arrays
- associative, stateless reduction
- measured speedup in a realistic benchmark

Avoid them for blocking I/O, small datasets, request code relying on the shared common pool, ordered stateful work, or pipelines with side effects. Virtual threads are usually clearer for many blocking I/O tasks.
