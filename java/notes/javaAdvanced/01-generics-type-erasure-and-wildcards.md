# 01 - Generics, Type Erasure, and Wildcards

## 1) Why Generics Exist

Generics provide compile-time type safety and remove most manual casts.

```java
static <T> T first(List<T> values) {
    if (values.isEmpty()) {
        throw new IllegalArgumentException("values must not be empty");
    }
    return values.getFirst();
}

System.out.println(first(List.of("Java", "Spring")));
// Output: Java
```

`T` is inferred as `String`. Passing an empty list fails immediately.

## 2) Bounded Type Parameters

```java
static <T extends Number> double total(List<T> values) {
    return values.stream().mapToDouble(Number::doubleValue).sum();
}

System.out.println(total(List.of(10, 20.5)));
// Output: 30.5
```

The bound allows `Number` methods while rejecting unrelated types.

## 3) PECS Rule

- Producer Extends: read values from `? extends T`.
- Consumer Super: write values into `? super T`.

```java
static void copyNumbers(List<? extends Number> source, List<? super Number> target) {
    target.addAll(source);
}

List<Integer> source = List.of(1, 2);
List<Number> target = new ArrayList<>();
copyNumbers(source, target);
System.out.println(target);
// Output: [1, 2]
```

## 4) Invariance

`List<Integer>` is not a subtype of `List<Number>`. Otherwise, code could insert a `Double` into an integer list.

```java
List<? extends Number> numbers = List.of(1, 2, 3);
System.out.println(numbers.getFirst());
// Output: 1
// numbers.add(4) does not compile because the exact element type is unknown.
```

## 5) Type Erasure

Generic type arguments are mostly removed at runtime. Consequently:

- `new T()` and `T.class` are illegal.
- `instanceof List<String>` is illegal.
- overloads cannot differ only by generic type arguments.

```java
System.out.println(new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass());
// Output: true
```

Use `Class<T>` when runtime type information is genuinely needed.

```java
static <T> T create(Class<T> type) throws ReflectiveOperationException {
    return type.getDeclaredConstructor().newInstance();
}

System.out.println(create(StringBuilder.class).getClass().getSimpleName());
// Output: StringBuilder
```

## 6) Best Practices

- Avoid raw types.
- Do not suppress unchecked warnings without proving safety.
- Keep public generic signatures small and readable.
- Use wildcards for API flexibility; use named type parameters when types must relate.
