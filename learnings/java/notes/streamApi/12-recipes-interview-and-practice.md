# 12 - Recipes, Interview Questions, and Practice

## 1) Frequency Map

```java
Map<String, Long> frequency = Stream.of("java", "spring", "java")
        .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
System.out.println(frequency);
// Output: {spring=1, java=2}
// HashMap key display order is not guaranteed.
```

## 2) Highest Value per Group

```java
record Sale(String region, int amount) {}

Map<String, Sale> highest = Stream.of(
        new Sale("N", 10), new Sale("N", 30), new Sale("S", 20))
        .collect(Collectors.toMap(
                Sale::region,
                Function.identity(),
                BinaryOperator.maxBy(Comparator.comparingInt(Sale::amount))));
System.out.println(highest.get("N"));
// Output: Sale[region=N, amount=30]
```

## 3) Null-Free Boundary

```java
List<String> cleaned = Stream.of("A", null, "B")
        .filter(Objects::nonNull)
        .toList();
System.out.println(cleaned);
// Output: [A, B]
```

Prefer rejecting invalid nulls at the input boundary when null is not part of the schema.

## 4) Interview Quick Answers

- Streams are lazy, single-use pipeline descriptions.
- Intermediate operations return a stream; terminal operations consume it.
- `map` is one-to-one; `flatMap` flattens zero-to-many results.
- `reduce` combines immutable values; `collect` performs mutable reduction.
- `Stream.toList()` returns an unmodifiable list.
- Stateful operations may need to buffer elements.
- Parallel reductions require associative, stateless operations.
- `findFirst` respects encounter order; `findAny` may enable more parallel freedom.

## 5) Practice Tasks

1. Group employees by department and calculate average salary.
2. Flatten orders into line items and total exact `BigDecimal` prices.
3. Build a duplicate-safe map with an explicit merge policy.
4. Find the three longest unique words without mutating the source.
5. Compare a readable loop and stream solution for the same validation task.
6. Benchmark a sequential and parallel CPU-bound pipeline using JMH.

## 6) Final Checklist

- source ownership and closing behavior are clear
- lambdas are stateless and non-interfering
- ordering assumptions are explicit
- duplicate and empty-result behavior is defined
- numeric types preserve required precision
- parallel execution is used only after measurement
