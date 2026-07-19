# 11 - Debugging, Errors, and Performance

## 1) Exceptions in Lambdas

Do not hide checked failures inside a broad wrapper. Handle them at the boundary that understands recovery.

```java
static int parseStrict(String value) {
    if (!value.matches("-?\\d+")) {
        throw new IllegalArgumentException("not an integer: " + value);
    }
    return Integer.parseInt(value);
}

System.out.println(Stream.of("10", "20").mapToInt(value -> parseStrict(value)).sum());
// Output: 30
```

## 2) Diagnose with Named Functions

```java
static boolean isLongWord(String value) {
    return value.length() >= 5;
}

System.out.println(Stream.of("Java", "Spring").filter(value -> isLongWord(value)).toList());
// Output: [Spring]
```

Named logic is easier to test and read than a large inline lambda.

## 3) Common Bugs

```java
Stream<String> stream = Stream.of("A", "B");
System.out.println(stream.findFirst().orElse("none"));
// Output: A
// Reusing stream now throws IllegalStateException.
```

Other common bugs:

- modifying the source during traversal
- relying on `HashSet` or `HashMap` iteration order
- using `peek` for required mutation
- forgetting a merge function in `toMap`
- assuming `findAny` returns the first element
- returning a lazy stream backed by an already closed resource

## 4) Performance

```java
int sum = IntStream.rangeClosed(1, 1000)
        .filter(value -> value % 2 == 0)
        .sum();
System.out.println(sum);
// Output: 250500
```

- primitive streams avoid boxing
- filter early when selectivity is high
- avoid repeated sorting and unnecessary materialization
- move filtering and aggregation to the database when appropriate
- use JMH for microbenchmarks
- choose readability unless measurements prove a bottleneck
