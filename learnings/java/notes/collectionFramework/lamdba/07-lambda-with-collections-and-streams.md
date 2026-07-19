# 07 - Lambdas with Collections and Streams

This chapter shows where lambdas appear in everyday collection code. Read the List, Map, and Stream basics first.

## The Main Idea

The collection owns data. The lambda supplies a small rule or action.

```java
List<String> names = new ArrayList<>(List.of("Asha", "", "Ravi"));
names.removeIf(name -> name.isBlank());
System.out.println(names);
// Output: [Asha, Ravi]
```

`removeIf` controls list removal. The lambda answers one question: “Is this name blank?”

## `forEach`: Perform an Action

```java
List<String> courses = List.of("Java", "SQL");
courses.forEach(course -> System.out.println(course));
// Output:
// Java
// SQL
```

Use `forEach` for a clear final side effect. Use a normal loop when you need `break`, `continue`, checked-exception handling, or several statements that read better step by step.

## `removeIf`: Remove Matching Values

```java
List<String> names = new ArrayList<>(List.of("Asha", "", "  ", "Ravi"));
names.removeIf(String::isBlank);
System.out.println(names);
// Output: [Asha, Ravi]
```

The predicate returns `true` for values that should be removed.

## `replaceAll`: Replace Every Value

```java
List<String> skills = new ArrayList<>(List.of("java", "sql"));
skills.replaceAll(String::toUpperCase);
System.out.println(skills);
// Output: [JAVA, SQL]
```

The unary operator receives one old value and returns its replacement.

## `sort`: Supply an Ordering Rule

```java
List<String> names = new ArrayList<>(List.of("Ravi", "Asha", "Kiran"));
names.sort(Comparator.comparingInt(String::length).thenComparing(String::compareTo));
System.out.println(names);
// Output: [Asha, Ravi, Kiran]
```

The comparator first uses length, then alphabetical order when lengths match. Comparator rules must be consistent; sorting is not just any two-input lambda.

## Map Operations

### `merge`: Insert or Combine

```java
Map<String, Integer> counts = new HashMap<>();
counts.merge("java", 1, Integer::sum);
counts.merge("java", 1, Integer::sum);
System.out.println(counts);
// Output: {java=2}
```

If the key is absent, Map stores `1`. If present, the function combines old and new values.

### `computeIfAbsent`: Create a Missing Value

```java
Map<String, List<String>> coursesByLevel = new HashMap<>();
coursesByLevel.computeIfAbsent("beginner", key -> new ArrayList<>()).add("Java");
System.out.println(coursesByLevel);
// Output: {beginner=[Java]}
```

The lambda runs only when the key has no value. Keep the creation function small and free from unrelated mutation.

### `forEach`: Receive Key and Value

```java
Map<String, Integer> scores = Map.of("Asha", 90, "Ravi", 85);
scores.forEach((name, score) -> System.out.println(name + " -> " + score));
// Output order is not guaranteed for this Map.of example.
```

Do not claim an order unless the map implementation promises it.

## Stream Pipeline

```java
List<String> result = List.of("java", "go", "python", "js")
        .stream()
        .filter(language -> language.length() >= 4)
        .map(String::toUpperCase)
        .sorted()
        .toList();
System.out.println(result);
// Output: [JAVA, PYTHON]
```

Read it as:

1. take the languages
2. keep names with at least four characters
3. make them uppercase
4. sort them
5. create an unmodifiable result list

## `flatMap`: Flatten Nested Collections

```java
List<List<Integer>> groups = List.of(List.of(1, 2), List.of(3, 4));
List<Integer> all = groups.stream().flatMap(List::stream).toList();
System.out.println(all);
// Output: [1, 2, 3, 4]
```

`map(List::stream)` would produce a stream of streams. `flatMap` joins their elements into one stream.

## Grouping

```java
Map<Integer, List<String>> byLength = List.of("a", "bb", "cc", "ddd")
        .stream()
        .collect(Collectors.groupingBy(String::length));
System.out.println(byLength);
// Output: {1=[a], 2=[bb, cc], 3=[ddd]}
```

The classifier function returns the key for each value.

## Mutation Rule

Collection methods such as `removeIf`, `replaceAll`, and `sort` change the collection. Stream operations normally produce a separate result.

Know which contract you are using. Do not mutate a collection while another operation is iterating over it unless the API explicitly supports that action.

## Parallel Stream Warning

Avoid shared mutation:

```java
// Unsafe design:
// List<String> result = new ArrayList<>();
// names.parallelStream().forEach(result::add);
```

Return or collect results instead. Use parallel streams only for measured CPU-heavy, independent work with safe operations.

## Quick Memory Card

- collection method owns traversal or update
- lambda supplies one action, test, transformation, or comparison
- know whether the operation mutates or returns a result
- do not assume map or parallel execution order
- named methods are clearer for domain rules
