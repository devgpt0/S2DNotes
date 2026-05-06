# 03 - Functional Interfaces

## 1) Core Concept

Lambda works with a functional interface:

- exactly one abstract method (SAM: Single Abstract Method)

Example:

```java
@FunctionalInterface
interface MathOp {
    int apply(int a, int b);
}
```

Use with lambda:

```java
MathOp add = (a, b) -> a + b;
System.out.println(add.apply(2, 3)); // 5
```

## 2) `@FunctionalInterface`

Recommended annotation:

- compiler checks SAM rule
- improves readability and intent

## 3) Can It Have Other Methods

Yes, functional interface can also have:

- `default` methods
- `static` methods
- methods from `Object` (`toString`, `hashCode`) do not count as abstract SAM

## 4) Custom Interface Design Tips

- name by behavior (`Validator`, `Transformer`, `Formatter`)
- keep method meaning clear
- prefer standard Java functional interfaces unless domain-specific need exists

## 5) Real Example

```java
@FunctionalInterface
interface Validator<T> {
    boolean test(T value);

    default Validator<T> and(Validator<T> other) {
        return v -> this.test(v) && other.test(v);
    }
}
```

