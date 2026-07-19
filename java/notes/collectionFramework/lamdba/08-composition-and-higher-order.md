# 08 - Combining Functions and Predicates

## Start with the Problem

Small rules are useful, but real work often needs several rules in a specific order.

Instead of writing one large lambda, we can combine small named functions.

## Function `andThen`

```java
Function<Integer, Integer> doubleNumber = number -> number * 2;
Function<Integer, Integer> addThree = number -> number + 3;

Function<Integer, Integer> doubleThenAdd = doubleNumber.andThen(addThree);
System.out.println(doubleThenAdd.apply(5));
// Output: 13
```

Trace: `5 * 2 = 10`, then `10 + 3 = 13`.

Read `a.andThen(b)` as “run `a`, then give its result to `b`.”

## Function `compose`

```java
Function<Integer, Integer> addThenDouble = doubleNumber.compose(addThree);
System.out.println(addThenDouble.apply(5));
// Output: 16
```

Trace: `5 + 3 = 8`, then `8 * 2 = 16`.

Read `a.compose(b)` as “run `b` first, then `a`.”

If the method names make you pause, use clearly named variables or a normal method. Readability matters more than composition syntax.

## Predicate `and`, `or`, and `negate`

```java
Predicate<String> notBlank = text -> !text.isBlank();
Predicate<String> atLeastThree = text -> text.length() >= 3;

Predicate<String> validName = notBlank.and(atLeastThree);
System.out.println(validName.test("Java"));
System.out.println(validName.test(""));
System.out.println(validName.test("Go"));
// Output:
// true
// false
// false
```

- `and`: both rules must pass
- `or`: at least one rule must pass
- `negate`: reverse true and false

Predicate composition short-circuits like `&&` and `||`.

## Consumer `andThen`

```java
Consumer<String> printStart = value -> System.out.print("[");
Consumer<String> printValue = value -> System.out.println(value + "]");
Consumer<String> printLabel = printStart.andThen(printValue);

printLabel.accept("Java");
// Output: [Java]
```

Consumers create side effects. If the first consumer throws, the second does not run. Do not use consumer chains when a transaction or rollback rule is required.

## A Function That Returns a Function

```java
Function<Integer, Function<Integer, Integer>> addTo =
        first -> second -> first + second;

Function<Integer, Integer> addTen = addTo.apply(10);
System.out.println(addTen.apply(5));
// Output: 15
```

Step by step:

1. `addTo.apply(10)` remembers `10`.
2. It returns another function.
3. The returned function receives `5`.
4. It calculates `10 + 5`.

A function that receives or returns behavior is called a **higher-order function**.

## Real Domain Example

```java
Predicate<Order> paid = Order::paid;
Predicate<Order> notCancelled = order -> !order.cancelled();
Predicate<Order> readyToShip = paid.and(notCancelled);

List<Order> ready = orders.stream().filter(readyToShip).toList();
```

The names express the business meaning better than repeating a long inline condition.

## When Not to Compose

Use a normal named method when you need:

- several branches
- detailed failure information
- checked exceptions
- logging or metrics around particular steps
- a transaction boundary
- a sequence that composition makes harder to follow

## Expert Understanding

- composed function output must match the next function input
- order changes the result
- predicates short-circuit
- captured values follow the effectively-final rule
- composition is useful when pieces remain independently meaningful and testable

## Quick Memory Card

- `first.andThen(second)`: first, then second
- `first.compose(second)`: second, then first
- predicates: `and`, `or`, `negate`
- consumer `andThen`: ordered side effects, no automatic rollback
- higher-order function: accepts or returns behavior
