# 01 - Stream Mental Model and Pipeline

## Start with a Loop

A stream is another way to express a data-processing loop. Instead of manually saying “take the next item,” you describe steps such as filter, transform, and collect. Use whichever version is easier to read.

## 1) Source, Intermediate Operations, Terminal Operation

```java
List<String> names = List.of("Asha", "Ravi", "Anu");
List<String> result = names.stream()                 // source
        .filter(name -> name.startsWith("A"))       // intermediate
        .map(String::toUpperCase)                    // intermediate
        .toList();                                   // terminal
System.out.println(result);
// Output: [ASHA, ANU]
```

Intermediate operations build a lazy pipeline. The terminal operation consumes it.

## 2) Laziness

```java
Stream<String> pipeline = Stream.of("a", "bb", "ccc")
        .filter(value -> {
            System.out.println("checking " + value);
            return value.length() > 1;
        });
System.out.println("pipeline created");
System.out.println(pipeline.count());
// Output:
// pipeline created
// checking a
// checking bb
// checking ccc
// 2
```

No element is processed until `count()` starts traversal.

## 3) Streams Are Single Use

```java
Stream<Integer> numbers = Stream.of(1, 2, 3);
System.out.println(numbers.count());
// Output: 3
// Calling another terminal operation on numbers throws IllegalStateException.
```

Create a new stream from the source for another traversal.

## 4) No Source Mutation

```java
List<Integer> source = new ArrayList<>(List.of(3, 1, 2));
List<Integer> sorted = source.stream().sorted().toList();
System.out.println(source);
System.out.println(sorted);
// Output:
// [3, 1, 2]
// [1, 2, 3]
```

The result of `Stream.toList()` is unmodifiable.

## 5) Pipeline Design

- filter early when it reduces work
- keep lambdas small and side-effect free
- name complex domain predicates and transformations
- finish with a result-producing terminal operation
