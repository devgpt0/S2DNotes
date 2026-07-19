# 05 - Terminal Operations and Reduction

## 1) Iteration and Counting

```java
Stream.of("A", "B").forEach(System.out::println);
System.out.println(Stream.of("A", "B").count());
// Output:
// A
// B
// 2
```

Use `forEachOrdered` when encounter order must be preserved in a parallel stream.

## 2) Finding and Matching

```java
Optional<String> first = Stream.of("cat", "horse")
        .filter(value -> value.length() > 3)
        .findFirst();
System.out.println(first.orElse("none"));
// Output: horse
```

## 3) Identity Reduction

```java
int sum = Stream.of(1, 2, 3, 4).reduce(0, Integer::sum);
System.out.println(sum);
// Output: 10
```

The identity must be neutral: `0 + x == x`.

## 4) Reduction Without Identity

```java
Optional<Integer> maximum = Stream.of(4, 9, 2).reduce(Integer::max);
System.out.println(maximum.orElseThrow());
// Output: 9
```

An empty stream has no maximum, so the result is optional.

## 5) Mutable Reduction

Use `collect` rather than `reduce` to build mutable containers.

```java
List<String> upper = Stream.of("a", "b")
        .map(String::toUpperCase)
        .collect(Collectors.toCollection(ArrayList::new));
System.out.println(upper);
// Output: [A, B]
```

## 6) Reduction Laws

For correct parallel execution, the accumulator and combiner must be associative, stateless, non-interfering, and compatible with the identity.
