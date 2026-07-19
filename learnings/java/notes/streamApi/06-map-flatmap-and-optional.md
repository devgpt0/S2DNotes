# 06 - `map`, `flatMap`, and `Optional`

## 1) One-to-One Mapping

```java
record User(String name) {}

List<String> names = Stream.of(new User("Asha"), new User("Ravi"))
        .map(User::name)
        .toList();
System.out.println(names);
// Output: [Asha, Ravi]
```

## 2) Flatten Nested Collections

```java
List<List<Integer>> rows = List.of(List.of(1, 2), List.of(3, 4));
List<Integer> flat = rows.stream().flatMap(Collection::stream).toList();
System.out.println(flat);
// Output: [1, 2, 3, 4]
```

`flatMap` maps one input to zero or more outputs and flattens them into one stream.

## 3) Optional Pipelines

```java
Optional<String> name = Optional.of(" asha ")
        .map(String::strip)
        .filter(value -> !value.isEmpty())
        .map(String::toUpperCase);
System.out.println(name.orElse("UNKNOWN"));
// Output: ASHA
```

## 4) Flatten Optionals

```java
List<Optional<Integer>> values = List.of(Optional.of(1), Optional.empty(), Optional.of(3));
System.out.println(values.stream().flatMap(Optional::stream).toList());
// Output: [1, 3]
```

## 5) `orElse` vs `orElseGet`

```java
String present = Optional.of("ready").orElseGet(() -> "created lazily");
System.out.println(present);
// Output: ready
```

`orElse` evaluates its argument eagerly. Use `orElseGet` when fallback creation is expensive or has side effects.

## 6) Optional Rules

- Prefer it as a return type for a possibly absent result.
- Do not use `null` inside an `Optional` pipeline.
- Do not call `get()` without first proving presence; use `orElseThrow`.
- Avoid optional fields and parameters unless a framework or design has a strong reason.
