# 02 - Lambda Syntax, from First Look to Expert Use

## Start with the Smallest Idea

A lambda is a small piece of code that you can store in a variable and run later.

```java
Function<Integer, Integer> doubleNumber = number -> number * 2;
System.out.println(doubleNumber.apply(5));
// Output: 10
```

Read the important line like this:

> Take a number, call it `number`, multiply it by `2`, and return the answer.

That is the whole idea. The remaining sections explain each piece and the rules around it.

## Why Does Java Need Lambdas?

Sometimes a method needs **behavior**, not just data.

For example, sorting needs to know *how* two values should be compared. A lambda lets us pass that rule directly:

```java
List<String> names = new ArrayList<>(List.of("Ravi", "Asha", "Kiran"));
names.sort((first, second) -> first.compareTo(second));
System.out.println(names);
// Output: [Asha, Kiran, Ravi]
```

Without a lambda, we would need a separate class or a longer anonymous-class block for this small rule.

## Learn These Four Words

- **lambda:** a small unnamed piece of behavior
- **parameter:** an input name, such as `number`
- **body:** the work after `->`, such as `number * 2`
- **functional interface:** an interface with one abstract method; it tells Java what inputs and result the lambda must have

You do not have to memorize the term *functional interface* yet. For now, think of it as the **shape** that the lambda must fit.

## Read a Lambda from Left to Right

```java
number -> number * 2
```

| Part | Simple meaning |
|---|---|
| `number` | input name |
| `->` | “use the input to do this work” |
| `number * 2` | work and returned result |

The `->` symbol is usually read as “goes to.”

## Complete Runnable Example

Save this as `LambdaSyntaxDemo.java`:

```java
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;

public class LambdaSyntaxDemo {
    public static void main(String[] args) {
        Supplier<Integer> answer = () -> 42;
        Function<Integer, Integer> square = number -> number * number;
        BiFunction<Integer, Integer, Integer> add =
                (left, right) -> left + right;
        Predicate<String> isLong = text -> text.length() > 5;

        System.out.println(answer.get());
        System.out.println(square.apply(5));
        System.out.println(add.apply(7, 3));
        System.out.println(isLong.test("Spring"));
    }
}
// Output:
// 42
// 25
// 10
// true
```

Run it:

```powershell
javac LambdaSyntaxDemo.java
java LambdaSyntaxDemo
```

## Understand It Line by Line

### 1. No Input

```java
Supplier<Integer> answer = () -> 42;
```

- `Supplier<Integer>` means “give me an `Integer` when I ask.”
- `()` means the lambda needs no input.
- `42` is returned.
- `.get()` runs a `Supplier`.

### 2. One Input

```java
Function<Integer, Integer> square = number -> number * number;
```

- the first `Integer` is the input type
- the second `Integer` is the result type
- `.apply(5)` runs the function with `5`

### 3. Two Inputs

```java
BiFunction<Integer, Integer, Integer> add =
        (left, right) -> left + right;
```

- the first two types are inputs
- the last type is the result
- two parameters need parentheses

### 4. A True-or-False Test

```java
Predicate<String> isLong = text -> text.length() > 5;
```

- `Predicate<String>` tests a `String`
- `.test("Spring")` runs it
- a predicate always returns `boolean`

## One Line or Several Lines

A one-expression lambda returns the expression automatically:

```java
Function<Integer, Integer> addOne = number -> number + 1;
System.out.println(addOne.apply(9));
// Output: 10
```

Use braces when the work needs several statements. Then write `return` yourself:

```java
Function<Integer, Integer> addOne = number -> {
    int result = number + 1;
    return result;
};
System.out.println(addOne.apply(9));
// Output: 10
```

## Rules That Prevent Common Errors

### Rule 1: A Lambda Needs a Known Shape

This is invalid:

```java
// var doubleNumber = number -> number * 2;
```

Java does not know the input and result types. Give it a functional-interface type:

```java
Function<Integer, Integer> doubleNumber = number -> number * 2;
```

The expert term for that surrounding type is **target type**.

### Rule 2: Do Not Mix Typed and Untyped Parameters

```java
// (String first, second) -> first + second; // does not compile
(String first, String second) -> first + second; // valid
(first, second) -> first + second;                // valid
```

### Rule 3: A Block That Produces a Value Needs `return`

```java
// number -> { number + 1; }         // does not compile
number -> { return number + 1; }     // valid
```

## Developer-Level Choice

Use a lambda when the behavior is short and obvious:

```java
names.removeIf(name -> name.isBlank());
```

Use a named method when the behavior has business rules or several branches:

```java
orders.removeIf(this::isExpiredAndUnpaid);
```

A lambda should make the code easier to read, not merely shorter.

## Expert Understanding

- a lambda is converted to an instance of a compatible functional interface
- the surrounding type lets the compiler infer parameter and result types
- a lambda is not “just a shorter method”; it is a value representing behavior
- the JVM may implement lambdas without creating the same kind of class used for an anonymous class
- never depend on the identity of a lambda object

Learn these points after you are comfortable writing and running the earlier examples.

## Quick Memory Card

- left of `->`: inputs
- right of `->`: work
- one expression: returned automatically
- block body: use braces and `return`
- lambda must fit a functional interface
- prefer a named method when logic becomes difficult to read

## Practice

Write a `Predicate<Integer>` that returns `true` for an even number. Predict both outputs before running:

```java
Predicate<Integer> isEven = number -> number % 2 == 0;
System.out.println(isEven.test(8));
System.out.println(isEven.test(7));
// Output:
// true
// false
```
