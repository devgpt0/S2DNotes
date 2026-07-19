# 10 - Advanced Lambda Patterns

These patterns are useful only after basic lambdas, functional interfaces, capture, and composition feel natural.

## 1. Strategy: Supply One Replaceable Rule

```java
@FunctionalInterface
interface DiscountPolicy {
    int discountedPrice(int amount);
}

static int checkout(int amount, DiscountPolicy policy) {
    if (amount < 0) throw new IllegalArgumentException("amount cannot be negative");
    return policy.discountedPrice(amount);
}

int finalPrice = checkout(1_000, amount -> amount * 90 / 100);
System.out.println(finalPrice);
// Output: 900
```

The checkout flow stays stable while the discount rule can change.

Use integer minor currency units in real money code and define rounding rules explicitly.

## 2. Command: Store an Action to Run Later

```java
Map<String, Runnable> commands = Map.of(
        "start", () -> System.out.println("Starting"),
        "stop", () -> System.out.println("Stopping"));

Runnable command = commands.get("start");
if (command == null) throw new IllegalArgumentException("unknown command");
command.run();
// Output: Starting
```

The map replaces a small dispatch `if`/`switch`. Reject an unknown command instead of using an empty action that hides invalid input.

## 3. Factory: Store Object Creation

```java
Supplier<List<String>> createList = ArrayList::new;
List<String> courses = createList.get();
courses.add("Java");
System.out.println(courses);
// Output: [Java]
```

A supplier is enough when object creation needs no input. Use a named factory when creation has validation, several steps, or an important domain meaning.

## 4. Decorator-Like Behavior

```java
static <T, R> Function<T, R> timed(
        String operation,
        Function<T, R> function) {
    return input -> {
        long started = System.nanoTime();
        try {
            return function.apply(input);
        } finally {
            long elapsed = System.nanoTime() - started;
            System.out.println(operation + " took " + elapsed + " ns");
        }
    };
}

Function<String, Integer> measuredLength = timed("length", String::length);
System.out.println(measuredLength.apply("Java"));
// Output includes a timing line, then:
// 4
```

This learning example prints timing. Production metrics should use the application's metrics system and must not expose sensitive input.

## 5. Partial Application

```java
Function<Integer, Function<Integer, Integer>> multiply =
        first -> second -> first * second;
Function<Integer, Integer> timesTen = multiply.apply(10);
System.out.println(timesTen.apply(7));
// Output: 70
```

The returned function remembers the first value. This is often called currying in everyday Java discussion, although strict functional-programming definitions distinguish currying from general partial application.

Use a normal domain method when nested generic types make intent harder to read.

## 6. Memoization Needs a Policy

Memoization caches a pure function result for a previously seen input.

Questions before implementing it:

- is the function truly deterministic?
- how many keys can appear?
- when do entries expire?
- is concurrent access safe?
- how much memory can the cache use?
- can a proven cache library handle this better?

An unbounded `HashMap` inside a lambda can become a memory leak. Do not add a generic memoizer without lifecycle and capacity requirements.

## 7. Fluent Configuration APIs

```java
RetryPolicy policy = RetryPolicy.builder()
        .retryWhen(Failure::isTransient)
        .delay(attempt -> Duration.ofMillis(100L * attempt))
        .maxAttempts(3)
        .build();
```

Lambdas let callers supply narrow policies. The API must still validate bounds, define exception behavior, and prevent unsafe retries of non-idempotent operations.

## Pattern Selection

Use a lambda when:

- one behavior varies
- the contract has one clear operation
- the behavior is short or a named method reference
- state and lifecycle remain simple

Use a class when:

- behavior owns several related operations
- it needs mutable lifecycle state
- configuration needs validation and names
- identity or observability matters
- the lambda type becomes difficult to read

## Expert Understanding

- a lambda can implement Strategy, Command, Factory, or policy injection without requiring a separate class
- the pattern is the relationship and responsibility, not the syntax
- hidden capture can turn a simple lambda into stateful behavior
- caches, retries, timing, and concurrency need explicit production policies
- choose the smallest design that keeps the contract and failures clear

## Quick Memory Card

- Strategy: choose a rule
- Command: run an action later
- Factory: create a value
- Decorator: wrap behavior with another concern
- partial application: remember some inputs
- memoization: cache pure results with a bound and lifecycle
