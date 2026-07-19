# Java Streams in Simple Words

Read this before the detailed Stream API chapters.

## The Main Idea

A stream describes a series of steps for processing values.

```java
List<String> names = List.of("Asha", "", "Ravi");

List<String> result = names.stream()
        .filter(name -> !name.isBlank())
        .map(String::toUpperCase)
        .toList();

System.out.println(result);
// Output: [ASHA, RAVI]
```

Read it like a sentence: take the names, keep the non-blank ones, make them uppercase, and collect them into a list.

## Why Not Always Use a Loop?

A loop explains **how** to move through values. A stream can explain **what result** you want.

Use whichever form is clearer. Streams do not replace every loop.

Equivalent loop:

```java
List<String> result = new ArrayList<>();
for (String name : names) {
    if (!name.isBlank()) {
        result.add(name.toUpperCase());
    }
}
System.out.println(result);
// Output: [ASHA, RAVI]
```

## Three Parts of a Stream

```java
names.stream()                 // source
        .filter(...)           // intermediate operation
        .toList();             // terminal operation
```

- **source:** where values come from
- **intermediate operation:** describes one processing step
- **terminal operation:** asks for a result and starts the work

Without a terminal operation, the pipeline normally does not process values.

## The Most Useful Operations

### `filter`: Keep Some Values

```java
List<Integer> even = List.of(1, 2, 3, 4).stream()
        .filter(number -> number % 2 == 0)
        .toList();
System.out.println(even);
// Output: [2, 4]
```

### `map`: Change Each Value

```java
List<Integer> lengths = List.of("Java", "SQL").stream()
        .map(String::length)
        .toList();
System.out.println(lengths);
// Output: [4, 3]
```

### `flatMap`: Turn Nested Values into One Flow

```java
List<List<String>> groups = List.of(List.of("A", "B"), List.of("C"));
List<String> letters = groups.stream().flatMap(List::stream).toList();
System.out.println(letters);
// Output: [A, B, C]
```

### `reduce`: Combine Many Values into One

```java
int total = List.of(10, 20, 30).stream().reduce(0, Integer::sum);
System.out.println(total);
// Output: 60
```

## Streams Do Not Store Data

A collection owns values. A stream is a one-use view of processing work.

```java
Stream<String> stream = names.stream();
System.out.println(stream.count());
// stream.count(); // IllegalStateException: stream already used
```

Create a new stream when you need another pipeline.

## Avoid Hidden Side Effects

Prefer:

```java
List<String> cleaned = names.stream().map(String::trim).toList();
```

Avoid mutating an outside list from inside the pipeline. Returning results makes the code easier to test and safer to parallelize.

## `Optional` in One Sentence

An `Optional<T>` says a result may contain one `T` or may be empty.

```java
Optional<String> first = names.stream().filter(name -> !name.isBlank()).findFirst();
System.out.println(first.orElse("No name"));
// Output: Asha
```

## Parallel Is Not Automatically Faster

Parallel streams split work across threads. Coordination has a cost and side effects become dangerous.

Use them only after measuring a large, CPU-heavy, independent operation. Do not use them to make blocking database or HTTP work “faster.”

## Beginner to Expert Path

1. **Beginner:** `filter`, `map`, and `toList` with printed output.
2. **Developer:** reductions, collectors, `Optional`, and side-effect-free pipelines.
3. **Senior:** laziness, ordering, short-circuiting, and readable stream design.
4. **Expert:** collector contracts, splitting, parallel cost, memory, and measurement.

## Quick Check

```java
long count = List.of("Java", "", "SQL")
        .stream()
        .filter(text -> !text.isBlank())
        .count();
System.out.println(count);
// Output: 2
```
