# 03 - Stateless Intermediate Operations

Stateless operations process each element independently.

## 1) `filter`

```java
List<Integer> even = Stream.of(1, 2, 3, 4)
        .filter(value -> value % 2 == 0)
        .toList();
System.out.println(even);
// Output: [2, 4]
```

## 2) `map`

```java
List<Integer> lengths = Stream.of("Java", "API")
        .map(String::length)
        .toList();
System.out.println(lengths);
// Output: [4, 3]
```

`map` produces exactly one result for each input element.

## 3) `peek`

```java
List<String> values = Stream.of("a", "b")
        .peek(value -> System.out.println("seen=" + value))
        .map(String::toUpperCase)
        .toList();
System.out.println(values);
// Output:
// seen=a
// seen=b
// [A, B]
```

Use `peek` for temporary diagnostics, not business mutation. Some optimized pipelines may elide traversal when the terminal result does not require it.

## 4) `mapMulti`

`mapMulti` can emit zero or more results without creating a stream for every input.

```java
List<Integer> expanded = Stream.of(1, 2, 3)
        .<Integer>mapMulti((value, output) -> {
            output.accept(value);
            if (value % 2 == 0) {
                output.accept(value * 10);
            }
        })
        .toList();
System.out.println(expanded);
// Output: [1, 2, 20, 3]
```

## 5) Good Lambdas

- deterministic for the same input
- do not mutate external collections
- do not perform slow network or database calls
- fit on one readable expression or call a named method
