# 06 - Lambda Variable Capture and Scope

## Start with the Smallest Idea

A lambda can use a local variable declared outside it:

```java
int bonus = 10;
Function<Integer, Integer> addBonus = score -> score + bonus;
System.out.println(addBonus.apply(80));
// Output: 90
```

The lambda uses `bonus` even though `bonus` is not one of its parameters. This is called **capturing a variable**.

## Why Should You Care?

Capture is convenient, but hidden changing data can make code difficult to understand and unsafe when several threads use it.

Java therefore gives local-variable capture one important rule:

> A captured local variable must be assigned only once.

## Learn These Three Words

- **capture:** use a value declared outside the lambda
- **scope:** the part of the code where a name can be used
- **effectively final:** assigned once, even when the word `final` is not written

## Complete Runnable Example

```java
import java.util.function.IntUnaryOperator;

public class CaptureDemo {
    public static void main(String[] args) {
        int bonus = 10;
        IntUnaryOperator addBonus = score -> score + bonus;

        System.out.println(addBonus.applyAsInt(80));
        System.out.println(bonus);
    }
}
// Output:
// 90
// 10
```

## Understand It Step by Step

1. `bonus` receives `10`.
2. `bonus` is never assigned again, so it is effectively final.
3. The lambda remembers the value it needs from `bonus`.
4. `applyAsInt(80)` gives `80` to `score`.
5. The lambda calculates `80 + 10`.
6. The original local variable still holds `10`.

## The Rule That Causes Confusion

This does not compile:

```java
int bonus = 10;
IntUnaryOperator addBonus = score -> score + bonus;
// bonus = 20;
```

Why? Because assigning `bonus` again means it is no longer effectively final.

Writing `final` makes the intention visible, but it does not change the rule:

```java
final int bonus = 10;
IntUnaryOperator addBonus = score -> score + bonus;
```

## A Final Reference Can Point to a Changing Object

This is the next important level:

```java
List<String> names = new ArrayList<>();
Consumer<String> remember = name -> names.add(name);

remember.accept("Asha");
remember.accept("Ravi");
System.out.println(names);
// Output: [Asha, Ravi]
```

`names` is never reassigned, but the `ArrayList` object changes.

Think of it this way:

- the label `names` continues pointing to the same list
- the contents inside that list can still change

This is legal Java. It may still be a poor design if the hidden mutation surprises readers.

## Local Variable vs Object Field

A field follows different rules:

```java
final class Counter {
    private int count;

    Runnable incrementAction() {
        return () -> count++;
    }

    int count() {
        return count;
    }
}

Counter counter = new Counter();
Runnable increment = counter.incrementAction();
increment.run();
increment.run();
System.out.println(counter.count());
// Output: 2
```

The lambda can change `count` because `count` is object state, not a method-local variable.

Legal does not mean thread-safe. If two threads update `count`, increments can be lost.

## Scope Rules

```java
int score = 80;
Function<Integer, Integer> add = value -> value + score;
```

- `score` comes from the surrounding method
- `value` exists only inside the lambda
- the lambda cannot declare another local variable named `score`
- `this` inside a lambda still means the surrounding object

Unlike an anonymous inner class, a lambda does not create a new meaning for `this`.

## Developer-Level Guidance

Good capture:

```java
final int minimumScore = 70;
Predicate<Integer> passed = score -> score >= minimumScore;
```

The captured value is stable configuration and the meaning is clear.

Risky capture:

```java
List<Order> results = new ArrayList<>();
orders.parallelStream().forEach(results::add);
```

Several threads may change a non-thread-safe list. Prefer collecting the result:

```java
List<Order> results = orders.parallelStream().toList();
```

## Expert Understanding

- local capture preserves stable values, so captured locals must be final or effectively final
- a captured reference can still point to a mutable object
- field access is object access and follows normal Java Memory Model rules
- capture can hide a dependency; pass important changing inputs explicitly
- under concurrency, prefer immutable values, ownership, or safe collectors over shared mutation

## Quick Memory Card

- lambda uses an outer local variable = capture
- captured local = final or effectively final
- final reference does not make the object immutable
- fields may change, but are not automatically thread-safe
- stable configuration is good capture; hidden shared mutation is risky

## Practice

Predict the output:

```java
String prefix = "COURSE-";
Function<Integer, String> createCode = id -> prefix + id;
System.out.println(createCode.apply(7));
// Output: COURSE-7
```

Now explain why adding `prefix = "LESSON-";` after the lambda declaration would fail compilation.
