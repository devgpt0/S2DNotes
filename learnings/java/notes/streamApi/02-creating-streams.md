# 02 - Creating Streams

## 1) Collections and Arrays

```java
System.out.println(List.of("Java", "Spring").stream().count());
System.out.println(Arrays.stream(new int[] {2, 4, 6}).sum());
// Output:
// 2
// 12
```

## 2) Values and Nullable Values

```java
System.out.println(Stream.of("A", "B").toList());
System.out.println(Stream.ofNullable(null).count());
// Output:
// [A, B]
// 0
```

Do not use `Stream.of(nullableValue)` when `null` should mean no element; it creates one null element.

## 3) Ranges

```java
System.out.println(IntStream.range(1, 5).boxed().toList());
System.out.println(IntStream.rangeClosed(1, 5).sum());
// Output:
// [1, 2, 3, 4]
// 15
```

## 4) Infinite Streams

```java
List<Integer> powers = Stream.iterate(1, value -> value * 2)
        .limit(5)
        .toList();
System.out.println(powers);
// Output: [1, 2, 4, 8, 16]
```

Always bound an infinite stream before a terminal operation that needs completion.

```java
List<Integer> sequence = Stream.iterate(1, value -> value <= 5, value -> value + 1)
        .toList();
System.out.println(sequence);
// Output: [1, 2, 3, 4, 5]
```

## 5) Files

```java
Path file = Files.createTempFile("stream-", ".txt");
Files.write(file, List.of("one", "two"));
try (Stream<String> lines = Files.lines(file)) {
    System.out.println(lines.count());
}
Files.delete(file);
// Output: 2
```

Close streams backed by I/O resources.

## 6) Builders

```java
Stream.Builder<String> builder = Stream.builder();
builder.add("A").add("B");
System.out.println(builder.build().toList());
// Output: [A, B]
```

Once built, a builder cannot be reused.
