# 01 - Why Lambdas Exist

## Start with the Problem

Sometimes we want to give a method a small piece of behavior.

Example: “Run this code on another thread.” Java represents that behavior with `Runnable`.

Before lambdas, even one print statement needed a long anonymous class:

```java
Runnable greeting = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};

greeting.run();
// Output: Hello
```

Most of that code describes the wrapper, not the useful work.

## The Same Behavior with a Lambda

```java
Runnable greeting = () -> System.out.println("Hello");
greeting.run();
// Output: Hello
```

Read it as:

> This behavior takes no input and prints `Hello` when it runs.

## What Changed?

Nothing changed about `Runnable`.

`Runnable` still has one method:

```java
void run();
```

Because there is exactly one abstract method, Java can understand which method body the lambda is providing.

## Behavior Can Be Passed Like a Value

Methods normally receive data:

```java
printName("Asha");
```

With a lambda, a method can receive behavior:

```java
static void runTwice(Runnable action) {
    action.run();
    action.run();
}

runTwice(() -> System.out.println("Practice"));
// Output:
// Practice
// Practice
```

`runTwice` decides **when and how often** to run the behavior. The caller decides **what the behavior does**.

## Complete Runnable Example

```java
import java.util.List;

public class WhyLambdaDemo {
    public static void main(String[] args) {
        List<String> courses = List.of("Java", "SQL", "Spring");
        courses.forEach(course -> System.out.println(course));
    }
}
// Output:
// Java
// SQL
// Spring
```

Step by step:

1. `forEach` visits one list value.
2. That value becomes the lambda parameter `course`.
3. The code after `->` prints it.
4. `forEach` repeats the behavior for every value.

## Learn These Words After the Example

- **lambda expression:** short syntax for behavior without a method name
- **anonymous:** has no declared method name of its own
- **functional interface:** interface with one abstract method that a lambda can implement
- **passing behavior:** giving code to another method so that method can run it

## What a Lambda Is Not

- it is not automatically asynchronous
- it is not automatically faster than a method
- it does not run merely because it was assigned to a variable
- it does not replace every normal method or class

The receiving API decides when and where a lambda runs.

## When a Lambda Helps

Use one for small, clear behavior such as:

- filtering values
- sorting with a comparison rule
- handling one event
- transforming one value
- submitting one task

Use a named method or class when behavior has several rules, needs its own state, or deserves a domain name.

## Beginner to Expert Understanding

1. **Beginner:** lambda is a small behavior you can run later.
2. **Developer:** it fits one functional-interface method and can be passed to APIs.
3. **Senior:** short lambdas improve intent; large lambdas hide intent.
4. **Expert:** runtime implementation, capture, allocation, and concurrency depend on context and must not be guessed.

## Quick Check

Predict the output:

```java
runTwice(() -> System.out.println("Java"));
// Output:
// Java
// Java
```

Next, learn the syntax that describes lambda inputs and results.
