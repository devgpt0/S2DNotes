# 04 - Stateful and Short-Circuit Operations

## 1) `distinct`

```java
System.out.println(Stream.of("A", "B", "A").distinct().toList());
// Output: [A, B]
```

`distinct` relies on `equals` and `hashCode` for ordered streams.

## 2) `sorted`

```java
List<String> sorted = Stream.of("pear", "fig", "apple")
        .sorted(Comparator.comparingInt(String::length).thenComparing(String::compareTo))
        .toList();
System.out.println(sorted);
// Output: [fig, pear, apple]
```

Comparators must be consistent and transitive.

## 3) `limit` and `skip`

```java
System.out.println(IntStream.rangeClosed(1, 10).skip(3).limit(4).boxed().toList());
// Output: [4, 5, 6, 7]
```

Use stable ordering when these operations represent pagination. Database pagination should happen in the database, not after loading every row.

## 4) `takeWhile` and `dropWhile`

```java
List<Integer> values = List.of(2, 4, 6, 3, 8);
System.out.println(values.stream().takeWhile(value -> value % 2 == 0).toList());
System.out.println(values.stream().dropWhile(value -> value % 2 == 0).toList());
// Output:
// [2, 4, 6]
// [3, 8]
```

These operate on the longest matching prefix, not all matching elements.

## 5) Short-Circuiting

```java
boolean found = Stream.of("A", "BB", "CCC")
        .anyMatch(value -> value.length() == 2);
System.out.println(found);
// Output: true
```

`anyMatch`, `allMatch`, `noneMatch`, `findFirst`, `findAny`, `limit`, and some `takeWhile` pipelines can finish without processing all elements.
