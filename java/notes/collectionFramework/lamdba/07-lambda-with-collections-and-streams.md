# 07 - Lambda with Collections and Streams

## 1) Collections API Usage

```java
List<String> names = new ArrayList<>(List.of("Ram", "Shyam", "Aman"));

names.removeIf(s -> s.startsWith("S"));
names.forEach(System.out::println);
names.replaceAll(String::toUpperCase);
```

## 2) Map API Usage

```java
Map<String, Integer> freq = new HashMap<>();
freq.merge("java", 1, Integer::sum);
freq.computeIfAbsent("python", k -> 0);
freq.forEach((k, v) -> System.out.println(k + " -> " + v));
```

## 3) Streams Pipeline

```java
List<String> result = List.of("java", "go", "python", "js").stream()
    .filter(s -> s.length() >= 4)
    .map(String::toUpperCase)
    .sorted()
    .toList();
```

## 4) `flatMap` Example

```java
List<List<Integer>> data = List.of(List.of(1, 2), List.of(3, 4));
List<Integer> all = data.stream()
    .flatMap(List::stream)
    .toList();
```

## 5) Collectors with Lambda

```java
Map<Integer, List<String>> byLength = List.of("a", "bb", "cc", "ddd").stream()
    .collect(Collectors.groupingBy(String::length));
```

## 6) Parallel Stream Caution

- use only when workload is CPU-heavy and independent
- avoid shared mutable state inside lambda

