# 09 - Primitive Streams and Numeric Work

Primitive streams avoid boxing for common numeric pipelines.

## 1) `IntStream`, `LongStream`, and `DoubleStream`

```java
int totalLength = Stream.of("Java", "Spring")
        .mapToInt(String::length)
        .sum();
System.out.println(totalLength);
// Output: 10
```

## 2) Numeric Operations

```java
IntStream values = IntStream.of(10, 20, 30);
IntSummaryStatistics statistics = values.summaryStatistics();
System.out.println(statistics.getAverage());
// Output: 20.0
```

The stream is consumed after `summaryStatistics()`.

## 3) Boxing and Unboxing

```java
List<Integer> squares = IntStream.rangeClosed(1, 4)
        .map(value -> value * value)
        .boxed()
        .toList();
System.out.println(squares);
// Output: [1, 4, 9, 16]
```

Use `boxed()` only when an object stream or collection is required.

## 4) Empty Results

```java
OptionalDouble average = IntStream.empty().average();
System.out.println(average.isEmpty());
// Output: true
```

`average`, `min`, and `max` return optionals because an empty stream has no value.

## 5) Numeric Correctness

```java
BigDecimal total = Stream.of("10.25", "20.75")
        .map(BigDecimal::new)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
System.out.println(total);
// Output: 31.00
```

Use `BigDecimal` for exact decimal money calculations. Construct it from strings or exact integer minor units, not binary floating-point values.
