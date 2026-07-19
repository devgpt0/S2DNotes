# 03 - Functional Interfaces in Simple Words

## Start with the Main Idea

A lambda needs a type that tells Java:

- what inputs arrive
- what result comes back
- which method the lambda supplies

That type is a **functional interface**.

## First Example

```java
@FunctionalInterface
interface MathOperation {
    int apply(int left, int right);
}

MathOperation add = (left, right) -> left + right;
System.out.println(add.apply(2, 3));
// Output: 5
```

## Read It Step by Step

1. `MathOperation` is an interface.
2. It has one abstract method named `apply`.
3. `apply` needs two `int` inputs and returns one `int`.
4. The lambda must therefore accept two values and produce an integer.
5. `add.apply(2, 3)` runs the lambda with `2` and `3`.

## Why “One Abstract Method” Matters

If an interface had two abstract methods, Java would not know which method body the lambda represents.

The formal name is **Single Abstract Method**, often shortened to **SAM**.

You only need to remember the simple rule: one abstract method gives the lambda one clear shape.

## What `@FunctionalInterface` Does

```java
@FunctionalInterface
interface Formatter {
    String format(String value);
}
```

The annotation asks the compiler to check the one-abstract-method rule.

It is not required for a valid functional interface, but it makes the intention clear and prevents someone from accidentally adding a second abstract method later.

## Default and Static Methods Are Allowed

```java
@FunctionalInterface
interface Validator<T> {
    boolean test(T value);

    default Validator<T> and(Validator<T> other) {
        return value -> test(value) && other.test(value);
    }

    static <T> Validator<T> alwaysValid() {
        return value -> true;
    }
}
```

The interface is still functional because it has only one **abstract** method. `default` and `static` methods already have implementations.

## Complete Validator Example

```java
@FunctionalInterface
interface Validator<T> {
    boolean test(T value);

    default Validator<T> and(Validator<T> other) {
        return value -> test(value) && other.test(value);
    }
}

public class FunctionalInterfaceDemo {
    public static void main(String[] args) {
        Validator<String> notBlank = value -> !value.isBlank();
        Validator<String> shortEnough = value -> value.length() <= 10;
        Validator<String> validName = notBlank.and(shortEnough);

        System.out.println(validName.test("Asha"));
        System.out.println(validName.test(""));
        System.out.println(validName.test("VeryLongCourseName"));
    }
}
// Output:
// true
// false
// false
```

The default `and` method returns a new validator that checks both rules.

## Use a Standard Interface When It Fits

Java already provides common shapes in `java.util.function`:

- `Predicate<T>`: value -> `boolean`
- `Function<T, R>`: value -> result
- `Consumer<T>`: value -> no result
- `Supplier<T>`: no input -> result

Use a custom interface when the domain name or contract adds useful meaning, such as `PricePolicy` or `RetryDecision`.

Do not create `MyFunction<T, R>` when standard `Function<T, R>` says everything needed.

## Method Contracts Still Matter

A functional interface is more than matching parameter types. Its name and documentation should state what implementations promise.

For example, a comparator must be consistent enough for sorting. Any two-argument integer lambda is not automatically a correct comparator.

## Expert Understanding

- methods matching `Object` methods do not normally count toward the single abstract method
- inherited abstract methods can still form one logical signature
- checked exceptions allowed by a lambda come from the interface method declaration
- the surrounding functional-interface type helps Java infer lambda parameter types and choose overloads

## Quick Memory Card

- lambda needs a functional-interface type
- functional interface = one abstract method
- annotation makes the compiler protect that intention
- default and static methods are allowed
- prefer standard interfaces unless a domain-specific contract adds meaning

## Practice

```java
@FunctionalInterface
interface Greeting {
    String message(String name);
}

Greeting greeting = name -> "Hello, " + name;
System.out.println(greeting.message("Asha"));
// Output: Hello, Asha
```

Point to the lambda input, body, interface method, and returned result.
