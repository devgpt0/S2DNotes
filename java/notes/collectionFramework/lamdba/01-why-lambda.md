# 01 - Why Lambda

## 1) Problem Before Java 8

Earlier, small behavior was written using:

- anonymous inner classes
- full class implementations

This was verbose for simple logic.

## 2) What Is Lambda

A lambda expression is an anonymous function:

- no name
- can be passed as data
- usually used where a single abstract method is expected

General form:

```java
(parameters) -> expression
(parameters) -> { statements }
```

## 3) First Example

Without lambda:

```java
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Hello");
    }
};
```

With lambda:

```java
Runnable r = () -> System.out.println("Hello");
```

## 4) Benefits

- less boilerplate
- better readability for behavior-passing
- natural fit for Stream API
- encourages functional style (composition, immutability)

## 5) Mental Model

Think: "I am passing behavior, not just data."

