# 04 - Built-in Functional Interfaces (Must Know)

These are in `java.util.function`.

## 1) `Predicate<T>`

Input: `T`, Output: `boolean`

```java
Predicate<String> nonEmpty = s -> !s.isBlank();
System.out.println(nonEmpty.test("java")); // true
```

## 2) `Function<T, R>`

Input: `T`, Output: `R`

```java
Function<String, Integer> len = s -> s.length();
System.out.println(len.apply("lambda")); // 6
```

## 3) `Consumer<T>`

Input: `T`, Output: none (`void`)

```java
Consumer<String> print = s -> System.out.println(s);
print.accept("Hello");
```

## 4) `Supplier<T>`

Input: none, Output: `T`

```java
Supplier<Double> random = () -> Math.random();
System.out.println(random.get());
```

## 5) `UnaryOperator<T>` and `BinaryOperator<T>`

Specializations of `Function`:

```java
UnaryOperator<Integer> square = x -> x * x;
BinaryOperator<Integer> sum = (a, b) -> a + b;
```

## 6) Primitive Specializations

Use for performance (avoid boxing):

- `IntPredicate`
- `IntFunction<R>`
- `ToIntFunction<T>`
- `IntUnaryOperator`

Example:

```java
IntUnaryOperator op = x -> x + 10;
System.out.println(op.applyAsInt(5)); // 15
```

## 7) `Bi*` Variants

- `BiPredicate<T, U>`
- `BiFunction<T, U, R>`
- `BiConsumer<T, U>`

