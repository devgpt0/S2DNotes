# 08 - List with Lambda and Streams (Complete)

## 1) Why Lambdas + Streams Matter for Lists

Lists are often transformed, filtered, grouped, and aggregated.

With lambdas + streams, we write that intent clearly:

- less boilerplate than manual loops
- easier composition of operations
- fewer mutation bugs when done properly

## 2) Core Stream Pipeline

Concept taught: Demonstrates 2) Core Stream Pipeline in practice.

```java
List<String> names = List.of("  Ram", "Shyam", "ram", "", "Mohan ");

List<String> result = names.stream()
    .map(String::trim)
    .filter(s -> !s.isEmpty())
    .map(String::toLowerCase)
    .distinct()
    .sorted()
    .toList();

System.out.println(result);
```

Expected output:

```text
[mohan, ram, shyam]
```

Pipeline order explained:

- `map(trim)` normalize spaces
- `filter` remove invalid entries
- `map(lowercase)` normalize case
- `distinct` remove duplicates
- `sorted` final order

## 3) In-Place Lambda Operations on List

These mutate same list object:

Concept taught: Demonstrates 3) In-Place Lambda Operations on List in practice.

```java
List<String> names = new ArrayList<>(List.of("  Ram", "", " Shyam "));
names.replaceAll(String::trim);
names.removeIf(String::isBlank);
System.out.println(names);
```

Expected output:

```text
[Ram, Shyam]
```

Use when mutability is intentional and safe.

## 4) Map + Filter + Collect to Different Types

Concept taught: Demonstrates 4) Map + Filter + Collect to Different Types in practice.

```java
List<String> words = List.of("java", "list", "stream");
Set<Integer> lengths = words.stream()
    .map(String::length)
    .collect(Collectors.toSet());
System.out.println(lengths);
```

Possible output:

```text
[4, 6]
```

(Set order may vary.)

## 5) Grouping and Counting

Concept taught: Demonstrates 5) Grouping and Counting in practice.

```java
List<String> words = List.of("a", "to", "tea", "go", "java", "api");
Map<Integer, Long> countByLen = words.stream()
    .collect(Collectors.groupingBy(String::length, Collectors.counting()));

System.out.println(countByLen);
```

Possible output:

```text
{1=1, 2=2, 3=2, 4=1}
```

## 6) Partitioning

Concept taught: Demonstrates 6) Partitioning in practice.

```java
List<Integer> nums = List.of(1, 2, 3, 4, 5, 6);
Map<Boolean, List<Integer>> parts = nums.stream()
    .collect(Collectors.partitioningBy(n -> n % 2 == 0));

System.out.println(parts.get(true));
System.out.println(parts.get(false));
```

Expected output:

```text
[2, 4, 6]
[1, 3, 5]
```

## 7) Flatten Nested Lists (`flatMap`)

Concept taught: Demonstrates 7) Flatten Nested Lists (`flatMap`) in practice.

```java
List<List<String>> nested = List.of(
    List.of("a", "b"),
    List.of("c"),
    List.of("d", "e")
);

List<String> flat = nested.stream()
    .flatMap(List::stream)
    .toList();

System.out.println(flat);
```

Expected output:

```text
[a, b, c, d, e]
```

## 8) Aggregation (`reduce`, `sum`)

Concept taught: Demonstrates 8) Aggregation (`reduce`, `sum`) in practice.

```java
List<Integer> nums = List.of(10, 20, 30);
int sum = nums.stream().mapToInt(Integer::intValue).sum();
int product = nums.stream().reduce(1, (a, b) -> a * b);

System.out.println(sum);
System.out.println(product);
```

Expected output:

```text
60
6000
```

## 9) `toList()` vs `Collectors.toList()`

Concept taught: Demonstrates 9) `toList()` vs `Collectors.toList()` in practice.

```java
List<Integer> a = List.of(1, 2, 3).stream().map(n -> n * 2).toList();
List<Integer> b = List.of(1, 2, 3).stream().map(n -> n * 2).collect(Collectors.toList());

System.out.println(a);
System.out.println(b);
```

Expected output:

```text
[2, 4, 6]
[2, 4, 6]
```

Important note:

- `Stream.toList()` returns unmodifiable list
- `Collectors.toList()` usually returns mutable list (implementation not strictly specified)

## 10) Parallel Stream Caution

Concept taught: Demonstrates 10) Parallel Stream Caution in practice.

```java
List<Integer> nums = IntStream.rangeClosed(1, 10).boxed().toList();
int total = nums.parallelStream().mapToInt(Integer::intValue).sum();
System.out.println(total);
```

Expected output:

```text
55
```

Use parallel streams only when:

- work per element is sufficiently heavy
- data size is large enough
- no shared mutable state inside lambda

## 11) Side Effects: What to Avoid

Bad pattern:

Concept taught: Demonstrates 11) Side Effects: What to Avoid in practice.

```java
List<Integer> out = new ArrayList<>();
nums.stream().forEach(out::add); // side-effect mutation
```

Better:

Concept taught: Demonstrates 11) Side Effects: What to Avoid in practice.

```java
List<Integer> out = nums.stream().toList();
```

## 12) Real Example: Transaction Summary

Concept taught: Demonstrates 12) Real Example: Transaction Summary in practice.

```java
record Tx(String user, int amount, String status) {}

List<Tx> txs = List.of(
    new Tx("u1", 100, "SUCCESS"),
    new Tx("u2", 200, "FAILED"),
    new Tx("u1", 50, "SUCCESS"),
    new Tx("u3", 300, "SUCCESS")
);

Map<String, Integer> totals = txs.stream()
    .filter(t -> t.status().equals("SUCCESS"))
    .collect(Collectors.groupingBy(Tx::user, Collectors.summingInt(Tx::amount)));

System.out.println(totals);
```

Expected output:

```text
{u1=150, u3=300}
```

## 13) Summary

Use lambda + streams to express list transformations declaratively. Keep pipelines pure, avoid side effects, and choose mutable in-place methods only when you intentionally want mutation.
