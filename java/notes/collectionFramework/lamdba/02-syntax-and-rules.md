# 02 - Lambda Syntax and Rules

## 1) Syntax Variants

```java
// no parameter
() -> 42

// one parameter (parentheses optional)
x -> x * x

// multiple parameters
(a, b) -> a + b

// block body
(a, b) -> {
    int sum = a + b;
    return sum;
}
```

## 2) Type Inference

Compiler infers parameter types from target type:

```java
Comparator<String> c = (s1, s2) -> s1.compareToIgnoreCase(s2);
```

Explicit types are optional:

```java
Comparator<String> c = (String s1, String s2) -> s1.compareToIgnoreCase(s2);
```

## 3) Return Rules

- single expression body: return is implicit
- block body: use `return` for non-void

```java
Function<Integer, Integer> f1 = x -> x + 1; // implicit return
Function<Integer, Integer> f2 = x -> { return x + 1; }; // explicit return
```

## 4) Not Allowed

- cannot mix typed and untyped params in same lambda
- cannot use lambda where no functional interface target exists

Invalid:

```java
// (String a, b) -> a + b   // compile error
```

## 5) `this` and `super`

Inside lambda, `this` refers to enclosing instance (not a new inner class object).

## 6) Best Practices

- keep lambdas short
- extract complex logic to method, then use method reference
- choose clear parameter names

