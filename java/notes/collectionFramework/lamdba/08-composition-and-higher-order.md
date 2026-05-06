# 08 - Composition and Higher-Order Patterns

## 1) Function Composition

```java
Function<Integer, Integer> times2 = x -> x * 2;
Function<Integer, Integer> plus3 = x -> x + 3;

Function<Integer, Integer> firstTimesThenPlus = times2.andThen(plus3); // (x * 2) + 3
Function<Integer, Integer> firstPlusThenTimes = times2.compose(plus3); // (x + 3) * 2
```

## 2) Predicate Composition

```java
Predicate<String> nonEmpty = s -> !s.isBlank();
Predicate<String> minLen3 = s -> s.length() >= 3;
Predicate<String> valid = nonEmpty.and(minLen3);
```

## 3) Consumer Chaining

```java
Consumer<String> c1 = s -> System.out.print("[");
Consumer<String> c2 = s -> System.out.print(s + "]");
Consumer<String> combined = c1.andThen(c2);
combined.accept("java"); // [java]
```

## 4) Higher-Order Function

Function that returns function:

```java
Function<Integer, Function<Integer, Integer>> adder = a -> b -> a + b;
System.out.println(adder.apply(10).apply(5)); // 15
```

## 5) Reusable Domain Rules

Build reusable predicates/functions instead of duplicating inline lambdas.

