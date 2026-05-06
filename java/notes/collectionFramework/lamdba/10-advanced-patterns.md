# 10 - Advanced Patterns (Expert Level)

## 1) Strategy Pattern with Lambda

```java
@FunctionalInterface
interface PriceStrategy {
    double apply(double amount);
}

double checkout(double amount, PriceStrategy strategy) {
    return strategy.apply(amount);
}

double finalPrice = checkout(1000, amt -> amt * 0.9); // 10% discount
```

## 2) Command Pattern

```java
Map<String, Runnable> commands = new HashMap<>();
commands.put("start", () -> System.out.println("Starting..."));
commands.put("stop", () -> System.out.println("Stopping..."));
commands.getOrDefault("start", () -> {}).run();
```

## 3) Factory via Constructor Reference

```java
Supplier<List<String>> listFactory = ArrayList::new;
```

## 4) Memoization Idea

Use lambda + map cache to avoid recomputation for pure functions.

## 5) Currying

```java
Function<Integer, Function<Integer, Integer>> multiply = a -> b -> a * b;
Function<Integer, Integer> times10 = multiply.apply(10);
```

## 6) DSL-Like APIs

Fluent APIs often accept lambdas for custom behavior:

- comparators
- retry policies
- validation rules
- pipeline steps

