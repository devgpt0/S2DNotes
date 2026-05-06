# 08 - List with Lambda and Streams

## 1) Filter + Map + Collect

```java
List<String> out = names.stream()
    .filter(s -> s.length() >= 3)
    .map(String::toUpperCase)
    .toList();
```

## 2) Remove/Transform In Place

```java
names.removeIf(String::isBlank);
names.replaceAll(String::trim);
```

## 3) Counting and Grouping

```java
Map<Integer, Long> countByLen = names.stream()
    .collect(Collectors.groupingBy(String::length, Collectors.counting()));
```

## 4) Distinct + Sorted

```java
List<String> clean = names.stream()
    .filter(s -> !s.isBlank())
    .map(String::trim)
    .distinct()
    .sorted()
    .toList();
```

## 5) Parallel Streams Note

Use only when data size and CPU work justify overhead.
Avoid shared mutable state in lambdas.

