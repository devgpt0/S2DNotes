# 13 - Set with Streams and Lambda

## 1) Dedup Pipeline

Concept taught: Stream + `toSet` for distinct values.

```java
List<String> names = List.of(" Ram ", "Sita", "Ram", "sita");
Set<String> out = names.stream()
    .map(String::trim)
    .map(String::toLowerCase)
    .collect(Collectors.toSet());
System.out.println(out);
```

Possible output:

```text
[ram, sita]
```

## 2) Stable Dedup with Order

Concept taught: Collect into `LinkedHashSet` to preserve encounter order.

```java
List<Integer> nums = List.of(3, 1, 3, 2, 1);
Set<Integer> stable = nums.stream()
    .collect(Collectors.toCollection(LinkedHashSet::new));
System.out.println(stable);
```

Expected output:

```text
[3, 1, 2]
```

## 3) Filtered Set Creation

Concept taught: Build subset via predicate.

```java
Set<Integer> evens = IntStream.rangeClosed(1, 10)
    .filter(n -> n % 2 == 0)
    .boxed()
    .collect(Collectors.toSet());
System.out.println(evens);
```

Possible output:

```text
[2, 4, 6, 8, 10]
```

## 4) Grouping to Sets

Concept taught: Use set downstream collector to enforce unique grouped values.

```java
List<String> words = List.of("ant", "apple", "bat", "ball", "ant");
Map<Character, Set<String>> grouped = words.stream().collect(
    Collectors.groupingBy(w -> w.charAt(0), Collectors.toSet())
);
System.out.println(grouped);
```

Possible output:

```text
{a=[apple, ant], b=[ball, bat]}
```

## 5) Summary

Streams and sets combine well for dedup, canonicalization, unique grouping, and filter pipelines.
