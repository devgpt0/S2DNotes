# 13 - Common Stream API Snippets and Solved Questions

## 1) Find Duplicate Values

```java
List<Integer> values = List.of(1, 2, 3, 2, 4, 1);
Set<Integer> seen = new HashSet<>();
Set<Integer> duplicates = values.stream()
        .filter(value -> !seen.add(value))
        .collect(Collectors.toCollection(LinkedHashSet::new));
System.out.println(duplicates);
// Output: [2, 1]
```

Interview note: this pipeline has controlled state and must remain sequential. A frequency collector is clearer for parallel use.

## 2) Character Frequency

```java
Map<Integer, Long> frequency = "banana".codePoints()
        .boxed()
        .collect(Collectors.groupingBy(
                Function.identity(),
                LinkedHashMap::new,
                Collectors.counting()));
frequency.forEach((codePoint, count) ->
        System.out.println(Character.toString(codePoint) + "=" + count));
// Output:
// b=1
// a=3
// n=2
```

## 3) Group Employees and Average Salary

```java
record Employee(String department, int salary) {}
List<Employee> employees = List.of(
        new Employee("IT", 100),
        new Employee("IT", 200),
        new Employee("HR", 90));

Map<String, Double> averages = employees.stream()
        .collect(Collectors.groupingBy(
                Employee::department,
                Collectors.averagingInt(Employee::salary)));
System.out.println(averages);
// Output: {HR=90.0, IT=150.0} (HashMap display order is not guaranteed).
```

## 4) Flatten Nested Lists

```java
List<List<String>> nested = List.of(List.of("A", "B"), List.of("C"));
List<String> flat = nested.stream().flatMap(Collection::stream).toList();
System.out.println(flat);
// Output: [A, B, C]
```

`flatMap` maps each list to a stream and joins them into one stream.

## 5) Top Three Distinct Numbers

```java
List<Integer> topThree = Stream.of(7, 3, 9, 9, 5, 8)
        .distinct()
        .sorted(Comparator.reverseOrder())
        .limit(3)
        .toList();
System.out.println(topThree);
// Output: [9, 8, 7]
```

Complexity is O(n log n). A size-three heap can achieve O(n log 3) for very large input.

## 6) Convert to Map with Duplicate-Key Policy

```java
record Sale(String product, int quantity) {}
Map<String, Integer> totals = Stream.of(
        new Sale("Book", 2), new Sale("Book", 3), new Sale("Pen", 1))
        .collect(Collectors.toMap(Sale::product, Sale::quantity, Integer::sum));
System.out.println(totals);
// Output: {Book=5, Pen=1} (display order is not guaranteed).
```

Without the merge function, duplicate keys throw `IllegalStateException`.

## 7) Partition Valid and Invalid Values

```java
Map<Boolean, List<Integer>> partition = Stream.of(-2, 0, 3, 5)
        .collect(Collectors.partitioningBy(value -> value > 0));
System.out.println(partition.get(true));
System.out.println(partition.get(false));
// Output:
// [3, 5]
// [-2, 0]
```

## Quick Interview Questions

- `map` vs `flatMap`? One-to-one transform vs transform-and-flatten zero/many values.
- `reduce` vs `collect`? Immutable combination vs mutable reduction/container construction.
- Why avoid side effects? They make laziness, reuse, and parallel correctness difficult.
- Why can a stream be used once? A terminal operation consumes its traversal pipeline.
- Intermediate vs terminal? Lazy pipeline-building operation vs traversal/result operation.
- Stateless vs stateful? Per-element independent work vs operations that buffer/history such as sorted/distinct.
- `findFirst` vs `findAny`? Encounter-order result vs freedom useful for parallel execution.
- `Stream.toList` mutability? Returns an unmodifiable list.
- `Collectors.toList` implementation? Mutability/type are not specified by its contract.
- `orElse` vs `orElseGet`? Eager fallback evaluation vs lazy supplier.
- `peek` use? Diagnostics, not required business mutation.
- `takeWhile` vs filter? Matching prefix only vs every matching element.
- Why primitive streams? Avoid boxing and provide numeric operations.
- Duplicate `toMap` keys? Throw unless an explicit merge policy is supplied.
- Empty reduce without identity? Returns Optional because no result may exist.
- Parallel stream requirements? Large suitable source, CPU work, stateless operations, associative reduction, measured benefit.
- Why parallel stream risky in servers? Shared common pool, blocking work, ordering, side effects, and request isolation.
- `groupingBy` vs partitioningBy? Arbitrary classifier keys vs exactly Boolean true/false groups.
- Files.lines rule? It owns an I/O resource and must be closed.
